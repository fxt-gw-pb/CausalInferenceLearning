#!/usr/bin/env python3
"""Public-only static build. No private sources or sibling paths are consulted."""
import json, pathlib, shutil, sys, importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from check_content import validate

def main():
    catalog,lessons=validate()
    out=ROOT/'dist'
    if out.exists():shutil.rmtree(out)
    out.mkdir()
    for name in ['index.html','styles.css','app.js','math.js','state.js','favicon.svg']:
        shutil.copy2(ROOT/'src'/name,out/name)
    (out/'content').mkdir()
    (out/'content'/'course.json').write_text(json.dumps({'catalog':catalog,'lessons':lessons},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (out/'.nojekyll').write_text('')
    print(f'Built {len(catalog["weeks"])} weeks / {len(lessons)} lessons to dist/. No deployment performed.')
if __name__=='__main__':main()
