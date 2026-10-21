import json,collections,statistics as st
R=json.load(open('/sessions/trusting-nice-davinci/mnt/outputs/rounds_all.json'))
S={'Nacho Toker':'Toker','Axel Itzcovitz':'Axel','Feli Garabato':'Feli','Antonio Santos':'Antonio','Lucas Greco':'Lucas','Sandro Anello':'Sandro','Bruno Feinsilber':'Bruno','Ale Feinsilber':'Ale','Dario Feinsilber':'Dario','Fede Moia':'Fede','Martin Feinsilber':'Martín'}
PL=list(S)
mean=lambda v:sum(v)/len(v)
dr=collections.defaultdict(list)
for r in R: dr[(r['mo'],r['dd'],r['r'])].append(r['s'])
for r in R: r['rel']=r['s']-mean(dr[(r['mo'],r['dd'],r['r'])]);r['region']=r['sub']
CO=['América del Norte','Centroamérica','América del Sur','Europa','Asia','África','Oceanía','Antártida']
RG=['América del Norte','Centroamérica','Caribe','América del Sur','Europa Occidental','Europa del Sur','Balcanes','Nórdicos y Bálticos','Europa del Este','Medio Oriente','Asia Central y Cáucaso','Asia del Sur','Asia Oriental','Sudeste Asiático','África del Norte','África Occidental','África Central','África Oriental','África Austral','Australia y Nueva Zelanda','Islas menores de Oceanía','Antártida']
assert set(r['region'] for r in R)<=set(RG),set(r['region'] for r in R)-set(RG)
N=len(R);glob=mean([r['s'] for r in R])
games=collections.Counter(r['p'] for r in R if r['r']==0)
G=len({(r['mo'],r['dd']) for r in R})
tot_games=sum(games.values())
by=lambda key:collections.defaultdict(list)
def grp(keyf):
    g=collections.defaultdict(list)
    for r in R: g[keyf(r)].append(r)
    return g
base={p:mean([r['s'] for r in R if r['p']==p]) for p in PL}
rel={p:mean([r['rel'] for r in R if r['p']==p]) for p in PL}
sd={p:st.pstdev([r['s'] for r in R if r['p']==p]) for p in PL}
n100={p:sum(1 for r in R if r['p']==p and r['s']==100) for p in PL}
nlow={p:sum(1 for r in R if r['p']==p and r['s']<80) for p in PL}
rk=sorted(PL,key=lambda p:-base[p]);rank={p:i+1 for i,p in enumerate(rk)}
# agrupaciones
cell=collections.defaultdict(list)
for r in R:
    cell[('cont',r['cont'],r['p'])].append(r['s']);cell[('region',r['region'],r['p'])].append(r['s']);cell[('pais',r['pais'],r['p'])].append(r['s'])
zones={'cont':CO,'region':RG,'pais':sorted({r['pais'] for r in R})}
ztot={k:collections.Counter() for k in zones}
for r in R:
    ztot['cont'][r['cont']]+=1;ztot['region'][r['region']]+=1;ztot['pais'][r['pais']]+=1
def top3(kind,z):
    L=sorted(((mean(cell[(kind,z,p)]),p,len(cell[(kind,z,p)])) for p in PL if cell[(kind,z,p)]),reverse=True)
    return L[:3]
def eligible(kind,z):
    if kind=='pais' and z in('Argentina','Brasil'): return True
    return any(len(cell[(kind,z,p)])>=10 for p in PL)
tops={}
for kind in zones:
    for z in sorted(zones[kind],key=lambda z:-ztot[kind][z]):
        if eligible(kind,z): tops[(kind,z)]=top3(kind,z)
def fm(m,n,minn=10): 
    s=f'{S[m[1]]} {m[0]:.1f} (n={m[2]})';return s if m[2]>=minn else f'*{s}*'
def fcell(v,b,minn=8):
    if not v: return '-'
    s=f'{mean(v):.1f} ({mean(v)-b:+.1f}) n={len(v)}';return s if len(v)>=minn else f'({s})'
