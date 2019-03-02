import math
import time
import pandas as pd
from Graph import *
from ControllerXYZ import *

class V_Node:
	def __init__(self, val, data, parent):
		"""
		Initializes a vertex_node. Stores position value according to tree depth, and a pointer to parent to reconstruct the full position.
		"""
		self.val = val
		self.parent = parent
		self.children = []
		self.data = None

	def lookup_child(self, val, k=1):
		"""
		Returns the top-k children of this vertex whose values are closest to the given value, and their distances to the value
		"""

		#always sort this.
		top_k = [(None, float('inf'))]*k

		for c in self.children:
			#print(c, '->', top_k)
			dist = abs(c.val - val)
			if dist < top_k[-1][1]:
				top_k[-1] = (c, dist)
				top_k = sorted(top_k, key=lambda x: x[1], reverse=False)
		return [x for x in top_k if x[1] < float('inf')]

	def insert(self, val):
		"""
		Adds a new node as a child of this one, and returns it. If a child with that value already exists, just return it.
		"""
		best = self.lookup_child(val, 1)
		if len(best) > 0 and best[0][1] == 0:
			return best[0][0]
		else:
			self.children.append(V_Node(val, None, self))
			out = self.children[-1]
			self.children = sorted(self.children, key=lambda x: x.val)
			return out

	def preorder(self, depth=0):
		print('\t'*depth, self)
		for child in self.children:
			child.preorder(depth=depth+1)

	def countnodes(self):
		s = 1
		for child in self.children:
			s += child.countnodes()
		return s

	def __repr__(self):
		return str(self.val) + ':' + str(self.data)

def load_from_csv(filepath):
	vertices = pd.read_csv(filepath)

	root = V_Node(float('inf'), None, None)

	for index, row in vertices.iterrows():
		#print('-'*20,index, '-'*20)
		x,y,z = row['x'], row['y'], row['z']
		thetas = (row['theta1'], row['theta2'], row['theta3'])

		v_curr = root.insert(x)
		v_curr = v_curr.insert(y)
		v_curr = v_curr.insert(z)
		v_curr.data = thetas
	print(len(vertices))
	return root

def tree_lookup(root, x, y, z, k=3):
	v_list = root.lookup_child(x, k)
	v_list = sorted(v_list, key=lambda x: x[1])
	v_list = v_list[:k]

	v_list_temp = []
	for v,dist in v_list:
		v_list_temp.extend(v.lookup_child(y, k))

	v_list = sorted(v_list_temp, key=lambda x:x[1])
	v_list = v_list[:k]

	v_list_temp = []
	for v,dist in v_list:
		v_list_temp.extend(v.lookup_child(z, k))

	v_list = sorted(v_list_temp, key=lambda x:x[1])
	v_list = v_list[:k]

	z_v = v_list[0][0]
	y_v = z_v.parent
	x_v = y_v.parent


	print('given coordinates:', (x, y, z))
	print('cartesian coordinates:', (x_v.val, y_v.val, z_v.val))
	print('error =', euclidean_dist((x, y, z), (x_v.val, y_v.val, z_v.val)))

	return v_list[0][0]

def euclidean_dist(actual, observed):
	s = 0
	for a, o in zip(actual, observed):
		s += (a-o) ** 2
	return s **0.5

def main():
	# root = V_Node(float('inf'), None)
	# root.insert(-10)
	# root.insert(-1)
	# root.insert(0)
	# root.insert(1)
	# root.insert(10)

	# print(root.children)
	# print('_'*50)
	# print(root.lookup_child(-3, 3))

	#SETUP

	verticesDF = pd.read_csv("vertices.csv")
	countDF = verticesDF.groupby(['x', 'y', 'z'])['theta1'].count()
	countDF = countDF.reset_index()

	print("finished groupby")

	graph = Graph("robot arm")
	graph.initialize(verticesDF)
	graph.build_graph()
	

	root = load_from_csv('vertices.csv')
	print('finished tree')
	# root.preorder()
	# print(root.countnodes())
	# print(root.children)


	#RUN

	v = tree_lookup(root, -2, -2, 8, 10)

	thetas = v.data
	nodestr = 'nodeID+{}+{}+{}'.format(thetas[0], thetas[1], thetas[2])

	print('Node1=', nodestr)

	v2 = tree_lookup(root, 0, -4, 4, 10)

	thetas2 = v2.data
	nodestr2 = 'nodeID+{}+{}+{}'.format(thetas2[0], thetas2[1], thetas2[2])

	print('Node2=', nodestr2)

	print('Path=')
	path = graph.dfs(graph.id_map[nodestr], graph.id_map[nodestr2])
	for p in path:
		print(p)

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


		print('Node1=', nodestr)
		print('Node2=', nodestr2)

		for p in path:
			print(p)

		(x_prev, y_prev, z_prev) = (x, y, z)
		(gx_prev, gy_prev, gz_prev) = (gx, gy, gz)
		p_node = c_node
		p_nodestr = c_nodestr

if __name__ == '__main__':
	main()