"""
First homework of Formal Language and Automata.
G=(V, T, P, S) ε: $  T: #
"""
import argparse
import os
import random
from itertools import combinations

parser = argparse.ArgumentParser(description="##################")
parser.add_argument('--filedir', '-f')
args = parser.parse_args()
txt_path = args.filedir
Flag = 0 # 是否能通过NPDA

def BL_DFS(_dict, root):
    """
    Traverse that path of all leaf nodes of the tree
    """
    _stack = []
    _stack.append(root)
    remark = {}
    result = []
    while(len(_stack) != 0):
        if _stack[-1] in _dict.keys():
            if _stack[-1] not in remark.keys():
                remark[_stack[-1]] = []
            not_choce = list(set(_dict[_stack[-1]]).difference(set(remark[_stack[-1]])))
            if len(not_choce) == 0:
                _stack.pop()
            else:
                temp = random.choice(not_choce)
                remark[_stack[-1]].append(temp)
                _stack.append(temp)
        if(len(_stack) > 0):
            if _stack[-1] not in _dict.keys():
                a = _stack[:]
                result.append(a)
                _stack.pop()
    return result

def Is_Left_recursion(lift, right):
    is_lift_recursion = 0
    temp = right.split('|')
    for _t in temp:
        if _t[0] == lift:
            is_lift_recursion = 1
    return is_lift_recursion

def delete_direct_left_recursion(lift, right):
    Lift = []
    Lift.append(lift)
    Right = []
    temp = right.split('|')
    r1 = ''
    r2 = ''
    for _t in temp:
        _t_list = list(_t)
        if lift == _t_list[0]:
            _t_list.remove(lift)
            _t_list.append(lift + '_')
            t = ''.join(_t_list)
            r2 = r2 + t + '|'
        else:
            _t_list.append(lift + '_')
            t = ''.join(_t_list)
            r1 = r1 + t + '|'
    r1 = r1.replace('$', '')
    r2 = r2 + '$'
    Lift.append(lift + '_')
    Right.append(r1[:-1])
    Right.append(r2)
    return Lift, Right

def print_function(list_A, list_B):
    for i in range(len(list_A)):
        print(list_A[i]+'->'+list_B[i])

def to_list(str):
    str_list = list(str)
    if '_' in str:
        for item in str_list:
            if item == '_':
                index = str_list.index(item)
                str_list[index-1] = str_list[index-1]+'_'
                str_list.remove('_')
    if '.' in str:
        for item in str_list:
            if item == '.':
                index = str_list.index(item)
                str_list[index-1] = str_list[index-1]+'.'
                str_list.remove('.')
    # string -> list
    return str_list

def get_transform_rule(left, right):
    transform_rule = {}
    # 开始状态
    transform_rule['q_0$z'] = [('q_1', 'Sz')]
    # 结束转移
    transform_rule['q_1$z'] = [('q_f', 'z')]
    # 其他转移  
    num = len(left)
    for i in range(num):
        # current_trans = []
        cur_right = right[i].split('|')
        for item in cur_right:
            current_state = []
            current_state.append('q_1')
            current_state.append(item[0])
            current_state.append(left[i])
            if item[1:] == '':
                temp = [('q_1', '$')]
            else:
                temp = [('q_1', item[1:])]
            trans_left = ''.join(current_state)
            if trans_left in transform_rule.keys():
                transform_rule[trans_left].append(temp[0])
            else:
                transform_rule[trans_left] = temp
    # print(transform_rule)
    return transform_rule

def matching_fc(in_list, num, control, p_stack, transform_rule):
    if num < len(in_list):
        cur_match_char = in_list[num]
    elif num == len(in_list):
        cur_match_char = '$'
    elif (num == len(in_list)+1) & (control == 'q_f'):
        global Flag
        Flag = 1
        print("符合")
        return
    cur_state = control + cur_match_char + p_stack[-1]
    if cur_state in transform_rule.keys():
        for item in transform_rule[cur_state]:
            _control = item[0]
            _trans_state = to_list(item[1])
            _trans_state.reverse()
            _p_stack = p_stack[:]
            _p_stack.pop(-1)
            for i in _trans_state:
                if i != '$':
                    _p_stack.append(i)
            matching_fc(in_list, num+1, _control, _p_stack, transform_rule)
    else:
        return

