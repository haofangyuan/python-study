#!/usr/bin/python3
# -*-coding:utf-8 -*-

import os
import sys
from git import Repo
from git.exc import GitCommandError


def git_commit(path, branch_name, no_change_commit):
    repo = Repo(path)

    # 远程库是否存在
    origin_exists = False
    origin = None
    if len(repo.remotes) == 0:
        print("没有配置远程仓库")
    else:
        origin_exists = True
        origin = repo.remotes.origin
        repo.heads[branch_name].set_tracking_branch(origin.refs[branch_name])

    branch = None
    for branch_item in repo.heads:
        print(branch_item.name)
        if branch_item.name == branch_name:
            branch = branch_item

    if branch is None:
        print("分支不存在！")
        return

    # 切换到boy分支
    cur_branch = repo.head.reference  # 当前活动分支
    print("当前活动分支: ", cur_branch)
    if cur_branch != branch:
        # repo.heads.reference = branch_boy
        branch.checkout()
        print(repo.head.reference)

    # untracked文件列表并git add
    print("未跟踪文件: ", repo.untracked_files)
    repo.index.add(items=repo.untracked_files)

    # 暂存区
    index = repo.index
    print("是否需要提交：", repo.is_dirty())
    # 本地修改未提交列表
    for v in index.diff(None):
        # 本地文件路径，修改类型，返回"m"表示modified。
        print("to commit: ", v.b_path, v.change_type)
        repo.index.add(items=[v.b_path])

    if not repo.is_dirty():
        if not no_change_commit:
            return
    else:
        # git commit
        commit_info = input("请输入commit信息: ").strip()
        commit_id = index.commit(commit_info)
        print("commit_id: ", commit_id)
        print(repo.head.reference.commit)
        if repo.head.reference.commit == commit_id:
            print("提交成功^_^")

    # boss分支git pull
    if not origin_exists:
        return
    try:
        origin.pull(branch_name)
    except:
        # We'll use this as a flag to determine whether we found any files with conflicts
        found_a_conflict = False
        print(repo.head.reference)
        print("git pull 出现错误:", sys.exc_info()[0])
        # print(repo.index.unmerged_blobs())
        unmerged_blobs = repo.index.unmerged_blobs()
        # We're really interested in the stage each blob is associated with.
        # So we'll iterate through all of the paths and the entries in each value
        # list, but we won't do anything with most of the values.
        for path in unmerged_blobs:
            print("冲突文件:{}", path)
            list_of_blobs = unmerged_blobs[path]
            for (stage, blob) in list_of_blobs:
                # Now we can check each stage to see whether there were any conflicts
                if stage != 0:
                    found_a_conflict = True

        print("found_a_conflict ", found_a_conflict)
        return

    repo.remotes.origin.push()


def git_commit_merge(path, branch_name_boy, branch_name_boss, no_change_merge=False):
    repo = Repo(path)

    # 远程库是否存在
    origin_exists = False
    origin = None
    if len(repo.remotes) == 0:
        print("没有配置远程仓库")
    else:
        origin_exists = True
        origin = repo.remotes.origin
        repo.heads[branch_name_boy].set_tracking_branch(origin.refs[branch_name_boy])
        repo.heads[branch_name_boss].set_tracking_branch(origin.refs[branch_name_boss])

    # 根据分支名字获取分支
    branch_boy = None
    branch_boss = None
    for branch in repo.heads:
        print(branch.name)
        if branch.name == branch_name_boy:
            branch_boy = branch
        if branch.name == branch_name_boss:
            branch_boss = branch

    if branch_boy is None:
        print("小弟分支不存在！")
        return
    if branch_boss is None:
        print("大哥分支不存在！")
        return

    # 切换到boy分支
    cur_branch = repo.head.reference  # 当前活动分支
    print("当前活动分支: ", cur_branch)
    if cur_branch != branch_boy:
        # repo.heads.reference = branch_boy
        branch_boy.checkout()
        print(repo.head.reference)

    # untracked文件列表并git add
    print("未跟踪文件: ", repo.untracked_files)
    repo.index.add(items=repo.untracked_files)

    # 暂存区
    index = repo.index
    print("是否需要提交：", repo.is_dirty())
    # 本地修改未提交列表
    for v in index.diff(None):
        # 本地文件路径，修改类型，返回"m"表示modified。
        print("to commit: ", v.b_path, v.change_type)
        repo.index.add(items=[v.b_path])

    if not repo.is_dirty():
        if not no_change_merge:
            return
    else:
        # git commit
        commit_info = input("请输入commit信息: ").strip()
        commit_id = index.commit(commit_info)
        print("commit_id: ", commit_id)
        print(repo.head.reference.commit)
        if repo.head.reference.commit == commit_id:
            print("提交成功^_^")

    # 合并到boss分支
    branch_boss.checkout()

    # boss分支git pull
    if origin_exists:
        try:
            origin.pull(branch_name_boss)
        except:
            # We'll use this as a flag to determine whether we found any files with conflicts
            found_a_conflict = False
            print(repo.head.reference)
            print("git pull 出现错误:", sys.exc_info()[0])
            # print(repo.index.unmerged_blobs())
            unmerged_blobs = repo.index.unmerged_blobs()
            # We're really interested in the stage each blob is associated with.
            # So we'll iterate through all of the paths and the entries in each value
            # list, but we won't do anything with most of the values.
            for path in unmerged_blobs:
                print("冲突文件:{}", path)
                list_of_blobs = unmerged_blobs[path]
                for (stage, blob) in list_of_blobs:
                    # Now we can check each stage to see whether there were any conflicts
                    if stage != 0:
                        found_a_conflict = True

            print("found_a_conflict ", found_a_conflict)
            return

    # git merge
    try:
        repo.git.merge(branch_name_boy, branch_name_boss)
    except GitCommandError as err:
        print("merge出现问题，需要人工处理！")
        print(err)
        return

    if origin_exists:
        repo.remotes.origin.push()


if __name__ == '__main__':
    print("我是哈哈本人，请选择服务模式：")
    print("[1] 母胎单体master自己处理，并提交远端")
    print("[2] 小弟给大哥交作业，大哥提交远端")
    mode_select = input().strip()
    if mode_select == '1':
        git_commit(os.getcwd())
    elif mode_select == '2':
        print("请输入小弟分支：")
        branch_name_boy = input()
        print("请输入大哥分支：")
        branch_name_boss = input()
        os.getcwd()

        git_commit_merge('E:\project\my-demo\git-test', 'dev', 'master', True)
    else:
        print("太任性不好的啦，哈哈大人不理你了，哼~~~")
