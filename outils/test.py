import sys,os,re,glob
from playwright.sync_api import sync_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
pages=sorted(glob.glob(R+'/*.html'));W=[int(x) for x in sys.argv[1:] if x!='-v'] or [390,768,1280]
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch();
    for f in pages:
        n=os.path.basename(f)
        kb=sum(os.path.getsize(R+'/'+i) for i in set(re.findall(r'images/[\w.\-]+',open(f).read())) if os.path.exists(R+'/'+i))
        if kb>1.5*1024*1024:bad.append(f'{n}: images {kb//1024} Ko > 1,5 Mo')
        for w in W:
            pg=b.new_page(viewport={'width':w,'height':844 if w<700 else 800});pg.goto('file://'+f);pg.wait_for_timeout(300)
            pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('on'))")
            r=pg.evaluate("""()=>{const o=[];const vh=innerHeight,d=document.documentElement;
            if(d.scrollWidth>innerWidth+1)o.push('débordement horizontal '+d.scrollWidth);
            document.querySelectorAll('body *').forEach(e=>{const cs=getComputedStyle(e);if(!e.childNodes.length||![...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()))return;if(cs.display=='none'||e.closest('.sr,.skip'))return;if(parseFloat(cs.fontSize)<15.99)o.push('texte '+cs.fontSize+' '+e.tagName+'.'+e.className+' "'+e.textContent.trim().slice(0,20)+'"')});
            document.querySelectorAll('a,button').forEach(e=>{const r=e.getBoundingClientRect(),cs=getComputedStyle(e);if(!r.width||cs.display=='none'||e.classList.contains('skip'))return;if(r.height<43.5||r.width<43.5)o.push('cible '+Math.round(r.width)+'x'+Math.round(r.height)+' '+(e.textContent.trim().slice(0,20)||e.className))});
            document.querySelectorAll('img').forEach(i=>{if(i.complete&&!i.naturalWidth)o.push('image cassée '+i.src.slice(-30));const r=i.getBoundingClientRect();if(r.width>i.naturalWidth+2&&i.naturalWidth)o.push('image agrandie '+i.src.slice(-30))});
            document.querySelectorAll('main>section').forEach(s=>{const h=s.getBoundingClientRect().height;o.push('H '+s.className.split(' ').filter(c=>c!='s'&&c!='s-dark')[0]+' '+Math.round(h/vh*100)+'%')});
            const h=document.querySelector('.site-footer');o.push('H footer '+Math.round(h.getBoundingClientRect().height/vh*100)+'%');return o}""")
            for x in r:
                if x.startswith('H '):
                    if '-v' in sys.argv:print(n,w,x)
                    elif w==1280 or w==390:bad.append(f'{n} {w}: {x}') if False else None
                else:bad.append(f'{n} {w}: {x}')
        # liens locaux
        for h in re.findall(r'href="([^"#:]+?)(?:#[^"]*)?"',open(f).read()):
            if not os.path.exists(R+'/'+h):bad.append(f'{n}: lien absent {h}')
    b.close()
print('\n'.join(sorted(set(bad))) or 'tout est OK')
