import re,csv,collections,glob,json
src=open('geo.py',encoding='utf8').read().split("rows=[]")[0]
ns={};exec(src,ns);classify=ns['classify'];CONT=ns['CONT']
M={m:i+1 for i,m in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'])}
M3={k[:3]:v for k,v in M.items()}
ROSTER=['Nacho Toker','Axel Itzcovitz','Feli Garabato','Antonio Santos','Lucas Greco','Sandro Anello','Bruno Feinsilber','Ale Feinsilber','Dario Feinsilber','Fede Moia','Martin Feinsilber']
NAME={'Tú':'Axel Itzcovitz','Alejandro Feinsilber':'Ale Feinsilber','Martín Feinsilber':'Martin Feinsilber','+54 9 11 3230-1243':'Antonio Santos'}
NAME.update({n:n for n in ROSTER})
places={}
for l in open('/sessions/trusting-nice-davinci/mnt/Maptap/informes/maptap-ciudades.md',encoding='utf8'):
    m=re.match(r'\| (\d+)/(\d+) \| (.*) \|\s*$',l)
    if m: places[(int(m.group(2)),int(m.group(1)))]=[x.strip() for x in m.group(3).split(' | ')]
# finales validados
fin=set()
for r in csv.DictReader(open('amateur_scores.csv')): fin.add((r['date'],r['player'].replace('Martín','Martin'),int(r['score'])))
cur=None;CH={}
for l in open('/sessions/trusting-nice-davinci/mnt/Maptap/informes/maptap-resultados-diarios.md',encoding='utf8'):
    m=re.match(r'## (2026-\d\d-\d\d)',l)
    if m: cur=m.group(1);continue
    m=re.match(r'\| (.+?) \| (\d+) \|',l)
    if cur and m: fin.add((cur,m.group(1).strip().replace('Martín','Martin'),int(m.group(2))))
hdr=re.compile(r'^\[[^\]]+\]\s+\*\*(.+?):\*\*\s?(.*)$')
url=re.compile(r'www\.maptap\.gg\s+(\w+)\s+(\d+)\s*$')
single=re.compile(r'^www\.maptap\.gg\s+(\w+)\s+(\d+)\s+(\d+)\S*\s+(\d+)\S*\s+(\d+)\S*\s+(\d+)\S*\s+(\d+)\S*\s+Final score:\s*(\d+)')
chh=re.compile(r'Challenge Round - (\w{3}) (\d+)')
rnd=re.compile(r'^\s*(\d+)\S*\s+(\d+)\S*\s+(\d+)\S*\s+(\d+)\S*\s+(\d+)\S*\s*$')
fn=re.compile(r'^Final score:\s*(\d+)')
cs=re.compile(r'^Score:\s*(\d+) in ([\d.]+)s')
games={};chg={};rej=[];chrej=[]
files=['chat.md','chat-d794649f.md']+[f.split('/')[-1] for f in glob.glob('/sessions/trusting-nice-davinci/mnt/uploads/*_chat.md')]
for f in files:
    lines=open('/sessions/trusting-nice-davinci/mnt/uploads/'+f,encoding='utf8').read().split('\n')
    sender=None;pend=None;mode=None
    for ln in lines:
        h=hdr.match(ln);txt=ln
        if h: sender=NAME.get(h.group(1).strip(),h.group(1).strip());txt=h.group(2);pend=None;mode=None
        if txt.startswith('>'): continue
        c=chh.search(txt)
        if c: mode='ch';pend=(M3[c.group(1)],int(c.group(2)),None);continue
        sl=single.match(txt)
        if sl and sl.group(1) in M and sender in ROSTER:
            rs=[int(x) for x in sl.groups()[2:7]];k=(M[sl.group(1)],int(sl.group(2)),sender);sc=int(sl.group(8));d=f'2026-{k[0]:02d}-{k[1]:02d}'
            if (d,sender,sc) in fin:
                if k not in games: games[k]=(rs,sc)
            else: rej.append((d,sender,sc,sum(rs)))
            pend=None;mode=None;continue
        u=url.search(txt)
        if u and u.group(1) in M: mode='n';pend=(M[u.group(1)],int(u.group(2)),None);continue
        if mode=='ch' and pend and pend[2] is None:
            r=rnd.match(txt)
            if r: pend=(pend[0],pend[1],[int(x) for x in r.groups()]);continue
        if mode=='ch' and pend and pend[2] is not None:
            m=cs.match(txt)
            if m and sender in ROSTER:
                k=(pend[0],pend[1],sender)
                if k not in chg: chg[k]=(pend[2],int(m.group(1)),float(m.group(2)))
            if m: pend=None;mode=None
            continue
        if mode=='n' and pend and pend[2] is None:
            r=rnd.match(txt)
            if r: pend=(pend[0],pend[1],[int(x) for x in r.groups()]);continue
        if mode=='n' and pend and pend[2] is not None:
            m=fn.match(txt)
            if m and sender in ROSTER:
                k=(pend[0],pend[1],sender);sc=int(m.group(1));d=f'2026-{pend[0]:02d}-{pend[1]:02d}'
                if (d,sender,sc) in fin:
                    if k not in games: games[k]=(pend[2],sc)
                else: rej.append((d,sender,sc,sum(pend[2])))
            if m: pend=None;mode=None

# partidas pegadas en el chat de la sesion (aun no estan en una exportacion)
EXTRA={(10,14,'Antonio Santos'):([94,98,80,83,99],898),(10,14,'Bruno Feinsilber'):([97,93,87,90,99],931),(10,14,'Feli Garabato'):([93,97,99,80,99],925),(10,14,'Fede Moia'):([96,98,92,89,95],930),
 (10,14,'Dario Feinsilber'):([96,97,80,80,99],890),(10,14,'Martin Feinsilber'):([97,93,80,86,99],905),
 (10,15,'Ale Feinsilber'):([100,80,93,93,46],783),(10,15,'Dario Feinsilber'):([91,91,10,94,64],676),
 (10,15,'Lucas Greco'):([98,92,95,99,65],872),(10,15,'Sandro Anello'):([100,98,91,97,63],860),
 (10,15,'Nacho Toker'):([95,97,99,98,92],960),(10,15,'Antonio Santos'):([91,99,86,98,75],881),
 (10,15,'Axel Itzcovitz'):([100,98,100,98,49],839),(10,15,'Feli Garabato'):([100,94,100,98,100],988),(10,15,'Fede Moia'):([99,96,99,95,75],903),
 (10,15,'Bruno Feinsilber'):([99,86,80,85,64],792),(10,15,'Martin Feinsilber'):([99,88,80,98,89],908),(10,16,'Sandro Anello'):([94,94,80,87,76],837),(10,16,'Axel Itzcovitz'):([100,95,85,90,97],926),(10,16,'Lucas Greco'):([100,95,89,87,86],892),(10,16,'Martin Feinsilber'):([97,92,80,88,83],862),(10,16,'Ale Feinsilber'):([100,99,86,91,100],944),(10,16,'Dario Feinsilber'):([100,93,96,91,95],943),(10,16,'Antonio Santos'):([100,96,80,86,93],893),(10,16,'Nacho Toker'):([100,93,91,88,98],933),(10,16,'Feli Garabato'):([100,99,98,79,83],881),(10,16,'Bruno Feinsilber'):([93,93,82,88,87],875),(10,16,'Fede Moia'):([98,84,99,83,82],875),(10,17,'Sandro Anello'):([98,100,100,97,81],932),(10,17,'Lucas Greco'):([99,100,92,96,80],911),(10,17,'Axel Itzcovitz'):([100,100,92,96,90],942),(10,17,'Bruno Feinsilber'):([96,100,80,97,80],887),(10,17,'Dario Feinsilber'):([94,100,80,94,88],900),(10,17,'Martin Feinsilber'):([95,100,77,94,80],871),(10,17,'Ale Feinsilber'):([37,100,80,100,78],831),(10,17,'Antonio Santos'):([99,100,80,97,81],893),(10,17,'Nacho Toker'):([97,100,100,96,80],925),(10,17,'Fede Moia'):([93,100,100,97,87],945),(10,17,'Feli Garabato'):([92,100,92,85,93],910),
 (10,18,'Axel Itzcovitz'):([94,100,100,93,85],928),(10,18,'Nacho Toker'):([95,100,99,92,95],954),(10,18,'Antonio Santos'):([95,95,100,87,85],906),(10,18,'Fede Moia'):([93,97,90,81,86],871),(10,18,'Dario Feinsilber'):([94,100,86,91,58],813),(10,18,'Bruno Feinsilber'):([94,100,100,91,14],709),(10,18,'Ale Feinsilber'):([96,95,100,80,85],886),(10,18,'Lucas Greco'):([96,100,86,91,69],848),(10,18,'Sandro Anello'):([99,100,86,94,62],839),(10,18,'Feli Garabato'):([94,97,86,89,88],894)}
for k,v in EXTRA.items():
    d=f'2026-{k[0]:02d}-{k[1]:02d}'
    if (d,k[2],v[1]) in fin and k not in games: games[k]=v
print('normal',len(games),'rechazadas',len(rej));print(rej[:40])
dates=sorted({(k[0],k[1]) for k in games});print(dates[0],dates[-1],len(dates))
# faltantes vs logs
det={(f'2026-{k[0]:02d}-{k[1]:02d}',k[2]) for k in games}
miss=sorted({(d,p) for d,p,s in fin if p in ROSTER}-det);print('faltan',len(miss),miss[:40])
# verificacion: la suma simple coincide aprox con final?
bad=[(k,sum(v[0]),v[1]) for k,v in games.items() if not(abs(v[1]-sum(v[0])*2)<=40)]
print('suma anomala',len(bad),bad[:5])
rows=[]
for (mo,dd,p),(rs,fs) in games.items():
    for i,s in enumerate(rs):
        pl=places[(mo,dd)][i];pa,sub=classify(pl);rows.append(dict(p=p,mo=mo,dd=dd,r=i,s=s,place=pl,pais=pa,sub=sub,cont=CONT[sub],final=fs))
rows.sort(key=lambda r:(r['mo'],r['dd'],r['p'],r['r']))
json.dump(rows,open('rounds_all.json','w'),ensure_ascii=False)
idu=lambda r:f"2026{r['mo']:02d}{r['dd']:02d}-{r['r']+1}"
seen={}
for r in rows: seen.setdefault(idu(r),(f"2026-{r['mo']:02d}-{r['dd']:02d}",r['r']+1,r['place'],r['pais'],r['sub'],r['cont']))
with open('ubicaciones_base.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['id_ubicacion','fecha','ronda','lugar','pais','region','continente'])
    for k in sorted(seen): w.writerow([k,*seen[k]])
print('filas normal',len(rows),'partidas',len(games))
