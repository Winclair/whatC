from lrsyn import ProdExpr


nl_prod_exprs = []
nl_left2prods = {}



def replace(prods):
	new_prods = []
	left = prods[0].left
	for prod in prods:
		first_sym = prod.rights[0]
		if is_endsym(first_sym) or first_sym == left:
			new_prods.append(prod)
		else:
			prods2 = left2prods[first_sym]
			for prod2 in prods2:
				new_prod = ProdExpr(left, prod2.rights + prod.rights[1:])
				new_prods.append(new_prod) 
	return new_prods			
				



def nonleft(left2prods):
	left = left2prods[0]
	new_left = left + "1"
	
	nl_left2prods[left] = []
	nl_left2prods[new_left] = []

	
	for prod in left2prods[1]:
		if prod.rights[0] == prod.left:
			new_prod = ProdExpr(new_left, prod.rights[1:] + [new_left])
			nl_prod_exprs.append(new_prod)
			nl_left2prods[new_left].append(new_prod)			
		else:
			new_prod = ProdExpr(left, prod.rights + [new_left])
			nl_prod_exprs.append(new_prod)
			nl_left2prods[left].append(new_prod)			
	
	# add void
	void = ProdExpr(new_left, [(None, None)])
	nl_prod_exprs.append(void)
	nl_left2prods[new_left].append(void)			
			
		

if __name__ == '__main__':
	p1 = ProdExpr('e', ['e', ('id', 'id')])
	p2 = ProdExpr('e', [('id', 'id')])
	left2prods = ('e', [ p1, p2])
	nonleft(left2prods)
	print(nl_prod_exprs)
	print(nl_left2prods)





