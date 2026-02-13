import sys
import csv
import configparser
import ast
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def update_progress(progress, transaction):

    bar_length = 50
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1
        status = "| Simulation completed...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent:  [{0}] {1}% | Number:  {2} {3}".\
        format( "#"*block + "-"*(bar_length-block), np.round((progress*100),1), transaction, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def create_distance_matrix(no_of_agents, distance):

    m = [[distance] * no_of_agents for i in range(no_of_agents)]
    for i in range(no_of_agents):
        m[i][i] = 0
    return m


def create_random_graph_distances(no_of_agents):

    n = no_of_agents  #number nodes
    m = n  #number edges

    G = nx.gnm_random_graph(n, m)

    while not nx.is_connected(G):
        G = nx.gnm_random_graph(n, m)

    distances = (nx.floyd_warshall_numpy(G)).tolist()

    print("Closeness centrality per agent:  " + str(nx.closeness_centrality(G)))

    # print the random graph
    nx.draw(G, with_labels=True)
    # plt.savefig('agent_graph.png')

    return distances


def common_elements(a, b):

    a_set = set(a)
    b_set = set(b)

    if len(a_set.intersection(b_set)) > 0:
        return list((a_set.intersection(b_set)))
    else:
        return []


def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

def load_file(filename):

    try:
        config = configparser.ConfigParser()
        config.read(filename)
        data = []
        simulation_config_parameters = config['PARAMETERS']

        # Check if all simulation parameters provided
        required = ['no_of_transactions','lambda','no_of_agents',
                    'alpha','latency','distance','tip_selection_algo',
                    'agent_choice','printing']
        if not all(key in simulation_config_parameters.keys() for key in required):
            print("Parameter error! Please provide " + ", ".join(required) + "!")
            sys.exit(1)

        # Load simulation parameters
        _no_of_transactions = int(simulation_config_parameters['no_of_transactions'])
        _lambda             = float(simulation_config_parameters['lambda'])
        _no_of_agents       = int(simulation_config_parameters['no_of_agents'])
        _alpha              = float(simulation_config_parameters['alpha'])
        _latency            = int(simulation_config_parameters['latency'])

        # distance: lista o valor único
        if isinstance(ast.literal_eval(simulation_config_parameters['distance']), list):
            _distance = ast.literal_eval(simulation_config_parameters['distance'])
        else:
            _distance = create_distance_matrix(
                _no_of_agents,
                float(simulation_config_parameters['distance'])
            )

        _tip_selection_algo = simulation_config_parameters['tip_selection_algo']

        # agent_choice: None o lista
        if simulation_config_parameters['agent_choice'] == 'None':
            _agent_choice = list(np.ones(_no_of_agents) / _no_of_agents)
        else:
            _agent_choice = ast.literal_eval(simulation_config_parameters['agent_choice'])

        _printing = config.getboolean('PARAMETERS','printing')

        data.append((
            _no_of_transactions,
            _lambda,
            _no_of_agents,
            _alpha,
            _latency,
            _distance,
            _tip_selection_algo,
            _agent_choice,
            _printing
        ))

        # Load change parameters (paso a paso)
        for section in config.sections():
             # ignoramos la sección base y la de comportamiento
            if section in ('PARAMETERS', 'BEHAVIOR'): 
                continue

            event = config[section]
            if 'step' not in event:
                print("Please provide a 'step' for the parameter change!")
                sys.exit(1)
            step = int(event['step'])

            # distancia
            if 'distance' not in event:
                d = False
            elif isinstance(ast.literal_eval(event['distance']), list):
                d = ast.literal_eval(event['distance'])
            else:
                d = create_distance_matrix(_no_of_agents, float(event['distance']))

            # agent_choice
            if 'agent_choice' not in event:
                ac = False
            elif event['agent_choice'] == 'None':
                ac = list(np.ones(_no_of_agents) / _no_of_agents)
            else:
                ac = ast.literal_eval(event['agent_choice'])
                if round(sum(ac), 3) != 1.0:
                    print(f"Agent choice not summing to 1.0: {sum(ac)}")
                    sys.exit(1)
                if len(ac) != _no_of_agents:
                    print(f"Agent choice length mismatch: {len(ac)} vs {_no_of_agents}")
                    sys.exit(1)

            data.append((step, d, ac))

        # --- NUEVA PARTE: parsear sección BEHAVIOR ---
        beh = {}
        if config.has_section('BEHAVIOR'):
            for k, v in config.items('BEHAVIOR'):
                # lista
                if v.startswith('[') and v.endswith(']'):
                    beh[k] = eval(v)
                # número (entero o float)
                elif v.replace('.','',1).isdigit():
                    beh[k] = float(v) if '.' in v else int(v)
                # texto
                else:
                    beh[k] = v
        # devolvemos también beh en el mismo objeto .config
        data.append(('__BEHAVIOR__', beh))

    except Exception as e:
        print(e)
        sys.exit(1)

    return data


def csv_export(self):

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        #Write genesis
        writer.writerow([0,[]])
        for transaction in self.DG.nodes:
            #Write all other transaction
            if(transaction.arrival_time != 0):
                line = []
                line.append(transaction)
                line.append(list(self.DG.successors(transaction)))
                line.append(transaction.arrival_time)
                line.append(transaction.agent)
                writer.writerow(line)

def parse_time(s: str) -> float:
    """
    Convierte "24h" → 1.0 (días), "48h" → 2.0, "3d" → 3.0
    para que coincida con arrival_time (en días).
    """
    unit = s[-1]
    value = int(s[:-1])
    if unit == 'h':
        return value / 24.0
    elif unit == 'd':
        return float(value)
    else:
        raise ValueError(f"Unidad no soportada: {s}")



#Lo comentado sería para un solo agente
def csv_export2(self, filename='data2.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Transaction ID",
            "Approved Transactions",
            "Arrival Time",
            #"Cumulative Weight",
            #"Exit Probability",
            #"Confirmation Confidence",
            "Agent ID",
            "Cumulative Weight Multi-Agent",
            "Exit Probability Multi-Agent",
            "Confirmation Confidence Multi-Agent"
        ])
        for transaction in self.DG.nodes:
            approved_transactions = list(self.DG.successors(transaction))
            arrival_time = transaction.arrival_time
            #cumulative_weight = getattr(transaction, 'cum_weight', 'N/A')
            #exit_probability = getattr(transaction, 'exit_probability', 'N/A')
            #confirmation_confidence = getattr(transaction, 'confirmation_confidence', 'N/A')
            agent_id = transaction.agent.id if transaction.agent else 'N/A'
            # Assuming you store multi-agent metrics in a dict on the transaction object
            cum_weight_ma = {agent.id: weight for agent, weight in transaction.cum_weight_multiple_agents.items()}
            exit_prob_ma = {agent.id: prob for agent, prob in transaction.exit_probability_multiple_agents.items()}
            conf_conf_ma = {agent.id: conf for agent, conf in transaction.confirmation_confidence_multiple_agents.items()}
            
            writer.writerow([
                transaction.id,
                approved_transactions,
                arrival_time,
                #cumulative_weight,
                #exit_probability,
                #confirmation_confidence,
                agent_id,
                cum_weight_ma,
                exit_prob_ma,
                conf_conf_ma
            ])

def csv_export_single_agent(self, filename='data_single_agent.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Transaction ID",
            "Approved Transactions",
            "Arrival Time",
            "Cumulative Weight",
            "Exit Probability",
            "Confirmation Confidence",
            "Agent ID"
        ])
        for transaction in self.DG.nodes:
            approved_transactions = list(self.DG.successors(transaction))
            arrival_time = transaction.arrival_time
            cumulative_weight = getattr(transaction, 'cum_weight', 'N/A')
            exit_probability = getattr(transaction, 'exit_probability', 'N/A')
            confirmation_confidence = getattr(transaction, 'confirmation_confidence', 'N/A')
            agent_id = transaction.agent.id if transaction.agent else 'N/A'
            
            writer.writerow([
                transaction.id,
                approved_transactions,
                arrival_time,
                cumulative_weight,
                exit_probability,
                confirmation_confidence,
                agent_id
            ])