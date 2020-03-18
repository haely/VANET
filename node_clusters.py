import numpy as np
import math
import matplotlib.pyplot as plt
import random
import statistics
import pylint

choice = str(input("Do you want to go ahead with default scenario settings? Enter Y or N: "))

cluster_list = []
if choice == 'N':
    field_len = input("Enter the side of the field in m: e.g. 700 ")
    time = input("Enter the refresh time for plots in s: e.g. 2 ")
    number_of_nodes = input("Enter the total number of nodes: e.g. 50 ")
    change = input("Enter the refresh time for cluster reassignment in s "
                   "(5:1 cluster:head): e.g. 7 ")
    stay_alive = input("Enter the number of times you want to update the heads: e.g. 10 ")

    field_len = int(field_len)
    time = int(time)
    number_of_nodes = int(number_of_nodes)
    change = int(change)
    stay_alive = int(stay_alive)

elif choice == 'Y':
    field_len = 700
    time = 2
    number_of_nodes = 50
    change = 7  # when different clusters can be visualised and are not too far away to never interfere
    stay_alive = 3

else:
    print("Invalid entry")
    exit()

"""
    This program implements the two-layer clustering in VANETs. The user provides the number of nodes for simulation,
    the speed of the nodes, the update time after which the plots are updated, and the number of simulations before 
    forming clusters.

    All the nodes begin at a random position in a 2D space.
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
    color:          Represents node level
    edge colors:    Represents the cluster level: No edge color for layer 1, layer 2 has blue or red edge colors
"""

mean_x = 0
mean_y = 0
pos_end = field_len
neg_end = -1 * field_len
list_of_clusters = []
head_list = []


