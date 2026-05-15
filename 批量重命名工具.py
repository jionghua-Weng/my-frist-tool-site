# -*- coding: utf-8 -*-
"""
批量重命名工具
功能：给文件夹里的文件批量添加前缀/后缀，修改前预览效果，确认后执行。
兼容：Python 3.6+，仅使用标准库，无需安装第三方依赖。
"""

import os
import sys


# === 获取文件夹中的文件列表 ===
def 获取文件列表(文件夹路径):
    """返回指定文件夹中所有文件的文件名列表（不含子目录）"""
    try:
        所有项 = os.listdir(文件夹路径)
        文件列表 = []
        for 项 in 所有项:
            完整路径 = os.path.join(文件夹路径, 项)
            if os.path.isfile(完整路径):
                文件列表.append(项)
        return sorted(文件列表)
    except FileNotFoundError:
        print("错误：找不到文件夹「{}」，请检查路径是否正确。".format(文件夹路径))
        return None
    except PermissionError:
        print("错误：没有权限访问文件夹「{}」。".format(文件夹路径))
        return None
    except Exception as e:
        print("错误：读取文件夹时发生意外错误：{}".format(e))
        return None


# === 预览重命名效果 ===
def 预览效果(文件列表, 前缀, 后缀, 文件夹路径):
    """打印重命名前后的对比预览"""
    if not 文件列表:
        print("文件夹「{}」中没有文件。".format(文件夹路径))
        return False

    print("\n" + "=" * 60)
    print("预览重命名效果（共 {} 个文件）：".format(len(文件列表)))
    print("=" * 60)
    print("{:<4s}  {:<35s}  →  {:<35s}".format("序号", "原文件名", "新文件名"))
    print("-" * 60)

    变更计数 = 0
    for 序号, 原文件名 in enumerate(文件列表, 1):
        名称, 扩展名 = os.path.splitext(原文件名)
        新文件名 = 前缀 + 名称 + 后缀 + 扩展名
        if 原文件名 != 新文件名:
            变更计数 += 1
            # 截断过长文件名以保证表格对齐
            原文件显示 = 原文件名 if len(原文件名) <= 32 else 原文件名[:29] + "..."
            新文件显示 = 新文件名 if len(新文件名) <= 32 else 新文件名[:29] + "..."
            print("{:<4d}  {:<35s}  →  {:<35s}".format(序号, 原文件显示, 新文件显示))
        else:
            print("{:<4d}  {:<35s}  →  （无变化）".format(序号, 原文件名[:32]))

    print("-" * 60)
    print("共 {} 个文件，其中 {} 个将被重命名。".format(len(文件列表), 变更计数))

    if 变更计数 == 0:
        print("提示：指定的前缀和后缀没有带来任何变化，无需执行。")
        return False

    return True


# === 执行批量重命名 ===
def 执行重命名(文件列表, 前缀, 后缀, 文件夹路径):
    """逐个执行文件重命名，返回成功和失败的计数"""
    成功数 = 0
    失败数 = 0

    for 原文件名 in 文件列表:
        名称, 扩展名 = os.path.splitext(原文件名)
        新文件名 = 前缀 + 名称 + 后缀 + 扩展名

        if 原文件名 == 新文件名:
            continue

        原路径 = os.path.join(文件夹路径, 原文件名)
        新路径 = os.path.join(文件夹路径, 新文件名)

        # 检查新文件名是否已存在
        if os.path.exists(新路径):
            print("警告：目标文件「{}」已存在，跳过「{}」。".format(新文件名, 原文件名))
            失败数 += 1
            continue

        try:
            os.rename(原路径, 新路径)
            print("成功：{} → {}".format(原文件名, 新文件名))
            成功数 += 1
        except PermissionError:
            print("失败：「{}」已被占用或没有权限重命名。".format(原文件名))
            失败数 += 1
        except Exception as e:
            print("失败：「{}」重命名出错：{}".format(原文件名, e))
            失败数 += 1

    return 成功数, 失败数


# === 获取用户输入 ===
def 获取用户输入():
    """交互式获取文件夹路径、前缀和后缀"""

    # --- 文件夹路径 ---
    while True:
        文件夹路径 = input("请输入文件夹路径：").strip()
        if 文件夹路径.startswith('"') and 文件夹路径.endswith('"'):
            文件夹路径 = 文件夹路径[1:-1]
        if not 文件夹路径:
            print("提示：文件夹路径不能为空，请重新输入。")
            continue
        if not os.path.exists(文件夹路径):
            print("提示：路径不存在，请重新输入。")
            continue
        if not os.path.isdir(文件夹路径):
            print("提示：该路径不是一个文件夹，请重新输入。")
            continue
        break

    # --- 前缀 ---
    前缀 = input("请输入要添加的前缀（不需要则直接回车）：").strip()
    if 前缀:
        # 检查前缀是否包含非法文件名字符
        非法字符 = set(r'<>:"/\|?*')
        if set(前缀) & 非法字符:
            print("警告：前缀包含文件名字符中的非法字符，已自动去除。")
            前缀 = "".join(c for c in 前缀 if c not in 非法字符)

    # --- 后缀 ---
    后缀 = input("请输入要添加的后缀（不需要则直接回车）：").strip()
    if 后缀:
        非法字符 = set(r'<>:"/\|?*')
        if set(后缀) & 非法字符:
            print("警告：后缀包含文件名字符中的非法字符，已自动去除。")
            后缀 = "".join(c for c in 后缀 if c not in 非法字符)

    # --- 检查是否至少指定了一个 ---
    if not 前缀 and not 后缀:
        print("提示：前缀和后缀都为空，没有可执行的操作。")
        return None, None, None

    return 文件夹路径, 前缀, 后缀


# === 主函数 ===
def main():
    """批量重命名工具入口"""
    print("=" * 40)
    print("     批量重命名工具")
    print("     支持添加前缀 / 后缀")
    print("=" * 40)

    # 获取用户输入
    结果 = 获取用户输入()
    if 结果 is None:
        return
    文件夹路径, 前缀, 后缀 = 结果

    # 获取文件列表
    文件列表 = 获取文件列表(文件夹路径)
    if 文件列表 is None:
        return

    # 预览效果
    if not 预览效果(文件列表, 前缀, 后缀, 文件夹路径):
        return

    # 确认执行
    print()
    确认 = input("确认执行以上重命名操作？（输入 y 确认，其他任意键取消）：").strip().lower()
    if 确认 != "y":
        print("已取消操作，没有文件被修改。")
        return

    # 执行重命名
    print("\n正在执行重命名...")
    成功数, 失败数 = 执行重命名(文件列表, 前缀, 后缀, 文件夹路径)

    # 输出结果
    print("\n" + "=" * 40)
    print("重命名完成！成功：{} 个，失败：{} 个。".format(成功数, 失败数))
    print("=" * 40)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消操作。")
        sys.exit(0)
    except Exception as e:
        print("程序发生未预期的错误：{}".format(e))
        sys.exit(1)
