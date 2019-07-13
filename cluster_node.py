# importing libraries

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import random
import itertools
import statistics

"""
    This program implements the two-layer clustering in VANETs. The user provides the number of nodes for simulation,
    the speed of the nodes, the update time after which the plots are updated, and the number of simulations before 
    forming clusters.
    4 layer 1 clusters are formed in the 4 quadrants
    2 layer 2 clusters are formed in the + and - Y axis
    
    All the nodes begin at a random position in a 2D space ranging from -250 m to +250 m in both directions.
    The nodes travel at a constant speed provided by the input in any of the four directions. The nodes randomly keep
    on changing the direction after the clusters are formed.
    
    Each node has attributes:
    unique ID
    current speed vector
    current position vector
    current direction           1:+X, 2:+Y, 3:-X, 4:-Y 
    a list of last 5 speed vectors
    a list of last 5 position vectirs
    a list of last 5 directions
    color:          Represents 1 of the 4 clusters
    marker:         Represents the node status: dot for cluster members, square for cluster heads
    edge colors:    Represents the cluster layer: No edge color for layer 1, layer 2 has blue or red edge colors
"""










speed = 4                                        # user input, constant throughout here
time = 2                                         # user input, constant throughout here, re-plot after every 't' seconds
number_of_nodes = 50                             # user input, constant throughout here
change = 20                                      # random number, when different clusters can be visualised and are not too far away to never interfere
speed_x = speed
speed_y = speed

list_of_clusters = [[], [], [], []]
cluster1 = []
cluster2 = []
cluster3 = []
cluster4 = []
head_list = []
class Node(object):
    """
        Node class:
        the attributes consist of   ID,                                 (Auto assigned, start with 1, auto-increment by 1)
                                    speed vector x component,           (derived from user input)
                                    speed vector y component,           (derived from user input)
                                    speed vector,                       (derived from user input)
                                    last five speed vector,             (list of last five speed vectors)
                                    time taken,                         (user input)
                                    position vector,                    (randomly assigned in range [(-250,250), (-250,250)]
                                    last five position vector,          (list of last five position vectors)
                                    last five x position                (list of last five x position vectors)
                                    last five y position                (list of last five y position vectors)
                                    direction                           (randomly assigned: 1: straight, 2 up, 3 down)
                                    last five directions                (list of last five directions)
                                    color                               (all nodes start with colour blue)
                                    marker                              (all nodes start with '.' and heads are promoted to 's'
                                    edgecolors                          (all nodes start with no edgeg color, heads that form a cluser have the same edge color)
    """
    _ID = 1                                                              # class global ID
    def __init__(self,
                 ID = 0,
                 init_speed_x = speed_x,
                 init_speed_y = speed_y,
                 init_speed = np.array([speed_x, speed_y]),
                 last_five_speed = list([np.array([0.0,0.0]), np.array([0.0,0.0]), np.array([0.0,0.0]), np.array([0.0,0.0]), np.array([0.0,0.0])]),
                 time_taken = time,
                 init_position = np.array([0.0,0.0]),
                 last_five_position = list([np.array([0.0,0.0]), np.array([0.0,0.0]), np.array([0.0,0.0]), np.array([0.0,0.0]), np.array([0.0,0.0])]),
                 last_five_x_position = [0,0,0,0,0],
                 last_five_y_position=[0, 0, 0, 0, 0],
                 direction = 0,
                 last_five_direction = [0,0,0,0,0],
                 color = 'blue',
                 marker = '.',
                 edgecolors = 'none'
                 ):

        self.ID = self._ID; self.__class__._ID += 1

        self.init_speed_x = init_speed_x
        self.init_speed_y = init_speed_y
        self.init_speed = init_speed
        self.last_five_speed = list([self.init_speed, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
                              np.array([0.0, 0.0])])

        self.time_taken = time_taken

        init_x = random.randint(-250, 250)
        init_y = random.randint(-250, 250)
        init_position = np.array([init_x, init_y])
        self.init_position = init_position
        self.last_five_x_position = [0, 0, 0, 0, 0]
        self.last_five_y_position = [0, 0, 0, 0, 0]
        self.last_five_position = list([self.init_position, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
                              np.array([0.0, 0.0])]),

        direction = random.randint(1,4)
        self.direction = direction
        self.last_five_direction = [self.direction,0,0,0,0]

        self.color = str('blue')
        self.marker = str('.')
        self.edgecolors = str('none')

    def update_speed(self, init_speed):
        if self.direction == 1:
            self.init_speed_x = speed
            self.init_speed_y = 0
        if self.direction == 2:
            self.init_speed_x = 0
            self.init_speed_y = speed
        if self.direction == 3:
            self.init_speed_x = 0
            self.init_speed_y = (-1)*speed
        if self.direction == 4:
            self.init_speed_x = (-1)*speed
            self.init_speed_y = 0
        self.init_speed = np.array([self.init_speed_x, self.init_speed_y])
        self.last_five_speed.append(self.init_speed)
        self.last_five_speed.pop(0)

    def update_position(self, init_position):
        self.init_position = self.init_position + self.init_speed*self.time_taken
        self.last_five_position = list(self.last_five_position)
        self.last_five_position.append(self.init_position)
        self.last_five_x_position.append(self.init_position[0])
        self.last_five_y_position.append(self.init_position[1])
        self.last_five_position.pop(0)
        self.last_five_x_position.pop(0)
        self.last_five_y_position.pop(0)

    def update_colors(self, init_position):
        x = self.init_position[0]
        y = self.init_position[1]
        self_x_mean = statistics.mean(self.last_five_x_position)
        self_y_mean = statistics.mean(self.last_five_y_position)


        if self_x_mean >= mean_x and self_y_mean >= mean_y:
            self.color = 'gold'
        if self_x_mean < mean_x and self_y_mean >= mean_y:
            self.color = 'deepskyblue'
        if self_x_mean >= mean_x and self_y_mean < mean_y:
            self.color = 'yellowgreen'
        if self_x_mean < mean_x and self_y_mean < mean_y:
            self.color = 'darksalmon'

    def update_directions(self, direction):
        direction = self.direction
        direction = random.randint(1,4)
        self.direction = direction


