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

	x, x_prev, gx_prev = 0, 0, 0 
	y, y_prev, gy_prev = 0, 0, 0
	z, z_prev, gz_prev = 0, 0, 0
	p_node = tree_lookup(root, x, y, z, k=10)
	p_thetas = p_node.data
	p_nodestr = 'nodeID+{}+{}+{}'.format(p_thetas[0], p_thetas[1], p_thetas[2])
	while True:
		pos, grad = getXYZ(list((x, y, z)), list((gx_prev, gy_prev, gz_prev)))
		x = pos[0]
		y = pos[1]
		z = pos[2]
		gx = grad[0]
		gy = grad[1]
		gz = grad[2]
		print('x:{}, y:{}, z{}'.format(x, y, z))

		c_node = tree_lookup(root, x, y, z, k=10)
		c_thetas = c_node.data
		c_nodestr = 'nodeID+{}+{}+{}'.format(c_thetas[0], c_thetas[1], c_thetas[2])

		path = graph.dfs(graph.id_map[p_nodestr], graph.id_map[c_nodestr])


		print('Node1=', p_nodestr)
		print('Node2=', c_nodestr)

		for p in path:
			print(p)

		(x_prev, y_prev, z_prev) = (x, y, z)
		(gx_prev, gy_prev, gz_prev) = (gx, gy, gz)
		p_node = c_node
		p_nodestr = c_nodestr


if __name__ == '__main__':
	main()