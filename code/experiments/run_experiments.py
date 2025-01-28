#!/usr/bin/env python3
import subprocess
import time
import os
import json
from datetime import datetime

def run_algorithm_experiments(algorithm_name: str, dataset: str, total_time: int = 3600, run_time: int = 60):
    """
    Voer een algoritme uit voor een bepaalde totale tijd, met elke run beperkt tot run_time seconden.
    
    Args:
        algorithm_name: Naam van het algoritme om uit te voeren
        dataset: Dataset om te gebruiken ('holland' of 'national')
        total_time: Totale tijd om experimenten uit te voeren (standaard: 1 uur)
        run_time: Tijdslimiet voor elke individuele run (standaard: 60 seconden)
    """
    # Verkrijg paden relatief aan dit script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    main_script = os.path.join(project_root, "main.py")
    results_dir = os.path.join(current_dir, 'results', algorithm_name)
    
    # Maak results directory aan als deze nog niet bestaat
    os.makedirs(results_dir, exist_ok=True)
    
    # Maak output bestandsnaam met timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(results_dir, f'{dataset}_{timestamp}.json')
    
    start = time.time()
    n_runs = 0
    results = []
    
    print(f"Start experimenten voor {algorithm_name} op {dataset} dataset")
    print(f"Resultaten worden opgeslagen in: {output_file}")
    
    while time.time() - start < total_time:
        print(f"Run: {n_runs + 1}")
        
        # Voer het algoritme uit met timeout
        try:
            cmd = ["python3", main_script, "--dataset", dataset, "--algorithm", algorithm_name]
            process = subprocess.run(cmd, 
                                  timeout=run_time, 
                                  capture_output=True, 
                                  text=True)
            
            # Extraheer kwaliteitsscore uit output
            # Gaat ervan uit dat de output een regel bevat zoals "Quality Score (K): 6449.00"
            for line in process.stdout.split('\n'):
                if "Quality Score (K):" in line:
                    score = float(line.split(":")[1].strip())
                    results.append({
                        'run': n_runs,
                        'score': score,
                        'time': time.time() - start
                    })
                    break
            
        except subprocess.TimeoutExpired:
            print(f"Run {n_runs + 1} is verlopen (timeout)")
            results.append({
                'run': n_runs,
                'score': None,
                'time': time.time() - start,
                'status': 'timeout'
            })
        
        # Sla resultaten op na elke run
        with open(output_file, 'w') as f:
            json.dump({
                'algorithm': algorithm_name,
                'dataset': dataset,
                'total_time': total_time,
                'run_time': run_time,
                'results': results
            }, f, indent=2)
        
        n_runs += 1

if __name__ == "__main__":
    # Lijst van algoritmes om te testen
    algorithms = [
        'random',
        'greedy',
        'beam_greedy',
        'beam_heuristics_random',
        'hill_climber',
        'a_star',
        'dijkstra'
    ]
    
    datasets = ['holland', 'national']
    
    # Voer experimenten uit voor elk algoritme en dataset
    for algorithm in algorithms:
        for dataset in datasets:
            run_algorithm_experiments(algorithm, dataset)