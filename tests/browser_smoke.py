#!/usr/bin/env python3
"""Optional isolated Chromium fixture tests. No public deployment or managed-browser access.
All https://causal.test/ responses are fulfilled from the local dist allowlist.
Requires Python playwright and an installed Chromium executable.
"""
import json,pathlib,sys,mimetypes
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'.qa';OUT.mkdir(exist_ok=True)
BASE='https://causal.test/project/'

def main():
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1050},device_scale_factor=1)
        def fixture(route):
            path=route.request.url.split('causal.test/project/',1)[-1].split('?',1)[0].split('#',1)[0] or 'index.html'
            file=(ROOT/'dist'/path).resolve()
            if not file.is_relative_to(ROOT/'dist') or not file.is_file(): route.abort();return
            route.fulfill(status=200,body=file.read_bytes(),content_type=mimetypes.guess_type(file)[0] or 'application/octet-stream')
        context.route('**/*',fixture)
        page=context.new_page();errors=[]
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto(BASE);page.get_by_role('heading',name='因果推断学习笔记',exact=True).wait_for()
        assert page.locator('.week-card').count()==9
        assert page.locator('#main .lesson-row').count()==39
        page.screenshot(path=str(OUT/'desktop-home.png'),full_page=True)
        page.locator('#toggle-weeks').click();assert page.locator('.week-card[open]').count()==9
        page.locator('#toggle-weeks').click();assert page.locator('.week-card[open]').count()==0
        page.locator('#search-button').click();page.locator('#search-input').fill('标准化')
        assert page.locator('.search-result').count()>0
        page.locator('#search-input').press('Escape');assert not page.locator('#search-dialog').is_visible()
        page.locator('#search-button').click();page.locator('#search-input').fill('<script>alert(1)</script>')
        assert page.locator('.search-result').count()==0
        page.locator('#search-input').press('Escape')
        page.goto(BASE+'#/lesson/w02-l04');page.locator('.reading-section').first.wait_for()
        assert page.locator('math').count()==2
        assert page.locator('math').first.evaluate('(e)=>e.getBoundingClientRect().height')>15
        page.locator('[data-bookmark]').click();assert page.locator('[data-bookmark]').get_attribute('aria-pressed')=='true'
        page.locator('[data-complete]').click();assert page.locator('[data-complete]').get_attribute('aria-pressed')=='true'
        page.reload();page.locator('[data-bookmark][aria-pressed=true]').wait_for()
        assert page.locator('[data-complete]').get_attribute('aria-pressed')=='true'
        page.screenshot(path=str(OUT/'desktop-lesson.png'),full_page=True)
        slider=page.locator('[data-target]');slider.fill('100');assert page.locator('[data-rd]').inner_text()=='−10.0'
        page.locator('.lab-reset').click();assert slider.input_value()=='50'
        first=page.locator('[data-exercise="w02-l04-target"]')
        first.locator('button[type=submit]').click();assert '请先选择' in first.locator('.answer-feedback').inner_text()
        first.locator('input[value="0"]').check();first.locator('button[type=submit]').click();assert first.locator('.answer-feedback.incorrect').is_visible()
        first.locator('input[value="1"]').check();first.locator('button[type=submit]').click();assert first.locator('.answer-feedback.correct').is_visible()
        page.goto(BASE+'#/saved');page.get_by_role('heading',name='学习记录',exact=True).wait_for();assert page.locator('.lesson-row').count()==2
        # Outline completion remains disabled; choose a currently unpopulated lesson.
        data=json.loads((ROOT/'dist/content/course.json').read_text());outlines=[l['id'] for l in data['lessons'] if l['status']=='outline']
        if outlines:
            page.goto(BASE+'#/lesson/'+outlines[-1]);page.locator('[data-complete]').wait_for();assert page.locator('[data-complete]').is_disabled()
        page.goto(BASE+'#/lab/standardization');page.locator('[data-target]').wait_for();page.locator('[data-target]').fill('0');assert page.locator('[data-rd]').inner_text()=='−4.0'
        page.screenshot(path=str(OUT/'desktop-lab.png'),full_page=True)
        page.goto(BASE+'#/missing');page.get_by_role('heading',name='没有找到这页内容').wait_for()
        page.get_by_role('link',name='返回课程目录',exact=True).click();page.locator('.feature').wait_for()
        page.go_back();page.get_by_role('heading',name='没有找到这页内容').wait_for()
        page.go_forward();page.locator('.feature').wait_for()
        mobile=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
        mobile.route('**/*',fixture);p=mobile.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
        p.goto(BASE);p.locator('.feature').wait_for();p.screenshot(path=str(OUT/'mobile-home.png'),full_page=True)
        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Mobile homepage overflow'
        p.locator('#menu-button').click();assert p.locator('#mobile-nav').is_visible()
        p.locator('#mobile-nav .primary-nav a[href="#/saved"]').click();assert not p.locator('#mobile-nav').is_visible();p.get_by_role('heading',name='学习记录',exact=True).wait_for()
        p.locator('#menu-button').click();p.locator('[data-close=mobile-nav]').click();assert not p.locator('#mobile-nav').is_visible()
        p.locator('#search-button').click();p.locator('#search-input').fill('潜在结果与标准化');p.locator('.search-result').click();p.locator('article').wait_for();assert not p.locator('#search-dialog').is_visible()
        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Mobile article overflow'
        p.screenshot(path=str(OUT/'mobile-lesson.png'),full_page=True)
        p.goto(BASE+'#/lab/standardization');p.locator('[data-target]').wait_for();p.screenshot(path=str(OUT/'mobile-lab.png'),full_page=True)
        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Mobile lab overflow'
        narrow=browser.new_context(viewport={'width':320,'height':740});narrow.route('**/*',fixture);np=narrow.new_page();np.goto(BASE+'#/lesson/w02-l04');np.locator('article').wait_for();assert np.evaluate('document.documentElement.scrollWidth<=innerWidth'),'320px article overflow'
        np.screenshot(path=str(OUT/'narrow-lesson.png'),full_page=True)
        # Resilient storage: both blocked and malformed local data.
        blocked=browser.new_context();blocked.route('**/*',fixture);blocked.add_init_script('Object.defineProperty(window,"localStorage",{get(){throw new Error("blocked for test")}})');bp=blocked.new_page();bp.on('pageerror',lambda e:errors.append(str(e)));bp.goto(BASE+'#/lesson/w02-l04');bp.locator('article').wait_for();bp.locator('[data-bookmark]').click();assert bp.locator('[data-bookmark]').get_attribute('aria-pressed')=='true'
        corrupt=browser.new_context();corrupt.route('**/*',fixture);corrupt.add_init_script('localStorage.setItem("causal-study:v1","{broken")');cp=corrupt.new_page();cp.goto(BASE);cp.locator('.feature').wait_for()
        assert not errors,errors
        report={'status':'passed','test_mode':'isolated local Chromium with routed dist fixtures; not managed cloud-browser access','viewports':['1440x1050','390x844','320x740'],'checks':['39 lesson routes/catalog entries','expand/collapse all','search and Escape/reopen','search injection literal','native MathML layout','bookmark and completion reload persistence','outline completion disabled','exercise empty/wrong/correct','slider endpoints and reset','saved view','unknown routes','back/forward','mobile menu close and navigation','mobile search navigation','horizontal overflow','blocked/corrupt storage resilience','zero page errors'],'screenshots':[x.name for x in OUT.glob('*.png')]}
        (OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False,indent=2));browser.close()
if __name__=='__main__':main()
