import re,collections
SRC='/sessions/trusting-nice-davinci/mnt/Maptap/informes/maptap-ciudades.md'
OUT='/sessions/trusting-nice-davinci/mnt/Maptap/informes/maptap-ciudades-analisis.md'
# pais EN -> (pais ES, región)
G={}
def add(sub,items):
    for it in items.split(';'):
        en,es=[x.strip() for x in it.split('=')]
        G[en]=(es,sub)
add('América del Norte',"USA=EE.UU.;Canada=Canadá;Mexico=México;Greenland=Groenlandia")
add('América Central continental',"Costa Rica=Costa Rica;Guatemala=Guatemala;Panama=Panamá")
add('Caribe',"Antigua and Barbuda=Antigua y Barbuda;Bermuda=Bermudas;Dominican Republic=Rep. Dominicana;Haiti=Haití;Jamaica=Jamaica;Trinidad and Tobago=Trinidad y Tobago;Puerto Rico=Puerto Rico;Martinique=Martinica")
add('América del Sur',"Argentina=Argentina;Bolivia=Bolivia;Brazil=Brasil;Chile=Chile;Colombia=Colombia;Ecuador=Ecuador;French Guiana=Guayana Francesa;Guyana=Guyana;Paraguay=Paraguay;Peru=Perú;Uruguay=Uruguay;Venezuela=Venezuela")
add('Europa Occidental',"England=Reino Unido;UK=Reino Unido;United Kingdom=Reino Unido;Austria=Austria;Belgium=Bélgica;France=Francia;Germany=Alemania;Liechtenstein=Liechtenstein;Netherlands=Países Bajos;Switzerland=Suiza;Luxembourg=Luxemburgo")
add('Europa del Sur',"Greece=Grecia;Italy=Italia;Malta=Malta;Portugal=Portugal;San Marino=San Marino;Spain=España")
add('Balcanes',"Albania=Albania;Kosovo=Kosovo;North Macedonia=Macedonia del Norte;Serbia=Serbia;Slovenia=Eslovenia;Bulgaria=Bulgaria")
add('Nórdicos y Bálticos',"Denmark=Dinamarca;Estonia=Estonia;Finland=Finlandia;Iceland=Islandia;Latvia=Letonia;Norway=Noruega;Sweden=Suecia")
add('Europa del Este',"Czech Republic=Chequia;Czechia=Chequia;Hungary=Hungría;Moldova=Moldavia;Poland=Polonia;Ukraine=Ucrania")
add('Medio Oriente',"Cyprus=Chipre;Iran=Irán;Iraq=Irak;Israel=Israel;Oman=Omán;Palestine=Palestina;Qatar=Qatar;Saudi Arabia=Arabia Saudita;Türkiye=Turquía")
add('Asia Central y Cáucaso',"Armenia=Armenia;Azerbaijan=Azerbaiyán;Georgia=Georgia")
add('Asia Central y Cáucaso',"Mongolia=Mongolia;Kazakhstan=Kazajistán;Kyrgyzstan=Kirguistán;Uzbekistan=Uzbekistán")
add('Asia del Sur',"Afghanistan=Afganistán;India=India;Nepal=Nepal;Pakistan=Pakistán;Sri Lanka=Sri Lanka")
add('Asia Oriental',"China=China;Japan=Japón;North Korea=Corea del Norte;South Korea=Corea del Sur;Taiwan=Taiwán")
add('Sudeste Asiático',"Indonesia=Indonesia;Malaysia=Malasia;Philippines=Filipinas;Singapore=Singapur;Thailand=Tailandia;Vietnam=Vietnam")
add('África del Norte',"Egypt=Egipto;Libya=Libia;Morocco=Marruecos;Tunisia=Túnez")
add('África Occidental',"Benin=Benín;Burkina Faso=Burkina Faso;Cote d'Ivoire=Costa de Marfil;Ghana=Ghana;Guinea-Bissau=Guinea-Bisáu;Liberia=Liberia;Senegal=Senegal")
add('África Central',"Cameroon=Camerún;Central African Republic=Rep. Centroafricana;Chad=Chad;Equatorial Guinea=Guinea Ecuatorial;Gabon=Gabón;Niger=Níger;Nigeria=Nigeria")
add('África Oriental',"Ethiopia=Etiopía;Kenya=Kenia;Somalia=Somalia;South Sudan=Sudán del Sur;Sudan=Sudán;Democratic Republic of Congo=RD del Congo;Democratic Republic of the Congo=RD del Congo;Tanzania=Tanzania;Uganda=Uganda")
add('África Austral',"Madagascar=Madagascar;Mauritius=Mauricio;Botswana=Botsuana;Eswatini=Esuatini;Lesotho=Lesoto;Mozambique=Mozambique;Malawi=Malaui;Angola=Angola;Namibia=Namibia;South Africa=Sudáfrica;Zimbabwe=Zimbabue")
add('Australia y Nueva Zelanda',"Australia=Australia;New Zealand=Nueva Zelanda")
add('Islas menores de Oceanía',"Papua New Guinea=Papúa Nueva Guinea;Solomon Islands=Islas Salomón;Tonga=Tonga;Guam=Guam")
G['Russia']=('Rusia','Europa del Este')
CONT={'América del Norte':'América del Norte','América Central continental':'América Central','Caribe':'América Central','América del Sur':'América del Sur',
'Europa Occidental':'Europa','Europa del Sur':'Europa','Balcanes':'Europa','Nórdicos y Bálticos':'Europa','Europa del Este':'Europa',
'Medio Oriente':'Asia','Asia Central y Cáucaso':'Asia','Asia del Sur':'Asia','Asia Oriental':'Asia','Sudeste Asiático':'Asia',
'África del Norte':'África','África Occidental':'África','África Central':'África','África Oriental':'África','África Austral':'África','Australia y Nueva Zelanda':'Oceanía','Islas menores de Oceanía':'Oceanía','Antártida':'Antártida'}
SUBORD=list(CONT); CONTORD=['América del Norte','América Central','América del Sur','Europa','Asia','África','Oceanía']
def classify(p):
    if 'Antarctica' in p: return ('Sin país (Antártida)','Antártida')
    if 'Matterhorn' in p: return ('Suiza','Europa Occidental')
    if 'Titanic' in p: return ('Sin país (Atlántico Norte)','América del Norte')
    if p=='Jerusalem': return ('Israel','Medio Oriente')
    if 'Gibraltar' in p: return ('Reino Unido','Europa del Sur')
    if 'Urumqi' in p: return ('China','Asia Central y Cáucaso')
    if 'Lhasa' in p: return ('China','Asia del Sur')
    if 'Hagåtña' in p: return G['Guam']
    if 'Puerto Rico' in p: return G['Puerto Rico']
    if 'Martinique' in p: return G['Martinique']
    if p in('Singapore','Luxembourg'): return G[p]
    last=p.split(',')[-1].strip()
    if last=='USA' and 'Guam' in p: return G['Guam']
    if last=='Russia':
        if any(k in p for k in('Vladivostok','Kamchatka')): return ('Rusia','Asia Oriental')
        if 'Chelyabinsk' in p: return ('Rusia','Asia Central y Cáucaso')
        return G['Russia']
    if last=='French Overseas Territory': return G['Martinique']
    return G[last]
