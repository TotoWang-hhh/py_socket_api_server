def add(server,logtype,text):
    server.log_with_binded(logtype,text)
    return 'Log added'
