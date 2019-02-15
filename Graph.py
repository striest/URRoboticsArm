import numpy as np

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
        return 'Point(name: %s, x=%s, y=%s, z = %s)' % (self.nodeID, self.x, self.y, self.z)

    def __eq__(self, v2):
        return self.nodeID == v2.nodeID

    def within_threshold(self, v2, s):
        a = np.array([self.theta1, self.theta2, self.theta3])
        b = np.array([v2.theta1, v2.theta2, v2.theta3])

        change = (3 * s * s + 1) ** .5

        distance = np.linalg.norm(a-b)

        if distance <= change and self.nodeID != v2.nodeID:
            return distance
        else:
            return -1


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

    def create_edges(self):

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

        for key in self.graph_map:
            v1 = self.id_map[key]
            '''
            for v2 in self.vertices:
                if v1.within_threshold(v2, 5) != -1:
                    csv_str = "{},{},{!s}".format(v1.nodeID, v2.nodeID, round(v1.within_threshold(v2, 5), 3))
                    csv_file_object.write(csv_str)
                    csv_file_object.write("\n")
            '''

            
