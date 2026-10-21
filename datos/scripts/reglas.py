"""Reglas de categorias (listas manuales por lugar/pais y reglas calculadas). Usado al dar de alta lugares nuevos."""
import numpy as np
S=lambda t:set(x.strip() for x in t.split(";"))
PL={}  # categorias por lugar (nombre corto)
PA={}  # categorias por pais
def P(name,desc,members): PL[name]=(desc,S(members))
def C(name,desc,members): PA[name]=(desc,S(members))

# ---------- POR LUGAR (manual) ----------
P("Capital nacional","Capital de un pais (incluye Jerusalen, Taipei y La Paz como sedes de gobierno)","Abuja;Accra;Ankara;Addis Ababa;Asunción;Athens;Baghdad;Baku;Bangkok;Bangui;Belgrade;Berlin;Bishkek;Bissau;Bogotá;Brussels;Budapest;Buenos Aires;Cairo;Canberra;Caracas;Chișinău;Copenhagen;Dakar;Dodoma;Doha;Gaborone;Georgetown;Guatemala City;Helsinki;Jakarta;Juba;Kabul;Kampala;Kathmandu;Khartoum;Kingston;Kinshasa;Kyiv;La Paz;Libreville;Lima;Lisbon;London;Luanda;Luxembourg;Mbabane;Mexico City;Mogadishu;Monrovia;Montevideo;Muscat;N'Djamena;New Delhi;Niamey;Nicosia;Nuku'alofa;Oslo;Panama City;Paris;Port Louis;Port Moresby;Port of Spain;Port-au-Prince;Prague;Pristina;Pyongyang;Quito;Reykjavík;Riga;Rome;San José;San Marino City;Santiago;Seoul;Singapore;Skopje;St John's;Stockholm;Taipei;Tallinn;Tashkent;Tehran;Tirana;Tokyo;Tunis;Ulaanbaatar;Vaduz;Valletta;Vienna;Warsaw;Washington DC;Wellington;Windhoek;Yamoussoukro;Yaoundé;Yerevan;Jerusalem;Hagåtña;Hargeisa")
P("Ciudad fluvial (< 10 km de un rio)","A menos de 10 km de un rio importante (ver dist_rio); revisar a mano","")
P("Dependencia o territorio no soberano","Dependencia o territorio sin soberania propia","")
P("Sede de Fórmula 1 (actual o histórica)","Ciudad que alguna vez alojo un GP puntuable de F1","")
P("Sede de Exposición Mundial (BIE)","Ciudad que alojo una Expo oficial del BIE","")
P("Ciudad lacustre (<= 5 km de un lago o mar interior)","A orillas de un lago grande o mar interior (ver dist_lago); revisar a mano","")
P("Ciudad volcanica (volcan holoceno a <= 50 km)","Volcan con erupcion fechada en los ultimos 10.000 anios a 50 km o menos (ver dist_volcan)","")
P("Sede de Juegos Olimpicos (verano o invierno)","Ciudad que alguna vez alojo unos Juegos Olimpicos (incluye area metropolitana, p.ej. Los Angeles)","")
P("Sede de Mundial de futbol masculino","Ciudad que alguna vez alojo partidos de un Mundial masculino de la FIFA (incluye 2026)","")
P("Lugar de altura (>= 1.490 m)","Altitud de 1.490 m o mas (calculada con scripts/obtener_altitudes.py)","")
P("Ciudad sismica (2+ terremotos M7+ a <= 100 km desde 1900)","Al menos 2 terremotos M7+ (USGS) a 100 km o menos desde 1900","")
P("Ciudad universitaria","Ciudad listada como college town / ciudad universitaria en Wikipedia (en, es, ja) o con ciudad universitaria emblematica","")
P("Antigüedad (fundada antes del año 1)","Ciudad o sitio fundado antes del anio 1","")
P("Atracción natural","Parque, montania, cascada, isla o paisaje natural","")
P("Patrimonio UNESCO urbano","Ciudad o centro historico inscrito en UNESCO (ver dist_unesco)","")
P("Monumento o sitio historico UNESCO","Sitio cultural UNESCO a <= 10 km (calculada)","")
P("Ciudad medieval (fundada 476-1499)","Fundada entre 476 y 1499 (cargar fundacion_anio al dar de alta)","")
P("Ciudad colonial (fundada 1500-1799)","Fundada entre 1500 y 1799 (cargar fundacion_anio al dar de alta)","")
P("Ciudad nueva (fundada desde 1895)","Fundada en 1895 o despues (cargar fundacion_anio al dar de alta)","")
P("Capital económica","Principal centro economico del pais y no capital nacional","")
P("Ciudad industrial","Ciudad definida por su industria","")
P("Capital regional","Capital o sede de gobierno de un estado, provincia o region","Albany;Annapolis;Helena;Pierre;Hartford;Charleston;Columbia;Indianapolis;Nashville;Oklahoma City;Salt Lake City;Phoenix;Madison;Boston;Honolulu;Edmonton;Regina;Winnipeg;Victoria;Toronto;Belfast;Morelia;Tepic;Durango;Cagliari;Oviedo;Zaragoza;Valencia;Florence;Trieste;Turin;Milan;Sydney;Melbourne;Brisbane;Perth;Hangzhou;Nanjing;Guangzhou;Urumqi;Lhasa;Hyderabad;Bengaluru;Kolkata;Mumbai;Lucknow;Patna;Thiruvananthapuram;Guwahati;Mombasa;Hamhung;Kupang;Makassar;Denpasar;Ambon;Porto Alegre;Belo Horizonte;Florianópolis;Rio de Janeiro;São Paulo;Cochabamba;Santa Cruz de la Sierra;Maracaibo;Maracay;Valledupar;Medellín;Concepción;Valparaíso;Salzburg;Stuttgart;Dortmund;Basel;Geneva;Zurich;Lucerne;St Gallen;Dundee;Inverness;Dijon;Nantes;Toulouse;Montpellier;Caen;Montreal;Moncton;Gander;Nanaimo;Kyoto;Osaka;Fukuoka;Kagoshima;Naha;Fukui;Wakayama;Kōchi;Busan;Daegu;Isfahan;Mashhad;Adana;Kano;Enugu;Jos;Calabar;Douala;Kumasi;Cotonou;Karachi;Lahore;Baguio;Iloilo City;Nha Trang;Huế;Taichung;Tainan;Miaoli City;Ipoh;Sevilla")
P("Ciudad costera","Ciudad sobre el mar u oceano (a menos de ~30 km de la costa)","Barcelona;Basra;Beira;Belfast;Brisbane;Busan;Cape Town;Casablanca;Cotonou;Dakar;Dalian;Doha;Douala;Dundee;Durban;Fukuoka;Gdańsk;Gothenburg;Guangzhou;Hamhung;Helsinki;Jakarta;Kagoshima;Karachi;Kolkata;Lisbon;Liverpool;Luanda;Melbourne;Mogadishu;Mombasa;Mumbai;Muscat;Nagasaki;Odessa;Osaka;Oslo;Perth;Port Louis;Port Said;Port of Spain;Porto;Port-au-Prince;Rio de Janeiro;Shanghai;Singapore;Stockholm;Sydney;Szczecin;Tallinn;Tampa;Tokyo;Trieste;Trondheim;Valparaíso;Veraval;Vladivostok;Wellington;Auckland;Baltimore;Boston;Atlantic City;Long Beach;San Francisco;Santa Monica;Monterey;Newport;Portland;Mobile;Houston;Honolulu;Tunis;Tel Aviv;Thessaloniki;Messina;Cagliari;Bizerte;Caen;Carthage;Larvik;Oulu;Turku;Kingston upon Hull;Newcastle upon Tyne;Newcastle;Hervey Bay;Cap-Haïtien;Puerto Plata;Puerto Madryn;Bahía Blanca;Punta Arenas;Ancud;Concepción;Florianópolis;Puntarenas;Panama City;Guadalcanal;Hagåtña;Ponce;Nuku'alofa;Naha;Ryotsu;Kōchi;Wakayama;Nishinomiya;Odawara;Fukui;Taipei;Tainan;Nha Trang;Thiruvananthapuram;Ratnagiri;Jamnagar;Kupang;Makassar;Ambon;Denpasar;Iloilo City;Dover Strait;Brodick Castle;Limassol;Valletta;Rhodes;Fort-de-France;Georgetown;Cayenne;Bissau;Monrovia;Libreville;Toamasina;Port Moresby;Kingston;St George's;St John's;Copenhagen;Gdańsk;Riga;Rome;Barcelona;Valencia;Hartford;New Delhi;Brooklyn;Ellis Island;Annapolis;Washington DC;Arlington;Kaolack;Accra;Cairo;Canberra")
P("Isla o pais insular","Lugar en una isla o en un pais insular","Honolulu;Hagåtña;Guadalcanal;Ambon;Kupang;Denpasar;Ubud;Makassar;Jakarta;Ponce;Port Louis;Nuku'alofa;Cagliari;Corsica;Messina;Naha;Ryotsu;Iloilo City;Baguio;Auckland;Christchurch;Hamilton;Wellington;Taipei;Taichung;Tainan;Miaoli City;Fukui;Fukuoka;Kagoshima;Kyoto;Mount Fuji;Nagasaki;Nishinomiya;Odawara;Osaka;Tokyo;Wakayama;Kōchi;Kandy;Sigiriya;Cap-Haïtien;Port-au-Prince;Puerto Plata;Kingston;Port of Spain;St John's;St George's;Fort-de-France;Reykjavík;Thingvellir;London;Leeds;Liverpool;Inverness;Dundee;Brodick Castle;Snowdon;Stonehenge;Dover Strait;Kingston upon Hull;Newcastle upon Tyne;Belfast;Toamasina;Tsingy de Bemaraha;Limassol;Nicosia;Valletta;Rhodes;Gander;Nanaimo;Ancud;Elephant Island;Port Moresby;Singapore;Hobart;Corsica;Cayenne")
P("Zona arida o desierto","Desierto o clima arido","Agadez;Salar de Uyuni;Copiapó;Tombstone;Tucson;Phoenix;Albuquerque;Salt Lake City;Doha;Muscat;Mecca;Medina;Khartoum;Tobruk;Cairo;Isfahan;Baikonur;Urumqi;Karachi;Kandahar;Windhoek;Gaborone;Niamey;N'Djamena;Hargeisa;Dori;Jamnagar;Baghdad;Basra;Babylon;Tehran;Mashhad;Samarkand;Tashkent;Mogadishu;Perth;Kuwait;Dodoma;Marrakech;Adana;Derinkuyu Underground City")
P("Guerras Mundiales","Escenarios, batallas, ciudades clave o simbolos de las guerras mundiales","Dover Strait;Versailles;Ypres;Nagasaki;Gdańsk;Nuremberg;Wolfsburg;Berlin;Warsaw;Białystok;Tobruk;Caen;Guadalcanal;Port Moresby;Hagåtña;Odessa;Singapore;Casablanca;Messina;Rivne;Honolulu;Athens;Rhodes;Brussels;Belgrade;Trieste;Dortmund;Szczecin;Toszek;Fort Knox;Annapolis;Arlington;Hamhung;Kyiv;Cherkasy;Ellis Island")
P("Europa turistica clasica","Ciudades europeas de turismo clasico","Paris;Rome;Barcelona;Vienna;Prague;Budapest;Florence;Salzburg;Lucerne;Lisbon;Athens;Berlin;London;Copenhagen;Zurich;Geneva;Brussels;Oslo;Stockholm;Versailles;Porto;Valencia;Zaragoza;Oviedo;Milan;Turin;Salzburg;Bordeaux Cathedral;Delft;The Hague;Haarlem;Leiden;St Gallen;Basel;Gothenburg;Trondheim;Rhodes;Thessaloniki;Dijon;Montpellier;Nantes;Toulouse;Cagliari;Trieste;Stuttgart;Dortmund;Nuremberg")
P("Lugar religioso","Centro religioso o de peregrinacion","Mecca;Medina;Jerusalem;Lhasa;Kandy;Gaya;Rome;Bordeaux Cathedral;Salt Lake City;Kyoto;Mashhad;Isfahan;Samarkand;Darjeeling;Adwa;Cap-Haïtien;Lucknow;Amritsar;Karbala")
P("Zona de conflicto o inestable","Lugar de pais con conflicto armado o inestabilidad grave en los 2020s","Kyiv;Odessa;Cherkasy;Rivne;Khan Younis;Jerusalem;Tel Aviv;Baghdad;Basra;Babylon;Kabul;Kandahar;Jalalabad;Mogadishu;Hargeisa;Khartoum;Juba;Bangui;Goma;Bukavu;Kinshasa;Dori;Niamey;Agadez;N'Djamena;Port-au-Prince;Cap-Haïtien;Tobruk;Pyongyang;Hamhung;Caracas;Maracaibo;Maracay;Adwa;Kano;Jos;Enugu;Karachi;Lahore")
P("Megaurbe (area metropolitana de mas de ~3M)","Gran area metropolitana","Addis Ababa;Ankara;Baghdad;Bangkok;Barcelona;Bengaluru;Berlin;Bogotá;Buenos Aires;Busan;Cairo;Caracas;Casablanca;Chicago;Dalian;New Delhi;Douala;Durban;Guangzhou;Hangzhou;Houston;Hyderabad;Jakarta;Karachi;Khartoum;Kinshasa;Kolkata;Lahore;Lima;London;Luanda;Medellín;Melbourne;Mexico City;Milan;Mumbai;Nanjing;Osaka;Paris;Philadelphia;Phoenix;Rio de Janeiro;Rome;Santiago;São Paulo;Seoul;Shanghai;Singapore;Sydney;Taipei;Tehran;Tokyo;Toronto;Washington DC;Yaoundé;Kano;Boston;Detroit;San Francisco;Tampa;Athens;Budapest;Warsaw;Kyiv;Guatemala City;Kabul;Tashkent;Accra;Dakar;Kumasi;Long Beach;Anaheim;Hollywood;Santa Monica;Brooklyn;Ellis Island;Brisbane;Perth;Daegu;Fukuoka;Pyongyang;Guntur;Lucknow;Patna;Mashhad;Isfahan;Doha;Dortmund;Stuttgart;Montreal;Edmonton;Belo Horizonte;Porto Alegre;Maracaibo")
P("Pueblo o ciudad chica (menos de ~150 mil)","Localidad pequena o sitio rural","Monowi;Brookings;Tombstone;Shanksville;Lake Geneva;Three Rivers;Fort Knox;Ellis Island;Annapolis;Helena;Pierre;Butte;Klamath Falls;Northampton;Newport;Princeton;Kalamazoo;Binghamton;Cedar Rapids;Macon;Monterey;Atlantic City;Gainesville;Dayton;Charleston;Green Bay;Fort Wayne;Hartford;Banff;Amboseli;Chitwan;Palenque;Thaba Bosiu;Ubud;Sigiriya;Geel;Ypres;Delft;Versailles;Vaduz;San Marino City;Luxembourg;Brodick Castle;Stonehenge;Snowdon;Larvik;Rovaniemi;Toszek;Celje;Ryotsu;Odawara;Gander;Moncton;Nanaimo;Victoria;Woodstock;Hervey Bay;Toowoomba;Ancud;Puntarenas;Copiapó;Ayacucho;Luján;Puerto Madryn;Florida;Cotapachi;Dori;Adwa;Salar de Uyuni;Tsingy de Bemaraha;Hamilton;Gibraltar;Corsica;St George's;Ciudad de la Paz;Hagåtña;Nuku'alofa;Valletta;Thingvellir;Ambon;Kupang;Fukui;Wakayama;Miaoli City;Veraval;Gaya;Darjeeling;Ratnagiri;Jamnagar;Khan Younis;Yamoussoukro;Eldoret;Kaolack;Bissau;Mbabane;Gaborone;Maseru;Pristina;Skopje;Tirana;Podgorica;Liberec;Szeged;Szczecin;Oulu;Turku;Trieste;Oviedo;Cagliari;Messina")
P("Ciudad con nombre repetido en otro pais","Ciudades que existen en mas de un pais o estado (ambiguas)","Victoria;Kingston;Georgetown;Hamilton;Birmingham;Portland;Columbia;Charleston;Albany;Newcastle;Newcastle upon Tyne;Newport;Princeton;Florida;Valencia;Santiago;La Paz;London;Toronto;Concepción;San José;Cordoba;Salem;Paris;Troy;Lima;Athens;Rome;Berlin;Warsaw;Moscow;Madison;Dover Strait;Brooklyn;Boston;Hollywood;Santa Monica;Long Beach;Arlington;Fort Worth;Oxford")

