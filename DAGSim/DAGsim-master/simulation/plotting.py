import pickle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import networkx as nx

def print_info(self):
    # Basic simulation information
    text = f"\nParameters: Transactions = {self.no_of_transactions}, Tip-Selection = {self.tip_selection_algo.upper()}, Lambda = {self.lam}"
    if self.no_of_agents != 1:
        text += f", Distances = {self.distances}"
    if self.tip_selection_algo == "weighted":
        text += f", Alpha = {self.alpha}"
    text += " | Simulation started...\n"
    print(text)


#############################################################################
# PRINTING AND PLOTTING
#############################################################################

def print_graph(self, save_path=None):

    # Positioning and text of labels
    pos = nx.get_node_attributes(self.DG, 'pos')
    lower_pos = {key: (x, y - 0.07) for key, (x, y) in pos.items()}  # For label offset (0.1)

    # Create labels with the confirmation confidence of every transaction (of the issuing agent)
    labels = {
        # transaction: str(str(np.round(transaction.exit_probability_multiple_agents[transaction.agent], 2)) + "  " +
        #                  str(np.round(transaction.confirmation_confidence_multiple_agents[transaction.agent], 2)))
        transaction: str(np.round(transaction.exit_probability_multiple_agents[transaction.agent], 2))
        for transaction in self.DG.nodes if transaction.agent is not None
    }
    # For genesis take agent 0 as default (always same value)
    labels[self.transactions[0]] = str(np.round(self.transactions[0].exit_probability_multiple_agents[self.agents[0]], 2))

    # col = [['r','b'][int(np.round(transaction.confirmation_confidence,1))] for transaction in self.DG.nodes()] #Color change for 100% confidence

    # Coloring of nodes
    tips = self.get_tips()
    for tip in tips:
        self.DG._node[tip]["node_color"] = '#ffdbb8'
        # self.DG._node[tip]["node_color"] = self.agent_tip_colors[int(str(tip.agent))]

    # col = list(nx.get_node_attributes(self.DG, 'node_color').values()) #Didn't work on Linux
    col = []
    for transaction in self.DG:
        col.append(self.DG._node[transaction]["node_color"])

    # Creating figure
    plt.figure(figsize=(14, 7))
    nx.draw_networkx(self.DG, pos, with_labels=True, node_size=100, font_size=5.5, node_color=col)
    # nx.draw_networkx_labels(self.DG, lower_pos, labels=labels, font_size=6)

    # Print title
    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam) + \
            ",  " + r'$d$' + " = " + str(self.distances[1][0])
    if self.tip_selection_algo == "weighted":
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.yticks([])
    plt.title(title)
    # plt.show()
    # Save the graph
    plt.savefig(save_path)

def print_tips_over_time(self, save_path=None):

    plt.figure(figsize=(14, 7))

    # Get no of tips per time
    no_tips = []
    for i in self.record_tips:
        no_tips.append(len(i))

    plt.plot(self.arrival_times, no_tips, label="Tips")

    # Cut off first 250 transactions for mean and best fit
    if self.no_of_transactions >= 250:
        cut_off = 250
    else:
        cut_off = 0

    # Plot mean
    x_mean = [self.arrival_times[cut_off], self.arrival_times[-1]]
    y_mean = [np.mean(no_tips[cut_off:]), np.mean(no_tips[cut_off:])]
    plt.plot(x_mean, y_mean, label="Average Tips", linestyle='--')

    # Plot best fitted line
    plt.plot(np.unique(self.arrival_times[cut_off:]), \
    np.poly1d(np.polyfit(self.arrival_times[cut_off:], no_tips[cut_off:], 1))\
    (np.unique(self.arrival_times[cut_off:])), label="Best Fit Line", linestyle='--')

    # Print title
    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam)
    if self.tip_selection_algo == "weighted":
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tips")
    plt.legend(loc='upper left')
    plt.title(title)
    # plt.show()
    plt.savefig(save_path)

def print_tips_over_time_multiple_agents_with_tangle(self, no_current_transactions, save_path=None):

    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)

    # Get no of tips per time
    for agent in self.agents:
        no_tips = [0]
        for i in agent.record_tips:
            no_tips.append(len(i))
        label = "Tips Agent " + str(agent)
        # plt.subplot(2, 1, int(str(agent))+1)
        plt.plot(self.arrival_times[:no_current_transactions], no_tips[:no_current_transactions], label=label, color=self.agent_colors[int(str(agent))])

        # Cut off first 60% of transactions
        if no_current_transactions >= 500:
            cut_off = int(no_current_transactions * 0.2)
        else:
            cut_off = 0

    # Print title
    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam) + \
            ",  " + r'$d$' + " = " + str(self.distances[1][0])
    if self.tip_selection_algo == "weighted":
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tips")
    plt.legend(loc='upper left')
    plt.title(title)

    plt.subplot(2, 1, 2)

    # Positioning and text of labels
    pos = nx.get_node_attributes(self.DG, 'pos')
    lower_pos = {key: (x, y - 0.1) for key, (x, y) in pos.items()}  # For label offset (0.1)

    # Create labels with the confirmation confidence of every transaction (of the issuing agent)
    labels = {
        transaction: str(str(np.round(transaction.exit_probability_multiple_agents[transaction.agent], 2)) + "  " +
                         str(np.round(transaction.confirmation_confidence_multiple_agents[transaction.agent], 2)))
        for transaction in self.DG.nodes if transaction.agent is not None
    }
    # For genesis take agent 0 as default (always same value)
    labels[self.transactions[0]] = str(np.round(self.transactions[0].exit_probability_multiple_agents[self.agents[0]], 2))

    # Coloring of tips
    tips = self.get_tips()
    for tip in tips:
        self.DG._node[tip]["node_color"] = self.agent_tip_colors[int(str(tip.agent))]

    # Didn't work on Linux
    # col = list(nx.get_node_attributes(self.DG, 'node_color').values())
    col = []
    for transaction in self.DG:
        col.append(self.DG._node[transaction]["node_color"])

    # Creating figure
    nx.draw_networkx(self.DG, pos, with_labels=True, node_size=100, font_size=5.5, node_color=col)
    # nx.draw_networkx_labels(self.DG, lower_pos, labels=labels, font_size=6)

    plt.xlabel("Time (s)")
    plt.yticks([])
    # plt.show()
    plt.savefig(save_path)

