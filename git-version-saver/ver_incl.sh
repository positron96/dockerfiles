REPO=${2:-"."}
COMMIT=${3:-HEAD}

DATE=$(git -C $REPO show --format="%cd" --date=short -s $COMMIT)
DATE_SHORT=$(git -C $REPO show --format="%cd" --date=format:%Y%m%d -s $COMMIT)
HASH=$(git -C $REPO show --format="%h" -s $COMMIT)
TAG=$(git -C $REPO describe --tags $COMMIT | sed 's/-g[a-z0-9]\{7\}//')
VER_SHORT="${DATE_SHORT}-$(echo $TAG | tr '\\' '_')-$HASH"
