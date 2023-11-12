CREATE TYPE TIP_SMECA AS ENUM ('komunalni', 'staklo', 'papir', 'plastika', 'glomazni', 'elektronički otpad');

CREATE TABLE kante_tip (
	id INT PRIMARY KEY,
	ime VARCHAR not NULL,
	prima TIP_SMECA not NULL,
	privatno BOOLEAN
);

CREATE TABLE četvrti (
	id INT PRIMARY KEY,
	ime VARCHAR not NULL,
	površina FLOAT not NULL,
	broj_stanovnika INT not NULL CHECK (broj_stanovnika > 0)
);

CREATE TABLE reciklažna_dvorišta (
	id INT PRIMARY KEY,
	ime VARCHAR not NULL,
	adresa VARCHAR not NULL
);

CREATE TABLE kante (
	id INT PRIMARY KEY,
	tip_id INT,
	četvrt_id INT,
	reciklažno_dvorište_id INT,
	geo_visina  FLOAT CHECK  ( (geo_visina  >=  -90  AND geo_visina  <= 90) OR NULL ),
	geo_širina FLOAT  CHECK  ( (geo_širina  >= -180  AND geo_širina <= 180) OR NULL ),
	FOREIGN KEY (četvrt_id) REFERENCES četvrti(id),
	FOREIGN KEY (tip_id) REFERENCES kante_tip(id),
	FOREIGN KEY (reciklažno_dvorište_id) REFERENCES reciklažna_dvorišta(id)
);

INSERT INTO četvrti (id, ime, površina, broj_stanovnika) VALUES
(1, 'DONJI grad', 3, 37024),
(2, 'Gornji grad – Medveščak', 10, 30962),
(3, 'Trnje', 7, 42282),
(4, 'Maksimir', 14, 48902),
(5, 'Peščenica – Žitnjak', 35, 56487),
(6, 'Novi Zagreb - istok', 17, 59055),
(7, 'Novi Zagreb - zapad', 63, 58103),
(8, 'Trešnjevka - sjever', 6, 55425),
(9, 'Trešnjevka - jug', 10, 66674),
(10, 'Črnomerec', 24, 38546),
(11, 'Gornja Dubrava', 40, 61481),
(12, 'Donja Dubrava', 11, 36363),
(13, 'Stenjevec', 12, 51390),
(14, 'Podsused - Vrapče', 36, 45759),
(15, 'Podsljeme', 60, 19165),
(16, 'Sesvete', 165, 70009),
(17, 'Brezovica', 127, 12.030);

INSERT INTO reciklažna_dvorišta (id, ime, adresa) VALUES
(1, 'RD PODSUSED-VRAPČE', 'Kovinska 8a'),
(2, 'RD ŽITNJAK', 'Čulinečka cesta 275'),
(3, 'RD TREŠNJEVKA SJEVER', 'Zagorska br. 3');


INSERT INTO kante_tip(id, ime, prima, privatno) VALUES
(1, 'gradska košara', 'komunalni', false),
(2, 'zeleno zvono', 'staklo', false),
(3, 'plava kocka', 'papir', false),
(4, 'žuta kocka', 'plastika', false);

INSERT INTO kante(id, tip_id, reciklažno_dvorište_id, geo_visina, geo_širina, četvrt_id) VALUES
(1, 1,  NULL, 45.812445738129384, 15.895851429442905, 14),
(2, 2,  NULL, 45.814827486667080, 15.898359123519928, 14),
(3, 3,  NULL, 45.814827486667080, 15.898359123519928, 14),
(4, 4,  NULL, 45.814827486667080, 15.898359123519928, 14),
(5, 1,  NULL, 45.819771257563694, 15.889821488692705, 14),
(6, 1,  NULL, 45.815012080822804, 15.89528178771937,  14),
(7, 1,  NULL, 45.81433340494386,  15.905920576844299, 14),
(8, 1,  NULL, 45.81344926019273,  15.906074020670552, 14),
(9, 1,  NULL, 45.81344926019273,  15.906074020670552, 14),
(10, 2, NULL, 45.815314573365406, 15.894662206102602, 14),
(11, 1,    1, 45.810364255041925, 15.853034187543082, 14),
(12, 1,    1, 45.810364255041925, 15.853034187543082, 14),
(13, 2,    1, 45.810364255041925, 15.853034187543082, 14),
(14, 2,    1, 45.810364255041925, 15.853034187543082, 14),
(15, 2,    1, 45.810364255041925, 15.853034187543082, 14),
(16, 3,    1, 45.810364255041925, 15.853034187543082, 14),
(17, 3,    1, 45.810364255041925, 15.853034187543082, 14);