class Node(object):
    """
        Node class:
        the attributes consist of   ID,                                 (Auto assigned, starts with 1, auto-incremented)
                                    speed vector x component,           (derived from user input)
                                    speed vector y component,           (derived from user input)
                                    speed vector,                       (derived from user input)
                                    last five speed vector,             (list of last five speed vectors)
                                    time taken,                         (user input)
                                    position vector,                    (randomly assigned in half of the range input
                                    last five position vector,          (list of last five position vectors)
                                    last five x position                (list of last five x position vectors)
                                    last five y position                (list of last five y position vectors)
                                    direction                           (randomly assigned: 1: straight, 2 up, 3 down)
                                    last five directions                (list of last five directions)
                                    color                               (all nodes start with colour blue)
                                    edgecolors                          (all nodes start with no edge color,
                                                                                  super-clusters have the same edge color)
    """
    _ID = 1  # class global ID

    def __init__(self,
                 ID=0,
                 init_speed_x=0,
                 init_speed_y=0,
                 init_speed=np.array([0, 0]),
                 last_five_speed=list(
                     [np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
                      np.array([0.0, 0.0])]),
                 time_taken=time,
                 init_position=np.array([0.0, 0.0]),
                 last_five_position=list(
                     [np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
                      np.array([0.0, 0.0])]),
                 last_five_x_position=[0, 0, 0, 0, 0],
                 last_five_y_position=[0, 0, 0, 0, 0],
                 direction=0,
                 last_five_direction=[0, 0, 0, 0, 0],
                 color='blue',
                 marker='o',
                 edgecolors='none'
                 ):

        self.ID = self._ID;
        self.__class__._ID += 1

        self.init_speed_x = random.randint(8,10)
        self.init_speed_y = random.randint(8,10)
        self.init_speed = np.array([self.init_speed_x, self.init_speed_y])
        self.last_five_speed = list([self.init_speed, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
                                     np.array([0.0, 0.0])])

        self.time_taken = time_taken
        init_x = random.randint(neg_end // 2.5, pos_end // 2.5)
        init_y = random.randint(neg_end // 2.5, pos_end // 2.5)
        init_position = np.array([init_x, init_y])
        self.init_position = init_position
        self.last_five_x_position = [0, 0, 0, 0, 0]
        self.last_five_y_position = [0, 0, 0, 0, 0]
        self.last_five_position = list(
            [self.init_position, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
             np.array([0.0, 0.0])]),

        direction = random.randint(1, 3)
        self.direction = direction
        self.last_five_direction = [self.direction, 0, 0, 0, 0]

        self.color = str('blue')
        self.marker = str('o')
        self.edgecolors = str('none')

    def update_speed(self, init_speed):
        if self.direction == 1:
            self.init_speed_x = self.init_speed_x
            self.init_speed_y = 0
        if self.direction == 2:
            self.init_speed_x = 0
            self.init_speed_y = self.init_speed_y
        if self.direction == 3:
            self.init_speed_x = 0
            self.init_speed_y = (-1) * self.init_speed_y
        if self.direction == 4:
            self.init_speed_x = (-1) * self.init_speed_x
            self.init_speed_y = 0
        self.init_speed = np.array([self.init_speed_x, self.init_speed_y])
        self.last_five_speed.append(self.init_speed)
        self.last_five_speed.pop(0)

    def update_position(self, init_position):
        self.init_position = self.init_position + self.init_speed * self.time_taken
        self.last_five_position = list(self.last_five_position)
        self.last_five_position.append(self.init_position)
        self.last_five_x_position.append(self.init_position[0])
        self.last_five_y_position.append(self.init_position[1])
        self.last_five_position.pop(0)
        self.last_five_x_position.pop(0)
        self.last_five_y_position.pop(0)

    def update_directions(self, direction):
        direction = self.direction
        direction = random.randint(1, 5)
        self.direction = direction


def init_node(total_nodes):
    node_list = []  # array that contains every node with its parameters
    for node in range(total_nodes):
        node_ = Node()
        node_list.append(node_)
    return node_list


# creates 'number_of_nodes' objects and stores in my_nodes list, to be called later
my_nodes = init_node(number_of_nodes)


def plot_positions(list_of_node_parameters):
    for node in range(len(list_of_node_parameters)):
        plt.xlim(neg_end, pos_end)
        plt.ylim(neg_end, pos_end)
        x = list_of_node_parameters[node].init_position[0]
        y = list_of_node_parameters[node].init_position[1]
        color = list_of_node_parameters[node].color
        node_marker = list_of_node_parameters[node].marker
        node_edgecolor = list_of_node_parameters[node].edgecolors
        plt.scatter(x, y, c=color, marker=node_marker, edgecolors=node_edgecolor)
    plt.pause(0.005)
def connect_heads(clusters, heads):
    for cluster in clusters:



def plot_update_for(num_updates, list_of_nodes):
    for j in range(change):  # for as many times as we want to update, 13 here
        for i in range(number_of_nodes):  # for every node
            list_of_nodes[i].update_speed(list_of_nodes[i].init_speed)  # update speed
            list_of_nodes[i].update_position(list_of_nodes[i].init_position)  # update position
        plot_positions(list_of_nodes)  # call the plot function that replots every 5 ms
        plt.cla()


# plots for the inital nodes. all blue
plot_update_for(change, my_nodes)


def node_latest_pos_list(list_of_node_ids, list_of_nodes):  # id_of_node is a list of node ids
    x_pos_list = []
    y_pos_list = []
    pos_list = []
    for i in list_of_node_ids:
        x_pos = list_of_nodes[i - 1].init_position[0]
        x_pos_list.append(x_pos)
        y_pos = list_of_nodes[i - 1].init_position[1]
        y_pos_list.append(y_pos)
    pos_list = [x_pos_list, y_pos_list]
    return pos_list


id_list = []
for i in range(number_of_nodes):
    curr_id = my_nodes[i].ID
    id_list.append(curr_id)


def update_pos_n_plot(list_of_node_ids, list_of_nodes):
    for i in list_of_node_ids:
        node_index = i - 1
        list_of_nodes[node_index].update_speed(list_of_nodes[node_index].init_speed)
        list_of_nodes[node_index].update_position(list_of_nodes[node_index].init_position)
    plot_positions(list_of_nodes)
    plt.cla()


def average_fn(z_list):
    z_mean = statistics.mean(z_list)
    return z_mean


for j in range(change):
    node_positions = node_latest_pos_list(id_list, my_nodes)
    x_pos_list = node_positions[0]
    y_pos_list = node_positions[1]
    mean_x = average_fn(x_pos_list)
    mean_y = average_fn(y_pos_list)
    update_pos_n_plot(id_list, my_nodes)


def elect_head(list_of_nodes):
    head_id = -1
    dist_radius = field_len / 5
    rem_id_list = id_list
    if len(rem_id_list) > 0:
        cluster_list = []
        for i in rem_id_list:
            temp_head_id = i - 1
            head_x = list_of_nodes[temp_head_id].init_position[0]
            head_y = list_of_nodes[temp_head_id].init_position[1]
            i_cluster = []

            for j in rem_id_list:
                mem_x = list_of_nodes[j - 1].init_position[0]
                mem_y = list_of_nodes[j - 1].init_position[1]
                if abs(mem_x - head_x) <= dist_radius and abs(mem_y - head_y) <= dist_radius:
                    rem_id_list.remove(j)
                    i_cluster.append(j)
                else:
                    pass
            # print(i_cluster)
            cluster_list.append(i_cluster)
        head_num_list = []
        for k in range(len(cluster_list)):
            head_num = min(cluster_list[k])
            head_index = head_num - 1
            list_of_nodes[head_index].color = 'red'
            head_num_list.append(head_num)
    else:
        raise ValueError('did not have enough nodes to form clusters')
        exit()
    return head_num_list, cluster_list


# this creates a list of heads called VANET_heads

VANET_heads = elect_head(list_of_nodes=my_nodes)[0]
VANET_clusters = elect_head(list_of_nodes=my_nodes)[1]
print(VANET_heads)
print(VANET_clusters)


# this updates the cluster members but not the cluster heads
def update_cluster_members(list_of_nodes):
    for j in range(5 * change):
        for i in range(number_of_nodes):
            node_list = my_nodes
            x_pos = node_list[i].init_position[0]
            y_pos = node_list[i].init_position[1]
            node = node_list[i]
            node_list[i].update_directions(node_list[i].direction)
            node_list[i].update_speed(node_list[i].init_speed)
            node_list[i].update_position(node_list[i].init_position)
            if node_list[i].ID not in VANET_heads:
                node.marker = str('o')
                node.color = str("blue")
                node_list[i].edgecolors = str('none')
            else:
                node_list[i].color = str("red")
                if statistics.mean(node_list[i].last_five_x_position) > 50:
                    node_list[i].edgecolors = str('gold')
                else:
                    node_list[i].edgecolors = str('green')
                node_list[i].marker = str('o')
            x_pos = node_list[i].init_position[0]
            x_pos_list.append(x_pos)
            y_pos = node_list[i].init_position[1]
            y_pos_list.append(y_pos)
        mean_x = average_fn(x_pos_list)
        mean_y = average_fn(y_pos_list)

        plot_positions(list_of_nodes)
        plt.cla()


for i in range(stay_alive):
    update_cluster_members(list_of_nodes=my_nodes)
    update_cluster_members(list_of_nodes=my_nodes)

print("End of programmne")