# ---------- POR PAIS (manual) ----------
C("Paises hispanohablantes","Pais cuya lengua oficial principal es el espanol","Argentina;Bolivia;Chile;Colombia;Costa Rica;Ecuador;España;Guatemala;México;Panamá;Paraguay;Perú;Puerto Rico;Rep. Dominicana;Uruguay;Venezuela;Guinea Ecuatorial")
C("Paises angloparlantes","Pais con ingles como lengua oficial principal","EE.UU.;Reino Unido;Canadá;Australia;Nueva Zelanda;Bermudas;Guyana;Jamaica;Trinidad y Tobago;Antigua y Barbuda;Guam;Puerto Rico;Sudáfrica;Nigeria;Ghana;Kenia;Uganda;Liberia;Malaui;Zimbabue;Botsuana;Namibia;Esuatini;Lesoto;Tonga;Papúa Nueva Guinea;Islas Salomón;Mauricio;Filipinas;Singapur;India;Pakistán")
C("Paises francofonos","Pais con frances como lengua oficial o muy extendida","Francia;Bélgica;Suiza;Luxemburgo;Haití;Guayana Francesa;Martinica;Camerún;Costa de Marfil;Senegal;Benín;Burkina Faso;Níger;Chad;Gabón;Rep. Centroafricana;RD del Congo;Madagascar;Túnez;Marruecos;Mauricio;Túnez;Burundi;Ruanda;Mali")
C("Alfabeto no latino","Pais cuya escritura principal no es latina (cirilico, arabe, chino, japones, etc.)","China;Japón;Corea del Sur;Corea del Norte;Taiwán;Rusia;Ucrania;Irak;Irán;Arabia Saudita;Egipto;Libia;Sudán;Afganistán;Pakistán;Israel;Palestina;Qatar;Omán;Georgia;Armenia;Grecia;Chipre;Mongolia;Kazajistán;Uzbekistán;Kirguistán;Nepal;India;Sri Lanka;Tailandia;Etiopía;Serbia;Macedonia del Norte;Moldavia;Azerbaiyán")
C("Paises de mayoria musulmana","Pais con mayoria de poblacion musulmana","Irak;Irán;Arabia Saudita;Egipto;Libia;Sudán;Afganistán;Pakistán;Qatar;Omán;Marruecos;Túnez;Turquía;Azerbaiyán;Uzbekistán;Kirguistán;Kazajistán;Indonesia;Malasia;Níger;Senegal;Somalia;Chad;Palestina;Kosovo;Albania;Burkina Faso")
C("Ex Yugoslavia","Pais que fue parte de Yugoslavia","Serbia;Croacia;Eslovenia;Bosnia y Herzegovina;Montenegro;Macedonia del Norte;Kosovo")
C("Bloque comunista","Estados comunistas de la Guerra Fria","Rusia;Ucrania;Bielorrusia;Moldavia;Lituania;Letonia;Estonia;Georgia;Armenia;Azerbaiyán;Kazajistán;Uzbekistán;Turkmenistán;Kirguistán;Tayikistán;Polonia;Chequia;Eslovaquia;Hungría;Bulgaria;Rumania;Albania;Serbia;Croacia;Eslovenia;Bosnia y Herzegovina;Montenegro;Macedonia del Norte;Kosovo;China;Vietnam;Corea del Norte;Mongolia;Laos;Camboya;Cuba")
C("Ex URSS","Pais que fue republica de la URSS","Rusia;Ucrania;Bielorrusia;Moldavia;Lituania;Letonia;Estonia;Georgia;Armenia;Azerbaiyán;Kazajistán;Uzbekistán;Turkmenistán;Kirguistán;Tayikistán")
C("Union Europea","Miembro de la UE","Francia;Alemania;Italia;España;Polonia;Países Bajos;Bélgica;Grecia;Hungría;Chequia;Portugal;Suecia;Austria;Finlandia;Dinamarca;Eslovenia;Letonia;Estonia;Luxemburgo;Malta;Chipre")
C("G20","Miembro del G20 (19 paises)","Argentina;Australia;Brasil;Canadá;China;Francia;Alemania;India;Indonesia;Italia;Japón;México;Rusia;Arabia Saudita;Sudáfrica;Corea del Sur;Turquía;Reino Unido;EE.UU.")
C("Paises campeones del mundo de futbol","Argentina, Brasil, Francia, Alemania, Italia, Espana, Inglaterra (Reino Unido), Uruguay","Argentina;Brasil;Francia;Alemania;Italia;España;Reino Unido;Uruguay")
C("Paises sin salida al mar","Pais mediterraneo (landlocked)","Bolivia;Paraguay;Suiza;Austria;Hungría;Chequia;Serbia;Macedonia del Norte;Kosovo;Moldavia;Luxemburgo;Liechtenstein;San Marino;Kazajistán;Uzbekistán;Kirguistán;Mongolia;Armenia;Azerbaiyán;Afganistán;Nepal;Etiopía;Uganda;Ruanda;Malaui;Zimbabue;Zambia;Botsuana;Lesoto;Esuatini;Níger;Chad;Rep. Centroafricana;Sudán del Sur;Burkina Faso;Mali;Bielorrusia")
C("Paises pequenos (menos de 5 millones de hab.)","Poblacion menor a ~5M","Uruguay;Costa Rica;Panamá;Namibia;Botsuana;Letonia;Estonia;Eslovenia;Islandia;Luxemburgo;Malta;Chipre;Mongolia;Georgia;Armenia;Moldavia;Macedonia del Norte;Kosovo;Albania;Lesoto;Esuatini;Mauricio;Qatar;Omán;Singapur;Tonga;Islas Salomón;Bermudas;Antigua y Barbuda;Guyana;Trinidad y Tobago;Haití;Jamaica;Gabón;Guinea Ecuatorial;Liberia;Rep. Centroafricana;Noruega;Finlandia;Nueva Zelanda;Liechtenstein;San Marino;Puerto Rico;Guam;Martinica;Guayana Francesa;Palestina;Guinea-Bisáu;Benín;Togo;Sin país (Atlántico Norte)")
C("Paises grandes (mas de 100 millones de hab.)","Poblacion mayor a ~100M","China;India;EE.UU.;Indonesia;Pakistán;Nigeria;Brasil;Rusia;México;Japón;Etiopía;Filipinas;Egipto;RD del Congo;Vietnam;Irán;Turquía")
C("Mundial: Sudamerica de habla hispana","Hispanoamerica sudamericana","Argentina;Bolivia;Chile;Colombia;Ecuador;Paraguay;Perú;Uruguay;Venezuela")


