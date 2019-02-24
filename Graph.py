import numpy as np
import pandas as pd

class Vertex:

    def __init__(self, nodeID, theta1, theta2, theta3, x, y, z):
        self.nodeID = nodeID

        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point(name: %s, t1=%s, t2=%s, t3=%s, x=%s, y=%s, z = %s)' % (self.nodeID, self.theta1, self.theta2, self.theta3, self.x, self.y, self.z)

    def __eq__(self, v2):
        return self.nodeID == v2.nodeID

    def within_threshold(self, v2, s):

        distance = self.get_euclidean(v2)

        change = (3 * s * s) ** .5

        if distance <= change and self.nodeID != v2.nodeID:
            return distance
        else:
            return -1

    def get_euclidean(self, v2):
            a = np.array([self.theta1, self.theta2, self.theta3])
            b = np.array([v2.theta1, v2.theta2, v2.theta3])

            distance = ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**.5

            return distance

    def get_nearby_vertices(self, s):

        list = []

        theta1_set = set([])
        theta2_set = set([])
        theta3_set = set([])

        theta1_set.add(max(0, self.theta1 - s))
        theta1_set.add(self.theta1)
        theta1_set.add(min(180, self.theta1 + s))

        theta2_set.add(max(0, self.theta2 - s))
        theta2_set.add(self.theta2)
        theta2_set.add(min(180, self.theta2 + s))

        theta3_set.add(max(0, self.theta3 - s))
        theta3_set.add(self.theta3)
        theta3_set.add(min(180, self.theta3 + s))

        for t1 in theta1_set:
            for t2 in theta2_set:
                for t3 in theta3_set:
                    line = "nodeID" + "+" + str(t1) + "+" + str(t2) + "+" + str(t3)
                    list.append(line)

        return list


class Graph:

    def __init__(self, name):
        self.name = name
        self.graph_map = {}
        self.id_map = {}

        self.vertices = []

    def initialize(self, verticesDF):

        for index, row in verticesDF.iterrows():
            v = Vertex(row['nodeID'], row['theta1'], row['theta2'], row['theta3'], row['x'], row['y'], row['z'])

            self.vertices.append(v)
            self.graph_map[v.nodeID] = []
            self.id_map[v.nodeID] = v

        print("finished initialize")

    def build_graph(self):

        count = 0

        for key in self.graph_map:
            v1 = self.id_map[key]

            nearby_vertices = v1.get_nearby_vertices(5)

            for v2_nodeID in nearby_vertices:
                if v1.nodeID != v2_nodeID:
                    v2 = self.id_map[v2_nodeID]

                    tempList = self.graph_map[v1.nodeID]
                    tempList.append(v2)
                    self.graph_map[v1.nodeID] = tempList

                    count += 1

                    #if count % 1000 == 0:
                        #print("edge count: " + str(count))

        print("finished building graph")

    def create_edges_raw(self):

        count  = 0

        for key in self.graph_map:
            v1 = self.id_map[key]
            for v2 in self.vertices:
                if v1.within_threshold(v2, 5) != -1:
                    tempList = self.graph_map[v1.nodeID]
                    tempList.append(v2)
                    self.graph_map[v1.nodeID] = tempList
                    count = count + 1

        print(count)

    def write_edges_to_csv(self, csvFile):
        csv_file_object = open(csvFile, "w")
        csv_file_object.write("v1_nodeID,v2_nodeID,distance")
        csv_file_object.write("\n")

        count = 0

        for key in self.graph_map:
            v1 = self.id_map[key]

            nearby_vertices = v1.get_nearby_vertices(5)

            for v2_nodeID in nearby_vertices:
                if v1.nodeID != v2_nodeID:
                    csv_str = "{},{},{!s}".format(v1.nodeID, v2_nodeID, round(v1.within_threshold(self.id_map[v2_nodeID], 5), 3))
                    csv_file_object.write(csv_str)
                    csv_file_object.write("\n")

                    count = count + 1

                    if count % 1000 == 0:
                        print("write count: " + str(count))

        print("finished writing edges to csv")

    def build_graph_from_file(self, edges_csv):
        edgesDF = pd.read_csv("edges.csv")

        for index, row in edgesDF.iterrows():

            v1_nodeID = row['v1_nodeID']
            v2_nodeID = row['v2_nodeID']

            v1 = self.id_map[v1_nodeID]
            v2 = self.id_map[v2_nodeID]

            tempList = self.graph_map[v1.nodeID]
            tempList.append(v2)
            self.graph_map[v1.nodeID] = tempList

            if index % 1000 == 0:
                print("build count: " + str(index))

        print("finished building graph")

    def dfs(self, v1, v2):

        nearby_vertices = self.graph_map[v1.nodeID];

        min_distance = 10000

        min_distance_vertex = v1

        for v in nearby_vertices:
            distance = v.get_euclidean(v2)
            if distance < min_distance:
                min_distance = distance
                min_distance_vertex = v

        if v1.nodeID == v2.nodeID:
            return [v2];
        else:
            print(min_distance_vertex)
            return [min_distance_vertex] + self.dfs(min_distance_vertex, v2)
