# AutoFTP
Function:下载ftp服务中指定目录中的所有文件（已下载过的文件不再重复下载）

Python FTP 操作：
    from ftplib import FTP                  # 加载ftp模块
    ftp = FTP()                             # 获取FTP对象
    ftp.set_debuglevel(0)                   # 关闭调试模式
    ftp.set_debuglevel(2)                   # 打开调试级别2，显示详细信息
    ftp.connect('IP', PORT)                 # 连接ftp，server和端口
    ftp.login('user','password')            # 登录用户
    print(ftp.getwelcome())                 # 打印欢迎信息
    ftp.cmd('xxx/xxx')                      # 进入远程目录
    ftp.quit                                # 退出ftp
    ftp.cwd(pathname)                       # 设置FTP当前操作的路径
    ftp.dir ([path[,...[,cb]])              # 显示 path 目录里的内容，可选的参数 cb 是一个回调函数，会传递给 retrlines()方法
    ftp.nlst()                              # 获取目录下的文件
    ftp.mkd(pathname)                       # 新建远程目录
    ftp.rmd(dirname)                        # 删除远程目录
    ftp.pwd()                               # 返回当前所在位置
    ftp.delete(filename)                    # 删除远程文件
    ftp.rename(fromname, toname)            # 将fromname改为toname
    ftp.storlines(cmd, f)	                # 给定 FTP 命令（如“ STOR filename”），用来上传文本文件。要给定一个文件对象 f
    ftp.storbinary(cmd, f[,bs=8192])	    # 与 storlines()类似，只是这个指令处理二进制文件。要给定一个文件对象 f，上传块大小 bs 默认为 8KB
    ftp.retrlines(cmd [, cb])               # 给定 FTP 命令（如“ RETR filename”），用于下载文本文件。可选的回调函数 cb 用于处理文件的每一行
    ftp.retrbinary(cmd,cb[,bs=8192[, ra]])	# 与 retrlines()类似，只是这个指令处理二进制文件。回调函数 cb 用于处理每一块（块大小默认为 8KB）下载的数据