# ---------- AJUSTES ----------
def rem(n,t,d=PL): d[n]=(d[n][0],d[n][1]-S(t))
rem("Ciudad costera","Hartford;New Delhi;Cairo;Canberra;Washington DC;Arlington;Amboseli;Basra;Kolkata;Kaolack")
rem("Capital regional","Douala;Dortmund;Busan;Daegu;Cotonou;Nha Trang;Taichung;Tainan;Miaoli City;Montreal;Moncton;Gander;Nanaimo;Sevilla;Dundee;Tehran;Kano")
rem("Guerras Mundiales","Fort Knox;Annapolis;Arlington;Hamhung;Cherkasy;Ellis Island;Toszek;Brussels;Szczecin;Trieste;Dortmund")
PL["Ciudad costera"]=(PL["Ciudad costera"][0],PL["Ciudad costera"][1]|S("Taichung;Victoria;The Hague;Inverness;Haarlem;Lima;Petropavlovsk-Kamchatsky;Athens;Montevideo;Salé;Montpellier;Calabar;Khan Younis;Buenos Aires;Brookings;Gibraltar;Delft;Baku;Nanaimo;Christchurch;Tobruk;Leiden;Miaoli City;Maracaibo;Huế;Reykjavík;Elephant Island"))  # revision 21/10: faltaban costeras reales (ver puente)
del PL["Ciudad con nombre repetido en otro pais"]
del PA["Mundial: Sudamerica de habla hispana"]
def _mas(n,t): PA[n]=(PA[n][0],PA[n][1]|S(t))
_mas("Union Europea","Bulgaria");_mas("Paises pequenos (menos de 5 millones de hab.)","Groenlandia")