o=[]
o.append(f'# MapTap - Desempeno por zona geografica (puntaje nominal por ronda)\n\nPuntaje nominal = puntaje de cada ronda (0 a 100), SIN multiplicadores. El Final score solo se uso para validar.\n\n## 0. Base\n\n- Dias: {G} (22/7 al 15/10/2026). Partidas: {tot_games}. Rondas: {N}. Promedio nominal general: {glob:.1f}.\n- Jugadores: los 11 fijos. Falta una partida con detalle: Ale del 1/9 (885), que no figura en el chat.\n- Partidas por jugador: '+', '.join(f'{S[p]} {games[p]}' for p in PL)+'.\n- Zonas: 7 continentes, 20 regiones (ver maptap-ciudades-analisis.md). Celdas con n menor a 8 entre parentesis; en tops, *cursiva* = menos de 10 rondas (poco confiable).\n')
def difft(kind,order,title,minn=0):
    s=f'\n## {title}\n\n| Zona | Rondas | Prom nominal | Dif vs general | Desvio |\n|---|--:|--:|--:|--:|\n'
    g=grp(lambda r:r[{'cont':'cont','region':'region','pais':'pais'}[kind]])
    for z in sorted([z for z in order if len(g[z])>=minn and g[z]],key=lambda z:-mean([x['s'] for x in g[z]])):
        v=[x['s'] for x in g[z]];s+=f'| {z} | {len(v)} | {mean(v):.1f} | {mean(v)-glob:+.1f} | {st.pstdev(v):.1f} |\n'
    return s
o.append(difft('cont',CO,'1. Dificultad por continente (todos los jugadores)'))
o.append(difft('region',RG,'2. Dificultad por region (todos los jugadores)'))
o.append(difft('pais',zones['pais'],'3. Dificultad por pais (todos los jugadores, minimo 25 rondas)',25))
def matrix(kind,order,title):
    s=f'\n## {title}\n\nCada celda: Prom (Dif contra el promedio del propio jugador) n.\n\n| Zona | '+' | '.join(S[p] for p in PL)+' |\n|---|'+'---|'*len(PL)+'\n| **General** | '+' | '.join(f'**{base[p]:.1f}**' for p in PL)+' |\n'
    for z in order: s+=f'| {z} | '+' | '.join(fcell(cell[(kind,z,p)],base[p]) for p in PL)+' |\n'
    return s
o.append(matrix('cont',CO,'4. Jugador por continente'))
o.append(matrix('region',RG,'5. Jugador por region'))
# tops
for kind,title in(('cont','6. Top 3 por continente'),('region','7. Top 3 por region'),('pais','8. Top 3 por pais')):
    o.append(f'\n## {title}\n\n'+('Entran las zonas donde al menos un jugador tiene 10 rondas o mas (paises: Argentina y Brasil entran siempre). Top 3 con todos los jugadores. *Cursiva* = menos de 10 rondas.\n\n' if kind!='cont' else 'Top 3 con todos los jugadores. *Cursiva* = menos de 10 rondas.\n\n')+'| Zona (rondas) | 1º | 2º | 3º |\n|---|---|---|---|\n')
    for (k,z),L in tops.items():
        if k==kind: o.append(f'| {z} ({ztot[k][z]}) | '+' | '.join(fm(m,10) for m in L)+(' | - ' if len(L)<3 else '')+' |\n')
    if kind!='cont':
        ex=[z for z in zones[kind] if (kind,z) not in tops]
        if kind=='region': o.append('\nZonas sin muestra suficiente: '+(', '.join(ex) if ex else 'ninguna')+'.\n')
        else: o.append(f'\nPaises sin muestra suficiente: {len(ex)} de {len(zones[kind])}.\n')
