# KANTE ZAGREB

Otvoreni skup podataka za kante za smeće u Zagrebu.
Laboratorijske vježbe iz kolegija otvorenog računarstva, Fakulteta elektrotehnike i računarstva Zagreb.

Autor: Fabian Penezić\
Verzija: 1.0\
Jezik: hrvatski\
Podaci stvoreni: 30.10.2023.\
Prostor: Grad Zagreb\
Baza podataka: PostgreSQL

## Uvoz za POSTGRESQL na operacijskom sustavu GNU/LINUX
Stvorite bazu podataka za kante za smeće
```
createdb kante_zagreb
```
Izvršite naredbe u datoteci "creation.sql"
```
psql -d kante_zagreb -a -f creation.sql
```

## Opis skupa podataka

### Entitet kante
| id | tip\_id | četvrt\_id | geo\_visina | geo_širina |
|----|---------|------------|-------------|------------|
|    |ključ na tip kante za smeće | ključ na četvrti u kojoj se nalazi | geografska visina | geografska širina |

### Entitet tip\_kante

| id |  ime    |   prima    |  privatno   |
|----|---------|------------|-------------|
|    | opisno ime tipa kante | tip smeća koje kanta prima (komunalno, plastika, staklo ...) | privatno=DA ili NE |

### Entitet četvrti
| id |  ime    |  površina |  broj\_stanovnika |
|----|---------|------------|-------------|
|    | ime četvrti| površina izražena u kvadratnim kilometrima | 

