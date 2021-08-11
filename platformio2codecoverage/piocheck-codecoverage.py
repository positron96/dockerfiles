#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import math
import logging
import argparse
from copy import deepcopy
import json
import hashlib

log = logging.getLogger(__name__)

# Source: https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#data-types
CODE_QUAL_ELEMENT = {
    "type": "issue",
    "severity": "--GITLAB-REQUIREMENT--",
    "check_name": "--CODE-CLIMATE-REQUIREMENT--",
    "description": "--CODE-CLIMATE-REQUIREMENT--",
    "categories": "--CODE-CLIMATE-REQUIREMENT--",
    "fingerprint": "--GITLAB-REQUIREMENT--",
    "location": {"path": "", "positions": {"begin": {"line": -1, "column": -1}}},
}


def __get_codeclimate_category(cppcheck_severity: str) -> str:
    """Get Code Climate category, from CppCheck severity string

    CppCheck: error, warning, style, performance, portability, information
    CodeQuality: Bug Risk, Clarity, Compatibility, Complexity, Duplication,
                 Performance, Security, Style
    """
    map_severity_to_category = {
        "error": "Bug Risk",
        "warning": "Bug Risk",
        "style": "Style",
        "performance": "Performance",
        "portability": "Compatibility",
        "information": "Style",
    }
    return map_severity_to_category[cppcheck_severity]


def __get_codeclimate_severity(cpio_severity: str) -> str:
    """Get Code Climate severity, from CppCheck severity string

    CodeQuality: info, minor, major, critical, blocker
    """
    map_severity_to_severity = {
        "high": "critical",
        "medium" : "major",
        "low" : "minor"
    }
    return map_severity_to_severity[cpio_severity]


def convert_file(fname_in: str, fname_out: str) -> bool:
    """Convert CppCheck XML file to GitLab-compatible "Code Quality" JSON report

    Args:
        fname_in (str): Input file path (CppCheck XML). Like 'cppcheck.xml'.
        fname_out (str): Output file path (code quality JSON). Like 'cppcheck.json'.

    Returns:
        bool: True if the conversion was successful.

    """
    fin = None
    json_out = ""

    log.debug("Reading input file: %s", os.path.abspath(fname_in))

    with open(fname_in, mode="r") as fin:
        json_out = __convert(json.load(fin) )

    log.debug("Writing output file: %s", fname_out)
    with open(fname_out, "w") as f_out:
        json.dump(json_out, f_out, indent=2)

    return True


def _get_line_from_file(filename: str, line_number: int) -> str:
    """Return a specific line in a file as a string.

    I've found that linecache.getline() will end up raising a UnicodeDecodeError
    if the source file we're opening has non-UTF-8 characters in it. So, here,
    we're explicitly escaping those bad characters.

    Side note, it seems CppCheck v2.0+ will generate a 'syntaxError' for
    "unhandled characters", so you could find these issues with your source code
    more easily.

    Args:
        filename (str): Name of file to open and read line from
        line_number (int): Number of the line to extract. Line number starts at 1.

    Returns:
        str: Contents of the specified line.
    """
    max_line_cnt = 0
    with open(filename, mode="rt", errors="backslashreplace") as fin:
        for i, line in enumerate(fin):
            if (i + 1) == line_number:
                # log.debug("Extracted line %s:%d", filename, line_number)
                return line
            max_line_cnt += 1

    log.warning(
        "Only %d lines in file. Can't read line %d from '%s'",
        max_line_cnt,
        line_number,
        filename,
    )
    # To keep going, let's just make a string out of the file & line number
    return str(filename) + str(line_number)


