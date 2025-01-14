## Belangrijke parameters
1. **Stations en verbindingen**:
    - We hebben 118 treinstations, met 22 belangrijke intercitystations en de reistijden tussen de stations in minuten.
    - Het doel is een netwerk van routes (trajecten) te creëren die alle verbindingen tussen deze stations volledig dekt.

2. **Route lengte**:
    - Elke route heeft een lengte *(n)*, wat het maximaal aantal stations vertegenwoordigt.
    - Het tijdsframe voor elke route mag niet meer dan 2 uur (120 minuten) bedragen voor Holland en 3 uur (180 minuten) voor Nederland.

3. **Lijnvoering**:
    - Het maximale aantal routes is 7 voor Holland en 20 voor Nederland.

## Het formuleren van de State space:

$P(n) = N \times (B-1)^{n-1}$
- N = number of start stations
- B = average branching factor
- n = max route length
r = $\sum_{k=2}^{24} P(k)$ ; total single route possibilities

Full network:  
- Totaal = $\sum_{i=1}^{7} r^{i}$

1. **State space**: 
    - De state space bestaat uit verschillende combinaties van routes zodat:
        - Elke route een subset van de verbindingen dekt.
        - De totale reistijd voor elke route binnen het gegeven tijdsframe van 120 (of 180) minuten ligt.
        - Het totale aantal routes niet meer dan 7 (of 20) is.
        
    - De functie $P(n) = N \times (B-1)^{n-1}$ kan worden geïnterpreteerd als het aantal manieren waarop een route van lengte *(n)* kan worden gevormd, waarbij:
        - N is het aantal begin stations.
        - B is de gemiddelde vertakfactor, wat het aantal mogelijke verbindingen vanaf elk station vertegenwoordigt.
        - n is het maximaal aantal stations in een route.

    - Dit helpt ons mogelijke route lengtes te genereren die passen binnen het tijdsframe.

2. **Beperkingen**:
    - De maximale totale reistijd mag de opgegeven limiet niet overschrijden (dus niet meer dan 2 (of 3) uur in totaal).