"""
    Following function plots the scatter plot for all the nodes 
    function arg: list of nodes with every node having the parameters from the class Node
    re-plots every 5 ms (0.005 s)
    Function to be called after updating speed and position (function in class)  
"""


def plot_positions(list_of_node_parameters):
    for node in range(len(list_of_node_parameters)):
        plt.xlim(-600,600)
        plt.ylim(-600,600)
        x = list_of_node_parameters[node].init_position[0]
        y = list_of_node_parameters[node].init_position[1]
        color = list_of_node_parameters[node].color
        node_marker = list_of_node_parameters[node].marker
        node_edgecolor = list_of_node_parameters[node].edgecolors
        plt.scatter(x, y, c=color, marker=node_marker, edgecolors=node_edgecolor)
    plt.pause(0.005)


def average_fn(z_list):
    z_mean = statistics.mean(z_list)
    return z_mean


def form_clusters(node):
    if node.color == 'gold':
        cluster1.append(node.ID)

    if node.color == 'deepskyblue':
        cluster2.append(node.ID)

    if node.color == 'darksalmon':
        cluster3.append(node.ID)

    if node.color == 'yellowgreen':
        cluster4.append(node.ID)

    list_of_clusters = [cluster1, cluster2, cluster3, cluster4]
    return list_of_clusters



x_pos_cluster = []
y_pos_cluster = []
dir_cluster = []



def elect_head(cluster):
    print(cluster)
    head_id = -1
    lowest_dist = 10**5
    for i in range(len(cluster)):
        node_id = int(cluster[i]-1)                      # node id is actually node index, should probably change original ids
        last_node_x = node_list[node_id].init_position[0]
        last_node_y = node_list[node_id].init_position[1]
        dir_node = node_list[node_id].direction
        x_pos_cluster.append(last_node_x)
        y_pos_cluster.append(last_node_y)
        dir_cluster.append(dir_node)
    x_pos_cluster_avg = statistics.mean(x_pos_cluster)
    y_pos_cluster_avg = statistics.mean(y_pos_cluster)
    dir_cluster_avg = statistics.mean(dir_cluster)
    for i in range(len(cluster)):
        node_id = int(cluster[i]-1)
        x_dev_sq = (statistics.mean(node_list[node_id].last_five_x_position) - x_pos_cluster_avg)**2
        y_dev_sq = (statistics.mean(node_list[node_id].last_five_x_position) - y_pos_cluster_avg)**2
        node_dist = math.sqrt(x_dev_sq + y_dev_sq)
        node_dir_avg = abs(node_list[node_id].direction - dir_cluster_avg)

        if (node_dir_avg*node_dist) <= lowest_dist:
            head_id = node_id+1
            lowest_dist = node_dist*node_dir_avg
        else:
            lowest_dist = lowest_dist
            head_id = head_id
    return head_id


