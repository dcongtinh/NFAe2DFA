from FA import NFAe

# Khởi tạo input
states = {1, 2, 3}  # trạng thái states
alphabet = {'a', 'b', 'e'}  # bộ chữ cái nhập alphabet
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

nfa = NFAe(states, alphabet, transition_function,
           start_state, accept_states)

transition_function_new = nfa.toDFA()
nfa.printDFA(transition_function_new)
