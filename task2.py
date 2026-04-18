class FloatDFA:
    def __init__(self):
        # 定义转移表：(当前状态, 输入类型) -> 下一个状态
        # 输入类型定义：0:数字, 1:正负号, 2:点, 3:指数符号(e/E)
        self.transitions = {
            0: {0: 2, 1: 1, 2: 3},
            1: {0: 2, 2: 3},
            2: {0: 2, 2: 4, 3: 5},
            3: {0: 4},
            4: {0: 4, 3: 5},
            5: {0: 7, 1: 6},
            6: {0: 7},
            7: {0: 7}
        }
        # 接受状态（合法的数值结尾）
        self.accept_states = {2, 4, 7}

    def _get_input_type(self, char):
        if char.isdigit(): return 0
        if char in ('+', '-'): return 1
        if char == '.': return 2
        if char in ('e', 'E'): return 3
        return None

    def validate(self, text):
        current_state = 0

        print(f"开始校验字符串: '{text}'")
        for char in text:
            input_type = self._get_input_type(char)
            if input_type is None or input_type not in self.transitions[current_state]:
                print(f"  -> 字符 '{char}' 导致非法转移，拒绝。")
                return False

            current_state = self.transitions[current_state][input_type]
            print(f"  -> 读取 '{char}', 进入状态 {current_state}")

        is_accepted = current_state in self.accept_states
        print(f"最终状态: {current_state}, 结果: {'接受' if is_accepted else '拒绝'}\n")
        return is_accepted


# --- 测试用例 ---
dfa = FloatDFA()
test_cases = ["+3.14", "1e-10", ".5", "12.", "abc", "1.2.3"]

for case in test_cases:
    dfa.validate(case)