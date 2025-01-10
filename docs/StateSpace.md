## Belangrijke parameters
1. **Stations en verbindingen**:
    - We hebben 118 treinstations, met 22 belangrijke intercitystations en de reistijden tussen de stations in minuten.
    - Het doel is een netwerk van routes (trajecten) te creëren die alle verbindingen tussen deze stations volledig dekt.

2. **Route lengte**:
    - Elke route heeft een lengte *(n)*, wat het aantal overstappen tussen stations vertegenwoordigt.
    - Het tijdsframe voor elke route mag niet meer dan 2 uur (120 minuten) bedragen voor Holland en 3 uur (180 minuten) voor Nederland.

3. **Lijnvoering**:
    - De dienstregeling moet zo worden opgesteld dat elke verbinding wordt bediend door ten minste één route.
    - Het maximale aantal routes is 7 voor Holland en 20 voor Nederland.

4. **Doelfunctie (kwaliteit van de lijnvoering)**:
    - De kwaliteit *K* van de lijnvoering wordt gegeven door:
    $K = p \times 10000 - (T \times 100 + Min)$
    waarbij:
    - *p* is de fractie is van de verbindingen die door de routes worden gedekt (tussen 0 en 1).
    - *T* is het aantal routes (trajecten) is.
    - *Min* is de totale tijd is over alle routes (in minuten).

5. **Optimalisatie**:
    - We maximaliseren *(K)* door routes te kiezen die alle verbindingen dekken, terwijl we het aantal routes *(T)* en de totale reistijd *(Min)* minimaliseert.

## Het formuleren van de State space:

$P(n) = N \times (B-1)^{n-1}$
- N = number of stations
- B = average branching factor
- n = route length
r = $\sum_{k=2}^{24} P(k)$ ; total single route possibilities

Full network:  
- Totaal = $\sum_{i=1}^{7} r^{i}$

1. **State space**: 
    - De state space bestaat uit verschillende combinaties van routes *(n)* zodat:
        - Elke route een subset van de verbindingen dekt.
        - De totale reistijd voor elke route binnen het gegeven tijdsframe van 120 (of 180) minuten ligt.
        - Het totale aantal routes niet meer dan 7 (of 20) is.
        
    - De functie $P(n) = N \times (B-1)^{n-1}$ kan worden geïnterpreteerd als het aantal manieren waarop een route van lengte *(n)* kan worden gevormd, waarbij:
        - N is het aantal stations in de huidige route is.
        - B is de gemiddelde vertakfactor, wat het aantal mogelijke verbindingen vanaf elk station vertegenwoordigt.
        - n is het aantal overstappen in de route is.

    - Dit helpt ons mogelijke route lengtes te genereren die passen binnen het tijdsframe.

2. **Beperkingen**:
    - Elke route moet een set van verbindingen tussen de stations dekken.
    - De maximale totale reistijd over alle routes moet worden geminimaliseerd en mag de opgegeven limiet niet overschrijden (dus niet meer dan 2 (of 3) uur in totaal).
    - Het aantal trajecten *(T)* moet zo klein mogelijk zijn, terwijl nog steeds alle verbindingen gedekt worden.

3. **Doelstelling**:
    - Het doel is een combinatie van trajecten te vinden die K maximaliseert, wat inhoudt dat we de fractie *(p)* (de fractie van gedekte verbindingen) maximaliseren, terwijl we *(T)* en *(Min)* minimaliseren.