MANUAL=list(PL)        # categorias que hay que decidir a mano para un lugar nuevo
def _hav(lat1,lon1,lat2,lon2):
    p=np.pi/180;a=np.sin((lat2-lat1)*p/2)**2+np.cos(lat1*p)*np.cos(lat2*p)*np.sin((lon2-lon1)*p/2)**2
    return float(12742*np.arcsin(np.sqrt(a)))
import csv,os
def _nivel_ingreso():
    f=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","dim_pais.csv")
    return {x["pais"]:x["nivel_ingreso"] for x in csv.DictReader(open(f,encoding="utf8"))}
def _flags(col):
    f=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","dim_pais.csv")
    return {x["pais"] for x in csv.DictReader(open(f,encoding="utf8")) if x[col]=="1"}
CAT_INGRESO={"alto":"Paises de ingresos altos","medio":"Paises de ingresos medios","bajo":"Paises de ingresos bajos"}
def dist_ba(lat,lon): return _hav(lat,lon,-34.6,-58.38)
CORTE_INTERIOR_KM=500   # "Ciudad interior": a mas de 500 km de la costa oceanica (Natural Earth 10m coastline)
_COSTA=[]
def _cargar_costa():
    import struct,os
    d=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"coastline","ne_10m_coastline.shp"),"rb").read();pos=100;segs=[]
    while pos<len(d):
        clen=struct.unpack('>i',d[pos+4:pos+8])[0]*2;rec=d[pos+8:pos+8+clen];pos+=8+clen
        if struct.unpack('<i',rec[:4])[0]!=3: continue
        n_p,n_pt=struct.unpack('<ii',rec[36:44]);parts=list(struct.unpack('<%di'%n_p,rec[44:44+4*n_p]))+[n_pt]
        pts=np.frombuffer(rec,dtype='<f8',count=n_pt*2,offset=44+4*n_p).reshape(-1,2)
        for i in range(n_p):
            q=pts[parts[i]:parts[i+1]]
            if len(q)>1: segs.append(np.hstack([q[:-1],q[1:]]))
    S=np.vstack(segs);_COSTA.extend([S,(S[:,0]+S[:,2])/2,(S[:,1]+S[:,3])/2])
