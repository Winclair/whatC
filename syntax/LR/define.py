
end_expr = {'VOID':(None, None), 'ID':('id', 'id'), 'NUM':('num','num'), 'STRING':('string','string'), 'BASIC':('keyword','BASIC')}

limiter = [';','[',']','(',')','{','}']

operator = ['+','-','*','/','!','%','^','&','=','|','<','<','>>','++','--','>','<']


def is_endsym(symbol):
	return type(symbol)==tuple
