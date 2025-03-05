#!/usr/bin/env python
# coding: utf-8

import argparse
import bs4
import requests
import json
import io
from zipfile import ZipFile

parser = argparse.ArgumentParser(description='Download all projects from Overleaf.')
parser.add_argument('cookie', help='Session cookie for Overleaf')
parser.add_argument('-s','--server', help='Overleaf server', default='https://www.overleaf.com')
parser.add_argument('-e','--extract', help='Extract zips', action='store_true')
parser.add_argument('--download-trashed', help='Download trashed projects', action='store_true')
parser.add_argument('-p','--project', help='Download specific project (by id). Can be given multiple times.', action='append')
args = parser.parse_args()

if 'overleaf.com' in args.server:
    cookie_name = 'overleaf_session2'
else:
    cookie_name = 'overleaf.sid'
cookies = {cookie_name: args.cookie}

req = requests.get(f'{args.server}/project', cookies=cookies)
soup = bs4.BeautifulSoup(req.text, 'html.parser')
tags = soup.find_all("meta", {"name": "ol-prefetchedProjectsBlob"})
assert len(tags) == 1
j = json.loads(tags[0].get("content"))
projects = j["projects"]
if args.project:
    projects = [p for p in projects if p["id"] in args.project]
elif not args.download_trashed:
    projects = [p for p in projects if not p["trashed"]]

for p in projects:
    req = requests.get(f'{args.server}/project/{p["id"]}/download/zip', cookies=cookies)
    if req.status_code != 200:
        print(f'Error downloading project {p["id"]}: {p["name"]}. Status code: {req.status_code}')
        continue
    
    if args.extract:
        with ZipFile(io.BytesIO(req.content), 'r') as z:
            z.extractall(p["name"])
        print(f'downloaded and extracted {p["id"]}: {p["name"]}')
    else:
        with open(f'{p["name"]}.zip', 'wb') as f:
            f.write(req.content)
        print(f'downloaded {p["id"]}: {p["name"]}.zip')
