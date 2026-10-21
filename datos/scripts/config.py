"""Configuracion compartida del modelo de datos MapTap."""
import os,re,unicodedata
D="/sessions/trusting-nice-davinci/mnt/Maptap/"
DD=os.environ.get("MAPTAP_DATOS",D+"datos/")
CORTE_PRO="2026-09-02"   # inicio del profesionalismo: unica definicion
# variantes de un mismo lugar -> nombre canonico
ALIAS={"Dundee, Scotland, UK":"Dundee, Scotland, United Kingdom","London, England, UK":"London, England, United Kingdom","Toronto, Canada":"Toronto, Ontario, Canada","Semipalatinsk, Kazakhstan":"Semey, Kazakhstan","the location where the Titanic sank":"Donde se hundio el Titanic"}
JUG=[("Nacho Toker","Toker"),("Axel Itzcovitz","Axel"),("Feli Garabato","Feli"),("Antonio Santos","Antonio"),("Lucas Greco","Lucas"),("Sandro Anello","Sandro"),("Bruno Feinsilber","Bruno"),("Ale Feinsilber","Ale"),("Dario Feinsilber","Dario"),("Fede Moia","Fede"),("Martin Feinsilber","Martín")]
slug=lambda s:re.sub(r"[^a-z0-9]+","-",unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()).strip("-")
CORTE_CHALLENGE_PRO="2026-09-28"  # el Challenge profesional arranca el 28/9 (cuando empezamos a registrarlo), no el 2/9 del torneo
