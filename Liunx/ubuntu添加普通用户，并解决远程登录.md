# 创建普通用户



```

# 创建用户，并指定用户目录，加入用户组sudo useradd username -d /home/username -m
#设置密码
sudo passwd username

#给用户增加sudo权限
sudo chmod u+w /etc/sudoers
#编辑权限文件
sudo vi /etc/sudoers
#在 root ALL=(ALL:ALL) ALL 添加一行
	username ALL=(ALL:ALL) ALL

#恢复文件权限
sudo chmod u-w /etc/sudoers
```

# 解决远程用户登录问题



```
sudo vi /etc/passwd
```

在追后一行追加 :/bin/bash

```
username：x:1001:1001::/home/biyunsheng:/bin/bash
```

