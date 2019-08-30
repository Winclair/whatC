from define import * 

class PreTable(object):
	"""docstring for PreTable"""
	def __init__(self, file):
		super(PreTable, self).__init__()
		self.file = file
		self.prod_exprs = {}
		self.endsym = {}
		self.non_endsym = {}
		self.pre_table = [[]]        


	def get_prod_exprs():
		with open(self.file) as f:
			j = 0
			for i, prod in enumerate(f):
				prod = prod.split(':')
				non_endsym[prod[0]] = i
				rights = prod[1].strip().split('|')
				right_list = []
				for rs in rights:
					temp = []
					for s in rs.split(' '):
						symbol = None
						if s[0].isalpha():
							if s!=s.upper():
								temp.append(s)
								continue
							else:
								symbol = end_expr[s]
						elif s in limiter:
							symbol = ('limiter', s)
						else:
							symbol = ('operator', s)
						temp.append(symbol)
						endsym[symbol] = j
						j += 1	
					right_list.append(temp)
				prod_exprs[prod[0]] = right_list
		endsym[(None, '$')] = j		


	def is_endsym(symbol):
		return type(symbol)==tuple

	def get_first(first_set, right_expr):

		for symbol in right_expr:
			if is_endsym(symbol):
				first_set.add(symbol)
				return symbol
			else:
				




					



	def get_pre_table(self):
		self.get_prod_exprs()

		for non_end, right in prod_exprs:
			non_i = non_endsym[non_end]





if __name__ == '__main__':
	get_prod_exprs('../grammer.txt')
	print(prod_exprs)
	print(endsym)
	print(non_endsym)	
		