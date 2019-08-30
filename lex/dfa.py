#!/usr/bin/env python
#-*- coding: utf-8 -*-

import copy

void = '$'

OP_LEVEL = {'*':3, '-':2, '|':1,'(': 0,'$':-1}


class NFANode(object):
	def __init__(self):
		super(NFANode, self).__init__()
		self.tag = None
		self.edge = {}
		
	def add_edge(self, alpha, tar_node):
		if alpha not in self.edge:
			self.edge[alpha] = set()
		self.edge[alpha].add(tar_node)	
	
	def __repr__(self):
		return str(self.tag)


class NFA(object):
	"""docstring for NFA"""
	def __init__(self, alpha=None):
		super(NFA, self).__init__()
		self.start_node = NFANode()
		self.end_node = NFANode()
		if alpha:
			if alpha[0] == "\\": 
				alpha = alpha[1:]
			self.start_node.add_edge(alpha, self.end_node)

	def cat_(self, nfa2):
		self.end_node.add_edge(void, nfa2.start_node)
		self.end_node = nfa2.end_node
		return self
		
	def or_(self, nfa2):
		new_nfa = NFA()
		new_nfa.start_node.add_edge(void, self.start_node)
		new_nfa.start_node.add_edge(void, nfa2.start_node)
		self.end_node.add_edge(void, new_nfa.end_node)
		nfa2.end_node.add_edge(void, new_nfa.end_node)
		return new_nfa
	
	def star_(self):
		new_nfa = NFA()
		new_nfa.start_node.add_edge(void, self.start_node)
		new_nfa.start_node.add_edge(void, new_nfa.end_node)
		self.end_node.add_edge(void, self.start_node)
		self.end_node.add_edge(void, new_nfa.end_node)
		return new_nfa
	


class NFAMaker(object):
	"""docstring for NFAMaker"""
	def __init__(self):
		super(NFAMaker, self).__init__()
		self.file = None
		self.delim_re = ['(',' ','|','\n','|','\t',')','*']
		self.left2exprs = {}
		self.single_re = ['keyword', 'letter', 'digit', 'operator', 'limiter']
		self.comp_re = ['identifier', 'string', 'number']
		self.mades = {}
		self.nfa = None

	def __get_exprs(self):
		with open(self.file) as f:
			for line in f:
				if line.isspace(): continue
				line = line.split(':')
				self.left2exprs[line[0].strip()] = [s.strip() for s in line[1].strip().split(' ')]

	def trans_to_subfix(expr):
		sub_expr = []
		op_stack = ['$']

		for re in expr:
			if re in ['*', '-', '|']:
				while OP_LEVEL[op_stack[-1]] >= OP_LEVEL[re]:
					sub_expr.append(op_stack.pop())
				op_stack.append(re)		
			elif re == '(':
				op_stack.append(re)
			elif re == ')':
				while op_stack[-1] != '(':
					sub_expr.append(op_stack.pop())	
				op_stack.pop()
			else:
				sub_expr.append(re)

		while op_stack[-1] != '$':
			sub_expr.append(op_stack.pop())	
		return sub_expr 			

	# not adding accept node	
	def get_nfa(self, expr):
		sub_expr = NFAMaker.trans_to_subfix(expr)
		stack = []
		nfa = None
		for e in sub_expr:
			if e == '*':
				 nfa = stack.pop().star_()
			elif e == '|':
				nfa = stack.pop().or_(stack.pop())
			elif e == '-':
				node = stack.pop()
				nfa = stack.pop().cat_(node)					
			else:
				if e in self.mades:
					nfa = copy.deepcopy(self.mades[e])
				else: 
					nfa = NFA(e)
					
			stack.append(nfa)

		return stack.pop()	


	def construct(self, file):
		self.file = file
		self.__get_exprs()

		# single re, then compound re 
		for left in self.single_re + self.comp_re:
			expr = self.left2exprs[left]
			#print("".join(expr))
			self.mades[left] = self.get_nfa(expr)
		# accept node 
		for left in self.left2exprs['start']:
			if left == '|': continue
			self.mades[left].end_node.tag = left 	
		# complete whole nfa
		self.nfa = self.get_nfa(self.left2exprs['start'])
		# add delim re
		delim_nfa = self.get_nfa(self.delim_re)
		delim_nfa.end_node.tag = 'delim';
		self.nfa = self.nfa.or_(delim_nfa)


class DFANode:
	def __init__(self, tag=None):
		self.tag = tag
		self.edge = {}

	def add_edge(self, alpha, tar_node):
		if alpha not in self.edge:
			self.edge[alpha] = tar_node


class DFA(object):
	def __init__(self, snode, enode):
		super(DFA, self).__init__()
		self.start_node = snode
		self.end_node = enode	



def void_closure(cur_state):

	clos = set(cur_state)
	stack = list(cur_state)  
	while stack:
		n = stack.pop()
		for e in n.edge:
			if e == void:
				tars = n.edge[e]
				for tar in tars:
					if tar not in clos:
						clos.add(tar)
						stack.append(tar)
	return clos	
						
#!!! 集合运算
def move(cur_state, e):
	next_state = set()
	for n in cur_state:
		next_state = next_state.union(n.edge.get(e, set()))
	return next_state	


###TEST###
###############单字符串匹配
def simple_lex(nfa, s):
	cur_state = void_closure({nfa.start_node})
	for c in s:
		cur_state = void_closure(move(cur_state, c))
	print(cur_state)	
	return (False in [n.tag==None for n in cur_state])	
			

def simple_lex_by_expr(expr, s):
	print("".join(expr))
	maker = NFAMaker()
	nfa = maker.get_nfa(expr)
	nfa.end_node.tag = 'dddd'
	return simple_lex(nfa, s)
###############

class C(object):
	"""docstring for C"""
	def __init__(self, c2=None):
		super(C, self).__init__()
		self.__p = {c2}
	def __mul__(self, c1=None):
		self.i *= 10 	
	def __repr__(self):
		return str(self.p)	



if __name__ == '__main__':
	maker = NFAMaker()
	maker.construct('re_exprs.txt')
	print(simple_lex(maker.nfa, '0.08888'))
	#simple_lex_by_expr(maker.left2exprs['digit'],'6')
	
	