class CFG2GreB():
    def __init__(self, filepath):
        self.filename = filepath
        self.num = 0 # 文法数量
        self.Str = []
        self.G_dict = {}
        self.Left = []
        self.Right = []
    
    def Get_CFG(self):
        f = open(self.filename, 'r')
        for line in f:
            line = line.strip()
            self.Str.append(line)
        f.close()
        self.num = len(self.Str)
        for str in self.Str:
            self.G_dict[str[0]] = str[3:] #CFG, such as S -> 0|0A|E
            self.Left.append(str[0]) # List of V, such as ['S', 'A']
            self.Right.append(str[3:]) # the formular: 0|0A|E
        print('#######初始文法########')
        print_function(self.Left, self.Right)
    
    def delete_useless_char(self):
        useful_char = [] # Useful V;
        _dict = {}
        # 将文法转换成树，用字典表示
        for i in range(len(self.Left)):
            temp = []
            formular = self.Right[i].split('|')
            for f in formular:
                flag = 0
                for t in self.Left:
                    if t in f: 
                        if t != self.Left[i]:
                            temp.append(t)
                        flag = 1
                if flag == 0:
                    if '$' == f:
                        temp.append('$')
                    else:
                        temp.append('#')
            if temp != []:
                _dict[self.Left[i]] = list(set(temp))
        # 遍历树 得到所有的从S出发的推导路径
        _result = BL_DFS(_dict, self.Left[0])
        # 得到无用符号及其索引
        for item in _result:
            if ('#' in item) | ('$' in item):
                for ch in item:
                    if ch not in ['#', '$']:
                        useful_char.append(ch)
        useful_char = list(set(useful_char))
        useless_char = list(set(self.Left).difference(useful_char))
        indexes = []
        for i in range(len(self.Left)):
            temp = self.Right[i].split('|')
            aa = []
            if self.Left[i] in useless_char:
                indexes.append(i)
            for _item in temp:
                for j in useless_char:
                    if j in _item:
                        aa.append(_item)
            temp = list(set(temp).difference(set(aa)))
            after_delete = ''
            for tt in temp:
                after_delete += tt+'|'
            self.Right[i] = after_delete[:-1]
        # 删除无用符号
        _times = 0
        for i in indexes:
            self.Right.pop(i - _times)
            self.Left.pop(i - _times)
            _times += 1
        print('#######消除无用符号########')
        # print(self.Left, self.Right)
        print_function(self.Left, self.Right)
    
    def delete_epsilon_generator(self):
        v_0 = [] # 可空集合
        self.num = len(self.Right)
        # 寻找可空变量
        for i in range(1, self.num):
            if '$' in self.Right[i]:
                v_0.append(self.Left[i])
        # print(v_0)
        # 去除ε产生式
        for i in range(self.num):
            temp = self.Right[i].split('|')
            _new_add = []
            for _t in temp:
                t_list = to_list(_t) # string -> list
                v0_in_t = list(set(v_0) & set(t_list)) # 当前产生式中的可空变量
                for j in range(1, len(v0_in_t)+1):
                    for _l in list(combinations(v0_in_t, j)):
                        _new = [_n for _n in t_list if _n not in list(_l)]
                        _new_add.append(''.join(_new))
            _temp = list(set(temp).union(set(_new_add)))
            if '' in _temp:
                _temp.remove('')
            # print(_temp)
            if i != 0: # 如果不是开始符号，删除产生式中的ε
                if '$' in _temp:
                    _temp.remove('$')
            after_delete = ''
            for tt in _temp:
                after_delete += tt+'|'
            self.Right[i] = after_delete[:-1]
        print('#######消除ε产生式########')
        print_function(self.Left, self.Right)

    def delete_Left_recursion(self):
        flag = 0
        self.num = len(self.Left)
        Var = self.Left[1:]
        Var.append(self.Left[0])
        for i in range(len(Var)): # 消除文法中的直接左递归
            if Is_Left_recursion(Var[i], self.G_dict[Var[i]]):
                _lift, _right = delete_direct_left_recursion(Var[i], self.G_dict[Var[i]])
                for ii in range(len(_lift)):
                        if _lift[ii] in self.Left:
                            index = self.Left.index(_lift[ii])
                            self.Right[index] = _right[ii]
                            self.G_dict[self.Left[index]] = _right[ii]
                        else:
                            self.Left.append(_lift[ii])
                            self.Right.append(_right[ii])
                            self.G_dict[_lift[ii]] = _right[ii]
        for i in range(len(Var)): # 消除文法中的间接左递归
            for j in range(i):
                if Var[j] in self.G_dict[Var[i]]: # 如果文法右边有之前的非终结符，带入替换
                    after_rep = []
                    cur = self.G_dict[Var[i]].split('|')
                    rep = self.G_dict[Var[j]].split('|')
                    for _c in cur:
                        if Var[j] in _c:
                            for _r in rep:
                                _c_list =  list(_c)
                                ind = _c_list.index(Var[j])
                                _c_list[ind] = _r
                                new_f = ''.join(_c_list)
                                after_rep.append(new_f)
                                # print(_c_list)
                        else:
                            after_rep.append(_c)
                    after_replace = ''
                    for tt in after_rep: # 判断代入之后是否存在直接左递归
                        if tt[0] == Var[i]:
                            flag = 1
                        after_replace += tt+'|'
                    self.G_dict[Var[i]] = after_replace[:-1]
                    if flag == 1: # 如果有直接左递归。消除直接左递归
                        new_lift, new_right = delete_direct_left_recursion(Var[i], self.G_dict[Var[i]])
                        for ii in range(len(new_lift)):
                            if new_lift[ii] in self.Left:
                                indx = self.Left.index(new_lift[ii])
                                self.Right[indx] = new_right[ii]
                                self.G_dict[self.Left[indx]] = new_right[ii]
                            else:
                                self.Left.append(new_lift[ii])
                                self.Right.append(new_right[ii])
                                self.G_dict[new_lift[ii]] = new_right[ii]              
        print('#######消除左递归########')
        print_function(self.Left, self.Right)

    def delete_singe_gnenrator(self):
        _queue = []        
        self.num = len(self.Left)
        # 得到链集合
        chain_set = {}
        for i in range(1, self.num):
            chain_set[self.Left[i]] = []
            _queue.append(self.Left[i])
            while(len(_queue) != 0):
                temp_list = self.G_dict[_queue[0]].split('|')
                for _t in temp_list:
                    if _t in self.Left:
                        _queue.append(_t)
                temp = _queue.pop(0)
                chain_set[self.Left[i]].append(temp)
        # 删除单一产生式
        for key in chain_set.keys():
            new_right = []
            cur_chain_set = chain_set[key][:]
            while(len(cur_chain_set) != 0):
                temp = self.G_dict[cur_chain_set[0]].split('|')
                for _t in temp:
                    new_right.append(_t)
                cur_chain_set.pop(0)
            # print(new_right)
            for value in chain_set[key]:
                if value in new_right:
                    new_right.remove(value)
            after_delete = ''
            for tt in new_right:
                after_delete += tt + '|'
            index = self.Left.index(key)
            self.Right[index] = after_delete[:-1]
        print('#######消除单一产生式########')
        print_function(self.Left, self.Right)

    def Is_V_at_first(self, _right):
        flag = 0
        v_at_first = []
        right_list = _right.split('|')
        for f in right_list:
            f_list = to_list(f) # string -> list
            if f_list[0] in self.Left:
                flag = 1
                v_at_first.append(f_list[0])
        return flag, v_at_first

    def to_GreiBach(self):
        self.num = len(self.Left)
        # 迭代消除非终结符号开始的文法
        flag = 1
        for i in range(self.num):
            while(flag):
                flag, v_at_first = self.Is_V_at_first(self.Right[i])
                v_rep = {}
                for v in v_at_first:
                    v_rep[v] = self.G_dict[v].split('|')
                right_list = self.Right[i].split('|')
                for r in right_list:
                    r_list = to_list(r) # string -> list
                    if r_list[0] in v_at_first:
                        for rep in v_rep[r_list[0]]:
                            r_list[0] = rep
                            new_r = ''.join(r_list)
                            right_list.append(new_r)
                        right_list.remove(r)
                after_replace = ''
                for tt in right_list:
                    after_replace += tt + '|'
                self.Right[i] =  after_replace[:-1]                
            flag = 1

        # 转换成GreiBach范式
        for j in range(self.num):
            temp_Right = self.Right[j].split('|')
            for _t in range(len(temp_Right)):
                t_list = to_list(temp_Right[_t])
                for _j in range(1, len(t_list)):
                    if t_list[_j] not in self.Left:
                        temp = t_list[_j]
                        t_list[_j] = t_list[_j].upper() + '.'
                        if t_list[_j] not in self.Left:
                            self.Left.append(t_list[_j])
                            self.Right.append(temp)
                temp_Right[_t] = ''.join(t_list)
            after_sub = ''
            for tt in temp_Right:
                after_sub += tt + '|'
            self.Right[j] = after_sub[:-1]   
        print('#######转换成Greibach范式########')
        print_function(self.Left, self.Right)

    def is_cfg(self, input):
        if input == '':
            if '$' in self.Right[0].split('|'):
                print('#######是否符合NPDA########')
                print("测试语言：", '$')
                print("符合")
            else:
                print('#######是否符合NPDA########')
                print("测试语言：", input)
                print("bu符合")
        else:
            input_list = list(input)
            transform_rule = get_transform_rule(self.Left, self.Right) 
            _stack = [] # 下推栈
            _stack.append('z') #栈的开始符号
            # 引入开始转移
            trans_state = transform_rule['q_0$z']
            _control = trans_state[0][0]
            _stack.pop(-1)
            trans_list = to_list(trans_state[0][1])
            trans_list.reverse()
            for i in trans_list:
                _stack.append(i)
            # 开始匹配
            print('#######是否符合NPDA########')
            print("测试语言：", input)
            matching_fc(input_list, 0, _control, _stack, transform_rule)
            # print('#######是否符合NPDA########')
            if Flag == 0:
                print("不符合")         

     
if __name__ == '__main__':
    c2g = CFG2GreB(r'E:\py_code\Master\CFG.txt')
    c2g.Get_CFG()
    c2g.delete_Left_recursion()
    c2g.delete_useless_char()
    c2g.delete_singe_gnenrator()
    c2g.delete_epsilon_generator()
    c2g.to_GreiBach()
    c2g.is_cfg('')
    # c2g.delete_useless_char()
    # c2g.delete_epsilon_generator()

