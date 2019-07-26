import numpy as np
import math
import matplotlib.pyplot as plt
import random
import statistics

choice = str(input("Do you want to go ahead with default scenario settings? Enter Y or N: "))


if choice == 'N':
    field_len = input("Enter the side of the field in m: e.g. 700 ")
    speed = input("Enter the speed of the nodes in m/s: e.g. 4 ")
    time = input("Enter the refresh time for plots in s: e.g. 2 ")
    number_of_nodes = input("Enter the total number of nodes: e.g. 50 ")
    change = input("Enter the refresh time for cluster reassignment in s "
                       "(5:1 cluster:head): e.g. 7 ")
    stay_alive = input("Enter the number of times you want to update the heads: e.g. 10 ")

    field_len = int(field_len)
    speed = int(speed)
    time = int(time)
    number_of_nodes = int(number_of_nodes)
    change = int(change)
    stay_alive = int(stay_alive)

elif choice == 'Y':
    field_len = 700
    speed = 4
    time = 2
    number_of_nodes = 50
    change = 7                 # when different clusters can be visualised and are not too far away to never interfere
    stay_alive = 10

else:
    print("Invalid entry")
    exit()


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


speed_x = speed
speed_y = speed
mean_x = 0
mean_y = 0
pos_end =field_len
neg_end = -1*(field_len)
list_of_clusters = [[], [], [], []]
cluster1 = []
cluster2 = []
cluster3 = []
cluster4 = []
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
                                    marker                              (all nodes start with '.' 
                                                                                and heads are promoted to 's'
                                    edgecolors                          (all nodes start with no edge color, 
                                                                                  supercluser have the same edge color)
    """
    _ID = 1  # class global ID

    def __init__(self,
                 ID=0,
                 init_speed_x=speed_x,
                 init_speed_y=speed_y,
                 init_speed=np.array([speed_x, speed_y]),
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
                 marker='.',
                 edgecolors='none'
                 ):

        self.ID = self._ID;
        self.__class__._ID += 1

        self.init_speed_x = init_speed_x
        self.init_speed_y = init_speed_y
        self.init_speed = init_speed
        self.last_five_speed = list([self.init_speed, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
                                     np.array([0.0, 0.0])])

        self.time_taken = time_taken

        init_x = random.randint(neg_end//2.5, pos_end//2.5)
        init_y = random.randint(neg_end//2.5, pos_end//2.5)
        init_position = np.array([init_x, init_y])
        self.init_position = init_position
        self.last_five_x_position = [0, 0, 0, 0, 0]
        self.last_five_y_position = [0, 0, 0, 0, 0]
        self.last_five_position = list(
            [self.init_position, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]),
             np.array([0.0, 0.0])]),

        direction = random.randint(1, 4)
        self.direction = direction
        self.last_five_direction = [self.direction, 0, 0, 0, 0]

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
            self.init_speed_y = (-1) * speed
        if self.direction == 4:
            self.init_speed_x = (-1) * speed
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
        direction = random.randint(1, 4)
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
        plt.xlim(neg_end,pos_end)
        plt.ylim(neg_end,pos_end)
        x = list_of_node_parameters[node].init_position[0]
        y = list_of_node_parameters[node].init_position[1]
        color = list_of_node_parameters[node].color
        node_marker = list_of_node_parameters[node].marker
        node_edgecolor = list_of_node_parameters[node].edgecolors
        plt.scatter(x, y, c=color, marker=node_marker, edgecolors=node_edgecolor)
    plt.pause(0.005)


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
    pos_list= []
    for i in list_of_node_ids:
        x_pos = list_of_nodes[i-1].init_position[0]
        x_pos_list.append(x_pos)
        y_pos = list_of_nodes[i-1].init_position[1]
        y_pos_list.append(y_pos)
    pos_list = [x_pos_list, y_pos_list]
    return pos_list


# repeat this everytime you want to elecet a head, calculates mmean
id_list = []
for i in range(number_of_nodes):
    curr_id = my_nodes[i].ID
    id_list.append(curr_id)


def update_pos_n_plot(list_of_node_ids, list_of_nodes):
    for i in list_of_node_ids:
        node_index = i-1
        list_of_nodes[node_index].update_speed(list_of_nodes[node_index].init_speed)
        list_of_nodes[node_index].update_position(list_of_nodes[node_index].init_position)
        list_of_nodes[node_index].update_colors(list_of_nodes[node_index].init_position)
    plot_positions(list_of_nodes)
    plt.cla()

def average_fn(z_list):
    z_mean = statistics.mean(z_list)
    return z_mean


# call this to form clusters, dorections unchanged. intitial cluster formation
for j in range(change):
    node_positions = node_latest_pos_list(id_list, my_nodes)
    x_pos_list = node_positions[0]
    y_pos_list = node_positions[1]
    mean_x = average_fn(x_pos_list)
    mean_y = average_fn(y_pos_list)
    update_pos_n_plot(id_list, my_nodes)

def call_clusters(node):
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


# this creates a list of clusters called VANET_clusters, usually called to elect heads
for i in range(number_of_nodes):
    node = my_nodes[i]
    VANET_clusters = call_clusters(node)



x_pos_cluster = []
y_pos_cluster = []
dir_cluster = []



def elect_head(cluster, list_of_nodes):
    head_id = -1
    lowest_dist = 10**5
    for i in range(len(cluster)):
        node_index = int(cluster[i]-1)
        last_node_x = list_of_nodes[node_index].init_position[0]
        last_node_y = list_of_nodes[node_index].init_position[1]
        dir_node = list_of_nodes[node_index].direction
        x_pos_cluster.append(last_node_x)
        y_pos_cluster.append(last_node_y)
        dir_cluster.append(dir_node)
    x_pos_cluster_avg = statistics.mean(x_pos_cluster)
    y_pos_cluster_avg = statistics.mean(y_pos_cluster)
    dir_cluster_avg = statistics.mean(dir_cluster)
    for i in range(len(cluster)):
        node_id = int(cluster[i]-1)
        x_dev_sq = (statistics.mean(list_of_nodes[node_index].last_five_x_position) - x_pos_cluster_avg)**2
        y_dev_sq = (statistics.mean(list_of_nodes[node_index].last_five_x_position) - y_pos_cluster_avg)**2
        node_dist = math.sqrt(x_dev_sq + y_dev_sq)
        node_dir_avg = abs(list_of_nodes[node_index].direction - dir_cluster_avg)

        if (node_dir_avg*node_dist) <= lowest_dist:
            head_id = node_index+1
            lowest_dist = node_dist*node_dir_avg
        else:
            lowest_dist = lowest_dist
            head_id = head_id
    head_index = head_id-1
    if statistics.mean(list_of_nodes[head_index].last_five_x_position) > 50:
        list_of_nodes[head_index].edgecolors = 'red'
    else:
        list_of_nodes[head_index].edgecolors = 'blue'
    list_of_nodes[head_index].marker = 's'
    return head_id


def assign_head(list_of_clusters, list_of_nodes):
    head1 = elect_head(list_of_clusters[0], list_of_nodes)
    head2 = elect_head(list_of_clusters[1], list_of_nodes)
    head3 = elect_head(list_of_clusters[2], list_of_nodes)
    head4 = elect_head(list_of_clusters[3], list_of_nodes)
    head_list = [head1, head2, head3, head4]
    return head_list

# this creates a list of heads called VANET_heads
VANET_heads = assign_head(VANET_clusters, list_of_nodes=my_nodes)
print(VANET_heads)


# this updates the cluster members but not the cluster heads
def update_cluster_members(list_of_nodes):
    for j in range(5*change):
        for i in range(number_of_nodes):
            node_list = my_nodes
            x_pos = node_list[i].init_position[0]
            y_pos = node_list[i].init_position[1]
            node = node_list[i]
            node_list[i].update_directions(node_list[i].direction)
            node_list[i].update_speed(node_list[i].init_speed)
            node_list[i].update_position(node_list[i].init_position)
            if node_list[i].ID not in VANET_heads:
                node_list[i].update_colors(node_list[i].init_position)
                node.marker = str('.')
                node_list[i].edgecolors = str('none')
            else:
                if statistics.mean(node_list[i].last_five_x_position) > 50:
                    node_list[i].edgecolors = str('red')
                else:
                    node_list[i].edgecolors = str('blue')
                node_list[i].marker = str('s')
            x_pos = node_list[i].init_position[0]
            x_pos_list.append(x_pos)
            y_pos = node_list[i].init_position[1]
            y_pos_list.append(y_pos)
        mean_x = average_fn(x_pos_list)
        mean_y = average_fn(y_pos_list)

        plot_positions(list_of_nodes)
        plt.cla()



# this updates cluster heads
def update_supercluster_menbers(VANET_clusters, VANET_heads, list_of_nodes):
    VANET_clusters.clear()
    VANET_heads.clear()
    cluster1.clear()
    cluster4.clear()
    cluster3.clear()
    cluster2.clear()
    list_of_clusters.clear()

    for i in range(number_of_nodes):
        node = my_nodes[i]
        VANET_clusters = call_clusters(node)

    VANET_heads = assign_head(VANET_clusters, list_of_nodes)
    print(VANET_heads)
    return VANET_heads


for i in range(stay_alive):
    update_cluster_members(list_of_nodes=my_nodes)
    VANET_heads = update_supercluster_menbers(VANET_clusters, VANET_heads, list_of_nodes=my_nodes)
    update_cluster_members(list_of_nodes=my_nodes)
