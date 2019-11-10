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
    speed = input("Enter the speed of the nodes in m/s: e.g. 4 ")
    time = input("Enter the refresh time for plots in s: e.g. 2 ")
    number_of_nodes = input("Enter the total number of nodes: e.g. 50 ")
    change = input("Enter the refresh time for cluster reassignment in s "
                       "(5:1 cluster:head): e.g. 7 ")
    stay_alive = input("Enter the number of times you want to update the heads: e.g. 3 ")

    field_len = int(field_len)
    speed = int(speed)
    time = int(time)
    number_of_nodes = int(number_of_nodes)
    change = int(change)
    stay_alive = int(stay_alive)

elif choice == 'Y':
    field_len = 700
    speed = 40
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
                                    color                               (all nodes start with colour C10)
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
                 color='C120',
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

        self.color = str('C10')
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

    def update_colors(self, init_position, cluster_list = cluster_list):
        curr_node_id = self.ID
        for cluster in cluster_list:
            for node in cluster:
                if curr_node_id == node:
                    self.color = cluster[-1]
        print(self.color)



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
print(my_nodes[1].ID)

# repeat this everytime you want to elecet a head, calculates mmean
id_list = []
for i in range(number_of_nodes):
    curr_id = my_nodes[i].ID
    id_list.append(curr_id)
print(id_list)

def elect_head(list_of_nodes):
    head_id = -1
    dist_radius = field_len/5
    rem_id_list = id_list
    if len(rem_id_list) > 0:
        cluster_list = []
        for i in id_list:
            temp_head_id = i

            head_x = list_of_nodes[temp_head_id-1].init_position[0]
            head_y = list_of_nodes[temp_head_id-1].init_position[1]
            i_cluster = []

            for j in rem_id_list:
                mem_x = list_of_nodes[j-1].init_position[0]
                mem_y = list_of_nodes[j-1].init_position[1]
                if abs(mem_x-head_x) <= dist_radius and abs(mem_y-head_y) <= dist_radius:
                    rem_id_list.remove(j)
                    i_cluster.append(j)
                else:
                    pass
            #print(i_cluster)
            if len(i_cluster)>0:
                cluster_list.append(i_cluster)



        head_id_list = []
        for cluster in cluster_list:

            head_id = min(cluster)


            #cluster_color = c=np.random.rand(3,)  #str('C' + str(100*head_id))
            #cluster.append(cluster_color)
            #list_of_nodes[head_id].marker = 's'
            #cluster_list.append(cluster)
            head_id_list.append(head_id)
        print(cluster_list)
        print(head_id_list)
    else:
        raise ValueError('did not have enough nodes to form clusters')
        exit()
    orphan_count = 0
    for cluster in cluster_list:
        temp = 0
        if len(cluster) == 1:
            orphan_count+=1
            orphan_id = cluster[0]
            print('my orphan')
            print(orphan_id)
            orphan_x = list_of_nodes[orphan_id - 1].init_position[0]
            orphan_y = list_of_nodes[orphan_id - 1].init_position[1]
            cluster_list.remove(cluster)
            loop_count = 0
            for cluster in cluster_list:
                if len(cluster) > 1:
                    for node in cluster:
                        node_x = list_of_nodes[node - 1].init_position[0]
                        node_y = list_of_nodes[node - 1].init_position[1]

                        if abs(orphan_x - node_x) <= dist_radius / 2 and abs(orphan_y - node_y) <= dist_radius / 4:
                            cluster.append(orphan_id)
                            temp += 1
                            loop_count+=1
                        else:
                            pass
                        if loop_count>1:
                            break
            if temp == 1:
                print('still an orphan')
                orphan_cluster = [orphan_id]
                cluster_list.append(orpan_cluster)
                head_id_list.append(orpan_id)
            else:
                print('orphan no more')

    if orphan_count == 0:
        print('we never had orphans' )

    return head_id_list, cluster_list



def form_clusters(cluster_list, list_of_nodes):
    for i_cluster in cluster_list:
        for j in i_cluster:
            list_of_nodes[j-1].color = min(i_cluster)

# this creates a list of heads called VANET_heads
VANET_heads = elect_head(list_of_nodes=my_nodes)
print(VANET_heads)

# we now have clusters and possibly orphans, now orphans will find clusters to join. 
#they look for closest cluster memberes i.e dist_radius is now field_len/7


