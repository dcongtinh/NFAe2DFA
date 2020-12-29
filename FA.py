import numpy as np
from prettytable import PrettyTable


class NFAe:
    current_states = None

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        # Khởi tạo input
        self.states = states
        self.n_state = len(states) + 1  # độ dài tập trạng thái
        self.alphabet = alphabet
        # Bộ chữ cái nhập không chứa epsilon
        self.alphabet_without_e = [alp for alp in alphabet if alp != 'e']
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_states = start_state
        # Tập các đỉnh kề
        # Ex: ke[1] = [2, 3] # Đỉnh 1 có các đỉnh kề là 2, 3
        ke = {}
        for u in states:
            ke[u] = []
        for key in transition_function.keys():
            u, w = key
            for v in transition_function[key]:
                ke[u].append((v, w))
        self.ke = ke
        # Mảng đánh dấu đỉnh đã duyệt
        self.visited = [False] * self.n_state

    def eClosure1(self, u, A):
        self.visited[u] = True
        A.append(u)
        for v, w in self.ke[u]:
            if not self.visited[v] and w == 'e':
                self.eClosure1(v, A)

    # Tính epsilon closure của tập các u

    def eClosure(self, v):  # v: vector, set, array
        A = np.array([], dtype='int')
        for u in v:
            tmp = []
            self.visited = [False] * self.n_state
            self.eClosure1(u, tmp)
            A = np.append(A, tmp, axis=0)
        return set(np.unique(A))

    # Tính các giá trị của hàm chuyên

    def transition_to_state(self, states, alp):
        v = set()
        for u in states:
            if (u, alp) in self.transition_function.keys():
                v = v | self.transition_function[(u, alp)]
        return v

    def in_accept_states(self, states):
        return (states & self.accept_states) != set()

    def toDFA(self):
        d = {}  # Ánh xạ sang trạng thái mới A, B, C,...
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # Tính epsilon closure của trạng thái bắt đầu
        start = self.eClosure(self.start_state)
        d[tuple(start)] = labels[0]  # Đánh dấu là A
        # Thêm start vào tập chuyển trạng thái mới (Q') của DFA
        states_new = [start]
        idx, transition_function_new = 0, []
        while idx < len(states_new):
            for alp in self.alphabet_without_e:
                t = self.transition_to_state(states_new[idx], alp)
                u = self.eClosure(t)
                if u != set() and u not in states_new:  # nếu u không có trong tập trạng thái Q' của DFA
                    # Thêm u vào tập trạng thái Q' của DFA
                    states_new.append(u)
                    d[tuple(u)] = labels[len(states_new)-1]
                    u = d[tuple(u)]
                elif u == set():
                    u = 'oo'
                else:
                    u = d[tuple(u)]
                transition_function_new.append(
                    ((d[tuple(states_new[idx])], alp), u))
                # print(states_new[idx], '0', e)

            idx += 1
        return transition_function_new

    def printDFA(self, transition_function_new):
        header = ['']
        for alp in self.alphabet_without_e:
            header.append(alp)
        table = PrettyTable(header)
        table.align['Label'] = 'l'
        table.border = table.header = True

        for i in range(0, len(transition_function_new), 2):
            u = transition_function_new[i][0][0]
            row = [u]
            for j in range(len(self.alphabet_without_e)):
                try:
                    u0 = transition_function_new[i+j][1]
                except:
                    u0 = 'oo'
                row.append(u0)
            table.add_row(row)

        print(table)

    def check(self, w):
        print("Chuoi " + w + " co thuoc ngon ngu da cho?")
        q = self.eClosure(self.start_state)
        for c in w:
            t = self.transition_to_state(q, c)
            q = self.eClosure(t)
        if self.in_accept_states(q):
            print("YES")
        else:
            print("NO")
