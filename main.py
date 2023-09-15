import tkinter as tk
import tkinter.ttk as ttk
import tttk
import tkinter.messagebox as msgbox
import ui
from server import Server
import sys
import threading
import warnings

import serverconsole.single


def addlog(logtype,text):
    match logtype:
        case 'info':
            loglst.insert(tk.END,text,bg='#ffffff',fg='#000000')
        case 'warning':
            loglst.insert(tk.END,text,bg='#ffffcc',fg='#000000')
        case 'error':
            loglst.insert(tk.END,text,bg='#ffcccc',fg='#ff0000')
        case _:
            warnings.warn('LOGTYPE ERROR')

def _run(cmd):
    global server
    try:
        #print(cmd)
        cmdlst=cmd.split(' ')
        pycmd=cmdlst[0]
        #print(pycmd)
        #print(cmdlst)
        params=cmdlst
        params.pop(0)
        #print(params)
        #params.pop[1]
        paramstr=''
        if len(params)>0:
            for p in params:
                paramstr+=str(p)+','
        #print(paramstr)
        #print('serverconsole.'+pycmd+'('+'server'+paramstr+')')
        exec("import serverconsole."+pycmd.split('.')[0])
        returntxt=eval('serverconsole.'+pycmd+'('+'server,'+paramstr+')')
        return str(returntxt)
    except Exception as e:
        #print(cmd)
        cmdlst=cmd.split(' ')
        pycmd=cmdlst[0]
        #print(pycmd)
        #print(cmdlst)
        params=cmdlst
        params.pop(0)
        #print(params)
        #params.pop[1]
        paramstr=''
        if len(params)>0:
            for p in params:
                paramstr+=str(p)+','
        #print(paramstr)
        #print('serverconsole.'+pycmd+'('+'server'+paramstr+')')
        returntxt=eval('serverconsole.single.'+pycmd+'('+'server,'+paramstr+')')
        return str(returntxt)
    finally:
        warnings.warn(str(pycmd)+' Not Found'+'\n')
        return 'Function '+str(pycmd)+' not found'

def run(cmd):
    returntxt=_run(cmd)
    print(returntxt)
    consoletxt.insert(tk.END,returntxt+'\n')

if '--port' in sys.argv:
    port=sys.argv[sys.argv.index('--port')+1]
else:
    port=7987


debug='--debug' in sys.argv
noui='--noui' in sys.argv

if not noui:
    whenlog=addlog
else:
    whenlog=None

server=Server(port=port,use_debug_port=debug,whenlog=whenlog)
server_t=threading.Thread(target=server.start)
server_t.start()

if noui:
    while True:
        cmd=input('PySAS Server> ')
        print(_run(cmd))
    exit()


win=tk.Tk()
win.title('PySAS UI')


loglst=ui.LogList(win,width=300)
#loglst.frame['width']=200
loglst.frame_pack(side=tk.LEFT,fill=tk.Y)
#loglst.pack_propagate(False)
loglst.frame.pack_propagate(False)

#ui.tooltip.CreateToolTip(loglst,loglst.curselection())

consolept=tk.Frame(win)

cmdinput=tttk.TipEnter(consolept,text='PySAS Server>',command=lambda:print('PLEASE WAIT'),btntxt='↑ RUN')
cmdinput.command=lambda:run(cmdinput.get())
cmdinput.refresh()
cmdinput.pack(side=tk.BOTTOM,fill=tk.X)

consoletxt=tk.Text(consolept,bg='#000000',fg='#ffffff',bd=0)
consoletxt.pack(fill=tk.BOTH,expand=True)

consolept.pack(side=tk.RIGHT,fill=tk.Y,expand=True)



server=Server(port=port,use_debug_port=debug,whenlog=addlog)

server_t=threading.Thread(target=server.start)
server_t.start()

win.mainloop()
