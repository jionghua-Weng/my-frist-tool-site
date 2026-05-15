def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "错误：除数不能为零"
    return a / b


def main():
    print("简易计算器")
    print("操作选项：+  -  *  /")

    try:
        a = float(input("请输入第一个数字："))
        op = input("请输入运算符：").strip()
        b = float(input("请输入第二个数字："))
    except ValueError:
        print("输入无效，请输入数字。")
        return

    ops = {"+": add, "-": subtract, "*": multiply, "/": divide}

    if op not in ops:
        print("不支持的运算符。")
        return

    result = ops[op](a, b)
    print(f"结果：{a} {op} {b} = {result}")


if __name__ == "__main__":
    main()
