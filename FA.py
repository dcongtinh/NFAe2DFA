import cv2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from utils import textcolor_display, remove_textcolor
from networkx.drawing.nx_agraph import to_agraph


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
        self.start_state_dfa = []
        self.accept_states_dfa = []
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

    def in_start_state(self, state):
        return (state & self.start_state) != set()

    def get_label_color(self, state, label):
        if self.in_start_state(state):
            self.start_state_dfa.append(label)
            return textcolor_display(label, 'start')

        if self.in_accept_states(state):
            self.accept_states_dfa.append(label)
            return textcolor_display(label, 'end')

        return label

    def toDFA(self):
        d = {}  # Ánh xạ sang trạng thái mới A, B, C,...
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # Tính epsilon closure của trạng thái bắt đầu
        start = self.eClosure(self.start_state)
        d[tuple(start)] = self.get_label_color(
            start, labels[0])  # Đánh dấu là A
        # Thêm start vào tập chuyển trạng thái mới (Q') của DFA
        states_new = [start]
        idx, transition_function_dfa = 0, []
        while idx < len(states_new):
            for alp in self.alphabet_without_e:
                t = self.transition_to_state(states_new[idx], alp)
                u = self.eClosure(t)
                if u != set() and u not in states_new:  # nếu u không có trong tập trạng thái Q' của DFA
                    # Thêm u vào tập trạng thái Q' của DFA
                    states_new.append(u)

                    d[tuple(u)] = self.get_label_color(
                        u, labels[len(states_new)-1])
                    u = d[tuple(u)]
                elif u == set():
                    u = 'oo'
                else:
                    u = d[tuple(u)]
                transition_function_dfa.append(
                    ((d[tuple(states_new[idx])], alp), u))
                # print(states_new[idx], '0', e)

            idx += 1
        return transition_function_dfa

    def printDFA(self, transition_function_dfa, table=True, graph=True):
        header = ['']
        for alp in self.alphabet_without_e:
            header.append(alp)
        _table = PrettyTable(header)
        _table.align['Label'] = 'l'
        _table.border = _table.header = True

        G = nx.MultiDiGraph()
        G.add_nodes_from(self.start_state_dfa, penwidth=2.0, color="blue")
        G.add_nodes_from([' '], penwidth=0.0)
        for u in self.start_state_dfa:
            G.add_edge(' ', u, label=' Start', penwidth=2.0)
        G.add_nodes_from(self.accept_states_dfa, penwidth=2.0, color="red")
        for i in range(0, len(transition_function_dfa), 2):
            u = transition_function_dfa[i][0][0]
            row = [u]
            for j in range(len(self.alphabet_without_e)):
                w = self.alphabet_without_e[j]
                try:
                    v = transition_function_dfa[i+j][1]
                    _u = remove_textcolor(u)
                    _v = remove_textcolor(v)
                    G.add_edge(_u, _v, label=' ' + w)
                except:
                    v = 'oo'
                row.append(v)
            _table.add_row(row)

        if table:
            print(_table)

        if graph:
            G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
            G.graph['graph'] = {'scale': '14'}

            A = to_agraph(G)
            A.layout('dot')
            filename = 'DFA.png'
            A.draw(filename)
            dfa = cv2.imread(filename)
            cv2.imshow('DFA', dfa)
            cv2.waitKey(0)

            # closing all open windows
            cv2.destroyAllWindows()

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
