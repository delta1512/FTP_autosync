from ftplib import FTP
import os
import glob
import datetime

global months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def time_check(cli, ser):
    if months.index(cli[1]) == months.index(ser[1]):
        if cli[2] == ser[2]:
            if cli[3][:-3] == ser[3][:-3]:
                return (int(cli[3][3:]) > int(ser[3][3:])-1 and
                        int(cli[3][3:]) > int(ser[3][3:])+1)
            else:
                return (int(cli[3][:-3]) > int(ser[3][:-3]))
        else:
            return (int(cli[2]) > int(ser[2]))
    else:
        return (months.index(cli[1]) > months.index(ser[1]))

root = '''root of sync directory'''
os.chdir(root)
clnt_files = glob.glob('*')
for i, f in enumerate(clnt_files):
    clnt_files[i] = [f]
    clnt_files[i].append(datetime.datetime.fromtimestamp(int(os.path.getmtime(f))).strftime('%b %d %H:%M').split())
    for x in clnt_files[i][1]:
        clnt_files[i].append(x)
    clnt_files[i].pop(1)

with FTP('''hostname of ftp server''') as ftp:
    ftp.login(user='''account for ftp server''', passwd='''passwd for account''')
    serv_files = []
    ftp.retrlines('LIST', serv_files.append)
    for i, x in enumerate(serv_files):
        serv_files[i] = x.split()
    tmp = []
    for i, x in enumerate(serv_files):
        tmp.append([])
        tmp[i].append(x[-1])
        tmp[i].append(x[5])
        tmp[i].append(x[6])
        tmp[i].append(x[7])
    serv_files = tmp
    del tmp
    put = []
    for clientf in clnt_files:
        found = False
        for servf in serv_files:
            if clientf[0] == servf[0]:
                found = True
                if clientf[0] == servf[0] and time_check(clientf, servf):
                    put.append(clientf[0])
        if not found:
            put.append(clientf[0])
    get = []
    for servf in serv_files:
        found = False
        for clientf in clnt_files:
            if servf[0] == clientf[0]:
                found = True
                if time_check(servf, clientf):
                    get.append(servf[0])
        if not found:
            get.append(servf[0])
    for f in put:
        ftp.storbinary('STOR ' + f, open(f, 'rb'))
        t = int(os.popen('date +%s').read())
        os.utime(f,(t, t))
    for f in get:
        ftp.retrbinary('RETR ' + f, open(f, 'wb').write)
