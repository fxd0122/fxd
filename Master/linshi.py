import random

dict_G = {'S': ['A', 'E', '#'], 'A': ['B', '$'], 'B': ['C'], 'C': ['#'], 'D':["#"]}
_Tree = {'A': ['B', 'C'], 'B': ['D', 'E'], 'D': ['F'], }

def BL_BFS(_dict, root):
    _queue = []
    _queue.append(root)
    result = []
    while(len(_queue) != 0):
        if _queue[0] not in _dict.keys():
            temp = _queue.pop(0)
            print(temp)
        else:
            for i in _dict[_queue[0]]:
                _queue.append(i)
            temp = _queue.pop(0)
            print(temp)

def BL_DFS(_dict, root):
    _stack = []
    _stack.append(root)
    remark = {}
    # remark.append(root)
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




def find_useful_char(_dict):
    _v = [] #推出非终结符
    _t = [] #推出终结符
    useful_char = []
    for key in _dict.keys():
        if ('#' in _dict[key]) | ('$' in _dict[key]):
            _t.append(key)
        for v in _dict[key]:
            if v in _dict.keys():
                _v.append(key)
    for v in _v:
        for i in _dict[v]:
            if i in _t:
                _v.append(0)
    return useful_char

def delete_direct_lift_recursion(lift, right):
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
            r1 = r1 + t + '|'
        else:
            _t_list.append(lift + '_')
            t = ''.join(_t_list)
            r2 = r2 + t + '|'
    r2 = r2 + '$'
    Lift.append(lift + '_')
    Right.append(r1[:-1])
    Right.append(r2)
    print(Lift, Right)

def to_list(str):
    str_list = list(str)
    if '_' in str:
        index = str_list.index('_')
        str_list[index-1] = str_list[index-1]+'_'
        str_list.remove('_')
    if '.' in str:
        index = str_list.index('.')
        str_list[index-1] = str_list[index-1]+'.'
        str_list.remove('.')
    # string -> list
    return str_list

if __name__ == '__main__':
    # BL_BFS(_Tree, 'A')
    # a = BL_DFS(_Tree, 'A')
    txt = 'a'
    temp = to_list(txt)
    print(txt.upper())

    """
    lift = 'ABC_D'
    if '_' in lift:
        _l = list(lift)
        index = _l.index('_')
        _l[index-1] = _l[index-1]+'_'
        _l.remove('_')
        print(_l)
    else:
        _l = list(lift)
        print(_l)    
    # delete_direct_lift_recursion(lift, right)
    Aa = '0|1|0C|1C'
    b = Aa.split('|')
    _list = list(b[2])
    a = list(set(['0']) & set(_list))
    from itertools import combinations
    List = [1,2,3]
    c = list(combinations(List,3))
    l1 = ['1','2','3','4']
    l2 = ['3','4','5','6']
    list3=[new for new in l1 if new not in l2]
    print(list3)
    from itertools import combinations
    a = ['A', 'B', 'C', 'A', '']
    b = a[:]
    print(b.reverse())
    x = [c.replace('A','#') for c in a]
    print(x)
    b = ['A', 'B']
    c = []
    for i in range(1, len(b)+1):
        for _l in list(combinations(b, i)):
            _new = [n for n in a if n not in list(_l)]
            c.append(''.join(_new))
    print(len(c))
    """

