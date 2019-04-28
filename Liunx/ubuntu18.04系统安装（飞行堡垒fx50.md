**决定把我的渣机脱坑**

# 一、制作启动盘

 1. 官方下载ubuntu18.04LTS iso文件
	 	[ubuntu官方链接](https://www.ubuntu.com/download/desktop
	
 2. UltraISO制作启动文件（采用试用）
	 	[UltraISO官方链接](http://cn.ultraiso.net/xiazai.html)
 3. 打开UltraISO 
 4. 打开文件选择iso文件
 5. 选择      启动 =》 写入硬盘映像
	 	![在这里插入图片描述](https://img-blog.csdnimg.cn/2019012600142722.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyODA2NDE2,size_16,color_FFFFFF,t_70)
 6. 点击便捷启动
	 	![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126001604436.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyODA2NDE2,size_16,color_FFFFFF,t_70)


 接着选择  便捷式启动=》Sysliunx=》写入新的驱动扇区=》sysliunx
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126001809177.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyODA2NDE2,size_16,color_FFFFFF,t_70)
 7. 接下来选择  =》写入
	 	注意 写入方式最好选择USB-HDD 兼容性比较好

u盘制作完成

# 二、bios设置

 1. 一般电脑设置为快速启动无法进入bios设置，需要在关闭快速启动， 电源选项=》系统设置 =》关闭快速启动
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126002224544.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyODA2NDE2,size_16,color_FFFFFF,t_70)
 2. 插入启动盘，开机 出现画面  =》长按F2 到bios设置
 3. bios设置
    Boot =》Lunch CSM=》设置为 enable，
    Security=》secure boot control-=》设置为disable
    Boot =》 将Boot Option #1 选择为 =》 UEFI 的启动盘
    然后按 F10 保存退出
    等待重启


 4. **之前被坑，我的不需要编辑，直接install就ok**选择 install Ubuntu =》按e键进入编辑模式选择 install Ubuntu =》按e键进入编辑模式
	 	在 linux这行 找到quiet splash，在后面空格接着输入 $vt_handoff acpi_osi=linux nomodeset
 6. 按F10 等待安装
 7. 选择语言 键盘布局语言
 8. 无线选择
 9. 更新和其他软件  （网不好就选正常安装吧，其他选项默认，勾选了其他的可能要等一会，系统在下载文件）
 10. 安装类型=》 根据自己的实际需求
 11. 选择地区 =》shanghai  （直接鼠标选择中国区域）  
 12. 如果有分盘需求选择其他选项
	 		=》【手打超链接，后续补上】 
 13. 用户配置
 14. 等待安装

其他配置链接：
	后续更新！

如有问题请评论区留言 第几步骤！

 


 	