def dist_costa(lat,lon):
    """Distancia (km) del punto al segmento de costa mas cercano."""
    if not _COSTA: _cargar_costa()
    S,mx,my=_COSTA;R=6371.0;rad=np.pi/180;rd=5.0
    while True:
        dl=np.abs((mx-lon+540)%360-180);m=(np.abs(my-lat)<=rd)&(dl<=rd/max(np.cos(lat*rad),0.05))
        if m.sum():
            s=S[m];cl=np.cos(lat*rad)
            x1=((s[:,0]-lon+540)%360-180)*rad*R*cl;y1=(s[:,1]-lat)*rad*R;x2=((s[:,2]-lon+540)%360-180)*rad*R*cl;y2=(s[:,3]-lat)*rad*R
            vx,vy=x2-x1,y2-y1;L2=vx*vx+vy*vy;t=np.clip(np.where(L2>0,-(x1*vx+y1*vy)/np.where(L2>0,L2,1),0),0,1)
            dd=float(np.hypot(x1+t*vx,y1+t*vy).min())
            if dd<rd*111*0.7 or rd>=90: return dd
        rd*=2

# ---------- rios (Natural Earth 10m: rivers_lake_centerlines + suplementos Europa, Norteamerica, Australia) ----------
import struct as _st
_RIOS={}
def _leer_rios(nombre,main):
    import os
    P=os.path.join(os.path.dirname(os.path.abspath(__file__)),"rios",nombre)
    b=open(P+".dbf","rb").read();n,hl,rl=_st.unpack("<IHH",b[4:12]);f=[];p=32
    while b[p]!=13: f.append((b[p:p+11].split(b"\0")[0].decode(),b[p+16]));p+=32
    off={};o=0
    for nm,ln in f: off[nm]=(o,ln);o+=ln
    meta=[]
    for i in range(n):
        r=b[hl+i*rl+1:hl+(i+1)*rl];g=lambda k:r[off[k][0]:off[k][0]+off[k][1]].replace(b"\0",b" ").decode("utf8","ignore").strip() if k in off else ""
        meta.append((g("featurecla"),g("name") or g("name_es"),g("scalerank")))
    d=open(P+".shp","rb").read();pos=100;segs=[];ids=[];k=0
    while pos<len(d):
        cl=_st.unpack(">i",d[pos+4:pos+8])[0]*2;rec=d[pos+8:pos+8+cl];pos+=8+cl;fc,nm,sr=meta[k];k+=1
        if _st.unpack("<i",rec[:4])[0]!=3 or fc!="River" or (not nm and not main) or (main and int(sr or 99)>8): continue
        n_p,n_pt=_st.unpack("<ii",rec[36:44]);parts=list(_st.unpack("<%di"%n_p,rec[44:44+4*n_p]))+[n_pt]
        pts=np.frombuffer(rec,dtype="<f8",count=n_pt*2,offset=44+4*n_p).reshape(-1,2)
        for i in range(n_p):
            q=pts[parts[i]:parts[i+1]]
            if len(q)>1: segs.append(np.hstack([q[:-1],q[1:]]));ids+=[nm]*(len(q)-1)
    return np.vstack(segs),ids
