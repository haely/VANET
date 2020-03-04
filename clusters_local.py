import numpy as np
import math
import matplotlib.pyplot as plt
import random
import statistics


choice = str(input("Do you want to go ahead with default scenario settings? Enter Y or N: "))
from statistics import mean

cluster_list = []
if choice == 'N':
    field_len = input("Enter the side of the field in m: e.g. 700 ")
    speed = input("Enter the speed of the nodes in m/s: e.g. 4 ")
    time = input("Enter the refresh time for plots in s: e.g. 2 ")
    number_of_nodes = input("Enter the total number of nodes: e.g. 50 ")
    change = input("Enter the refresh time for cluster reassignment in s (5:1 cluster:head): e.g. 7 ")
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
    change = 7  # when different clusters can be visualised and are not too far away to never interfere
    stay_alive = 10
else:
    print("Invalid entry")
    exit()

speed_x = speed
speed_y = speed
mean_x = 0
mean_y = 0
pos_end = field_len
neg_end = -1 * (field_len)
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
        init_x = random.randint(neg_end // 2.5, pos_end // 2.5)
        init_y = random.randint(neg_end // 2.5, pos_end // 2.5)
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

    def update_colors(self, init_position, cluster_list=cluster_list):
        curr_node_id = self.ID
        for cluster in cluster_list:
            for node in cluster:
                if curr_node_id == node:
                    self.color = cluster[-1]
        # print

    def update_directions(self, direction):
        direction = self.direction
        direction = random.randint(1, 3)
        self.direction = direction


def init_node(total_nodes):
    node_list = []  # array that contains every node with its parameters
    for node in range(total_nodes):
        node_ = Node()
        node_list.append(node_)
    return node_list


# creates 'number_of_nodes' objects and stores in my_nodes list, to be called later
my_nodes = init_node(number_of_nodes)
# print(my_nodes[1].ID)
# repeat this everytime you want to elecet a head, calculates mmean
id_list = []
for i in range(number_of_nodes):
    curr_id = my_nodes[i].ID
    id_list.append(curr_id)
#print("These are node ids:")
#print(id_list)


def elect_head(list_of_nodes):
    head_cluster_list = []
    head_id = -1
    dist_radius = field_len // 5
    rem_id_list = id_list
    print(rem_id_list)
    if len(rem_id_list) > 0:
        cluster_list = []
        for i in rem_id_list:
            #print(i)
            temp_head_id = i
            head_x = list_of_nodes[temp_head_id - 1].init_position[0]
            head_y = list_of_nodes[temp_head_id - 1].init_position[1]
            i_cluster = []
            for j in rem_id_list:
                mem_x = list_of_nodes[j - 1].init_position[0]
                mem_y = list_of_nodes[j - 1].init_position[1]
                if abs(mem_x - head_x) <= dist_radius and abs(mem_y - head_y) <= dist_radius:
                    rem_id_list.remove(j)
                    i_cluster.append(j)

            print(i_cluster)
            if len(i_cluster) > 0:
                print(i_cluster)
                cluster_list.append(i_cluster)
        head_id_list = []
        for cluster in cluster_list:
            head_id = min(cluster)
            head_id_list.append(head_id)

    else:
        raise ValueError('did not have enough nodes to form clusters')
        exit()
    lenf = 0
    for cluster in cluster_list:
        lenf += len(cluster)
    print(lenf)
    print(rem_id_list)
    orphan_count = 0
    for cluster in cluster_list:
        temp = 0
        if len(cluster) == 1:
            orphan_count += 1
            orphan_id = cluster[0]
            #print('my orphan')
            #print(orphan_id)
            orphan_x = list_of_nodes[orphan_id - 1].init_position[0]
            orphan_y = list_of_nodes[orphan_id - 1].init_position[1]
            cluster_list.remove(cluster)
            head_id_list.remove(orphan_id)
            loop_count = 0
            for cluster in cluster_list:
                if len(cluster) > 1:
                    head_cluster = min(cluster)
                    head_x = list_of_nodes[head_cluster - 1].init_position[0]
                    head_y = list_of_nodes[head_cluster - 1].init_position[1]

                    if abs(orphan_x - head_x) <= dist_radius / 3 and abs(orphan_y - head_y) <= dist_radius / 3:
                        cluster_list.remove(cluster)
                        head_id_list.remove(head_cluster)
                        cluster.append(orphan_id)
                        temp += 1
                        loop_count += 1
                        cluster_list.append(cluster)
                        head_id_list.append(head_cluster)
                        print('orphan no more')
                    if loop_count > 0:
                        break
            if temp == 0:
                #print('still an orphan')
                orphan_cluster = [orphan_id]
                cluster_list.append(orphan_cluster)
                head_id_list.append(orphan_id)
                #print('orphan no more')
    if orphan_count == 0:
        print('we never had orphans')
    head_cluster_list.append(head_id_list)
    head_cluster_list.append(cluster_list)
    return head_cluster_list



# this creates a list of heads called VANET_heads
VANET_heads = elect_head(list_of_nodes=my_nodes)
#VANET_heads = VANET_heads.tolist()
print(VANET_heads)
cluster_list = VANET_heads[1]
head_list = VANET_heads[0]
print("clusters after orphan update")
print(cluster_list)
print("heads after orphan update")
print(head_list)
lenf=0
for cluster in cluster_list:
    lenf += len(cluster)
print(lenf)

# we now ave clusters and possibly orphans, now orphans will find clusters to join. tey look for closest cluster memberse i.e dis_radii is now field_len/7
def update_cluster_head(list_of_clusters, list_of_nodes):
    # updated_head_list = []
    global updated_head_list
    # New_head = 0
    for cluster in list_of_clusters:
        sum_x = 0
        sum_y = 0
        for node in cluster:
            xmean_node = mean(list_of_nodes[node - 1].last_five_x_position)
            ymean_node = mean(list_of_nodes[node - 1].last_five_y_position)
            sum_x = sum_x + xmean_node
            sum_y = sum_y + ymean_node
        xmean_cluster = sum_x / len(cluster)
        ymean_cluster = sum_y / len(cluster)
        curr_head = min(cluster)
        xmean_curr = mean(list_of_nodes[curr_head - 1].last_five_x_position)
        ymean_curr = mean(list_of_nodes[curr_head - 1].last_five_y_position)
        curr_min = abs(xmean_cluster - xmean_curr) * abs(ymean_cluster - ymean_curr)
        for node in cluster:
            xmean_node = mean(list_of_nodes[node - 1].last_five_x_position)
            ymean_node = mean(list_of_nodes[node - 1].last_five_y_position)
            if abs(xmean_node - xmean_cluster) * abs(ymean_node - ymean_cluster) <= curr_min:
                curr_min = abs(xmean_node - xmean_cluster) * abs(ymean_node - ymean_cluster)
                new_head = node
            else:
                new_head = curr_head
        # updated_head_list = []
        updated_head_list.append(new_head)
        updated_head_list = set(updated_head_list)
        updated_head_list = list(updated_head_list)
    return updated_head_list


updated_head_list = []
new_heads = update_cluster_head(list_of_clusters=cluster_list, list_of_nodes=my_nodes)
print("heads after first recheck")
print(new_heads)


def update_clusters(list_of_nodes, list_of_new_heads, list_of_ids):
    updated_cluster_list = []
    dist_radius = field_len / 5
    # updated_head_list = []
    # global updated_cluster_list
    rem_id_list = [ele for ele in list_of_ids if ele not in list_of_new_heads]
    for head in list_of_new_heads:
        head_j = head - 1
        head_x = list_of_nodes[head_j].init_position[0]
        head_y = list_of_nodes[head_j].init_position[1]
        i_cluster = []
        i_cluster.append(head)
        for j in rem_id_list:
            mem_x = list_of_nodes[j - 1].init_position[0]
            mem_y = list_of_nodes[j - 1].init_position[1]
            if abs(mem_x - head_x) <= dist_radius and abs(mem_y - head_y) <= dist_radius:
                rem_id_list.remove(j)
                i_cluster.append(j)
            else:
                pass
        updated_cluster_list.append(i_cluster)

    if len(rem_id_list) > 0:
        temp = 0
        print("we have orphans")
        print(rem_id_list)
        for orphan_id in rem_id_list:
            orphan_x = list_of_nodes[orphan_id - 1].init_position[0]
            orphan_y = list_of_nodes[orphan_id - 1].init_position[1]
            loop_count = 0
            for cluster in updated_cluster_list:
                for node in cluster:
                    node_x = list_of_nodes[node - 1].init_position[0]
                    node_y = list_of_nodes[node - 1].init_position[1]
                    if abs(orphan_x - node_x) <= dist_radius / 4 and abs(orphan_y - node_y) <= dist_radius / 4:
                        cluster.append(orphan_id)
                        updated_cluster_list.append(cluster)
                        rem_id_list.remove(orphan_id)
                        temp += 1
                        loop_count += 1
                    else:
                        pass
                    if loop_count > 0:
                        break
            if temp > 1:

                orphan_cluster = [orphan_id]
                updated_cluster_list.append(orphan_cluster)
                list_of_new_heads.append(orphan_id)
            else:
                pass

    return updated_cluster_list, list_of_new_heads


my_id_list = []
for i in range(number_of_nodes):
    curr_id = my_nodes[i].ID
    my_id_list.append(curr_id)

updated_cluster = update_clusters(list_of_nodes=my_nodes, list_of_new_heads=new_heads, list_of_ids=my_id_list)
print("cluster after first recheck")
print(updated_cluster[0])
print("also heads")
print(updated_cluster[1])

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

def update_pos_n_plot(list_of_node_ids, list_of_nodes):
    for i in list_of_node_ids:
        node_index = i - 1
        list_of_nodes[node_index].update_speed(list_of_nodes[node_index].init_speed)
        list_of_nodes[node_index].update_position(list_of_nodes[node_index].init_position)
        list_of_nodes[node_index].update_colors(list_of_nodes[node_index].init_position)

for j in range(change):
    node_positions = node_latest_pos_list(list_of_node_ids=my_id_list, list_of_nodes=my_nodes)
    x_pos_list = node_positions[0]
    y_pos_list = node_positions[1]
    update_pos_n_plot(id_list, my_nodes)
updated_head_list = []
new_heads = update_cluster_head(list_of_clusters=cluster_list, list_of_nodes=my_nodes)
print("heads after second recheck")
print(new_heads)
updated_cluster = update_clusters(list_of_nodes=my_nodes, list_of_new_heads=new_heads, list_of_ids=my_id_list)
print("cluster after second recheck")
print(updated_cluster)

new_heads.sort()
#for head in new_heads:
