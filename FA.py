import cv2
import numpy as np
import networkx as nx
from prettytable import PrettyTable
from networkx.drawing.nx_agraph import to_agraph
from utils import textcolor_display, remove_textcolor


class NFAe:
    current_states = None

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        # Khởi tạo input
        self.states = states
        self.n_state = len(states) + 1  # độ dài tập trạng thái
        self.alphabet = alphabet
        # Bộ chữ cái nhập không chứa epsilon
        self.alphabet_without_e = [alp for alp in alphabet if alp != 'ε']
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
            if not self.visited[v] and w == 'ε':
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

    def in_accept_states(self, states, name='NFAe'):
        accept_states = {}
        if name == 'NFAe':
            accept_states = self.accept_states

        elif name == 'DFA':
            accept_states = set(self.accept_states_dfa)

        return (states & accept_states) != set()

    def in_start_state(self, state, name='NFAe'):
        start_state = {}
        if name == 'NFAe':
            start_state = self.start_state

        elif name == 'DFA':
            start_state = set(self.start_state_dfa)

        return (state & start_state) != set()

    def get_label_color(self, state, label):
        if self.in_start_state(state, 'DFA'):
            return textcolor_display(str(label), 'start')

        if self.in_accept_states(state, 'DFA'):
            return textcolor_display(str(label), 'end')

        return label

    def toDFA(self):
        d = {}  # Ánh xạ sang trạng thái mới A, B, C,...
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.keDFA = {}
        for label in labels:
            self.keDFA[label] = []
        self.states_dfa = {'A'}
        self.start_state_dfa = {'A'}
        self.accept_states_dfa = set()
        # Tính epsilon closure của trạng thái bắt đầu
        start = self.eClosure(self.start_state)
        d[tuple(start)] = labels[0]  # Đánh dấu là A
        # Thêm start vào tập chuyển trạng thái mới (Q') của DFA
        states_new = [start]
        idx = 0

        while idx < len(states_new):
            for alp in self.alphabet_without_e:
                t = self.transition_to_state(states_new[idx], alp)
                v = self.eClosure(t)
                if v != set() and v not in states_new:  # nếu v không có trong tập trạng thái Q' của DFA
                    # Thêm v vào tập trạng thái Q' của DFA
                    states_new.append(v)
                    label = labels[len(states_new)-1]
                    d[tuple(v)] = label
                    self.states_dfa.add(label)
                    if self.in_start_state(v):
                        self.start_state_dfa.add(d[tuple(v)])

                    if self.in_accept_states(v):
                        self.accept_states_dfa.add(d[tuple(v)])
                    v = d[tuple(v)]
                elif v == set():
                    v = 'oo'
                else:
                    v = d[tuple(v)]
                self.keDFA[d[tuple(states_new[idx])]].append((v, alp))
            idx += 1
        self.states_dfa = sorted(self.states_dfa)
        self.start_state_dfa = sorted(self.start_state_dfa)
        self.accept_states_dfa = sorted(self.accept_states_dfa)

    def printGraph(self, name="DFA"):
        if name == "NFAe":
            states = self.states
            start_state = self.start_state
            accept_states = self.accept_states
            ke = self.ke
        else:
            states = self.states_dfa
            start_state = self.start_state_dfa
            accept_states = self.accept_states_dfa
            ke = self.keDFA

        G = nx.MultiDiGraph()
        G.add_nodes_from(tuple(start_state), penwidth=2.0, color="blue")
        G.add_nodes_from([' '], penwidth=0.0)
        for u in start_state:
            G.add_edge(' ', u, label=' Start', penwidth=2.0)
        G.add_nodes_from(tuple(accept_states), penwidth=2.0, color="red")

        for u in states:
            for v, w in ke[u]:
                G.add_edge(u, v, label=' ' + w)

        G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
        G.graph['graph'] = {'scale': '14'}

        A = to_agraph(G)
        A.layout('dot')
        filename = name + '.png'
        A.draw(filename)
        fig = cv2.imread(filename)
        cv2.imshow(name, fig)
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()
        pass

    def printDFAFuncTable(self):
        header = ['']
        for alp in self.alphabet_without_e:
            header.append(alp)
        table = PrettyTable(header)
        table.align['Label'] = 'l'
        table.border = table.header = True
        for u in self.states_dfa:
            row = [self.get_label_color({u}, u)]
            for v, w in self.keDFA[u]:
                row.append(self.get_label_color({v}, v))
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
