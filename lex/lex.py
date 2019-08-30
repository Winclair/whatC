from dfa import DFA, DFANode, NFAMaker, void_closure, move


class Lex(object):
	"""docstring for Lex"""
	def __init__(self, dfa, file):
		super(Lex, self).__init__()
		self.dfa = dfa
		self.file = file
		self.tokens = []

	def analyze(self):
		with open(self.file) as f:
			for s in f:
				s = s.strip()
				if s: s = s + ' '
				cur_node = self.dfa.start_node
				start_index = 0
				for i, c in enumerate(s):
					temp_node = cur_node.edge.get(c, None)
					if not temp_node:
						if not cur_node.tag: 
							assert(False)
						else: 
							self.tokens.append((cur_node.tag, s[start_index:i]))
							if c == ' ':
								cur_node = self.dfa.start_node
								start_index = i+1
							else: 
								cur_node = self.dfa.start_node.edge.get(c, None)
								if not cur_node: assert(False)
					else:
						cur_node = temp_node
							


class Lex_by_NFA(object):
	"""docstring for Lex_by_NFA"""
	def __init__(self, file):
		super(Lex_by_NFA, self).__init__()
		self.file = file
		self.nfa = self.get_nfa()
		self.tokens = []
		self.start_state = void_closure({self.nfa.start_node})

	def get_nfa(self):
		maker = NFAMaker()
		maker.construct('re_exprs.txt')
		return maker.nfa

	def accept_tag(self, state):
		acc_tags = [n.tag for n in state if n.tag]
		if 'keyword' in acc_tags: return 'keyword'
		if acc_tags:return acc_tags[0] 		
		return None	

	def error(self, i_line, s, start_index, i):
		word = s[start_index:i]
		print("ERROR: line {}, {}".format(i_line, word))
		assert(False)	
			
	def analyze(self):
		with open(self.file) as f:
			for i_line, s in enumerate(f):
				s = s.strip()
				if s: s += " " 
				cur_state = self.start_state
				start_index = 0
				for i, c in enumerate(s):
					next_state = void_closure(move(cur_state, c))
					if not next_state:
						acc_tag = self.accept_tag(cur_state)
						if not acc_tag: 
							self.error(i_line, s, start_index, i)
						else: 
							if acc_tag != 'delim':
								self.tokens.append((acc_tag, s[start_index:i]))
							cur_state = void_closure(move(self.start_state, c))
							if not cur_state: assert(False)
							start_index = i
					else:
						cur_state = next_state



if __name__ == '__main__':
	'''
	a = DFANode()
	b = DFANode('end')

	a.add_edge('a', a)
	a.add_edge('b', b)

	dfa1 = DFA(a, b)

	lex = Lex(dfa1, 'test.txt')
	lex.analyze()
	print(lex.tokens)
	'''
	lex = Lex_by_NFA('test.txt')
	lex.analyze()
	print(lex.tokens)








		


		