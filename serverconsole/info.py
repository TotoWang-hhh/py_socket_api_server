import time

def showall(server):
    txtlst=''
    txtlst+="===Server Info===\n"
    txtlst+="[Uptime] "+str(time.time()-server.starttime)+'\n'
    if server.isrunning:
        txtlst+="[Status] Running\n"
    elif not server.isrunning:
        txtlst+="[Status] Paused\n"
    else:
        txtlst+="[Status] Unknown\n"
    return txtlst

def uptime(server):
    return str(time.time()-server.starttime)

def status(server):
    txtlst=''
    if server.isrunning:
        txtlst+="[Status] Running\n"
    elif not server.isrunning:
        txtlst+="[Status] Paused\n"
    else:
        txtlst+="[Status] Unknown\n"
    return txtlst
