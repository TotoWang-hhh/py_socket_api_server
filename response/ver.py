global_latestver='.beforever'

if global_latestver=='.beforever':
    global_latestver='0.0.0'

def get_latestver():
    global global_latestver
    return global_latestver

def get_ifnewver(clientver):
    global global_latestver
    if clientver=='.beforever':
        clientver='0.0.0'
    list1 = str(clientver).split(".")
    list2 = str(global_latestver).split(".")
    #print(list1)
    #print(list2)
    # 循环次数为短的列表的len
    for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
        if int(list1[i]) == int(list2[i]):
            pass
        elif int(list1[i]) < int(list2[i]):
            return -1
        else:
            return 1
    # 循环结束，哪个列表长哪个版本号高
    if len(list1) == len(list2):
        return {'newver':False,'insidever':False,'msg':'您的版本为最新'}
    elif len(list1) < len(list2):
        return {'newver':False,'insidever':True,'msg':'若未经允许，请勿使用内部版本'}
    else:
        return {'newver':True,'insidever':False,'latest':str(get_latestver()),'msg':'新版可用，请更新至v'+str(global_latestver)}
