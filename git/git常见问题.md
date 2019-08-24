# 连接成功host警告

```
Warning: Permanently added the RSA host key for IP address '13.229.188.59' to the list of known hosts.
```

## 解决办法

liunx

```
vim /etc/hosts
添加 13.229.188.59 github.com
```

windows

```
C:\Windows\System32\drivers\etc\hosts  
添加 13.229.188.59 github.com
```

测试：

```
ssh -T git@github.com
```

# 终端自动显示分支

```
vi ~/.bash_profile
```

\### 显示git分支

```
parse_git_branch () {

git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/[\1]/'

}

 

BLACK="\[\033[0;38m\]"

RED="\[\033[0;31m\]"

RED_BOLD="\[\033[01;31m\]"

BLUE="\[\033[01;34m\]"

GREEN="\[\033[0;32m\]"

 

export PS1="$BLACK[ \u@$RED\h $GREEN\w$RED_BOLD\$(parse_git_branch)$BLACK ] "
```

\####