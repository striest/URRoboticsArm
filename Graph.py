

class Vertex:

    def __init__(self, nodeID, x, y, z):
        self.nodeID = nodeID
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point(name, %s, x=%s, y=%s, z = %z)' % (self.name, self.x, self.y, self.z)

    def __eq__(self, v2):
        return self.name == v2.name and self.x == x and self.y == y and self.z == z

class Graph:

    def __init__(self, name):
        self.name = name
        self.graph_map = {}

        self.vertices = []

    def initialize(self, verticesDF):

        for index, row in verticesDF.iterrows():
            v = Vertex(row['nodeID'], row['x'], row['y'], row['z'])

            self.vertices.append(v)
            self.graph_map[v.nodeID] = []

    def create_edges(self):

        count = 0
        for key in self.graph_map:
            print(key)
            count = count + 1

        print(count)