# analisis general
o.append('\n## 9. Ranking general de jugadores\n\nExceso = puntaje del jugador menos el promedio de todos los que jugaron esa misma fecha y ronda (neutraliza la dificultad del dia).\n\n| # | Jugador | Partidas | Prom nominal | Exceso | Desvio | Rondas de 100 | Rondas <80 |\n|--:|---|--:|--:|--:|--:|--:|--:|\n')
for p in rk: o.append(f'| {rank[p]} | {S[p]} | {games[p]} | {base[p]:.1f} | {rel[p]:+.1f} | {sd[p]:.1f} | {n100[p]} | {nlow[p]} |\n')
# especialistas
o.append('\n## 10. Mejor y peor de cada zona (n minimo 8)\n\n| Zona | Mejor | Peor |\n|---|---|---|\n')
for kind,order in(('cont',CO),('region',RG)):
    for z in order:
        L=sorted(((mean(cell[(kind,z,p)]),p,len(cell[(kind,z,p)])) for p in PL if len(cell[(kind,z,p)])>=8),reverse=True)
        if len(L)>=2: o.append(f'| {z} | {S[L[0][1]]} {L[0][0]:.1f} (n={L[0][2]}) | {S[L[-1][1]]} {L[-1][0]:.1f} (n={L[-1][2]}) |\n')
        else: o.append(f'| {z} | sin muestra (n>=8 de al menos 2 jugadores) | |\n')
# posicion de ronda
o.append('\n## 11. Por posicion de ronda\n\n| Jugador | R1 | R2 | R3 | R4 | R5 |\n|---|--:|--:|--:|--:|--:|\n| **Grupo** | '+' | '.join(f'**{mean([r["s"] for r in R if r["r"]==i]):.1f}**' for i in range(5))+' |\n')
rp={p:[mean([r['s'] for r in R if r['p']==p and r['r']==i]) for i in range(5)] for p in PL}
for p in PL: o.append(f'| {S[p]} | '+' | '.join(f'{x:.1f}' for x in rp[p])+' |\n')
# evolucion mensual
MN={7:'Jul (22-31)',8:'Ago',9:'Sep',10:'Oct (1-14)'}
o.append('\n## 12. Evolucion mensual (promedio nominal por ronda)\n\n| Jugador | '+' | '.join(MN.values())+' | Dif Oct-Jul |\n|---|--:|--:|--:|--:|--:|\n')
mon={}
for p in PL:
    row=[];mon[p]={}
    for m in MN:
        v=[r['s'] for r in R if r['p']==p and r['mo']==m];mon[p][m]=(mean(v) if v else None,len(v))
        row.append(f'{mean(v):.1f} ({len(v)})' if v else '-')
    d=(mon[p][10][0]-mon[p][7][0]) if mon[p][10][0] and mon[p][7][0] else None
    o.append(f'| {S[p]} | '+' | '.join(row)+f' | {d:+.1f} |\n' if d is not None else f'| {S[p]} | '+' | '.join(row)+' | - |\n')
o.append('\nEntre parentesis, rondas del mes.\n')
# hallazgos
cd=sorted(CO,key=lambda z:-mean([r['s'] for r in R if r['cont']==z]))
rd=sorted([z for z in RG if ztot['region'][z]>=30],key=lambda z:-mean([r['s'] for r in R if r['region']==z]))
mz=lambda k,z:mean([r['s'] for r in R if r[k]==z])
dev=[]
for p in PL:
    for z in RG:
        v=cell[('region',z,p)]
        if len(v)>=8: dev.append((mean(v)-base[p],p,z,len(v)))