def print_tips_over_time_multiple_agents(self, no_current_transactions, save_path=None):

    plt.figure(figsize=(14, 7))

    # Get no of tips per time
    for agent in self.agents:
        no_tips = [0]
        for i in agent.record_tips:
            no_tips.append(len(i))
        label = "Tips Agent " + str(agent)
        plt.plot(self.arrival_times[:no_current_transactions], no_tips[:no_current_transactions], label=label)

        # Cut off first 60% of transactions
        if no_current_transactions >= 500:
            cut_off = int(no_current_transactions * 0.2)
        else:
            cut_off = 0

        # Plot mean
        label = "Average Tips Agent " + str(agent)
        x_mean = [self.arrival_times[cut_off], self.arrival_times[no_current_transactions - 1]]
        y_mean = [np.mean(no_tips[cut_off:no_current_transactions - 1]), np.mean(no_tips[cut_off:no_current_transactions - 1])]
        plt.plot(x_mean, y_mean, label=label, linestyle='--')
        print(np.mean(no_tips))

    # Print title
    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam) + \
            ",  " + r'$d$' + " = " + str(self.distances[1][0])
    if self.tip_selection_algo == "weighted":
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of tips")
    plt.legend(loc='upper left')
    plt.title(title)
    # plt.show()
    plt.savefig(save_path)

def print_attachment_probabilities_alone(self, save_path=None):

    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam) + \
            ",  " + r'$d$' + " = " + str(self.distances[1][0])
    if self.tip_selection_algo == "weighted":
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)

    with open('subtangle_attach_prob.pkl', 'wb') as handle:
        pickle.dump(self.record_attachment_probabilities, handle, protocol=pickle.HIGHEST_PROTOCOL)

    plt.figure(figsize=(14, 7))

    x = np.squeeze([i[0] for i in self.record_attachment_probabilities])
    y = np.squeeze([i[1] for i in self.record_attachment_probabilities])

    plt.plot(x, y, label="Attachment probability sub-Tangle branch")
    plt.ylim(0, 0.7)

    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), label="Best Fit", linestyle='--')

    x_mean = [i for i in x]
    y_mean = [np.mean(y) for i in y]
    print(np.mean(y))
    print(np.std(y))
    plt.plot(x_mean, y_mean, label="Average", linestyle='-')

    plt.xlabel("Transactions")
    plt.ylabel("Probability to attach to sub-Tangle branch")
    plt.legend(loc='upper left')
    plt.title(title)
    plt.tight_layout()
    # plt.show()
    plt.savefig(save_path)

def print_attachment_probabilities_all_agents(self, save_path=None):

    title = "Transactions = " + str(self.no_of_transactions) + \
            ",  " + r'$\lambda$' + " = " + str(self.lam) + \
            ",  " + r'$d$' + " = " + str(self.distances[1][0])
    if self.tip_selection_algo == "weighted":
        title += ",  " + r'$\alpha$' + " = " + str(self.alpha)

    plt.figure(figsize=(20, 10))

    # Attachment probabilities
    plt.subplot(1, 2, 1)

    x = np.squeeze([i[0] for i in self.record_attachment_probabilities])
    y = np.squeeze([i[1] for i in self.record_attachment_probabilities])

    labels = ["Agent " + str(i) for i in range(len(y))]

    plt.plot(x, y)
    plt.xlabel("Transactions")
    plt.ylabel("Probability to attach to sub-Tangle branch")
    plt.legend(labels, loc="upper right", ncol=2)

    # Boxplot
    plt.subplot(1, 2, 2)

    data = []

    for agent in range(self.no_of_agents):
        agent_data = [i[1][agent] for i in self.record_attachment_probabilities]
        data.append(agent_data)

    plt.boxplot(data, 0, '+')
    plt.xlabel("Agents")
    plt.xticks(np.arange(1, self.no_of_agents + 1), np.arange(0, self.no_of_agents))
    plt.suptitle(title)
    plt.tight_layout()
    plt.subplots_adjust(top=0.94)
    # plt.show()
    plt.savefig(save_path)
