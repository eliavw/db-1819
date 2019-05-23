## 1. Inleiding

In deze notebook kan je je oplossingen voor de eerste 3 queries testen. 

- Eerst wordt je script automatisch gerund met verschillende parameters
- De resultaten worden opgeslagen in `.csv` files (in de `out` folder)
- Die `.csv` files worden vergeleken met de `.csv` files van de oplossing (te vinden in de `solution` folder).
- Elke query krijgt een score toegekend. Cf. https://en.wikipedia.org/wiki/F1_score.  
- Een kort rapport wordt weergegeven die je pointers kan geven over wat er mis is met je query. 
    - TP: True Positives
    - TN: True Negatives
    - FP: False Positives
    
Na release van de modeloplossingen kan je natuurlijk alles controleren.
    
## 2. Uitvoeren

Dit proces bestaat uit 3 stappen.

1. Eerst dien je terug verbinding te maken met de gegevensbank.
2. Dan dien je de filename van je ingevulde script in te vullen. Je "ingevulde script" is het bestand dat **ALLE INGEVULDE FUNCTIES EN NIETS ANDERS** bevat. Hieronder importeren we het script `example.py` van in de `scripts` folder.
3. Run het script. Dit doen we met behulp van de `run_external_script` functie die we eerder importeerden. (De parameters en de kolomnamen worden automatisch ingelezen uit de `.json` files in de `solution` folder.)
    
    
## 3. Evaluatie

Het externe script is nu uitgevoerd met de door ons vastgelegde parameters. Op die manier zijn er `.csv` files gemaakt in de `out` directory.

Die `.csv` files worden nu vergeleken met door ons aangemaakte `.csv` files van de correcte oplossingen. Op die manier wordt de score berekend. Alleen de eerste 3 queries kan je nu al controleren.

## 4. Reports

Om te kijken wat je score was, cf. de `out` folder:
   - in `out/reports` vind je gegeneerde reports. Het `execution_report` is een log van het uitvoeren van je script. Het `evaluation_report` is een kleine samenvatting van je behaalde scores.
   - in `out/results` vind je de `.csv` files die je queries geproduceerd hebben.


        