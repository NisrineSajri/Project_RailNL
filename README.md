# **RailNL**

Voor deze case hebben wij gewerkt aan het ontwerpen van een efficiënt lijnennetwerk voor intercitytreinen in Nederland. Ons doel was om trajecten te creëren die niet alleen zoveel mogelijk verbindingen bedienen, maar ook een zo hoog mogelijke kwaliteitsscore \(K\) behalen: 

$K = p \cdot 10000 - (T \cdot 100 + \text{Min})$

Waarbij:  
- K : de kwaliteit van de lijnvoering,  
- p : de fractie van de bereden verbindingen (tussen 0 en 1),  
- T : het aantal trajecten,  
- Min : het totaal aantal minuten in alle trajecten samen.  

### **Stap 1: Noord- en Zuid-Holland**  
Onze eerste stap was gericht op de provincies Noord- en Zuid-Holland. Dit gebied bevat 22 intercitystations en hun verbindingen, inclusief reistijden. Ons doel was om maximaal 7 trajecten te ontwerpen, waarbij elk traject binnen een tijdsframe van 2 uur moet blijven.

### **Stap 2: Heel Nederland**  
Na het voltooien van de lijnvoering voor Noord- en Zuid-Holland hebben we onze aanpak uitgebreid naar heel Nederland. Dit vergde een grotere schaal en complexiteit: maximaal 20 trajecten, waarbij elk traject binnen een tijdsframe van 3 uur moest blijven. Hier golden dezelfde optimalisatiecriteria, met als doel om zoveel mogelijk verbindingen efficiënt te bedienen en \(K\) te maximaliseren.  

---

### **De gebruikte algoritmes**  

Voor het vinden van de optimale lijnvoering hebben we gebruikgemaakt van verschillende algoritmes, elk met hun eigen aanpak:  

1. **Random**: Een basisaanpak waarbij trajecten willekeurig worden gegenereerd om als startpunt te dienen.  
2. **Greedy**: Een algoritme dat als startstation steeds voor een station kiest met het minst aantal verbindingen.
3. **Beam Greedy**: Een algoritme dat verbindingen selecteert met de meeste ongebruikte stations.
4. **Beam Greedy Random**: Combineert de beam greedy algoritme met willekeurigheid, zodat er meer variatie en robuustheid in de oplossingen ontstaat.  
5. **Beam Heuristics Random**: Het algoritme maakt gebruik van een heuristiek die rekening houdt met de tijd die nodig is om een nieuwe route toe te voegen, het aantal ongebruikte stations en een penalty voor het starten van een nieuw traject.
6. **Hill Climber**: Een iteratief optimalisatie-algoritme dat kleine wijzigingen aanbrengt in een willekeurige lijnvoering, waarbij het kan starten vanaf een willekeurig station of de route volledig vervangt. Het proces gaat door zolang de score \(K\) verbetert.
7. **Dijkstra's**: Het algoritme start bij het station met de meeste ongebruikte verbindingen. Vervolgens worden de kortste paden naar alle andere stations berekend, waarbij alleen ongebruikte verbindingen worden meegenomen. Het algoritme kiest het station dat het verst bereikbaar is als eindstation van een traject.
8. **Dijkstra's Heuristic**: Een algoritme dat een uitbreiding is op Dijkstra's algoritme. Dit algoritme kiest, in tegenstelling tot Dijkstra's algoritme, als start station het station met de minste verbindingen. Ook worden routes gecombineerd als dit mogelijk is. Hierbij geldt dan dat de verbinding van het laatste station van traject 1 naar het eerste station van traject 2 moet bestaan (om traject 1 en traject 2 te kunnen combineren). 

## Aan de slag
**Handleiding voor het gebruik van de main-functie**

Main.py is ontworpen om een rail netwerk optimalisatie uit te voeren, waarbij je verschillende algoritmes kunt kiezen om routes in een netwerk te vinden. Het script maakt gebruik van de command line om opties door te geven. Hieronder leggen we stap voor stap uit hoe je het script kunt gebruiken.

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

De main.py-module kan worden uitgevoerd vanuit de commandoregel. Gebruik "run --help" voor een overzicht van alle beschikbare opties.

```
python3 main.py run --help
```

**Commandoregelopties:**

Het script heeft drie hoofdmodi:

**run** – Voert een enkel algoritme uit.

- --algorithm: Kies het algoritme dat je wilt gebruiken. 
    - Er zijn verschillende opties:
        - random, greedy, beam_greedy, beam_greedy_random, beam_heuristics_random, hill_climber, dijkstra_heuristic, dijkstra
        - Standaard wordt het random algoritme gekozen.
- --dataset: Kies de dataset die je wilt gebruiken: holland of national.
    - Standaard wordt holland gekozen.
- --iterations: Stel het aantal iteraties in dat het algoritme moet doorlopen.
    - Standaard is dit 1000 iteraties.

**experiment** – Voert experimenten uit met verschillende algoritmes en datasets.

- --algorithm: Kies het algoritme dat je wilt gebruiken. 
    - Er zijn verschillende opties:
        - random, greedy, beam_greedy, beam_greedy_random, beam_heuristics_random, hill_climber, dijkstra_heuristic, dijkstra, all
        - Standaard wordt all uitgekozen
- --dataset: Kies de dataset die je wilt gebruiken: holland, national, both.
    - Standaard wordt both gekozen.
- --total-time: Stel de totale tijd (in seconden) in die voor de experimenten beschikbaar is.
    - Standaard wordt 3600 seconden gekozen.
- --run-time: Stel de tijdslimiet (in seconden) in voor elke run van het experiment.
    - Standaard wordt 60 seconden gekozen.

**analyze** – Analyseert de resultaten van uitgevoerde experimenten.
- Je hebt geen extra argumenten nodig, gewoon deze modus kiezen en het script zal de resultaten automatisch analyseren en visualiseren.


### **Voorbeelden**

Voer het Random algoritme uit op de nationale dataset met 5000 iteraties:
```
python3 main.py run --algorithm random --dataset national --iterations 5000
``` 
Experimenten uitvoeren met alle algoritmes en beide datasets met een totale tijd van 7200 seconden en een tijdslimiet van 120 seconden voor elke run:
```
python3 main.py experiment --algorithm all --dataset both --total-time 7200 --run-time 120

```
Resultaten van experimenten analyseren:

```
python3 main.py analyze
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
- /code/experiments: bevat experimenten van diverse algoritmen
- /code/experiments/results: bevat de visualisaties van de experimenten
- /code/tests: bevat de testen om de classes te testen
- /data: Bevat de benodigde databestanden voor het genereren van routes en het creëren van visualisaties
- /docs: bevat de documenten die we hebben geschreven in dit project
- /visualization: bevat de code voor de visualisatie en de png-bestanden

## Auteurs 

- Sophie Kaandorp
- Sean Park
- Nisrine Sajri 