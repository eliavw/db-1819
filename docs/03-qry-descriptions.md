## 3.1 Query 01

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe met: de teamnaam, het jaar, en het aantal homeruns per team, en dit voor alle teams.

Sorteer op aantal homeruns van hoog naar laag.


## 3.2 Query 02

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe met: de voornaam, achternaam, geboortejaar, geboortemaand, geboortedag van spelers die hun eerste major league appearance maakten na een gegeven *`datum_x`*. 

Sorteer alfabetisch oplopend op achternaam.


## 3.3 Query 03

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat, per club: de clubnaam en de voor- en achternaam van alle managers weergeeft, die ooit voor de club gewerkt hebben als niet-playermanager. Per club mag een welbepaalde manager slechts 1 keer in het resultaat voorkomen. 

Sorteer alfabetisch oplopend op clubnaam.


## 3.4 Query 04

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat alle teams bevat die in `league_l` gespeeld hebben in een jaar na `jaar_y` maar niet in die league gespeeld hebben vroeger dan `jaar_x` (excl. `jaar_y` and `jaar_x`).

Het resultaat bestaat uit uit teamID, naam, jaar en wins en losses in dat jaar.

Sorteer oplopend op teamID en dan oplopend op yearID.


## 3.5 Query 05

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat alle personen bevat die zowel een speler als een manager prijs hebben gewonnen. Van deze personen zijn we geïnteresseerd in: de ID, de nameGiven en het aantal spelersprijzen. 

Sorteer aflopend op het aantal gewonnen spelersprijzen en dan aflopend op spelerIDs.


## 3.6 Query 06

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat alle unieke personen bevat die in 3 opeenvolgende jaren een spelersprijs hebben gewonnen. Van deze personen willen we de playerID.

Sorteer oplopend op playerID.


## 3.7 Query 07

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat alle personen bevat die een spelersprijs gewonnen hebben in `jaar_y` terwijl ze speelden voor een team gemanaged, in dat jaar, door team manager `manager_x`. Van deze personen willen we de playerID, voornaam en achternaam.

Sorteer oplopend op playerID.


## 3.8 Query 08

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat alle personen bevat wiens gemiddelde loon hoger is dan het gemiddelde loon over alle spelers en jaren. Van deze personen willen we de ID, voornaam en achternaam.

Sorteer oplopend op playerID.


## 3.9 Query 09

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat voor alle teams: hun team ID, naam, beste jaar en het aantal wins in dat jaar bevat.

Het _beste jaar_ voor een team wordt hier gedefinieerd als het jaar met het hoogste aantal wins. In het geval van jaren met hetzelfde aantal wins is het meest recente jaar het beste jaar. 

Sorteer aflopend op aantal wins en dan aflopend op teamID.


## 3.10 Query 10

**Beschrijving**

Het resultaat van deze functie is een Pandas dataframe dat alle teams bevat waar in jaar `jaar_y` geen speler van dat team een award heeft gewonnen.

Een speler speelt voor een team wanneer deze betaald wordt door dat team. Voor elk van die teams bevat het resultaat de teamID en naam.

Sorteer oplopend op teamID.