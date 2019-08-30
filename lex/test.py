from dfa import simple_lex_by_expr, NFAMaker
import pytest




def test_answer():
	assert simple_lex_by_expr(['a'], 'a') == True 
	assert simple_lex_by_expr(['a'], 'b') == False 
	assert simple_lex_by_expr(['a'], '') == False 
	assert simple_lex_by_expr(['a', '|', 'c', '-', 'b'], 'cb') == True 
	assert simple_lex_by_expr(['a', '|', 'c', '-', 'b'], 'a') == True 
	assert simple_lex_by_expr(['a', '|', 'c', '-', 'b'], 'cb') == True 
	assert simple_lex_by_expr(['a','-','b'], 'ba') == False 

	assert simple_lex_by_expr(['a','-','(','b','|','a','*',')'], 'ab') == True 
	assert simple_lex_by_expr(['a','-','(','b','|','a','*',')'], 'a') == True 
	assert simple_lex_by_expr(['a','-','(','b','|','a','*',')'], 'aaaaaaaaaaaaaaaa') == True 
	
	assert simple_lex_by_expr(['a','-','(','b','|','a','*',')'], 'aaaaaaaaaaaaaaaab') == False







'''
执行语句为：pytest test.py

'''