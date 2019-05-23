# 1. Inleiding

Cf. het document `prerequisites.pdf` in de `docs` folder. 

## 1.1 Python packages

De import statements (cf. boven) vormen de standaardconfiguratie van python-packages die we gebruiken. _Van deze configuratie afwijken is dan ook op eigen risico, gezien dat betekent dat je ook afwijkt van de configuratie van de computer waarop wij jullie oplossingen runnen._

## 1.2 Interageren met een gegevensbank

Naast de standaard packages, importeren we ook drie zelfgemaakte functies. Deze implementeren functionaliteiten die je vaak zal nodig hebben als je vanuit python queries naar je gegevensbank wil sturen: `verbind_met_GB`, `run_query` en `res_to_df`. Hun source code (en documentatie) bekijken geeft de nodige informatie over hoe ze te gebruiken:
    
    
## 1.3 Kolomnamen en input parameters

We leggen op voorhand reeds de **kolomnamen van de oplossingen**, en de **naam en types van de inputparameters** vast. Hier moet je je dus aan houden en mag je dus niks aan wijzigen.

- Het aantal kolommen (en hun volgorde) van jullie oplossing en de onze moeten exact overeen komen, vandaar dat de kolomnamen hieronder gegeven zijn. Dit komt trouwens van pas bij het opstellen van je queries! 
    
- Dankzij de voorbeeldparameters, die al gegeven zijn in de functiedefinitie e.g.: `query_42(connection, col_names, super_voorbeeldparam = 101)` weten jullie exact welke vorm en type (integer, lijst, etc) de inputparameters moeten hebben. Wijzig zeker niets aan de naam van die parameters (*super_voorbeeldparam* blijft *super_voorbeeldparam*). De default waarden geven op hun beurt dan weer informatie over het type van de inputparameters. Let wel: de (soms onnozele) default waarden zijn _louter ter illustratie_, zorg ervoor dat je query ook met andere waarden dan de defaults werkt!

**Samengevat: oplossingen die deze vorm niet respecteren, zullen crashen op onze machines en resulteren in een score van 0 op die query.**