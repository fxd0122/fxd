trans_rule = {'q_0|1': ['q_0', 'a', 'R'], 'q_0|0': ['q_1', '0', 'L'], 'q_1|a': ['q_2', '1', 'R'], 'q_2|0': ['q_3', '0', 'R'],
              'q_3|1': ['q_3', 'b', 'R'], 'q_3|0': ['q_4', '0', 'L'], 'q_4|b': ['q_5', '1', 'R'], 'q_5|0': ['q_6', '0', 'R'],
              'q_6|1': ['q_6', 'c', 'R'], 'q_6|0': ['q_7', '0', 'L'], 'q_7|c': ['q_8', '1', 'R'], 'q_8|0': ['q_8', '0', 'R'],
              'q_8|$': ['q_9', '0', 'L'], 'q_9|0': ['q_10', '1', 'L'], 'q_10|1': ['q_10', '1', 'L'], 'q_10|0': ['q_11', '0', 'L'],
              'q_11|1': ['q_11', '1', 'L'], 'q_11|0': ['q_12', '0', 'L'], 'q_12|1': ['q_12', '1', 'L'], 'q_12|b': ['q_5', '1', 'R'],
              'q_5|1': ['q_5', '1', 'R'], 'q_8|1': ['q_8', '1', 'R'], 'q_12|0': ['q_13', '0', 'R'], 'q_13|1': ['q_13', '1', 'R'],
              'q_13|0': ['q_14', '0', 'R'], 'q_14|1': ['q_14', '$', 'R'], 'q_14|0': ['q_15', '$', 'R'], 'q_15|1': ['q_15', '1', 'R'],
              'q_15|0': ['q_15', '0', 'R'], 'q_15|$': ['q_16', '0', 'L'], 'q_16|0': ['q_16', '0', 'L'], 'q_16|1': ['q_16', '1', 'L'],
              'q_16|a': ['q_2', '1', 'R'], 'q_2|1': ['q_2', '1', 'R'], 'q_11|c': ['q_8', '1', 'R'], 'q_8|1': ['q_8', '1', 'R'],
              'q_16|$': ['q_f', '$', 'R']}

def Get_tape(x, y):
    tape = []
    for i in range(y):
        tape.append('1')
    tape.append('0')
    for i in range(x):
        tape.append('1')
    tape.append('0')
    tape.append('1')
    tape.append('0')
    tape.append('0')
    return tape

def TM_compute(tape, transform_rule):
    control = 'q_0'
    num = 0
    while(control != 'q_f'):
        flag = 0
        if num < len(tape):
            if num < 0:
                current_char = '$'
            else:
                current_char = tape[num]
        elif num == len(tape):
            current_char = '$'
        cur_state = control + '|' + current_char
        next_state =  transform_rule[cur_state]
        control = next_state[0]
        if (num < len(tape)) & (num >= 0):
            if next_state[1] == '$':
                tape.pop(num)
                flag = 1
            else:   tape[num] = next_state[1]
        elif num == len(tape):
            tape.append(next_state[1])
        if flag == 1:
            if next_state[2] == 'R':
                num = num
            if next_state[2] == 'L':
                num = num - 1
        else:
            if next_state[2] == 'R':
                num = num + 1
            if next_state[2] == 'L':
                num = num - 1

def Get_result(tape):
    _list = []
    for i in range(len(tape)):
        if tape[i] == '0':
            _list.append(i)
    return _list[2] - _list[1] - 1


if __name__ == '__main__':
    x = 9
    y = 3
    tape = Get_tape(x, y)
    print(tape)
    TM_compute(tape, trans_rule)
    # print(tape)
    result = Get_result(tape)
    print("{}^{}".format(x, y), "=", result)


