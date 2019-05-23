# 2. Instructies bij gebruik van de notebook

Hieronder volgen 10 onvolledige functies (e.g., `query_42(connection, col_names, super_voorbeeldparam = ['joske', 'jef'])`). Aan jullie om ze aan te vullen zodat de functie:  

1. Een corecte query opstelt
2. De query uitvoert op de database
3. Het resultaat teruggeeft in een DataFrame.

Voor stap 2 en 3 zijn de nodige functies al voorhanden, i.e.: `run_query(connection, query)` en `res_to_df(res, column_names)`. Jullie werk zal dus vooral bestaan uit stap 1, queries opstellen. Elke functie heeft minstens 2 inputargumenten:

1. `connection`:   Een connection object 
2. `column_names`: De kolomnamen van het Pandas DataFrame
    
Gevolgd door eventuele extra argumenten (e.g., `super_voorbeeldparam = ['joske','jef']`) die dienen om parameters in te query te injecteren. 

**Nogmaals: verander niets aan de namen van de functies, namen van de functie-argumenten en de kolomnamen van de resulterende DataFrames. Wijzigingen hieraan leiden onvermijdelijk tot een score van 0 op die query.**

Je kan naar believen extra cellen toevoegen om je queries te testen, resultaten te inspecteren etc. We vragen jullie om de finale, ingevulde functies te kopiëren naar een extern script dat enkel en alleen deze oplossingen bevat. Cf. de laatste sectie van deze notebook voor instructies omtrent hoe in te dienen.

## 2.1 Voorbeeld-query opstellen

Om jullie al wat op weg te zetten volgt hier een voorbeeldje over hoe je te werk kan gaan.

**Beschrijving**

Het resultaat van deze functie is een Pandas DataFrame met teamnaam, jaar en aantal homeruns van teams die meer dan een gegeven aantal `homeruns` hadden in dat jaar.

Sorteer aflopend op aantal homeruns.

**Oplossing**

## 2.2 Voorbeeld-query runnen

Om een query te runnen maken we gebruik van de hulpfunctie die we eerder ter beschikking stelden (e.g. `verbind_met_GB`). Concreet bestaat dit proces uit twee stappen:

1. Eerst maken we een verbindingsobject met de databank
2. Vervolgens runnen we onze query, en inspecteren we het resultaat.