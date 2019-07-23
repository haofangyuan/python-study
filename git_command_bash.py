#!/usr/bin/python3
# -*-coding:utf-8 -*-

import os

def bash_shell(bash_command):
    """
    python 中执行 bash 命令
    :param bash_command:
    :return: bash 命令执行后的控制台输出
    """
    try:
        print(os.popen(bash_command).read())
        return os.popen(bash_command).read().strip()
    except:
        return None


def find_target(target_path="./../", key='.git'):
    """
    查找目标目录所在的目录 ： 如 ／aa/bb/.git --> return /aa/bb/
    :param target_path:
    :param key: target
    :return:
    """
    walk = os.walk(target_path)
    for super_dir, dir_names, file_names in walk:
        for dir_name in dir_names:
            if dir_name == key:
                dir_full_path = os.path.join(super_dir, dir_name)
                print('dir_full_path', dir_full_path, 'super_dir', super_dir)
                yield super_dir


if __name__ == '__main__':
    # 返回当前工作目录
    cwd = os.getcwd()
    target_path = os.getcwd()
    target_path = "E:\project\my-demo\git-test"

    # this for git
    for git_path in find_target(target_path, '.git'):
        print('git_path：', git_path)
        # 改变当前工作目录到指定的路径
        os.chdir(git_path)
        if git_path == os.getcwd():
            print('find git in -->', git_path)
            print(bash_shell('pwd'))
            print(bash_shell('git status'))
            print(bash_shell('git add .'))
            c = input("输入commit信息").strip()
            print('请输入commit信息：', c)
            print(bash_shell('git commit . -m ' + c))
            print(bash_shell('git status'))
            print(bash_shell('git log --oneline'))
        else:
            print('error in chdir 2 {}'.format(git_path))
        if os.getcwd() != cwd:
            os.chdir(cwd)
        if os.getcwd() != cwd:
            print('change 2 cwd FAIL !!!  {}'.format(cwd))
