# Blockchain Simulators

## General Description
This guide covers two blockchain simulators, **BlockSim** and **DAGSim**, used to simulate different scenarios with blockchain and DAG (Directed Acyclic Graph) technologies. This activity is part of the project R&D&I Laboratory on Cybersecurity, Privacy, and Secure Communications (TRUST Lab) financed by European Union NextGeneration-EU, the Recovery Plan, Transformation and Resilience,through INCIBE.

## BlockSim Simulator

**BlockSim** is an open-source blockchain simulator that captures the network, consensus, and incentive layers of blockchain systems. BlockSim aims to provide simulation constructs that are intuitive, hide unnecessary details, and can be easily manipulated to address a wide range of blockchain design and deployment questions (related to performance, reliability, security, or other properties of interest). At the core of BlockSim is a Base Model, which contains several functional blocks (e.g., blocks, transactions, and nodes) common across blockchains, that can be extended and configured as suited for the system and study of interest. BlockSim is implemented in **Python**.

For more details about BlockSim, you can refer to the paper at the following link: https://www.frontiersin.org/articles/10.3389/fbloc.2020.00028/full 

## Installation and Requirements

Before you can use BlockSim  simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- sklearn 
>pip install sklearn
- xlsxwriter
>pip install xlsxwriter

## Running the simulator

Before you run the simulator, you can access the configuration file *InputsConfig.py* to choose the model of interest (Base Model 0, Bitcoin Model 1 and Ethereum Model 2) and to set up the related parameters.
The parameters include the number of nodes (and their fraction of hash power), the block interval time, the block propagation delays, the block and transaction sizes, the block rewards, the tranaction fees etc.
Each model has a slightly different (or additional) parameters to capture it.

To run the simulator, one needs to trigger the main class *Main.py* either from the command line
> python Main.py

or using any Python editor such as Spyder.

## Statistics and Results

The results of the simulator is printed in an excel file at the end of the simulation. The results include the blockchain ledger, number of blocks mined, number of stale (uncles) blocks and the rewards gained by each miner etc. 


## DAGSim Simulator

**DAGSim** is a simulator used to model different scenarios with DAG technologies. Unlike traditional blockchains, DAGs allow for a more flexible and efficient structure for transaction confirmation.

For more details about DAGSim, you can refer to the paper at the following link: https://eprint.iacr.org/2018/1062.pdf 

## Installation and Requirements

Before you can use DAGSim  simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- networkx
>pip install networkx

## Running the simulator

Before running the simulator, you can configure the desired settings in the core.py or core_multiprocessing.py files, depending on whether you want to run the simulation with a single agent or multiple agents.

To run the simulator, you need to trigger either core.py or core_multiprocessing.py from the command line:

> python core.py

or

> python core_multiprocessing.py

or using any Python editor such as VS Code.

## Statistics and Results

DAGSim provides detailed results on the performance of the DAG network, including the number of confirmed transactions, the confirmation time, and the overall network efficiency.

## Authors and Modifications
Both simulators were developed by their respective original authors. This activity is part of the project R&D&I Laboratory on Cybersecurity, Privacy, and Secure Communications (TRUST Lab) financed by European Union NextGeneration-EU, the Recovery Plan, Transformation and Resilience,through INCIBE.