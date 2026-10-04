#!/usr/bin/env python3
import json,pathlib,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
TYPES={'paragraph','list','callout','equation','table','code','exercise','interactive','diagram'}
def validate():
    catalog=json.loads((ROOT/'content/catalog.json').read_text())
    assert len(catalog['weeks'])==9,'Expected nine weeks'
    counts=[10,8,2,4,3,2,3,2,5]
    ids=[];lessons=[];exercises=set()
    schema=json.loads((ROOT/'content/schema/lesson.schema.json').read_text())
    try:
        import jsonschema
    except ImportError:
        jsonschema=None
    for wi,w in enumerate(catalog['weeks'],1):
        assert w['number']==wi and w['id']==f'w{wi:02}'
        assert len(w['lessons'])==counts[wi-1]
        for i,lid in enumerate(w['lessons'],1):
            assert re.fullmatch(r'w0[1-9]-l\d{2}',lid)
            data=json.loads((ROOT/'content/lessons'/f'{lid}.json').read_text())
            if jsonschema:jsonschema.validate(data,schema)
            assert data['id']==lid and data['week']==wi and data['order']==i
            assert data['status'] in ['outline','draft','demo','ready']
            assert data['codeStatus'] in ['none','not-run','verified']
            if data['status']=='outline':assert not data['sections'],'Outline must not silently contain unfinished prose'
            sectionids=set();localex=[]
            for s in data['sections']:
                assert s['id'] not in sectionids and re.fullmatch('[a-z][a-z0-9-]*',s['id']);sectionids.add(s['id'])
                for b in s['blocks']:
                    assert b['type'] in TYPES
                    if b['type']=='exercise':
                        assert b['id'] not in exercises and re.fullmatch('[a-z0-9-]+',b['id'])
                        assert 2<=len(b['options'])<=5 and 0<=b['answer']<len(b['options'])
                        exercises.add(b['id']);localex.append(b['id'])
                    if b['type']=='table':assert all(len(row)==len(b['headers']) for row in b['rows'])
                    if b['type']=='code':assert b['execution'] in ['not-run','verified']
                    if b['type']=='interactive':assert b['kind']=='standardization'
                    if b['type']=='diagram':assert b['kind']=='confounding-dag'
            assert localex==data['exerciseIds'],'Exercise IDs must match visible exercises'
            for r in data['references']:assert r['url'].startswith('https://')
            ids.append(lid);lessons.append(data)
    assert len(ids)==len(set(ids))==39
    assert {x.stem for x in (ROOT/'content/lessons').glob('*.json')}==set(ids)
    public_text=json.dumps({'catalog':catalog,'lessons':lessons},ensure_ascii=False)
    for forbidden in ['library_file_id','source_video','/workspace/','/Users/','/tmp/','review_ledger','transcript','causal_course_private','.mp4','.m4a','.wav','.pdf!']:
        assert forbidden not in public_text, f'Forbidden public-source or style marker: {forbidden}'
    print(f'Content valid: 9 weeks, 39 unique lessons, {len(exercises)} exercises; '+('full JSON Schema validated.' if jsonschema else 'core validation passed (optional jsonschema unavailable).'))
    return catalog,lessons
if __name__=='__main__':validate()