def __convert(arr_in) -> str:

    if len(arr_in) == 0:
        log.info("Empty file imported. Skipping...")
        return True

    arr_out = list()

    # Ensure this XML report has errors to convert
    # if not isinstance(arr_in["results"]["errors"], dict):
    #     log.warning("Nothing to do")
    #     return []]

    # if not isinstance(dict_in["results"]["errors"]["error"], list):
    #     dict_in["results"]["errors"]["error"] = list(
    #         [dict_in["results"]["errors"]["error"]]
    #     )

    # log.debug("Got the following dict:\n%s\n", str(dict_in))
    # log.debug("Type is {}\n".format(str(type(dict_in["results"]["errors"]))))
    # log.debug("Type is {}\n".format(str(type(dict_in["results"]["errors"]["error"]))))

    for section in arr_in:
        defects = section['defects']
        tool = section['tool']
        for error in defects:

            log.debug("Processing -- %s", str(error))

            tmp_dict = dict(CODE_QUAL_ELEMENT)
            rule = error["id"]
            tmp_dict["check_name"] = rule
            tmp_dict["categories"] = list(
                __get_codeclimate_category(error["category"]).split("\n")
            )
            tmp_dict["severity"] = __get_codeclimate_severity(error["severity"])
            tmp_dict["description"] = f"[{tool}] {error['message']}"

            path = ""
            line = -1
            column = -1
            
            # if "@file0" in error["location"]:
            #     tmp_dict["description"] = "Also see source file: {}\n\n{}".format(
            #         error["location"]["@file0"], tmp_dict["description"]
            #     )

            path = error["file"]
            line = int(error["line"])

            column = 0
            if "column" in error:
                column = int(error["column"])

            tmp_dict["location"]["path"] = path
            tmp_dict["location"]["positions"]["begin"]["line"] = line
            tmp_dict["location"]["positions"]["begin"]["column"] = column

            tmp_dict["content"] = {"body": ""}

            # REMOVING the below lines, because reports with many issues can be
            # difficult for GitLab to parse. Maybe we'll make this a CLI arg in the
            # future so users can get verbose messages if they want them?
            # if "@verbose" in error:
            #    # Sometimes CppCheck will put the same message in @msg and @verbose
            #    # fields. Don't bloat the JSON report with redundant info.
            #    if error["@verbose"] != tmp_dict["description"]:
            #        tmp_dict["content"]["body"] = error["@verbose"]

            if "cwe" in error and error['cwe'] is not None:
                cwe_id = error["cwe"]
                tmp_dict["description"] += f" (CWE-{cwe_id})"

                # Append to Markdown-format content
                msg = f"Refer to [CWE-{cwe_id}]: https://cwe.mitre.org/data/definitions/{cwe_id}.html"
                tmp_dict["content"]["body"] += msg

            # GitLab requires the fingerprint field. Code Climate describes this as
            # being used to uniquely identify the issue, so users could "exclude it
            # from future analysis."
            #
            # The components of the fingerprint aren't well defined, but Code Climate
            # has some examples here:
            # https://github.com/codeclimate/codeclimate-duplication/blob/1c118a13b28752e82683b40d610e5b1ee8c41471/lib/cc/engine/analyzers/violation.rb#L83
            # https://github.com/codeclimate/codeclimate-phpmd/blob/7d0aa6c652a2cbab23108552d3623e69f2a30282/tests/FingerprintTest.php

            codeline = ''#_get_line_from_file(path, line).strip()

            # _Might_ remove the (rounded) line number if something else seems better, in the future.
            fingerprint_str = (
                path
                + ":"
                + str(int(math.ceil(line / 10.0)) * 10)
                + "-"
                + rule
                + "-"
                + codeline
            )
            log.debug("Fingerprint string: '%s'", fingerprint_str)
            tmp_dict["fingerprint"] = hashlib.md5(
                (fingerprint_str).encode("utf-8")
            ).hexdigest()

            # Append this record
            arr_out.append( deepcopy(tmp_dict))

    if len(arr_out) == 0:
        log.warning("Result is empty")
    return arr_out


def __init_logging():
    """Setup root logger to log to console, when this is run as a script"""
    h_console = logging.StreamHandler()
    log_fmt_short = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s: %(message)s", datefmt="%H:%M:%S"
    )
    h_console.setFormatter(log_fmt_short)

    # Add console handler to root logger
    logging.getLogger("").addHandler(h_console)


def __get_args() -> argparse.Namespace:
    """Parse CLI args with argparse"""
    # Make parser object
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input-file",
        metavar="INPUT_XML_FILE",
        dest="input_file",
        type=str,
        default="piocheck.json",
        help="the cppcheck XML output file to read defects from (default: %(default)s)",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        metavar="FILE",
        dest="output_file",
        type=str,
        default="codecoverage.json",
        help="output filename to write JSON to (default: %(default)s)",
    )

    # parser.add_argument(
    #     "-s",
    #     "--source-dir",
    #     metavar="SOURCE_DIR",
    #     type=str,
    #     default=".",
    #     help="Base directory where source code files can be found. (default: '%(default)s')",
    # )

    parser.add_argument(
        "-l",
        "--loglevel",
        metavar="LVL",
        type=str,
        choices=["debug", "info", "warn", "error"],
        default="debug",
        help="set logging message severity level (default: '%(default)s')",
    )

    parser.add_argument(
        "-v",
        "--version",
        dest="print_version",
        action="store_true",
        help="print version and exit",
    )

    return parser.parse_args()


def main() -> int:
    """Convert a CppCheck XML file to Code Climate JSON file, at the command line."""

    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        return 1

    __init_logging()
    m_log = logging.getLogger(__name__)

    args = __get_args()
    logging.getLogger().setLevel(args.loglevel.upper())

    if args.print_version:
        print(__version__)
        return 0

    # t_start = timeit.default_timer()

    if not convert_file(fname_in=args.input_file, fname_out=args.output_file):
        m_log.error("Conversion failed")
        return 1

    # t_stop = timeit.default_timer()
    # log.debug("Conversion time: %f ms", ((t_stop - t_start) * 1000))

    return 0

    # log.debug("Generating SVG badge")
    # badge = anybadge.Badge("cppcheck", "-TESTING-")
    # badge.write_badge(os.path.splitext(args.output_file)[0] + ".svg", overwrite=True)


if __name__ == "__main__":
    sys.exit(main())