def _dmin(S,ids,lat,lon):
    cl=np.cos(np.radians(lat));R=6371.0;rad=np.pi/180
    x1=(S[:,0]-lon)*rad*R*cl;y1=(S[:,1]-lat)*rad*R;x2=(S[:,2]-lon)*rad*R*cl;y2=(S[:,3]-lat)*rad*R
    vx,vy=x2-x1,y2-y1;L2=vx*vx+vy*vy;t=np.clip(np.where(L2>0,-(x1*vx+y1*vy)/np.where(L2>0,L2,1),0),0,1)
    dd=np.hypot(x1+t*vx,y1+t*vy);j=int(dd.argmin());return round(float(dd[j]),1),ids[j]
CORTE_RIO_KM=10     # rio principal (escala <= 8, archivo base)
CORTE_RIO_SUP_KM=4.5  # rio con nombre de los suplementos (mas detallados)
def dist_rio(lat,lon):
    """(km, nombre, es_fluvial). Fluvial = rio principal a <= 10 km o rio con nombre de los suplementos a <= 4.5 km. Siempre revisar a mano."""
    if not _RIOS:
        _RIOS["m"]=_leer_rios("ne_10m_rivers_lake_centerlines",True)
        ss=[_leer_rios(f"ne_10m_rivers_{r}",False) for r in("europe","north_america","australia")]
        _RIOS["s"]=(np.vstack([s for s,_ in ss]),sum((i for _,i in ss),[]))
    dm,nm=_dmin(*_RIOS["m"],lat,lon);ds,ns=_dmin(*_RIOS["s"],lat,lon)
    if ds<=CORTE_RIO_SUP_KM and ds<=dm: return ds,ns,True
    return dm,nm,dm<=CORTE_RIO_KM

