# 有穷自动机.py

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

        # 状态的语义化映射（用于演示和输出打印）
        self.state_desc = {
            0: "初始状态",
            1: "符号位",
            2: "整数部分",
            3: "起始小数点",
            4: "小数部分",
            5: "指数符号(E)",
            6: "指数符号位",
            7: "指数部分"
        }

    def _get_input_type(self, char):
        # 编译原理优化：严格限制为 ASCII 数字 0-9，避免 char.isdigit() 把 '²' 或 '１' 认作数字
        if '0' <= char <= '9': return 0
        if char in ('+', '-'): return 1
        if char == '.': return 2
        if char in ('e', 'E'): return 3
        return None

    def validate(self, text):
        current_state = 0
        path = [f"(q0: {self.state_desc[0]})"]

        for char in text:
            input_type = self._get_input_type(char)

            # 处理非法字符或没有定义转移的情况
            if input_type is None or input_type not in self.transitions[current_state]:
                path.append(f"--['{char}' 💥非法转移]--> 拒绝 (死状态)")
                print("   " + "\n   ".join(path))
                return False

            # 状态转移
            next_state = self.transitions[current_state][input_type]
            path.append(f"--['{char}']--> (q{next_state}: {self.state_desc[next_state]})")
            current_state = next_state

        is_accepted = current_state in self.accept_states

        # 打印转移路径
        print("   " + "\n   ".join(path))

        if is_accepted:
            print(f"\n✅ 结果: 【接受】 (最终停留在接受状态 q{current_state})")
        else:
            print(f"\n❌ 结果: 【拒绝】 (最终停在非接受状态 q{current_state})")

        return is_accepted


if __name__ == "__main__":
    dfa = FloatDFA()

    print("=" * 60)
    print(" 🤖 浮点数词法分析器 - 有穷自动机 (DFA) ")
    print("=" * 60)
    print("本程序使用 DFA 识别合法的浮点数字面量，支持科学计数法。")
    print("合法示例：+3.14, -1e-10, .5, 12., 1.2.3(非法)")
    print("输入 'q' 或 'exit' 退出程序。\n")

    # 交互式人工测试循环
    while True:
        try:
            user_input = input("\n👉 请输入要校验的字符串: ").strip()

            if user_input.lower() in ['q', 'quit', 'exit']:
                print("程序已退出。👋")
                break

            if not user_input:
                continue

            print(f"\n开始校验: '{user_input}'")
            print("-" * 40)
            dfa.validate(user_input)
            print("-" * 40)

        except KeyboardInterrupt:
            print("\n程序已退出。👋")
            break