---
counter: True
comment: True
---

# Git 命令相关

!!!abstract
    一些常用 / 常忘的 git 命令

## 分支

- `git branch <branch_name>` 创建分支
- `git checkout <branch_name>` 切换分支
- `git checkout -b <branch_name>` 创建分支，并切换过去
- `git diff <branch_name> master` 显示分支和主分支的差别
- `git clone -b <branch_name> <repo_url>` 克隆单个分支
- `git branch -d <branch_name>` 删除分支
- `git branch -a` 查看所有分支
- `git merge` 合并分支

## 远程仓库

- `git fetch` 获取远程仓库的历史记录
- `git pull` 将本地仓库更新, pull = fetch + merge
- `git push origin <branch_name>` 将分支推送到远程仓库


## 改写提交

- `git commit --amend` 修改最近的提交
- `git revert HEAD` 取消过去的提交
- `git reset --soft HEAD^` 撤销 commit（不更改文件）
- `git reset --hard HEAD^` 撤销 commit（文件回退到上一版本）
- `git rm --cached <file>` 已 add 未 commit 的文件退回未 add 状态
- `git checkout .` 取消本次未被commit的修改
- `git rebase <commit_name>` 变基
- `git rebase -i <commit_name>` 合并/修改提交，**最好用fetch+rebase的方式来合并**



## 标签

- `git tag` 显示所有标签列表
- `git tag <tag_name>` 添加轻标签
- `git tag -a <tag_name>` 添加注解标签
- `git tag -d <tag_name>` 删除标签

## awesome_git_log

为了方便查看`commit`相关信息，用`alias`来简化操作，将下面代码粘贴到`bashrc`中，然后在终端中直接`awe+tab`即可。

  

```shell
# git
function git_branch {
   branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
   if [ "${branch}" != "" ];then
       if [ "${branch}" = "(no branch)" ];then
           branch="(`git rev-parse --short HEAD`...)"
       fi
       echo " ($branch)"
   fi
}

alias __git_awesome_log="git log --oneline --decorate --all --graph"
alias awesome_git_log="git log --oneline --decorate --all --graph"
```

## Reference

- [猴子都能懂的GIT入门](https://backlog.com/git-tutorial/cn/intro/intro1_1.html)
- [Git命令备忘](https://note.tonycrane.cc/cs/tools/git/)