# ---------- lagos (Natural Earth 10m lakes + Europa, Norteamerica, Australia) y volcanes (Smithsonian GVP, Holoceno) ----------
import os, struct
def _ldbf(P):
    b=open(P+'.dbf','rb').read();n,hl,rl=struct.unpack('<IHH',b[4:12]);f=[];p=32
    while b[p]!=13: f.append((b[p:p+11].split(b'\0')[0].decode(),b[p+16]));p+=32
    off={};o=0
    for nm,ln in f: off[nm]=(o,ln);o+=ln
    out=[]
    for i in range(n):
        r=b[hl+i*rl+1:hl+(i+1)*rl];out.append({k:r[a:a+l].replace(b'\0',b' ').decode('utf8','ignore').strip() for k,(a,l) in off.items() if k in('name','name_es','scalerank','featurecla')})
    return out
def _lpolys(P):
    meta=_ldbf(P);d=open(P+'.shp','rb').read();pos=100;res=[];k=0
    while pos<len(d):
        cl=struct.unpack('>i',d[pos+4:pos+8])[0]*2;rec=d[pos+8:pos+8+cl];pos+=8+cl;m=meta[k];k+=1
        if struct.unpack('<i',rec[:4])[0]!=5: continue
        bb=struct.unpack('<4d',rec[4:36]);n_p,n_pt=struct.unpack('<ii',rec[36:44]);parts=list(struct.unpack('<%di'%n_p,rec[44:44+4*n_p]))+[n_pt]
        pts=np.frombuffer(rec,dtype='<f8',count=n_pt*2,offset=44+4*n_p).reshape(-1,2)
        res.append((m.get('name') or m.get('name_es') or '',bb,[pts[parts[i]:parts[i+1]] for i in range(n_p)]))
    return res
def _lload(names):
    L=[]
    for n in names: L+=_lpolys(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lagos',f'ne_10m_{n}'))
    return L
def _inside(x,y,ring):
    xs,ys=ring[:,0],ring[:,1];x2,y2=np.roll(xs,-1),np.roll(ys,-1)
    c=((ys>y)!=(y2>y))&(x<(x2-xs)*(y-ys)/(y2-ys+1e-12)+xs);return c.sum()%2==1
def _ldist(lat,lon,L):
    best=(1e9,'');cl=np.cos(np.radians(lat));R=111.19
    for nm,bb,rings in L:
        m=0.5
        if lon<bb[0]-m or lon>bb[2]+m or lat<bb[1]-m or lat>bb[3]+m: continue
        if _inside(lon,lat,rings[0]) and not any(_inside(lon,lat,h) for h in rings[1:]): return 0.0,nm
        for q in rings:
            x1=(q[:-1,0]-lon)*R*cl;y1=(q[:-1,1]-lat)*R;x2=(q[1:,0]-lon)*R*cl;y2=(q[1:,1]-lat)*R
            vx,vy=x2-x1,y2-y1;L2=vx*vx+vy*vy;t=np.clip(np.where(L2>0,-(x1*vx+y1*vy)/np.where(L2>0,L2,1),0),0,1)
            d=float(np.hypot(x1+t*vx,y1+t*vy).min())
            if d<best[0]: best=(d,nm)
    return best

_LAGOS=[]
CORTE_LAGO_KM=5
def dist_lago(lat,lon):
    """(km, nombre) al lago mas cercano (borde; 0 si esta dentro). Ciudad lacustre = <= 5 km; revisar a mano (mares interiores como el Caspio no estan)."""
    if not _LAGOS: _LAGOS.extend(_lload(["lakes","lakes_europe","lakes_north_america","lakes_australia"]))
    d,n=_ldist(lat,lon,_LAGOS);return (round(d,1) if d<1e8 else None),n
_VOLC=[]
CORTE_VOLCAN_KM=50
def dist_volcan(lat,lon):
    """(km, nombre) al volcan holoceno mas cercano (catalogo GVP). Ciudad volcanica = <= 50 km."""
    import csv
    if not _VOLC:
        for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"volcanes","holocene.csv"),encoding="utf8")): 
            if r["ultima_erupcion"].strip().lower()!="unknown": _VOLC.append((r["nombre"],float(r["lat"]),float(r["lon"])))
    best=(1e9,"");r=np.pi/180
    for n,a,b in _VOLC:
        dl=(b-lon)*r;h=np.sin((a-lat)*r/2)**2+np.cos(lat*r)*np.cos(a*r)*np.sin(dl/2)**2;d=12742*np.arcsin(np.sqrt(h))
        if d<best[0]: best=(d,n)
    return round(float(best[0]),1),best[1]

