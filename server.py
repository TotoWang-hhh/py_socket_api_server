# Py Socket API Server
# Modified From PyVP Server (.beforever)
# 2023 By 真_人工智障

import socket
#import response.ver
import json
from log import logger
import time
import warnings

class Server():
    def __init__(self,port=7987,use_debug_port=False,whenlog=None):
        self.port=port
        if use_debug_port:
            self.port=10000
        self.skt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isrunning=False
        self.skt.bind(('',self.port))
        self.skt.listen(1000)
        self.whenlog=whenlog
        self.starttime=time.time()
    def handle(self):
        client, address = self.skt.accept()
        self.log_with_binded('info','REQUEST FROM '+str(address))
        while True:
            recvmsg=client.recv(1024)
            #把接收到的数据进行解码
            #输入
            try:
                strData = recvmsg.decode("utf-8")
            except Exception as e:
                self.log_with_binded('warning','DATA DECODE ERROR '+str(e)+' (disconnected)')
                resmsg='无法处理您的请求！温馨提示：请注意IP是否正确 | Cannot handle your request! Tip: Plese Check the IP address'
                break
            #设置退出条件
            if strData == 'q' or strData == '':
                self.log_with_binded('info',str(address)+' DISCONNECTED')
                break
            try:
                jsonmsg=json.loads(strData)
            except Exception as e:
                self.log_with_binded('warning','DATA FORMAT ERROR '+str(e)+' (disconnected after recording in errmsg/)')
                errmsgf=open("./errmsg/%s.txt" % time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),'w')
                errmsgf.write('FROM: '+str(address)+'\n====================\n\n'+strData)
                errmsgf.close()
                resmsg=json.dumps({'error':'NOT JSON'})
                break
            self.log_with_binded('info',"RECV < %s" % strData)
            paramjson=jsonmsg
            del paramjson['func']
            jsonmsg=json.loads(strData)
            paramstr=''
            for p in list(paramjson.keys()):
                if type(paramjson[p])==str:
                    paramstr+=str(p)+'='+"'"+paramjson[p]+"'"+','
                else:
                    paramstr+=str(p)+'='+paramjson[p]+','
            #msg = input("发送: ")
            #发送数据，需要进行编码
            resraw=self.runapi(jsonmsg['func'],paramstr)
            if type(resraw)==dict:
                resmsg=json.dumps(resraw)
            else:
                resmsg=str(resraw)
            self.log_with_binded('info','SEND > %s' % resmsg)
            client.send(resmsg.encode("utf-8"))
    def start(self):
        self.isrunning=True
        self.run()
    def run(self):
        while self.isrunning:
            self.handle()
    def pause(self):
        self.isrunning=False
    def resocket(self,port=None):
        if port==None:
            port=self.port
        self.pause()
        self.skt.close()
        self.skt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.bind('',port)
        self.skt.listen(5)
        self.run()
    def set_port(self,port=7987):
        self.port=port
        self.resocket(port)
    def log_with_binded(self,logtype,info):
        timeinfo=time.strftime("[%Y/%m/%d %H:%M:%S] ", time.localtime())
        match logtype:
            case 'info':
                if self.whenlog!=None:
                    self.whenlog(logtype,timeinfo+info)
                logger.info(info)
            case 'warning':
                if self.whenlog!=None:
                    self.whenlog(logtype,timeinfo+info)
                logger.warning(info)
            case 'error':
                if self.whenlog!=None:
                    self.whenlog(logtype,timeinfo+info)
                logger.error(info)
            case _:
                warnings.warn('Log type error')
    def runapi(self,cmd,params=''):
        global server
        try:
            #print(cmd)
            cmdlst=cmd.split(' ')
            pycmd=cmdlst[0]
            #print(pycmd)
            #print(cmdlst)
            #print(params)
            #params.pop[1]
            #print(paramstr)
            #print('serverconsole.'+pycmd+'('+'server'+paramstr+')')
            eval('import response.'+pycmd)
            result=eval('response.'+pycmd+'('+str(params)+')')
            return result
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
            result=eval('response.single.'+pycmd+'('+'server,'+str(params)+')')
            return result
        except Exception as e:
            warnings.warn(str(pycmd)+' Not Found'+'\n'+str(e))
            return {"Error":'API '+str(pycmd)+' not found'}

