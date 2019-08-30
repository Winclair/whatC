from define import * 
from queue import Queue

prod_exprs = []
left2prods = {}


class ProdExpr(object):
	def __init__(self, left, rights):
		super(ProdExpr, self).__init__()
		self.left = left 
		self.rights = rights 
	
	def __repr__(self):
		right_str = ""
		for rs in self.rights:
			if is_endsym(rs):
				right_str += "{} ".format(rs[1])
			else:
				right_str += "{} ".format(rs)
		return("{}->{}".format(self.left, right_str))			



	
def get_prod_exprs(file):

	prod_exprs.append(ProdExpr('e0', ['e']))
	left2prods['e0'] = [0]

	i = 1
	with open(file) as f:
		for prods in f:
			prods = prods.split(':')
			left2prods[prods[0]] = []
			rights_list = prods[1].strip().split('|')

			for rs in rights_list:
				rights = []
				for s in rs.split(' '):
					symbol = None
					if s[0].isalpha():
						if s!=s.upper():
							rights.append(s)
							continue
						else:
							symbol = end_expr[s]
					elif s in limiter:
						symbol = ('limiter', s)
					else:
						symbol = ('operator', s)
					rights.append(symbol)	
				prod_exprs.append(ProdExpr(prods[0], rights))
				left2prods[prods[0]].append(i)
				i += 1


class LRNode(object):
	"""docstring for LRNode"""

	def __init__(self, core_items):
		super(LRNode, self).__init__()
		self.core_items = core_items
		self.noncore_items = []
		self.edge = {}
		self.goto = {}
		self.visited = {}
		self.construct()

	def construct(self):
		# get items and goto 	
		for item in self.core_items:
			self.closure(item)

	####### closure	and goto
	def add_to_goto(self, X, item):
		#if is_endsym(X): X = X[1]
		if not self.goto.get(X):
			self.goto[X] = []
		self.goto[X].append(item)	
		
	def X_after_dot(self, item):
		try:
			return (prod_exprs[item[0]].rights)[item[1]]
		except IndexError:
			return None
			
	def closure(self, item):			
		X = self.X_after_dot(item)
		if not X: return
		self.add_to_goto(X, (item[0], item[1]+1))
		
		if self.visited.get(X, 0): return
		else: self.visited[X] = 1

		prods = left2prods.get(X)
		if not prods: return
		for p in prods:
			self.noncore_items.append((p, 0))
			self.closure((p, 0))
	####### closure
	
	def __eq__(self, core_items1):
		return self.core_items == core_items1

	def __repr__(self):
		return "core_items: {}\nnoncore_items: {}\ngoto: {}\nedge: {}".format(
		        self.core_items, self.noncore_items, self.goto, self.edge)


class LRDFA(object):
	"""docstring for LRDFA"""
	def __init__(self):
		super(LRDFA, self).__init__()
		self.states = []
		self.unfin_nodes = Queue()
		self.I0 = LRNode([(0,0)]) 
		self.construct()

	def construct(self):
		self.states.append(self.I0)
		self.unfin_nodes.put(self.I0)
		i = 1
		while not self.unfin_nodes.empty():
			I = self.unfin_nodes.get()
			for X, core_items in I.goto.items():
				if core_items in self.states:
					I.edge[X] = self.states.index(core_items)
				else:	
					I1 = LRNode(core_items)
					I.edge[X] = i
					i += 1
					self.states.append(I1)
					self.unfin_nodes.put(I1)
		
		


FOLLOW = {'e0': {('end', '$')}, 
          'e': {('operator', '+'), ('limiter', ')'), ('end', '$')},
          't': {('operator', '+'), ('limiter', ')'), ('operator', '*'), ('end', '$')},
          'f': {('operator', '+'), ('limiter', ')'), ('operator', '*'), ('end', '$')}
         }




class LRTable(object):
	"""docstring for LRTable"""
	def __init__(self, lrdfa):
		super(LRTable, self).__init__()
		self.lrdfa = lrdfa
		self.actions = []
		self.gotos = []
		self.construct()
	
	def construct(self):
		for state in self.lrdfa.states:
			act = {}
			gt = {}
			for X, i_state in state.edge.items():
				if is_endsym(X):
					act[X] = ('s', i_state)
				else:
					gt[X] = i_state
			
			for item in state.core_items:
				if state.X_after_dot(item) == None:
					left = prod_exprs[item[0]].left
					if left == 'e0': 
						act[('end', '$')] = ('acc', "")
						break
					for a in FOLLOW[left]:
						if act.get(a): 
							continue
						else: act[a] = ('r', item[0])
			self.actions.append(act)		 
			self.gotos.append(gt)		 
	
	
	def __repr__(self):
		s = "action:\n" 
		for act in self.actions:
			for a in act:  
				s += "{}: {}{}   ".format(a[1], act[a][0], act[a][1]) 
			s += '\n'
		s += '\ngoto\n'
		
		for gt in self.gotos:
			for A in gt:
				s += '{}:{}  '.format(A, gt[A])
			s += '\n'				
		return s



class LRSyner(object):
	"""docstring for LRSyner"""
	def __init__(self, tokens):
		super(LRSyner, self).__init__()
		self.tokens = tokens
		self.lrtable = None
		self.constrcut()

	def constrcut(self):
		get_prod_exprs('grammer.txt')
		dfa = LRDFA()
		self.lrtable = LRTable(dfa)
		self.tokens.append(('end', '$'))
		
	def run(self):
		
		i_token = 0
		stack = [0]
		while 1:
			token = self.tokens[i_token]
			act = self.lrtable.actions[stack[-1]].get(token, None)
			if not act:  
				print("ERROR!")
				break
			if act[0] == 'acc':
				print('DO')
				break
			if act[0] == 's':
				i_token += 1
				stack.append(act[1])
			if act[0] == 'r':
				prod = prod_exprs[act[1]]
				for j in range(len(prod.rights)):
					stack.pop()
				gt = self.lrtable.gotos[stack[-1]][prod.left]	
				stack.append(gt)	
	

			
if __name__ == '__main__':
	tokens = [('id', 'id'), ('operator', '*'), ('id', 'id')]
	ser = LRSyner(tokens)
	ser.run()
	