def assign_head(list_of_clusters):
    head1 = elect_head(list_of_clusters[0])
    head2 = elect_head(list_of_clusters[1])
    head3 = elect_head(list_of_clusters[2])
    head4 = elect_head(list_of_clusters[3])
    head_list = [head1, head2, head3, head4]
    if node.ID in head_list:
        node.marker = 's'
    return head_list

node_list = []                                                      # array that contains every node with its parameters

for node in range(number_of_nodes):
    node_ = Node()
    node_list.append(node_)

for j in range(change):                                              # for as many times as we want to update, 13 here
    for i in range(number_of_nodes):                                 # for every node
        node_list[i].update_speed(node_list[i].init_speed)           # update speed
        node_list[i].update_position(node_list[i].init_position)     # update position
    plot_positions(node_list)                                        # call the plot function that replots every 5 ms
    plt.cla()


#################
# clusters are now formed #
############

"""
    Maintain a list of last 5 positions, directions, speed.
    Directions now change randomly
"""

x_pos_list = []
y_pos_list = []

for i in range(number_of_nodes):
    x_pos = node_list[i].init_position[0]
    x_pos_list.append(x_pos)
    y_pos = node_list[i].init_position[1]
    y_pos_list.append(y_pos)


"""
    create a list of clusters, every cluster is a list of node IDs in the cluster
    current clustering parameter: average position
    coloured accordingly
"""



mean_x = average_fn(x_pos_list)
mean_y = average_fn(y_pos_list)
temp = []
for j in range(change):                                              # for as many times as we want to update, 13 here
    for i in range(number_of_nodes):                                 # for every node
        node_ = node_list[i]

    plot_positions(node_list)                                        # call the plot function that replots every 5 ms

    plt.cla()

x_pos_list = []
y_pos_list = []

for j in range(change//change):
    for i in range(number_of_nodes):
        x_pos = node_list[i].init_position[0]
        y_pos = node_list[i].init_position[1]
        node = node_list[i]


        node_list[i].update_speed(node_list[i].init_speed)
        node_list[i].update_position(node_list[i].init_position)
        node_list[i].update_colors(node_list[i].init_position)


        x_pos = node_list[i].init_position[0]
        x_pos_list.append(x_pos)
        y_pos = node_list[i].init_position[1]
        y_pos_list.append(y_pos)
    mean_x = average_fn(x_pos_list)
    mean_y = average_fn(y_pos_list)

    plot_positions(node_list)

    plt.cla()
for i in range(number_of_nodes):
    node = node_list[i]
    VANET_clusters = form_clusters(node_list[i])

print(VANET_clusters)
VANET_heads = assign_head(VANET_clusters)

for j in range(5*change):
    for i in range(number_of_nodes):
        x_pos = node_list[i].init_position[0]
        y_pos = node_list[i].init_position[1]
        node = node_list[i]
        node_list[i].update_directions(node_list[i].direction)

        node_list[i].update_speed(node_list[i].init_speed)
        node_list[i].update_position(node_list[i].init_position)
        if node_list[i].ID not in VANET_heads:
            node_list[i].update_colors(node_list[i].init_position)
            my_clusters = form_clusters(node_list[i])
        else:
            node_list[i].marker = 's'
        x_pos = node_list[i].init_position[0]
        x_pos_list.append(x_pos)
        y_pos = node_list[i].init_position[1]
        y_pos_list.append(y_pos)
    mean_x = average_fn(x_pos_list)
    mean_y = average_fn(y_pos_list)

    plot_positions(node_list)
    plt.cla()



print(VANET_heads)

for j in range(5*change):
    for i in range(number_of_nodes):
        x_pos = node_list[i].init_position[0]
        y_pos = node_list[i].init_position[1]
        node = node_list[i]
        node_list[i].update_directions(node_list[i].direction)

        node_list[i].update_speed(node_list[i].init_speed)
        node_list[i].update_position(node_list[i].init_position)

        if node_list[i].ID not in VANET_heads:
            node_list[i].update_colors(node_list[i].init_position)
        else:
            if statistics.mean(node_list[i].last_five_x_position) > 50:
                node_list[i].edgecolors = 'red'
            else:
                node_list[i].edgecolors = 'blue'
            node_list[i].marker = 's'

        x_pos = node_list[i].init_position[0]
        x_pos_list.append(x_pos)
        y_pos = node_list[i].init_position[1]
        y_pos_list.append(y_pos)
    mean_x = average_fn(x_pos_list)
    mean_y = average_fn(y_pos_list)

    plot_positions(node_list)
    plt.cla()
