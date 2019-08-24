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
vi ~/.bashrc
```

\### 显示git分支

```
function git_branch {  
   branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"  
   if [ "${branch}" != "" ];then  
       if [ "${branch}" = "(no branch)" ];then  
           branch="(`git rev-parse --short HEAD`...)"  
       fi  
       echo " ($branch)"  
   fi  
}  

export PS1='\u@\h \[\033[01;36m\]\W\[\033[01;32m\]$(git_branch)\[\033[00m\] \$ '  
```

刷新bash

```
sourc e .bashrc
```

