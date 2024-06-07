
class InputsConfig:

    model = 2

    ''' Input configurations for Bitcoin model '''
    if model == 1:
        ''' Block Parameters '''
        Binterval = 600 # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0  # The block size in MB
        Bdelay = 1  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 6.5  # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Full"  # Full/Light to specify the way of modelling transactions
        Tn = (1/(3600*24))*48 # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 1
        Tfee = 0.000062  # The average transaction fee
        Tsize = 1  # The average transaction size  in MB

        ''' Node Parameters '''
        Nn = 10000 # the total number of nodes in the network
        NODES = []
        from Models.Bitcoin.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        for i in range(Nn):
            NODES.append(Node(id=i, hashPower=100))

        ''' Simulation Parameters '''
        simTime = 3600*24*92  # the simulation length (in seconds)
        Runs = 1 # Number of simulation runs

    ''' Input configurations for Ethereum model '''
    if model == 2:

        ''' Block Parameters '''
        Binterval = 12.45  # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0  # The block size in MB
        Blimit = 8000000  # The block gas limit
        Bdelay = 1  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 2  # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Full"  # Full/Light to specify the way of modelling transactions
        Tn = (1/(3600*24))*48  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 0.1
        # The transaction fee in Ethereum is calculated as: UsedGas X GasPrice
        Tsize = 1  # The average transaction size  in MB

        ''' Drawing the values for gas related attributes (UsedGas and GasPrice, CPUTime) from fitted distributions '''

        ''' Uncles Parameters '''
        hasUncles = True  # boolean variable to indicate use of uncle mechansim or not
        Buncles = 7  # maximum number of uncle blocks allowed per block
        Ugenerations = 2  # the depth in which an uncle can be included in a block
        Ureward = 0
        UIreward = Breward / 32  # Reward for including an uncle
        ''' Node Parameters '''
        Nn = 10000 # the total number of nodes in the network
        NODES = []
        from Models.Ethereum.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        for i in range(Nn):
            NODES.append(Node(id=i, hashPower=100))

        ''' Simulation Parameters '''
        simTime = 24*3600*92 # the simulation length (in seconds)
        Runs = 1  # Number of simulation runs
