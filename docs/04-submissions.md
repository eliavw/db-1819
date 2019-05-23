## 4. Hoe en wat in te dienen?

Nu je alle queries ingevuld (en hopelijk getest), ben je klaar om je taak in te dienen.

1. **Maak een leeg bestand** aan, en geef het de bestandsnaam met formaat: `dd_X_groep_YY.py`.
    - `dd` verwijst naar de dag van je oefenzitting, e.g. `wo` voor woensdag
    - `X`  is een integer die verwijst naar de volgnummer van je oefenzitting op die dag, e.g. `1`
    - `YY` zijn twee integers die verwijzen naar de volgnummer van je groepje, e.g.: `03`
    -  Een goede bestandsnaam is dus bijvoorbeeld: `wo_1_groep_03.py`


2. Kopieer **ALLE INGEVULDE FUNCTIES EN NIETS ANDERS** naar dit bestand. Het bevat dus _enkel en alleen_ de functies:
    - query_01(connection, column_names)
    - query_02(connection, column_names, datum_x='1980-01-16')
    - etc, etc


3. **TIP**: voor de eerste 3 queries kan je je oplossing zelfs testen via de `verification.ipynb` notebook!
    - Eerst wordt je script automatisch gerund met verschillende parameters
    - De resultaten worden opgeslagen in `.csv` files (in de `out` folder)
    - Die `.csv` files worden vergeleken met de `.csv` files van de oplossing (te vinden in de `solution` folder).
    - Elke query krijgt een score toegekend. Cf. https://en.wikipedia.org/wiki/F1_score.  
    - Al dan niet sorteren is verantwoordelijk voor 10% van je score.
    - Een kort rapport wordt weergegeven die je hints kan geven over wat er mis is met je query. 
        - TP: True Positives
        - TN: True Negatives
        - FP: False Positives
        

4. Als je oplossing definitief is, submit je je `dd_X_groep_YY.py` via Toledo.     


5. Nogmaals, als finale submissie verwachten we een python bestand (e.g., `wo_1_groep_03.py`) dat jullie ingevulde functies bevat en niks anders. De ingevulde notebook is niet acceptabel.