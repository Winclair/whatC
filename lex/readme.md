#### 重要类用途

Lex(一个DFA): 文本 ----> tokens

Lex_by_NFA:  文本 ----> tokens

DFA: NFA ----> DFA

NFAMaker： 正则表达式---->NFA

NFA: 一个不确定自动机


#### 数据结构

##### 正则表达式
* 操作符： * | -
* 存储: ab*|d ------> ['a', '-', 'b', '*', '|', 'd'] ，其中*表达式为'\*'


##### NFA
* NFANode：tag(非接收结点为None, 接收结点为对象的标签)、edge: { 边字符 : 目标结点集合, ... }

* NFA: start_node、 end_node

* 方法：NFA的连接、合并、星号运算


##### Lex_by_NFA
* 方法
analyze: 启动分析器，得到tokens
error: 错误处理，打印错误所在行数、单词、并报错、退出程序


#### 依赖与构造流程
* NFAMaker: 正则表达式 --> 后缀表达式 --> NFA基本运算 --> 最终NFA

* Lex_by_NFA:  文本 --> NFAMaker.nfa --> tokens  

