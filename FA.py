class NFA:
    current_states = None

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_states = start_state

    def transition_to_state_with_input(self, input_value):

        res = set()
        for item in self.current_states:
            if (item, input_value) not in self.transition_function.keys():
                continue
            else:
                # tồn tại đường đi từ trạng thái hiện tại trên input_value
                res = res | self.transition_function[(item, input_value)]
        self.current_states = res

    def in_accept_state(self):

        return self.current_states & self.accept_states

    def go_to_initial_state(self):
        self.current_states = self.start_state

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        print("trang thai bat dau la:", self.start_state)
        print("chuoi can kiem tra la:", input_list)
        for inp in input_list:
            if inp not in self.alphabet:
                print("Ton tai ky tu khong thuoc bo chu cai nhap")
                return
            self.transition_to_state_with_input(inp)
        return self.in_accept_state()
