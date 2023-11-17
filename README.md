# Reciklažna dvorišta Zagreb

Otvoreni skup podataka za reciklažna dvorišta grada Zagreba. Projekt je stvoren u edukativne svrhe i
podaci su fiktivni.
Laboratorijske vježbe iz kolegija otvorenog računarstva, Fakulteta elektrotehnike i računarstva Zagreb.

Autor: Fabian Penezić\
Verzija: 1.0\
Jezik: hrvatski\
Podaci stvoreni: 15.11.2023.\
Prostor: Grad Zagreb\
Baza podataka: PostgreSQL\
Kolegij: Otvoreno računarsvto 
Fakultet: Fakutlet računarstva i elektrotehnike 


## Uvoz za POSTGRESQL na operacijskom sustavu GNU/LINUX
Stvorite bazu podataka za kante za smeće
```
createdb kante_zagreb
```
Izvršite naredbe u datoteci "creation.sql"
```
psql -d kante_zagreb -a -f creation.sql
```

## Upute za pokretanje lokalne instance
### Instalacija paketa i konfiguracija python venv-a
```
python -m venv kante_zagreb_venv
source kante_zagreb_venv/bin/activate
pip install -r requirements.txt
```
Sljedeće kako bi se poslužitelj mogao spojiti na instancu PostgreSQL baze,
potrebno je definirati u okolišnu varijablu KANTE\_ZAGREB\_USER. Pretpostavka je
da je na Vašem sustavu već ispravno postavljen PostgreSQL.
```
export KANTE_ZAGREB_USER=[ime korisnika koji ime pravo pristupa bazi kante_zagreb]
```
Sad je sve spremno za pokretanje, sljedeća naredba pokreće instancu "kante\_zagreb" na 
0.0.0.0:1234.
```
cd src
python ./main.py export -s 0.0.0.0 -p 1234
```


## Opis skupa podataka

### Entitet reciklažno dvorište
| id | ime | adresa | četvrt | telefonski\_broj | radno\_vrijeme | geo\_širina | geo\_duljina |
|----|---------|------------|-------------|------------|
|    | ime RD-a | adresa RD-a | gradska četvrt u kojoj se nalazi RD | radno vrijeme RD-a | zemljopisna širina RD-a | zemljopisna dužina RD-a | 

### Entitet kante

| id |  id\_dvorišta    |   prima   | 
|----|---------|------------|-------------|
|    | Id reciklažnog dvorišta kojem kanta pripada | tip otpada koje kanta prima (plastika, staklo ...) | 


