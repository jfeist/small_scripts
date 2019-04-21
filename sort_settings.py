#!/usr/bin/env python
# coding: utf-8

import json

def sort_json_settings(fi):
    with open(fi,'r',encoding='utf8') as f:
        js = json.load(f)

    for k,v in js.items():
        if type(v) is list and 'args' not in k:
            js[k] = sorted(v)

    with open(fi,'w',encoding='utf8') as f:
        json.dump(js,f,sort_keys=True,ensure_ascii=False,indent=2)
        f.write('\n')

if __name__ == "__main__":
    import sys
    for fi in sys.argv[1:]:
        sort_json_settings(fi)
        print("rewrote",fi)
