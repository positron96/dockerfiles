#!/bin/env python

import urllib.request
import urllib.error
import json
import os
import subprocess as se

REG_HOST = os.getenv('REG_HOST', 'ghcr.io')
REG_PATH = os.getenv('REG_PATH', 'positron96/dockerfiles')

PATH = os.getenv('REPO_PATH', '.')#'/home/positron/Documents/dockerfiles'

folders = [ f for f in os.listdir(PATH) if os.path.isdir(os.path.join(PATH,f) ) ]
folders = [ f for f in folders if os.path.isfile(os.path.join(PATH, f, 'Dockerfile') )]

OUTFILE = os.getenv('OUTFILE', 'files.txt')

def getlocal(f):
    r = se.run('git log "--format=%H %cs" -1 '+f, cwd=PATH, shell=True, capture_output=True).stdout
    r = r.decode().strip().split(' ', 1)
    #return datetime.datetime.fromisoformat(r[1]), r[0]
    return f'{r[1]}-{r[0][0:8]}'
    

def gettoken(realm,scope,service=None, **kwargs):
    with urllib.request.urlopen(f"{realm}?service={service}&scope={scope}") as response:
        r = json.loads( response.read() )
        token = r['token']
        return token
  
def getregistry(folder, token=None):
    """
    @see https://docs.docker.com/registry/spec/auth/token/
    """
    try:
        headers = {}
        if token: headers['Authorization'] = 'Bearer '+token
        req = urllib.request.Request(f"https://{REG_HOST}/v2/{REG_PATH}/{folder}/tags/list", 
            headers=headers)
        with urllib.request.urlopen(req) as response:
            _tags = json.loads(response.read() ) ['tags']

#         tags = []
#         for t in _tags:
#             try:
#                 tags.append( (datetime.date.fromisoformat(t[0:10]), t[11:] ) )
#             except: 
#                 pass
#         print( sorted(tags, key=lambda t:t[0]) )
        return _tags
    except urllib.error.HTTPError as e:
        if e.code==401:
            auth = e.headers['Www-Authenticate'].split(' ', 1)[1]
            auth = [s.split('=') for s in auth.split(',')]
            auth = { s[0]:s[1][1:-1] for s in auth }
            try:
                token = gettoken(**auth)
                return getregistry(folder, token)
            except urllib.error.HTTPError as ee:
                ee._cause_ = e
                e = ee
                
        raise e

def need_update(l,rr):    
    return not (l in set(rr))
    


with open(OUTFILE, 'w') as ff:
    cnt=0
    for f in folders:
        l = getlocal(f)
        try:
            r = getregistry(f)
        except Exception as e:
            print('failed registry request:', e)
            r = ()
        if need_update(l,r):
            tag = f'{REG_HOST}/{REG_PATH}/{f}'
            #print(f'docker build {f} --tag {tag}:{l} --tag {tag}:latest')
            print('will rebuild', f, tag, l)
            ff.write(f'{f} {tag} {l}\n')
            cnt += 1
        else:
            print('no need to update ', f)
    if cnt==0:
        print('No folders to build')
        
        


