# Rail Network Optimization
De Nederlandse overheid wil het treinverkeer efficiënter en duurzamer maken door het spoornetwerk te optimaliseren. Dit project bevat verschillende algoritmen om de kwaliteit van een spoornetwerk te evalueren en te verbeteren. De resultaten omvatten onder andere de kwaliteitsscore van de oplossing en de gegenereerde treinroutes.


## Aan de slag

**Vereisten**

Deze codebase is volledig geschreven in Python 3.10.12. De vereiste Python-packages zijn opgesomd in requirements.txt. Installeer ze eenvoudig met:

```
pip install -r requirements.txt
``` 

Of, indien je Conda gebruikt:

```
conda install --file requirements.txt
```

### Gebruik

De main.py-module kan worden uitgevoerd vanuit de commandoregel. Gebruik --help voor een overzicht van alle beschikbare opties.

```
python3 main.py --help
```

**Commandoregelopties:**
 
--algorithm: Specificeert welk algoritme moet worden uitgevoerd. 

Kies uit:
- random, greedy, beam_greedy, beam_greedy_random, beam_heuristics_random, hill_climber, a_star, dijkstra.
- Standaard: random

--iterations: Het aantal iteraties voor het RandomAlgorithm. Standaard: 1000.

--dataset: Selecteert de dataset:
- holland (voor Nederland)
- national (voor landelijke datasets)
- Standaard: holland.

**Voorbeelden**

Voer alle algoritmen uit op de Holland-dataset:

```
python3 main.py --algorithm all --dataset holland
```

Voer het Random Algorithm uit op de nationale dataset met 5000 iteraties:
```
python3 main.py --algorithm random --dataset national --iterations 5000
``` 

Voer het beam_greedy_random-algoritme uit:

```
python3 main.py --algorithm beam_greedy_random --dataset holland
```

**Verwachte Output**

Bij het uitvoeren van een algoritme wordt de volgende informatie weergegeven:

- Kwaliteit van de oplossing: Een evaluatie van de efficiëntie van het gevonden spoornetwerk.

- Routes: Een lijst van de gegenereerde treinroutes.

- Visualisatie: Een interactieve kaart van Nederland waarop alle Routes duidelijk worden weergegeven, elk in een eigen kleur.

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- /code: bevat alle code van dit project
- /code/algorithms: bevat de code voor algoritmes
- /code/classes: bevat de zes benodigde classes voor deze case
- /code/visualisation: bevat de code voor de visualisatie
- /data: Bevat de benodigde databestanden voor het genereren van routes en het creëren van visualisaties.

## Auteurs 

- Sophie Kaandorp
- Sean Park
- Nisrine Sajri 