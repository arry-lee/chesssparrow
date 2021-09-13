from ftplib import FTP

host = "10.203.180.240"
port = 2121
user = "lixnrv"
passwd = "lixnrv"
path = 'DCIM'

with FTP() as ftp:
    ftp.connect(host=host,port=port)
    ftp.login(user=user,passwd=passwd)
    print(ftp.getwelcome())
    print(ftp.pwd())
    ftp.cwd('DCIM')
    # [print(file) for file in ftp.nlst() if file.endswith('mp4')]
    # print([ftp.size(file) for file in ftp.nlst() if file.endswith('mp4')])
    # 下载文件
    [ftp.retrbinary('RETR %s' % file, open(file,'wb').write) for file in ftp.nlst() if file.startswith('Screenshots-')]

    # ftp.delete(file)
    # 上传文件
    # file = 'src/img/tmp.png' 
    # ftp.storbinary('STOR %s' % 'tmp.png', open(file,'rb'))


    # [ftp.delete(file) for file in ftp.nlst() if file.startswith('new1')]
    # ftp.mkd('QIPU')

# print(filelist)