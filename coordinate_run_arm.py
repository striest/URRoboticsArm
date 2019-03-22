import math
import time
from initialize import *
import pickle
from Graph import *
from ControllerXYZ import *

def main():
    print('Loading pickles')

    root = pickle.load(open('v_tree.p', 'rb'))
    graph = pickle.load(open('graph.p', 'rb'))

    print(root)
    print(graph)

    print('Ready!')

    x, x_prev  = 0, 0
    y, y_prev = 0, 0
    z, z_prev = 0, 0

    initial_position = input("Starting Position: ")

    init_list = initial_position.split(",")

    x_prev = float(init_list[0])
    y_prev = float(init_list[1])
    z_prev = float(init_list[2])

    print('x:{}, y:{}, z:{}'.format(x_prev, y_prev, z_prev))

    p_node = tree_lookup(root, x_prev, y_prev, z_prev, k=10)
    p_thetas = p_node.data
    p_nodestr = 'nodeID+{}+{}+{}'.format(p_thetas[0], p_thetas[1], p_thetas[2])

    while True:

        new_position = input("New Position: ")
        new_list = new_position.split(",")

        x = float(new_list[0])
        y = float(new_list[1])
        z = float(new_list[2])

        print('x:{}, y:{}, z{}'.format(x, y, z))

        c_node = tree_lookup(root, x, y, z, k=10)
        c_thetas = c_node.data
        c_nodestr = 'nodeID+{}+{}+{}'.format(c_thetas[0], c_thetas[1], c_thetas[2])

        print('Node1=', p_nodestr)
        print('Node2=', c_nodestr)

        path = graph.dfs(graph.id_map[p_nodestr], graph.id_map[c_nodestr])

        for p in path:
            print(p)

        (x_prev, y_prev, z_prev) = (x, y, z)
        p_node = c_node
        p_nodestr = c_nodestr




if __name__ == '__main__':
	main()