dev.sort()
tr=[(mon[p][10][0]-mon[p][7][0],p) for p in PL if mon[p][10][0] and mon[p][7][0] and mon[p][10][1]>=15 and mon[p][7][1]>=15]
tr.sort()
cons=sorted(PL,key=lambda p:sd[p])
rpg=[mean([r['s'] for r in R if r['r']==i]) for i in range(5)]
H=[f'Continente mas facil: {cd[0]} ({mz("cont",cd[0]):.1f}); mas dificil: {cd[-1]} ({mz("cont",cd[-1]):.1f}).',
f'Regiones extremas (30 rondas o mas): {rd[0]} {mz("region",rd[0]):.1f} la mas facil y {rd[-1]} {mz("region",rd[-1]):.1f} la mas dificil.',
f'Mejor exceso contra el resto: {S[max(PL,key=lambda p:rel[p])]} ({max(rel.values()):+.1f} por ronda); mas bajo: {S[min(PL,key=lambda p:rel[p])]} ({min(rel.values()):+.1f}).',
f'Mas parejo: {S[cons[0]]} (desvio {sd[cons[0]]:.1f}); mas irregular: {S[cons[-1]]} (desvio {sd[cons[-1]]:.1f}).',
f'Rondas de 100: lidera {S[max(PL,key=lambda p:n100[p])]} con {max(n100.values())}; el grupo suma {sum(n100.values())} de {N}.',
f'Ronda mas facil del grupo: R{rpg.index(max(rpg))+1} ({max(rpg):.1f}); mas dificil: R{rpg.index(min(rpg))+1} ({min(rpg):.1f}).',
f'Mayor fortaleza relativa (n>=8): {S[dev[-1][1]]} en {dev[-1][2]} ({dev[-1][0]:+.1f} sobre su promedio, n={dev[-1][3]}).',
f'Mayor debilidad relativa (n>=8): {S[dev[0][1]]} en {dev[0][2]} ({dev[0][0]:+.1f} bajo su promedio, n={dev[0][3]}).']
if tr: H.append(f'Evolucion Jul-Oct (15 rondas o mas en ambos meses): mejor tendencia {S[tr[-1][1]]} ({tr[-1][0]:+.1f}); peor {S[tr[0][1]]} ({tr[0][0]:+.1f}).')
o.append('\n## 13. Hallazgos\n\n'+''.join(f'- {h}\n' for h in H))
# verificacion
chk=[]
chk.append(f'Rondas = partidas x 5: {tot_games}x5={tot_games*5} vs {N}: {"OK" if tot_games*5==N else "ERROR"}')
chk.append('Suma de rondas por continente = total: '+('OK' if sum(ztot['cont'].values())==N else 'ERROR'))
chk.append('Suma de rondas por region = total: '+('OK' if sum(ztot['region'].values())==N else 'ERROR'))
chk.append('Suma de rondas por pais = total: '+('OK' if sum(ztot['pais'].values())==N else 'ERROR'))
ok=all(abs(base[p]-mean([r['s'] for r in R if r['p']==p]))<1e-9 for p in PL)
chk.append('Promedios por jugador recalculados: '+('OK' if ok else 'ERROR'))
chk.append('Cada top cumple la regla de ingreso: '+('OK' if all(eligible(k,z) for (k,z) in tops) else 'ERROR'))
o.append('\n## 14. Verificaciones\n\n'+''.join(f'- {c}\n' for c in chk))
open('/sessions/trusting-nice-davinci/mnt/Maptap/informes/maptap-desempeno-geografico.md','w',encoding='utf8').write(''.join(o))
# perfiles
hold=collections.defaultdict(lambda:{'cont':[],'region':[],'pais':[]})
for (k,z),L in tops.items():
    for i,m in enumerate(L): hold[m[1]][k].append(f'{i+1}º {z}'+('*' if m[2]<10 else ''))

def det(p):
    def tb(kind,order,minshow,flag,title):
        L=[]
        for z in order:
            v=cell[(kind,z,p)]
            if len(v)>=minshow: L.append((mean(v)-base[p],z,mean(v),len(v)))
        L.sort(reverse=True)
        omit=len([z for z in order if 0<len(cell[(kind,z,p)])<minshow])
        t=f'\n**{title}** (ordenado de mejor a peor contra su promedio de {base[p]:.1f}; entre parentesis n menor a {flag})\n\n| Zona | Prom | Dif | n |\n|---|--:|--:|--:|\n'
        for d,z,m,n in L:
            row=f'{z} | {m:.1f} | {d:+.1f} | {n}';t+=f'| ({row[:row.index(" |")]}) | {m:.1f} | {d:+.1f} | {n} |\n' if n<flag else f'| {row} |\n'
        if omit: t+=f'\nOmitidas por tener menos de {minshow} rondas: {omit}.\n'
        return t
    return '\n### Detalle completo por zona (Dif = zona menos su promedio general)\n'+tb('cont',CO,1,8,'Continentes')+tb('region',RG,1,8,'Regiones')+tb('pais',zones['pais'],5,10,'Paises (minimo 5 rondas)')
