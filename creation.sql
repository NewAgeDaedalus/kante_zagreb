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

CREATE TABLE kante (
	id INT PRIMARY KEY,
	tip_id INT,
	četvrt_id INT,
	geo_visina  FLOAT CHECK (geo_visina  >=  -90  AND geo_visina  <=  90),
	geo_širina FLOAT CHECK (geo_širina >= -180  AND geo_širina <= 180),
	FOREIGN KEY (tip_id) REFERENCES kante_tip(id),
	FOREIGN KEY (četvrt_id) REFERENCES četvrti(id)
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

INSERT INTO kante_tip(id, ime, prima, privatno) VALUES
(1, 'gradska košara', 'komunalni', false),
(2, 'zeleno zvono', 'staklo', false),
(3, 'plava kocka', 'papir', false),
(4, 'žuta kocka', 'plastika', false);

INSERT INTO kante(id, tip_id, četvrt_id, geo_visina, geo_širina) VALUES
(1, 1,  14, 45.812445738129384, 15.895851429442905),
(2, 2,  14, 45.814827486667080, 15.898359123519928),
(3, 3,  14, 45.814827486667080, 15.898359123519928),
(4, 4,  14, 45.814827486667080, 15.898359123519928),
(5, 1,  14, 45.819771257563694, 15.889821488692705),
(6, 1,  14, 45.815012080822804, 15.89528178771937),
(7, 1,  14, 45.81433340494386, 15.905920576844299),
(8, 1,  14, 45.81344926019273, 15.906074020670552),
(9, 1,  14, 45.81344926019273, 15.906074020670552),
(10, 2, 14, 45.815314573365406, 15.894662206102602);

