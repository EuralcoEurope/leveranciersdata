#!/usr/bin/env python3
"""Bouwt data/yoto.json, data/*.csv en data/leveranciers.sqlite uit de handmatig gecontroleerde brondata hieronder.
Gebruik: python3 tools/build.py   (vanuit de repo-root)"""
import json, csv, sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")

SUPPLIER = dict(
    id="yoto", naam="Henan YongTong Aluminium Co., Ltd (YOTO)", naam_origineel="河南永通铝业有限公司",
    land="CN", regio="Henan (Gongyi)", valuta=None, incoterms=None, minimale_afname=None, levertijd=None,
    betaalvoorwaarden=None, certificeringen=None,
    adres="河南省巩义市回郭镇工业园区 (Huiguo Town Industrial Park, Gongyi, Henan)",
    website="www.yotoly.com", email="yoto@yotoly.com; admin@yotoly.com; sales@defeller.com",
    telefoon="+86 371 6426 5222 / 6426 3777 (binnenland); +86 371 5552 6225 (Zhengzhou export); +86 21 6075 0721 (Shanghai export)",
    export_afdelingen="Zhengzhou: Henan Yongyang Imp. and Exp. Co., Ltd / Henan Wealthall International Trading Co., Ltd; Shanghai: Shanghai Defeller International Trading Co., Ltd",
    bron_bestand="IMG_9632.JPG", bron_pagina="achterkant",
    opmerking="Boekje bevat geen prijzen, minimale afname, levertijden, certificaten of normen. Velden blijven leeg (niet bekend).",
)

# Eén blok per productvorm (= één tabel in het boekje). Legeringsgroepen volgen de rijen van de tabel.
FORMS = [
 dict(vorm="plaat", vorm_origineel="铝板 / Aluminum Sheet", bron="IMG_9620.JPG", pagina=None,
  pagina_noot="paginanummer niet zichtbaar op foto",
  groepen=[["1050","1060","1100","1200"],["3003","3004","3005","3105"],["5005","5052","5754","5083"],["6061"],["8011"]],
  tempers=["O","T6","H12","H22","H14","H24","H18","H32","H111","H112","H116","H321"],
  dikte=[(0.2,4.0),(4.0,200.0)], breedte=(500,2200), lengte=(500,9000), diameter=None, binnendiameter=None,
  extra=None, vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering (bv. T6 alleen logisch bij 6061). Temper per legering bevestigen.","Temperlijst eindigt op 'etc.': andere tempers mogelijk.","Dikte in twee banden (0.2-4.0 en 4.0-200 mm): per band zijn breedte/lengte niet apart opgegeven."]),
 dict(vorm="traanplaat", vorm_origineel="铝花纹板 / Aluminum Checkered Plate", bron="IMG_9621.JPG", pagina="07-08",
  pagina_noot=None,
  groepen=[["1050","1060","1100","1200"],["3003","3005","3105"],["5005","5052","5754"],["8011"]],
  tempers=["O","H12","H22","H14","H24","H18","H32"],
  dikte=[(0.3,4.0),(4.0,10.0)], breedte=(500,1550), lengte=(500,9000), diameter=None, binnendiameter=None,
  extra=dict(patroon="Big five bar, Small five bar, Two bar, Diamond", afwerking="Mill finish, Bright finish"),
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'.","5083 staat NIET bij traanplaat in dit boekje (wel bij Euralco-praktijk gebruikelijk): bij leverancier navragen."]),
 dict(vorm="coil", vorm_origineel="铝卷 / Aluminum Coil", bron="IMG_9622.JPG", pagina=None,
  pagina_noot="paginanummer niet zichtbaar op foto",
  groepen=[["1050","1060","1100","1200"],["3003","3004","3005","3105"],["5005","5052","5754","5083"],["6061"],["8011"]],
  tempers=["O","H12","H22","H14","H16","H24","H18","H32","H112","T6"],
  dikte=[(0.2,4.0),(4.1,10.0)], breedte=(500,2200), lengte=None, diameter=None, binnendiameter=[508,405,305,150,75],
  extra=dict(hoofdproducten="1-, 3-, 5- en 8-serie"),
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'.","Binnendiameter (ID) is een lijst van losse waarden, geen bereik."]),
 dict(vorm="band", vorm_origineel="铝带 / Aluminum Strip", bron="IMG_9623.JPG", pagina="09-10",
  pagina_noot=None,
  groepen=[["1050","1060","1100","1200"],["3003","3004"],["5005","5052"],["8011"]],
  tempers=["O","H12","H22","H14","H16","H24","H18","H32","H112","T6"],
  dikte=[(0.2,3.0)], breedte=(20,1550), lengte=None, diameter=None, binnendiameter=[508,405,305,150,75],
  extra=dict(hoofdproducten="1-, 3-, 5- en 8-serie"),
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'."]),
 dict(vorm="cirkel", vorm_origineel="铝圆片 / Aluminum Circle", bron="IMG_9624.JPG", pagina=None,
  pagina_noot="paginanummer niet zichtbaar op foto",
  groepen=[["1050","1060","1100"],["3003","3004","3005","3105"],["5005","5052","5754","5083"]],
  tempers=["O","H12","H22","H14","H24","H18","H32","H111","H112"],
  dikte=[(0.25,6.0)], breedte=None, lengte=None, diameter=(50,1200), binnendiameter=None,
  extra=None,
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'."]),
 dict(vorm="gecoat_coil", vorm_origineel="氟碳/聚酯预辊涂铝卷 / Pre-painted Aluminium Coil (PE/PVDF)", bron="IMG_9625.JPG", pagina="11-12",
  pagina_noot=None,
  groepen=[["1050","1060","1100"],["3003","3004","3005","3105"],["5005","5052","5754"]],
  tempers=["H12","H22","H14","H24","H18","H32"],
  dikte=[(0.2,2.5)], breedte=(50,1500), lengte=None, diameter=None, binnendiameter=[405,505],
  extra=dict(coating="PE / PVDF"),
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'.","Bovenrand van de foto is afgesneden; tabel zelf volledig leesbaar."]),
 dict(vorm="gebosseleerde_coil", vorm_origineel="压花铝卷 / Embossed Aluminium Coil", bron="IMG_9626.JPG", pagina=None,
  pagina_noot="paginanummer niet zichtbaar op foto",
  groepen=[["1050","1060","1100","1200"],["3003","3005","3105"],["8011"]],
  tempers=["O","H12","H22","H14","H24","H18","H32"],
  dikte=[(0.2,2.0)], breedte=(300,1250), lengte=None, diameter=None, binnendiameter=[508,405,305,150],
  extra=None,
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'."]),
 dict(vorm="folie", vorm_origineel="铝箔 / Aluminum Foil", bron="IMG_9627.JPG", pagina="13-14",
  pagina_noot=None,
  groepen=[["8011"],["3003"],["1100"],["1235"]],
  tempers=["O","H12","H22","H14","H24","H18"],
  dikte=[(0.006,0.2)], breedte=(40,1550), lengte=None, diameter=None, binnendiameter=[508,305,150,75],
  extra=None,
  vlaggen=["Temperlijst geldt voor de hele tabel, niet per legering.","Temperlijst eindigt op 'etc.'.","Rijen in de tabel zijn niet schoon gegroepeerd; alle vier legeringen delen dezelfde waarden."]),
]

def rng(r): return None if r is None else f"{r[0]}-{r[1]}"

def build():
    offers = []
    for f in FORMS:
        for g in f["groepen"]:
            for alloy in g:
                dik = f["dikte"]
                offers.append(dict(
                    id=f"yoto-{f['vorm']}-{alloy}", leverancier_id="yoto", vorm=f["vorm"], vorm_origineel=f["vorm_origineel"],
                    legering=alloy, tempers=f["tempers"], tempers_per_legering_bevestigd=False, tempers_open_einde=True,
                    dikte_banden_mm=[list(b) for b in dik], dikte_min_mm=min(b[0] for b in dik), dikte_max_mm=max(b[1] for b in dik),
                    breedte_min_mm=f["breedte"][0] if f["breedte"] else None, breedte_max_mm=f["breedte"][1] if f["breedte"] else None,
                    lengte_min_mm=f["lengte"][0] if f["lengte"] else None, lengte_max_mm=f["lengte"][1] if f["lengte"] else None,
                    diameter_min_mm=f["diameter"][0] if f["diameter"] else None, diameter_max_mm=f["diameter"][1] if f["diameter"] else None,
                    binnendiameter_mm=f["binnendiameter"], extra=f["extra"],
                    maatwerk="op klantspecificatie (按客户要求生产各种规格)",
                    beschikbaarheid="op bestelling (aanname: boekje noemt geen voorraad)",
                    prijs=None, prijs_valuta=None, prijsbasis=None, minimale_afname=None, levertijd=None, norm=None,
                    bron_bestand=f["bron"], bron_pagina=f["pagina"], bron_pagina_noot=f["pagina_noot"],
                    betrouwbaarheid="hoog (tabel scherp gelezen)", vlaggen=f["vlaggen"]))
    json.dump(dict(leverancier=SUPPLIER, aanbod=offers), open(f"{D}/yoto.json","w"), ensure_ascii=False, indent=1)
    # CSV (platte versie)
    cols = [k for k in offers[0] if k not in ("tempers","dikte_banden_mm","binnendiameter_mm","extra","vlaggen")]
    with open(f"{D}/yoto_aanbod.csv","w",newline="",encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols+["tempers","dikte_banden_mm","binnendiameter_mm","extra","vlaggen"])
        for o in offers:
            w.writerow([o[c] for c in cols]+[";".join(o["tempers"]),";".join(rng(b) for b in o["dikte_banden_mm"]),
                       ";".join(map(str,o["binnendiameter_mm"] or [])), json.dumps(o["extra"],ensure_ascii=False) if o["extra"] else "", " | ".join(o["vlaggen"])])
    # SQLite
    p = f"{D}/leveranciers.sqlite"
    if os.path.exists(p): os.remove(p)
    c = sqlite3.connect(p); c.executescript(open(f"{ROOT}/schema.sql").read())
    s = SUPPLIER
    c.execute("INSERT INTO leverancier VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
      (s["id"],s["naam"],s["naam_origineel"],s["land"],s["regio"],s["valuta"],s["incoterms"],s["minimale_afname"],s["levertijd"],s["betaalvoorwaarden"],s["certificeringen"],s["adres"],s["website"],s["email"],s["telefoon"],s["export_afdelingen"],s["bron_bestand"],s["bron_pagina"],s["opmerking"],None))
    for o in offers:
        c.execute("INSERT INTO aanbod VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
          (o["id"],o["leverancier_id"],o["vorm"],o["vorm_origineel"],o["legering"],o["dikte_min_mm"],o["dikte_max_mm"],json.dumps(o["dikte_banden_mm"]),
           o["breedte_min_mm"],o["breedte_max_mm"],o["lengte_min_mm"],o["lengte_max_mm"],o["diameter_min_mm"],o["diameter_max_mm"],
           json.dumps(o["binnendiameter_mm"]) if o["binnendiameter_mm"] else None, json.dumps(o["extra"],ensure_ascii=False) if o["extra"] else None,
           o["maatwerk"],o["beschikbaarheid"],o["prijs"],o["prijs_valuta"],o["prijsbasis"],o["minimale_afname"],o["levertijd"],o["norm"],
           o["bron_bestand"],o["bron_pagina"],o["bron_pagina_noot"],o["betrouwbaarheid"]))
        for t in o["tempers"]: c.execute("INSERT INTO aanbod_temper VALUES (?,?)",(o["id"],t))
        for v in o["vlaggen"]: c.execute("INSERT INTO vlag VALUES (NULL,?,?,'open')",(o["id"],v))
    c.commit(); c.close()
    print(len(offers),"aanbodregels")

if __name__ == "__main__": build()
