import math

class V_Node:
	def __init__(self, val, parent):
		"""
		Initializes a vertex_node. Stores position value according to tree depth, and a pointer to parent to reconstruct the full position.
		"""
		self.val = val
		self.parent = parent
		self.children = []

	def lookup_child(self, val, k=1):
		"""
		Returns the top-k children of this vertex whose values are closest to the given value, and their distances to the value
		"""

		#always sort this.
		top_k = [(None, float('inf'))]*k

		for c in self.children:
			print(c, '->', top_k)
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
			self.children.append(V_Node(val, self))
			return self.children[-1]

	def __repr__(self):
		return str(self.val)



def main():
	root = V_Node(float('inf'), None)
	root.insert(-10)
	root.insert(-1)
	root.insert(0)
	root.insert(1)
	root.insert(10)

	print(root.children)
	print('_'*50)
	print(root.lookup_child(-5, 6))

if __name__ == '__main__':
	main()