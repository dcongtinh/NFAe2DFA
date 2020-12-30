from FA import NFAe

# Nhập input
states = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}  # trạng thái states
alphabet = {'a', 'b', 'ε'}  # bộ chữ cái nhập alphabet
alphabet = sorted(alphabet)

# Hàm chuyển trạng thái
transition_function = {
    (0, 'ε'): {1, 7},
    (1, 'ε'): {2, 4},
    (2, 'a'): {3},
    (3, 'ε'): {6},
    (4, 'b'): {5},
    (5, 'ε'): {6},
    (6, 'ε'): {1, 7},
    (7, 'a'): {8},
    (8, 'b'): {9},
    (9, 'b'): {10},
}


start_state = {0}  # trạng thái bắt đầu
accept_states = {10}  # trạng thái kết thúc

nfae = NFAe(states, alphabet, transition_function,
            start_state, accept_states)

# nfae.printNFAe()
nfae.toDFA()
nfae.printNFAeFuncTable()
nfae.printDFAFuncTable()
# nfae.printGraph('NFAe')
# nfae.printGraph('DFA')

# w = "aaaaaaabb"
# nfae.check(w)
