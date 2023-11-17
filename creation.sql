CREATE TYPE OTPAD_ENUM AS ENUM (
	'papir', 'karton', 'plastika', 'metalna ambalaža', 'stiropor',
	'stare baterije', 'stakleni ambalažni otpad', 'ravno staklo',
	'PET - boce', 'PE - folija', 'limenke',
	'stari lijekovi', 'otpadne gume bez naplatka',
	'metalni glomazni otpad (električna i elektronička oprema)',
	'elektronički otpad', 'glomazni otpad',
	'drveni otpad', 'tekstil', 'odjeća',
	'akumulatore', 'fluorescentne cijevi', 'zeleni otpad',
	'otpadna motorna i jestiva ulja', 'kiseline', 'lužine',
	'ambalažu onečišćenu opasnim tvarima'
);

CREATE TYPE ČETVRT_ENUM AS ENUM (
	'Donji grad', 'Gornji grad - Medveščak',
	'Trnje', 'Maksimir', 'Peščenica – Žitnjak', 'Novi Zagreb - istok',
	'Novi Zagreb - zapad', 'Trešnjevka - sjever', 'Trešnjevka - jug',
	'Črnomerec', 'Gornja Dubrava', 'Donja Dubrava',
	'Stenjevec', 'Podsused - Vrapče', 'Podsljeme',
	'Sesvete', 'Brezovica'
);

CREATE TABLE reciklažna_dvorišta (
	id INT PRIMARY KEY,
	ime VARCHAR not NULL,
	adresa VARCHAR not NULL,
	telefonski_broj VARCHAR,
	četvrt ČETVRT_ENUM,
	radno_vrijeme VARCHAR,
	geo_širina  FLOAT CHECK  ( (geo_širina  >=  -90  AND geo_širina  <= 90) OR NULL ),
	geo_dužina FLOAT  CHECK  ( (geo_širina  >= -180  AND geo_širina <= 180) OR NULL )
);

CREATE TABLE kante (
	id INT PRIMARY KEY,
	id_dvorišta INT,
	prima OTPAD_ENUM not NULL,
	FOREIGN KEY (id_dvorišta) REFERENCES reciklažna_dvorišta(id)
);

INSERT INTO reciklažna_dvorišta (id, ime, adresa, telefonski_broj, četvrt, radno_vrijeme, geo_širina, geo_dužina) VALUES
(
	1, 'RD PODSUSED-VRAPČE', 'Kovinska 8a', '0998022161', 'Podsused - Vrapče', 'pon-sub 6:30-20.00;ned 08:00-14:00',
	45.81035819927017, 15.853001480286329
),
(
	2, 'RD ŽITNJAK', 'Čulinečka cesta 275', '0912678061', 'Peščenica – Žitnjak', 'pon-sub 6:30-20.00',
	45.795238918491314, 16.079816696725796
),
(
	3, 'RD TREŠNJEVKA SJEVER', 'Zagorska br. 3', '0912678117', 'Novi Zagreb - istok', 'pon-sub 6:30-20.00',
	45.80803899507244, 15.94719390622892
),
(
	4, 'RD ŠPANSKO,', 'D.Cesarića 2a', '0912678118', 'Stenjevec', 'pon-sub 6:30-20.00',
	45.80301908528808, 15.906203396726143
),
(
	5, 'RD SESVETE JELKOVEC', 'Ulica Borisa Ulricha 5', '0998036772', 'Sesvete', 'pon-sub 6:30-20.00;ned 8:00-16:00',
	45.812281535349754, 16.115370028949076	
),
(
	6, 'RD SESVETE', 'Jelkovečka bb', '0993118457', 'Sesvete', 'pon-sub 6:30-20.00',
	45.820402025029345, 16.11480686789116
),
(
	7, 'RD PRILESJE', 'Prilesje 1c', '0998022158', 'Maksimir', 'pon-sub 6:30-20.00',
	45.824554759035045, 16.013712640789787
),
(
	8, 'RD KLARA', 'Sisačka cesta br. 10', '0992633091', 'Novi Zagreb - zapad', 'pon-sub 6:30-20.00;ned 8:00-16:00',
	45.7541394572736, 15.956226175817887
),
(
	9, 'RD KAJZERICA', 'Žarka Dolinara br.5', '0998022159', 'Novi Zagreb - zapad', 'pon-sub 6:30-20.00',
	45.7804750245322, 15.964410396725041
),
(
	10, 'RD JAKUŠEVEC,', 'Sajmišna cesta bb', '098272762', 'Novi Zagreb - istok', 'pon-sub 6:30-20.00',
	45.76846811168185, 16.024057404239304
);

INSERT INTO kante (id, id_dvorišta, prima) VALUES
-- Spremnici za RD PODSUSED-VRAPČE
(1, 1, 'papir'),
(2, 1, 'papir'),
(3, 1, 'karton'),
(4, 1, 'ravno staklo'),
(5, 1, 'ravno staklo'),
(6, 1, 'plastika'),
(7, 1, 'stare baterije'),
-- Spremnici za RD ŽITNJAK
(8, 2, 'papir'),
(9, 2, 'karton'),
(10, 2, 'ravno staklo'),
(11, 2, 'ravno staklo'),
(12, 2, 'plastika'),
(13, 2, 'stare baterije'),
(14, 2, 'PET - boce'),
(15, 2, 'tekstil'),
(16, 2, 'zeleni otpad'),
-- Spremnici za RD TREŠNJEVKA SJEVER
(17, 3, 'papir'),
(18, 3, 'ravno staklo'),
(19, 3, 'limenke'),
(20, 3, 'glomazni otpad'),
(21, 3, 'glomazni otpad'),
(22, 3, 'elektronički otpad'),
-- Spremnici za RD RD ŠPANSKO
(23, 4, 'papir'),
(24, 4, 'ravno staklo'),
(25, 4, 'limenke'),
(26, 4, 'glomazni otpad'),
(27, 4, 'plastika'),
(28, 4, 'elektronički otpad'),
-- Spremnici za RD SESVET JELKOVEC
(29, 5, 'papir'),
(30, 5, 'papir'),
(31, 5, 'ravno staklo'),
(32, 5, 'ravno staklo'),
-- Spremnici za RD SESVETE
(33, 6, 'papir'),
(34, 6, 'papir'),
(35, 6, 'plastika'),
(36, 6, 'ravno staklo'),
(37, 6, 'PET - boce'),
-- Spremnici za RD PRILESJE
(38, 7, 'ravno staklo'),
(39, 7, 'ravno staklo'),
(40, 7, 'drveni otpad'),
(41, 7, 'akumulatore'),
(42, 7, 'kiseline'),
(43, 7, 'lužine'),
-- Spremnici za RD KLARA
(44, 8, 'papir'),
(45, 8, 'papir'),
(46, 8, 'ravno staklo'),
(47, 8, 'ravno staklo'),
(48, 8, 'glomazni otpad'),
(49, 8, 'elektronički otpad'),
(50, 8, 'otpadna motorna i jestiva ulja'),
-- Spremnici RD KAJZERICA
(51, 9, 'drveni otpad'),
(52, 9, 'drveni otpad'),
(53, 9, 'papir'),
(54, 9, 'papir'),
(55, 9, 'karton'),
(56, 9, 'karton'),
-- Spremnici za RD JAKUŠEVEC
(57, 10, 'plastika'),
(58, 10, 'plastika'),
(59, 10, 'PET - boce'),
(60, 10, 'PET - boce');
