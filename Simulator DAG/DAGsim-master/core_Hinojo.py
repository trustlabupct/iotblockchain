import os
import shutil
import timeit
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulation.helpers import update_progress, csv_export2, csv_export
from simulation.plotting import print_graph, print_tips_over_time, print_tips_over_time_multiple_agents, print_tips_over_time_multiple_agents_with_tangle, print_attachment_probabilities_all_agents
from simulation.simulation_multi_agent import Multi_Agent_Simulation

# Parámetros de la simulación
nodos_list = [50,100,200,500,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
lambda_list = [1, 4, 24, 48, 1440]   # Tasas de generación de transacciones por día
alpha = 0.5
distance = 1
tip_selection_algo = "weighted"

base_directory = "simulation_results"

# Crear directorio base si no existe
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

for no_of_agents in nodos_list:
    agent_dir = os.path.join(base_directory, str(no_of_agents))
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
    
    for lambda_value in lambda_list:
        lambda_dir = os.path.join(agent_dir, str(lambda_value))
        if not os.path.exists(lambda_dir):
            os.makedirs(lambda_dir)
        
        print(f"Iniciando simulación con {no_of_agents} nodos y tasa de generación de {lambda_value} transacciones por día.")
        start_time = timeit.default_timer()

        # Calculamos el número de transacciones basado en la duración del cultivo, ej. 92 días
        no_of_transactions = lambda_value * 92 #* no_of_agents  # Ajusta según los días del cultivo

        # Crear e iniciar simulación
        simu = Multi_Agent_Simulation(no_of_transactions, lambda_value, no_of_agents, alpha, distance, tip_selection_algo, 1, _printing=True)
        simu.setup()
        simu.run()
        csv_export2(simu)
        csv_export(simu)


        # Generar y guardar gráficos
        print_graph(simu, save_path=os.path.join(lambda_dir, "network_graph.png"))
        print_tips_over_time(simu, save_path=os.path.join(lambda_dir, "tips_over_time.png"))
        print_tips_over_time_multiple_agents(simu, simu.no_of_transactions, save_path=os.path.join(lambda_dir, "tips_over_time_multi.png"))
        print_tips_over_time_multiple_agents_with_tangle(simu, simu.no_of_transactions, save_path=os.path.join(lambda_dir, "tangle_multi.png"))
        print_attachment_probabilities_all_agents(simu, save_path=os.path.join(lambda_dir, "attachment_probabilities.png"))

        # Imprimir tiempo total de la simulación
        total_time = np.round(timeit.default_timer() - start_time, 3)
        print(f"Tiempo total de simulación: {total_time} segundos\n")