# Clustering in wireless ad-hoc networks
Simulating multi-level clustering in VANET
Control packets:
_V2VclusterInfoHeader_: (pos, speed, direction, degree, vehicleID, clusterID, timestamp)
_InitiateClusterHeader_: (temp cluster ID, timestamp)
_FormClusterHeader_: same as clusterinfo packet.
1. All the nodes broadcast the mobility state.
2. The slowest node originates initiatecluster
3. 2r stable nodes react to this by changing their clusterID to that of the slowest node which originates the message. All of these nodes start calculating their suitability score and broadcast _FormClusterHeader_
4. A cluster is now formed. Control packets are periodically exchanged between neighbours to assure stability. A more suitable head/node leads to changing the cluster.
5. All nodes can send data packets to each other, A cluster member on receiving any data packet establishes a connection with its head and this cluster head then broadcasts the packet to its members.

*Additions/Changes in methods:*
All cluster heads and standalone nodes that are now a part of the supercluster will call the head election method once again to elect a supercluster head.
Need to look into the threshold changes and if we need them.
Nodes that are both cluster heads and supercluster members can be treated as 2 different nodes for control packet transmission. This might simplify the TDMA problem of two different control packets.
I was thinking different port numbers for cases like these might be of help, but I do not know enough about that and also how the code for that works in ns3.


Contributor: 
Haely Shah
