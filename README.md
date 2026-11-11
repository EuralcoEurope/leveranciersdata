# Leveranciersdata Euralco

Aluminiumleveranciers uit boekjes (foto's) naar een database voor het ERP.

- `schema.sql` – tabellen: leverancier, aanbod (leverancier × vorm × legering), aanbod_temper, vlag
- `data/yoto.json` / `data/yoto_aanbod.csv` – ingelezen data per leverancier
- `data/leveranciers.sqlite` – alles samen (gebouwd met `python3 tools/build.py`)
- `bronnen/<leverancier>/` – de foto's (verkleind tot 1800 px), bestandsnaam staat bij elk record als bron

## Regels
- NULL/leeg = niet in het boekje. Er wordt niets aangevuld of geschat.
- Elk aanbodrecord heeft `bron_bestand` + `bron_pagina`, en vlaggen voor wat onzeker is.
- Prijzen (later): alleen als indicatie met valuta en brondatum.

## Status
| Leverancier | Land | Foto's | Records | Gecontroleerd door Loek |
|---|---|---|---|---|
| Henan YongTong (YOTO) | CN | 9 | 81 | nee |
