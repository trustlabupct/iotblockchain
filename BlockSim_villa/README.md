# BlockSim Simultor

## What is BlockSim Simulator?
**BlockSim** is an open source blockchain simulator, capturing network, consensus and incentives layers of blockchain systems. BlockSim aims to provide simulation constructs that are intuitive, hide unnecessary detail and can be easily manipulated to be applied to a large set of blockchains design and deployment questions (related to performance, reliability, security or other properties of interest). At the core of BlockSim is a Base Model, which contains a number of functional blocks (e.g., blocks, transactions and nodes) common across blockchains, that can be extended and configured as suited for the system and study of interest. BlockSim is implemented in **Python**.

For more details about BlockSim, we refer to our journal paper that can be freely accessed online https://www.frontiersin.org/articles/10.3389/fbloc.2020.00028/full

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

## Contact

For any query about how to use or even extend the simulator, feel free to contact me **alharbi.maher@gmail.com**

Para Bitcoin:

Block: Define el modelo base de un bloque en la blockchain, incluyendo atributos como profundidad, id, id del bloque previo, timestamp, minero, transacciones y tamaño.

BlockCommit: Maneja y ejecuta eventos relacionados con la creación y recepción de bloques, propaga bloques a otros nodos, y actualiza la blockchain local de los nodos.

Consensus: Implementa el protocolo de consenso PoW (Proof of Work) usando una distribución exponencial para modelar el tiempo de minado basado en el poder de hash de cada minero, y resuelve forks en la cadena aplicando la regla de la cadena más larga.

Node: Define un nodo en la red de Bitcoin, asignándole un poder de hash, una blockchain local, un pool de transacciones, un contador de bloques minados y un balance de recompensas acumuladas.

Incentives: Calcula y distribuye las recompensas entre los nodos participantes, basándose en los bloques y las transacciones incluidas en ellos.

Network: Modela la red y define los retrasos en la propagación de bloques y transacciones usando distribuciones exponenciales.

Transaction: Define el modelo de una transacción en la blockchain de Ethereum, incluyendo atributos como id, timestamp, remitente, destinatario, valor, tamaño y tarifa.

LightTransaction: Gestiona un pool compartido de transacciones pendientes y selecciona las transacciones a incluir en los bloques, priorizándolas por tarifas.

FullTransaction: Crea transacciones completas, maneja su propagación entre los nodos y selecciona transacciones a incluir en los bloques basándose en su tarifa y tamaño.