medsd=st.median(sd.values())
P=['# MapTap - Perfiles de jugadores (puntaje nominal por ronda)\n\nBase: '+f'{G} dias, {tot_games} partidas, {N} rondas. Promedio general {glob:.1f}. Perfil contra el PROPIO promedio del jugador (Dif = promedio en la zona menos su promedio general); la comparacion contra los demas esta en los tops y en el exceso del ranking. Zonas: n minimo 8 (continente y region) y 5 (pais) en los resumenes; (*) en tops = menos de 10 rondas.\n']
for p in rk:
    g=lambda k:[(mean(cell[(k,z,p)])-base[p],z,len(cell[(k,z,p)])) for z in zones[k] if len(cell[(k,z,p)])>=8]
    cz=sorted(g('cont'));rz=sorted(g('region'))
    pz=sorted((mean(cell[('pais',z,p)])-base[p],z,len(cell[('pais',z,p)])) for z in zones['pais'] if len(cell[('pais',z,p)])>=5)
    f=lambda L:', '.join(f'{z} ({d:+.1f}, n={n})' for d,z,n in L)
    mi=rp[p].index(max(rp[p]));ma=rp[p].index(min(rp[p]))
    mm=[(mon[p][m][0],MN[m],mon[p][m][1]) for m in MN if mon[p][m][0] is not None]
    gm=[r for r in R if r['p']==p];gm_sorted=sorted(gm,key=lambda r:(r['mo'],r['dd']))
    h=len(gm_sorted)//2;t1=mean([r['s'] for r in gm_sorted[:h]]);t2=mean([r['s'] for r in gm_sorted[h:]])
    pr=[]
    if rel[p]>1.5: pr.append('rinde claramente por encima del grupo')
    elif rel[p]>0.3: pr.append('rinde algo por encima del grupo')
    elif rel[p]>-0.8: pr.append('rinde en linea con el grupo')
    else: pr.append('rinde por debajo del grupo')
    pr.append('es muy parejo' if sd[p]<medsd-0.8 else ('es irregular' if sd[p]>medsd+0.8 else 'tiene una regularidad promedio'))
    estilo=f'{S[p]} {pr[0]} ({rel[p]:+.1f} por ronda contra los demas) y {pr[1]} (desvio {sd[p]:.1f}). '
    if rz: estilo+=f'Su mejor zona es {rz[-1][1]} ({rz[-1][0]:+.1f}) y la que mas le cuesta es {rz[0][1]} ({rz[0][0]:+.1f}). '
    estilo+=f'En lo que va del torneo {"mejora" if t2-t1>0.8 else ("baja" if t2-t1<-0.8 else "se mantiene estable")} ({t1:.1f} en la primera mitad de sus rondas contra {t2:.1f} en la segunda).'
    P.append(f'\n## {S[p]}\n\n**Resumen:** {games[p]} partidas, {len(gm)} rondas, promedio nominal {base[p]:.1f} (puesto {rank[p]} de 11), exceso {rel[p]:+.1f} por ronda.\n\n**Consistencia:** desvio {sd[p]:.1f} (mediana del grupo {medsd:.1f}); {n100[p]} rondas de 100 y {nlow[p]} rondas bajo 80.\n\n**Mejores zonas (continente):** {f([x for x in cz[::-1] if x[0]>0][:2])}\n\n**Peores zonas (continente):** {f([x for x in cz if x[0]<0][:2])}\n\n**Mejores zonas (region):** {f([x for x in rz[::-1] if x[0]>0][:3])}\n\n**Peores zonas (region):** {f([x for x in rz if x[0]<0][:3])}\n\n**Paises donde mas brilla:** {f([x for x in pz[::-1] if x[0]>0][:3])}\n\n**Paises donde mas sufre:** {f([x for x in pz if x[0]<0][:3])}\n\n**Rondas:** mejor R{mi+1} ({rp[p][mi]:.1f}), peor R{ma+1} ({rp[p][ma]:.1f}).\n\n**Tendencia mensual:** '+' | '.join(f'{l} {m:.1f} ({n})' for m,l,n in mm)+'\n\n**Top 3:** '+('; '.join(f'{k}: '+', '.join(hold[p][k]) for k in ('cont','region','pais') if hold[p][k]) or 'ninguno')+f'\n\n**Estilo:** {estilo}\n'+det(p))
open('/sessions/trusting-nice-davinci/mnt/Maptap/informes/maptap-perfiles-jugadores.md','w',encoding='utf8').write(''.join(P))
print(''.join(chk[0:0]));print('\n'.join(chk));print('\n'.join(H))
print(len(tops),collections.Counter(k for k,z in tops))
