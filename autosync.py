from ftplib import FTP
import os
import glob
import datetime

def useless(function):
    pass

root = _folder to sync
os.chdir(root)
file_list = glob.glob('*')
for i, f in enumerate(file_list):
    file_list[i] = [f]
    file_list[i].append(datetime.datetime.fromtimestamp(int(os.path.getmtime(f))).strftime('%b %d %H:%M').split())
    for x in file_list[i][1]:
        file_list[i].append(x)
    file_list[i].pop(1)

with FTP(_server) as ftp:
    ftp.login(user=_username, passwd=_password)
    flist = []
    ftp.retrlines('LIST', flist.append)
    for i, x in enumerate(flist):
        flist[i] = x.split()
    tmp = []
    for i, x in enumerate(flist):
        tmp.append([])
        tmp[i].append(x[-1])
        tmp[i].append(x[5])
        tmp[i].append(x[6])
        tmp[i].append(x[7])
    flist = tmp
    del tmp
    put = []
    for clientf in file_list:
        diff = True
        for servf in flist:
            if clientf == servf:
                diff = False
        if diff:
            put.append(clientf[0])
    get = []
    for servf in flist:
        diff = True
        for clientf in file_list:
            if servf == clientf:
                diff = False
        if diff:
            get.append(servf[0])
    for f in put:
        ftp.storbinary('STOR ' + f, open(f, 'rb'))
        t = int(os.popen('date +%s').read())
        os.utime(f,(t, t))
    for f in get:
        ftp.retrbinary('RETR ' + f, useless)
