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
            const h=document.querySelector('.site-footer');o.push('H footer '+Math.round(h.getBoundingClientRect().height/vh*100)+'%');if(document.querySelectorAll('h1').length!==1)o.push('h1 x'+document.querySelectorAll('h1').length);
            document.querySelectorAll('img').forEach(i=>{if(!i.hasAttribute('alt'))o.push('alt manquant '+i.src.slice(-25))});
            const P=c=>{const m=c.match(/[\d.]+/g).map(Number);return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1}};
            const L=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b)};
            const bgOf=e=>{let x=e;while(x){const cs=getComputedStyle(x);if(cs.backgroundImage!=='none')return null;const c=P(cs.backgroundColor);if(c.a>.5)return c;x=x.parentElement}return {r:255,g:255,b:255,a:1}};
            document.querySelectorAll('body *').forEach(e=>{if(![...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()))return;const cs=getComputedStyle(e);if(cs.display=='none'||e.closest('.sr,.skip,svg'))return;const bg=bgOf(e);if(!bg)return;let c=P(cs.color);if(c.a<1)c={r:c.r*c.a+bg.r*(1-c.a),g:c.g*c.a+bg.g*(1-c.a),b:c.b*c.a+bg.b*(1-c.a)};const l1=L(c),l2=L(bg),r=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);const fs=parseFloat(cs.fontSize),big=fs>=24||(fs>=18.66&&+cs.fontWeight>=700);if(r<(big?3:4.5))o.push('contraste '+r.toFixed(1)+' '+e.tagName+'.'+e.className+' "'+e.textContent.trim().slice(0,18)+'"')});
            const rc=e=>e&&e.offsetParent!==null?e.getBoundingClientRect():null;const lg=rc(document.querySelector('.logo')),nv=rc(document.querySelector('.nav-list')),cl=rc(document.querySelector('.call')),bg2=rc(document.querySelector('.burger'));
            const ov=(a,b)=>a&&b&&a.left<b.right&&b.left<a.right;if(ov(lg,nv)||ov(nv,cl)||ov(lg,cl)||ov(lg,bg2)||ov(cl,bg2))o.push('chevauchement en-tête');
            if(innerWidth>980&&!nv)o.push('menu absent');if(innerWidth<=980&&!bg2)o.push('burger absent');
            return o}""")
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
