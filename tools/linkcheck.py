import os,re,sys,urllib.parse
root=sys.argv[1] if len(sys.argv)>1 else '.'
bad=[];n=0;refs=0
for d,_,fs in os.walk(root):
    if '/tools' in d: continue
    for f in fs:
        if not f.endswith('.html'): continue
        n+=1;p=os.path.join(d,f);s=open(p,encoding='utf8').read()
        for u in re.findall(r'(?:href|src)="([^"#?]+)',s):
            if re.match(r'(https?:|mailto:|tel:|data:|javascript:)',u): continue
            refs+=1;t=os.path.normpath(os.path.join(d,urllib.parse.unquote(u)))
            if not os.path.exists(t): bad.append((p,u))
print('pages',n,'refs',refs,'broken',len(bad))
for b in bad[:30]: print(b)