rows=[]
for l in open(SRC,encoding='utf8'):
    m=re.match(r'\| (\d+/\d+) \| (.*) \|\s*$',l)
    if m: rows.append((m.group(1),[x.strip() for x in m.group(2).split(' | ')]))
assert len(rows)>=85 and all(len(r[1])==5 for r in rows)
data=[(d,i,p)+classify(p) for d,r in rows for i,p in enumerate(r)]
data=[(d,i,p,pa,sub,CONT[sub]) for d,i,p,pa,sub in data]
N=len(data);print(N)
def cnt(idx):
    c=collections.defaultdict(lambda:[0]*5)
    for t in data: c[t[idx]][t[1]]+=1
    return c
def tab(title,c,order=None,extra=None):
    keys=order or sorted(c,key=lambda k:(-sum(c[k]),k))
    keys=[k for k in keys if k in c]
    s=f'\n## {title}\n\n| {title.split(" por ")[-1].capitalize()} | R1 | R2 | R3 | R4 | R5 | Total | % |\n|---|--:|--:|--:|--:|--:|--:|--:|\n'
    for k in keys:
        v=c[k];t=sum(v);s+=f'| {k} | '+' | '.join(map(str,v))+f' | **{t}** | {t*100/N:.1f}% |\n'
    return s
o=[f'# MapTap - Analisis geografico por ronda y por dia (22/7 al 15/10/2026)\n\nBase: {len(rows)} fechas x 5 rondas = {N} lugares (maptap-ciudades.md). R1..R5 = ronda.\n\nCriterios: Hawaii cuenta como EE.UU. (pais). Guam y Puerto Rico se cuentan como pais propio y Guam esta en Islas menores de Oceania y Puerto Rico en Caribe. Jerusalen se cuenta en Israel. Rusia se parte por lugar: Vladivostok y Kamchatka en Asia Oriental, Chelyabinsk en Asia Central y Cáucaso, el resto en Europa del Este. Titanic (Atlantico Norte): sin pais, asignado a America del Norte como region y continente. Continente Centroamerica incluye las regiones Centroamerica y Caribe. Gibraltar: Reino Unido en Europa del Sur. China se parte por lugar: Urumqi (Xinjiang) en Asia Central y Cáucaso y Lhasa (Tibet) en Asia del Sur; el resto en Asia Oriental. Mongolia en Asia Central y Cáucaso. Escocia, Inglaterra, Gales e Irlanda del Norte: Reino Unido.\n']
o.append(tab('Resumen por continente',cnt(5),CONTORD))
o.append(tab('Resumen por región',cnt(4),SUBORD+[]))
o.append(tab('Resumen por pais',cnt(3)))
# detalle por dia
o.append('\n## Detalle por dia: pais\n\n| Fecha | R1 | R2 | R3 | R4 | R5 |\n|---|---|---|---|---|---|\n')
for d,_ in rows:
    o.append(f'| {d} | '+' | '.join(t[3] for t in data if t[0]==d)+' |\n')
o.append('\n## Detalle por dia: región\n\n| Fecha | R1 | R2 | R3 | R4 | R5 |\n|---|---|---|---|---|---|\n')
for d,_ in rows:
    o.append(f'| {d} | '+' | '.join(t[4] for t in data if t[0]==d)+' |\n')
o.append('\n## Detalle por dia: continente\n\n| Fecha | R1 | R2 | R3 | R4 | R5 |\n|---|---|---|---|---|---|\n')
for d,_ in rows:
    o.append(f'| {d} | '+' | '.join(t[5] for t in data if t[0]==d)+' |\n')
# lugares por pais
by=collections.defaultdict(list)
for t in data: by[t[3]].append(t)
o.append('\n## Lugares por pais\n\n')
for k in sorted(by,key=lambda k:(-len(by[k]),k)):
    o.append(f'- **{k}** ({len(by[k])}): '+'; '.join(f'{t[2].split(",")[0]} ({t[0]} R{t[1]+1})' for t in by[k])+'\n')
open(OUT,'w',encoding='utf8').write(''.join(o))
for t in data:
    pass
print(sorted(collections.Counter(t[5] for t in data).items()))
print(sorted(collections.Counter(t[4] for t in data).items()))
