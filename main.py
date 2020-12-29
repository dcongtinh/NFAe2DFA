import numpy as np
from prettytable import PrettyTable

# Khởi tạo input
states = {1, 2, 3}  # trạng thái states
n_state = len(states) + 1  # độ dài tập trạng thái
alphabet = {'a', 'b', 'e'}  # bộ chữ cái nhập alphabet
# bộ chữ cái nhập không chứa epsilon
alphabet_without_e = [alp for alp in alphabet if alp != 'e']
# Hàm chuyển trạng thái
transition_function = {
    (1, 'a'): {3},
    (1, 'e'): {2},
    (2, 'a'): {1},
    (3, 'a'): {2},
    (3, 'b'): {2, 3},
}
start_state = {1}  # trạng thái bắt đầu
accept_states = {2}  # trạng thái kết thúc

# Tập các đỉnh kề
# Ex: ke[1] = [2, 3] # Đỉnh 1 có các đỉnh kề là 2, 3

ke = {}
for u in states:
    ke[u] = []

for key in transition_function.keys():
    u, w = key
    for v in transition_function[key]:
        ke[u].append((v, w))

# Mảng đánh dâu đã thăm các đỉnh
visited = [False] * n_state

# DFS tìm các đỉnh kề với u có nhãn epsilon và được lưu vào A
# Hay tính epsilon closure của u


def eClosure1(u, A):
    global visited
    visited[u] = True
    A.append(u)
    for v, w in ke[u]:
        if not visited[v] and w == 'e':
            eClosure1(v, A)

# Tính epsilon closure của tập các u


def eClosure(v):  # v: vector, set, array
    global visited
    A = np.array([], dtype='int')
    for u in v:
        tmp = []
        visited = [False] * n_state
        eClosure1(u, tmp)
        A = np.append(A, tmp, axis=0)
    return set(np.unique(A))

# Tính các giá trị của hàm chuyên


def transition_to_state(states, alp):
    v = set()
    for u in states:
        if (u, alp) in transition_function.keys():
            v = v | transition_function[(u, alp)]
    return v


def NFAe2DFA():
    d = {}  # Ánh xạ sang trạng thái mới A, B, C,...
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # Tính epsilon closure của trạng thái bắt đầu
    start = eClosure(start_state)
    d[tuple(start)] = labels[0]  # Đánh dấu là A
    # Thêm start vào tập chuyển trạng thái mới (Q') của DFA
    states_new = [start]
    idx, transition_function_new = 0, []
    while idx < len(states_new):
        isDone = True
        for alp in alphabet_without_e:
            t = transition_to_state(states_new[idx], alp)
            u = eClosure(t)
            if u != set() and u not in states_new:  # nếu u không có trong tập trạng thái Q' của DFA
                states_new.append(u)  # Thêm u vào tập trạng thái Q' của DFA
                d[tuple(u)] = labels[len(states_new)-1]
                u = d[tuple(u)]
                isDone = False
            elif u == set():
                u = 'oo'
            else:
                u = d[tuple(u)]

            transition_function_new.append(
                ((d[tuple(states_new[idx])], alp), u))
            # print(states_new[idx], '0', e)

        idx += 1
        if isDone:  # Không còn trạng thái nào chưa xét
            break
    return transition_function_new


def print_table(transition_function_new):
    transition_function_new = NFAe2DFA()

    header = ['']
    for alp in alphabet_without_e:
        header.append(alp)
    table = PrettyTable(header)
    table.align['Label'] = 'l'
    table.border = table.header = True

    for i in range(0, len(transition_function_new), 2):
        u = transition_function_new[i][0][0]
        row = [u]
        for j in range(len(alphabet_without_e)):
            try:
                u0 = transition_function_new[i+j][1]
            except:
                u0 = 'oo'
            row.append(u0)
        table.add_row(row)

    print(table)


if __name__ == '__main__':
    transition_function_new = NFAe2DFA()
    print_table(transition_function_new)
