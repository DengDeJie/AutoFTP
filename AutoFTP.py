# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 09:34:39 2019

@author: dendejie

Function:下载ftp服务器中指定目录中的所有文件（已下载过的文件不再重复下载）

"""

import ftplib 
import os
import socket
 
HOST = 'XXX.XX.XX.X'#ftp地址
USER = 'XXX'   #用户名
PASSWD = 'XXXXXX' #用户密码

LocalDir = r'D:\FTPDowdoads' #本地存贮路径
FTPDir=r'/338x series/006.ExampleCode'#需要下载的ftp目录路径
local_fname='checkfile.txt'#用本地存放已下载过的文件名

local_files=[]#存放从checkfile.txt中读回的文件名
appendFiles=[]#存放需要写进checkfile.txt的文件各


def FtpConnect(host, username, passwd):
    '''
    连接并登录ftp服务器
    
    host:ftp地址
    username:用户名
    passwd:用户密码
    '''
    try:
        ftp = ftplib.FTP(HOST)
        #ftp.encoding = 'utf-8' #解决中文乱码问题
        #ftp.set_debuglevel(0)  #不开启调试模式        
    except (socket.error, socket.gaierror):
        print('Error, cannot reach ' + HOST)
        return None
    else:
        print('Connect To Host Success...') 
    
    try:
        ftp.login(USER, PASSWD)
    except ftplib.error_perm:
        print('Username or Passwd Error')
        #ftp.quit()
        return None
    else:
        print(ftp.getwelcome())  #显示登录ftp信息
        print('Login Success...')
        ftp.dir()#显示目录下所有目录信息
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")        	
    return ftp	

def filelist(ftp):
    '''
    递归ftp当前目录下的所有文件及目录信息    
    '''
    flist=[]
    ftp.dir('.',flist.append)#将目录中的内容存进flist列表
    files = [f.split()[-1] for f in flist if f.startswith('-')]#读取flist列表中的信息，以-开头的是常规文件，将该信息以空字符分割成列表，取最后的元素即为文件名
    fids=[f.split(None, 4)[-1] for f in flist if f.startswith('-')] #读取flist列表中的信息，以-开头的是常规文件，将该信息以前4个空字符分割成列表，
                                                                    #最后的元素包括了文件的大小，修改日期时间，可作为文件的标识
    dictf=dict(zip(files,fids))#将文件名与对应的标识合成字典
    dirs = [f.split()[-1] for f in flist if f.startswith('d')]#读取flist列表中的信息，以d开头的是目录，将该信息以空字符分割成列表，取最后的元素即为目录名
    #print(dirs)
    return(dictf,dirs)

def FtpDownloadDir(ftp,ftp_dir,local_dir):
    '''
    递归下载ftp指定目录下的所有文件及目录
    '''
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f'Walking to {ftp_dir}')
    print(f'Walking to {local_dir}')
    if ftp_dir=="/":
        dirname = "AllDir"#用于本地创建新目录，如果下载的是FTP根目录，则在目录名为AllDir
    else:
        dirname = os.path.basename(ftp_dir)#否则本地目录名与FTP目录名一样
    
    ftp.cwd(ftp_dir)#进入ftp对应目录
    os.chdir(local_dir)#进入本地下载目录
    
    if os.path.exists(dirname):#如果本地dirname目录已存在
        os.chdir(dirname)#则直接进入该目录
    else:
        try:
            os.mkdir(dirname)#否则在本地创建该目录
        except OSError:
            print('OSError!')
        else:
           os.chdir(dirname)#创建完后进入该目录 

    ftp_curr_dir = ftp.pwd()#获取FTP当前目录路径
    local_curr_dir = os.getcwd()#获取本地当前目录路径
    #print(f'Changing to {ftp_curr_dir}')
    #print(f'Changing to {local_curr_dir}') 
    
    dictf,dirs = filelist(ftp)#调用filelist函数，递归ftp当前目录下的所有文件及目录 
    
    for f,k in dictf.items():#获取到的文件信息的键值对
        if k not in local_files:#文件标识与本地存储的已下载过的文件标识做对比
            FtpDownloadFile(ftp,f,f)#k不在local_files中说明该文件未下载过，则下载该文件
            appendFiles.append(k)#同时将该文件的标识存储到appenFiles列表中，用于下载完成后更新本地的checkfile.txt文件
        
    for d in dirs:#对子目录进行处理
        FtpDownloadDir(ftp,d,local_curr_dir)#调用自身，递归下载子目录中的文件
        ftp.cwd('..')
        os.chdir('..')#每次递归完成后，ftp及本地都返回上一层目录，继续其他子目录的处理
    os.chdir(local_dir)

def FtpDownloadFile(ftp, remotefile, localfile):
    '''
    下载ftp当前目录的文件到本地的当前目录中
    '''    
    buffer_size = 10240  #默认是8192
    try:
        f = open(localfile, 'wb')
        ftp.retrbinary(f'RETR {remotefile}', f.write,buffer_size)
    except ftplib.error_perm:
        print(f'File:{f} Download Error')
        #os.unlink(localpath)
    else:
        print(f'File:{f} Download Success...')
    finally:
        f.close()

def operfile(fileTxt,op):
    '''
    操作下载目录中的文件
    op为'r'时读取该文件，如文件不存在则忽略
    op为'w'时追加写入文件
    '''
    fp=os.path.join(LocalDir,fileTxt)
    if op=='r':
        print(f'从 {fp} 中读取本地文件列表')                  
        try:
            with open(fp,'r')as ft:
                for line in ft:
                    line = line.strip()
                    local_files.append(line) 
        except Exception as e:
            print(e)
    elif op=='w':
        print(f'更新 {fileTxt} 中文件列表')
        try:
            with open(fp,'a') as ft:
                ft.writelines([f'{x}\n' for x in appendFiles])
        except Exception as e:
            print(e)
    else:
        print("参数2请输入'r'或者'w'！")
    
                
if __name__ == '__main__':
    ftp = FtpConnect(HOST, USER, PASSWD)#连接并登录ftp服务器    
    if ftp:#如果登录成功
        operfile(local_fname,'r')#从checkfile.txt中获取已下载过的文件
        FtpDownloadDir(ftp,FTPDir,LocalDir)#将ftp指定目录下的文件更新到本地目录中
        if appendFiles:#如果有新文件更新到本地
            operfile(local_fname,'w')#则将其追加到checkfile.txt中
            appendFiles=[]#清空列表
        else:
            print(f'无需更新{local_fname}')
        ftp.quit()
        print("FTP QUIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        
        

