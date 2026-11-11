-- Leveranciersdatabase Euralco. Alle velden behalve id/naam/bron zijn optioneel: NULL = "niet in het boekje" (niet: nul of onbekend-aangevuld).
CREATE TABLE leverancier (
  id TEXT PRIMARY KEY, naam TEXT NOT NULL, naam_origineel TEXT,
  land TEXT, regio TEXT, valuta TEXT, incoterms TEXT, minimale_afname TEXT, levertijd TEXT, betaalvoorwaarden TEXT, certificeringen TEXT,
  adres TEXT, website TEXT, email TEXT, telefoon TEXT, export_afdelingen TEXT,
  bron_bestand TEXT NOT NULL, bron_pagina TEXT, opmerking TEXT, ervaring_euralco TEXT   -- ervaring_euralco: door Loek in te vullen
);
CREATE TABLE aanbod (        -- één regel per leverancier x productvorm x legering
  id TEXT PRIMARY KEY, leverancier_id TEXT NOT NULL REFERENCES leverancier(id),
  vorm TEXT NOT NULL,         -- plaat, traanplaat, coil, band, cirkel, gecoat_coil, gebosseleerde_coil, folie (later: profiel, buis, staaf)
  vorm_origineel TEXT, legering TEXT NOT NULL,
  dikte_min_mm REAL, dikte_max_mm REAL, dikte_banden_json TEXT,
  breedte_min_mm REAL, breedte_max_mm REAL, lengte_min_mm REAL, lengte_max_mm REAL, diameter_min_mm REAL, diameter_max_mm REAL,
  binnendiameter_json TEXT, extra_json TEXT,
  maatwerk TEXT, beschikbaarheid TEXT,
  prijs REAL, prijs_valuta TEXT, prijsbasis TEXT, minimale_afname TEXT, levertijd TEXT, norm TEXT,
  bron_bestand TEXT NOT NULL, bron_pagina TEXT, bron_pagina_noot TEXT, betrouwbaarheid TEXT
);
CREATE TABLE aanbod_temper (aanbod_id TEXT REFERENCES aanbod(id), temper TEXT, PRIMARY KEY(aanbod_id,temper));
CREATE TABLE vlag (id INTEGER PRIMARY KEY, aanbod_id TEXT REFERENCES aanbod(id), tekst TEXT NOT NULL, status TEXT DEFAULT 'open');
