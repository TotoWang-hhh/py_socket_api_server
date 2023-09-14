def about(server):
    return '===About===\nPython Visual Programmer Server\n2023 By rgzz666\n'

def hello(server):
    return 'Hello! PyVP Server Console\n'

def start(server):
    server.start()
    return 'Server Started\n'

def pause(server):
    server.pause()
    return 'Server Paused\n'

def exit(server):
    exit()

def help(server):
    helpf=open("./cmdhelp.txt",'r',encoding='utf-8')
    helptxt=helpf.read()
    helpf.close()
    return helptxt+'\n'
