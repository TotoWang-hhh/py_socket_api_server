def start(server):
    server.start()
    return 'Server Started'

def pause(server):
    server.pause()
    return 'Server Paused'

def serverexit(server):
    server.pause()
    server.skt.close()
    return 'Server Closed'
