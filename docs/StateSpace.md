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
        - n is het maximaal route lengte op dat moment

    - Dit helpt ons mogelijke route lengtes te genereren die passen binnen het tijdsframe.

2. **Beperkingen**:
    - De maximale totale reistijd mag de opgegeven limiet niet overschrijden (dus niet meer dan 2 (of 3) uur in totaal).

## De berekening van de State Space 
$P(n) = N \times (B-1)^{n-1}$
- N = number of start stations (dus 22 bij Holland en 61 bij nationaal)
- B = average branching factor is het totaal verbindingen delen door het totaal stations (dus bij Holland is dat $\frac{28}{22}$ en bij Nationaal is dat $\frac{89}{61}$)

r = $\sum_{k=2}^{24} P(k)$ ; total single route possibilities (dus Bij holland is dat $\frac{120}{5} = 24$ en bij Nationaal is dat $\frac{180}{5}$)
  
Totaal = $\sum_{i=1}^{7} r^{i}$ (bij Holland is dat 7 en Nationaal is dat 20)


Holland:
- $\sum_{i=1}^{7} (\sum_{k=2}^{24} 22 \times (0.27)^{n-1})^{i}$ = 9.1 $\times 10^{8}$

Nationaal: 
- $\sum_{i=1}^{20} (\sum_{k=2}^{36} 61 \times (0.46)^{n-1})^{i}$ = 1.6 $\times 10^{35}$