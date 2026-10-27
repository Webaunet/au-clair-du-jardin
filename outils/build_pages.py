import re,os,sys
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
idx=open(R+'/index.html').read()
head0=idx[:idx.index('<svg width="0"')]
shell=idx[idx.index('<svg width="0"'):idx.index('<main')]
foot=idx[idx.index('</main>')+len('</main>'):]
for n in ['prestations','a-propos','contact']:
    f=open(R+f'/outils/pages/{n}.html').read()
    t=re.search(r'<!--title:(.*?)-->',f).group(1);d=re.search(r'<!--desc:(.*?)-->',f).group(1);c=re.search(r'<!--current:(.*?)-->',f).group(1)
    body=re.sub(r'<!--(title|desc|current):.*?-->\n','',f)
    h=re.sub(r'<title>.*?</title>',f'<title>{t}</title>',head0)
    h=re.sub(r'(<meta name="description" content=").*?(">)',lambda m:m.group(1)+d.replace('"','&quot;')+m.group(2),h)
    s=shell.replace(' aria-current="page"','').replace(f'<a href="{c}">',f'<a href="{c}" aria-current="page">')
    assert f'href="{c}" aria-current="page"' in s,n
    open(R+f'/{n}.html','w').write(h+s+body+foot)
print('pages ok')
