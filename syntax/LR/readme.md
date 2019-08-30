#### 数据结构

prod_exprs列表[ ProdExpr类(left、right), ...]

left2prods = { X:[prod_index, ...], ...}


项item(包含点位置的ProdExpr): (prods_index, dot_pos)

LR(0)自动机结点：

core_items列表、非内核项列表(closure方法生成)、边集edge{symbol:Node}、


goto字典：{ X: [items] }, 所有A->.X到A->X.(item)的转换 


states列表：依次创建的LRNone

unfin_nodes: 队列，为完成edge属性的LRNode

LRtable分析表：
actions = [ {end_symbol:('s'/'r', state_index/prod_index), ...}, ...]


#### 符号约定
a: 终结字符
A: 非终结字符
X: a|A


#### 左递归消除
a -> a ID | ID
转换为：
a->ID a1, a1 -> a a1 | None  


#### 程序逻辑
---->: 生成

函数get_prod_exprs---->全局变量(prod_exprs, left2prods) ----> LRNode ----> LRDFA ----> 

LRTable -----> LRSyner 