# ---------- terremotos (USGS, M7+ desde 1900) y altitud ----------
_SISM=[]
CORTE_SISMO_KM=100
def n_sismos(lat,lon):
    """Cantidad de terremotos M7+ (USGS desde 1900) a <= 100 km. Ciudad sismica = al menos 2."""
    import csv
    if not _SISM:
        for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"terremotos","usgs_m7_desde_1900.csv"),encoding="utf8")): _SISM.append((float(r["latitude"]),float(r["longitude"])))
        _SISM[:]=[np.array([a for a,_ in _SISM]),np.array([b for _,b in _SISM])]
    la,lo=_SISM;r=np.pi/180;dl=(lo-lon)*r;h=np.sin((la-lat)*r/2)**2+np.cos(lat*r)*np.cos(la*r)*np.sin(dl/2)**2
    return int((12742*np.arcsin(np.sqrt(h))<=CORTE_SISMO_KM).sum())
CORTE_ALTURA_M=1490   # "Lugar de altura": altitud_m >= 1490 (Open-Meteo / Copernicus DEM; scripts/obtener_altitudes.py)

# ---------- UNESCO (Patrimonio Mundial, lista 2026; un punto por sitio) ----------
_UNESCO=[]
CORTE_UNESCO_KM=10
def dist_unesco(lat,lon):
    """(km, sitio mas cercano, hay_sitio_cultural_a_<=10km). Monumento o sitio historico UNESCO = sitio cultural a <= 10 km y la ciudad no es "Patrimonio UNESCO urbano"."""
    import csv
    if not _UNESCO:
        f=list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"unesco","whc_2026.csv"),encoding="utf8")))
        _UNESCO.extend([np.array([float(x["latitude"]) for x in f]),np.array([float(x["longitude"]) for x in f]),[x["name_en"] for x in f],[x["category"] for x in f]])
    la,lo,nm,ct=_UNESCO;r=np.pi/180;dl=(lo-lon)*r;h=np.sin((la-lat)*r/2)**2+np.cos(lat*r)*np.cos(la*r)*np.sin(dl/2)**2;d=12742*np.arcsin(np.sqrt(h));j=int(d.argmin())
    m=np.where(d<=CORTE_UNESCO_KM)[0];cult=any(ct[k]=="Cultural" for k in m)
    return round(float(d[j]),1),nm[j],cult

def auto_categorias(pais,lat,lon,manual):
    """Categorias de un lugar nuevo: las manuales que se le pasan + las de pais + las calculadas + los complementos."""
    bad=set(manual)-set(MANUAL)
    assert not bad,f"categorias manuales desconocidas: {bad}"
    c=set(manual); d=dist_ba(lat,lon)
    c|={n for n,(_,m) in PA.items() if pais in m}
    if not pais.startswith("Sin pais") and not pais.startswith("Sin país"):
        niv=_nivel_ingreso().get(pais)
        assert niv,f"pais '{pais}' no esta en datos/dim_pais.csv: agregarlo con su clase del Banco Mundial (alto/medio/bajo)"
        c.add(CAT_INGRESO[niv])
        for col,nom in (("monarquia","Monarquías"),("otan","OTAN"),("commonwealth","Commonwealth"),("liga_arabe","Liga Árabe"),("opep","OPEP"),("g7","G7"),("brics","BRICS")):
            if pais in _flags(col): c.add(nom)
    if dist_unesco(lat,lon)[2] and "Patrimonio UNESCO urbano" not in c: c.add("Monumento o sitio historico UNESCO")
    a=abs(lat)
    if a<23.5: c.add("Zona tropical (|lat| < 23,5)")
    if a>=55: c.add("Zonas frías (|lat| ≥ 55)")
    if dist_costa(lat,lon)>CORTE_INTERIOR_KM: c.add("Ciudad interior (> 500 km de la costa)")
    return c
