# -*- coding: utf-8 -*-

# 获取引擎服务端API的模块
import server.extraServerApi as serverApi
# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
ServerSystem = serverApi.GetServerSystemCls()

# 在modMain中注册的Server System类
class moreTorchServerSystem(ServerSystem):

    # ServerSystem的初始化函数
    def __init__(self, namespace, systemName):
        # 首先调用父类的初始化函数
        super(moreTorchServerSystem, self).__init__(namespace, systemName)
        print "===== TutorialServerSystem init ====="
        # 初始时调用监听函数监听事件
        self.ListenEvent()
        self.buzhou = None

    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        # 在自定义的ServerSystem中监听引擎的事件ServerChatEvent，回调函数为OnServerChat
        self.DefineEvent("ToClient")
        self.DefineEvent("destory")
        self.ListenForEvent("MoreTorch", "moreTorchClientSystem", "toServer", self, self.toServer)

    # 反监听函数，用于反监听事件，在代码中有创建注册就对应了销毁反注册是一个好的编程习惯，不要依赖引擎来做这些事。
    def UnListenEvent(self):
        self.UnListenForEvent("MoreTorch", "moreTorchClientSystem", "toServer", self, self.toServer)
        self.UnDefineEvent("ToClient")
        self.UnDefineEvent("destory")

    #服务器通知客户端完成一些事件
    def toServer(self, args):
        self.jiSuanBlock2(args["mPlayerId"])
        self.sendMessage(args["mPlayerId"], "开启矿物查看成功！")

    #保存key与value
    def saveKeyValue(self, key, value):
        levelcomp = self.CreateComponent(serverApi.GetLevelId(), "Minecraft", "extraData")
        levelcomp.SetExtraData(key, value)

    #获取key得到value
    def getKeyValue(self, key):
        comp = self.CreateComponent(serverApi.GetLevelId(), "Minecraft", "extraData")
        return comp.GetExtraData(key)

    #玩家信息发送组件
    def sendMessage(self, eid, msg):
        comp = self.CreateComponent(eid, "Minecraft", "msg")
        comp2 = self.CreateComponent(eid, "Minecraft", "name")
        comp.SendMsg(comp2.GetName(), msg)

    #遍历计算方块数量，并筛选出矿物
    def jiSuanBlock2(self, eid):
        x = int(self.getPos(eid)[0])
        y = int(self.getPos(eid)[1])
        z = int(self.getPos(eid)[2])

        xx = x - 10
        yy = y + 10
        zz = z - 10

        xx2 = x + 10
        yy2 = y - 10
        zz2 = z + 10

        startx = min(xx, xx2)
        stopx = max(xx, xx2)
        starty = min(yy, yy2)
        stopy = max(yy, yy2)
        startz = min(zz, zz2)
        stopz = max(zz, zz2)

        for nx in range(startx, stopx + 1):
            for nz in range(startz, stopz + 1):
                for ny in range(starty, stopy + 1):
                    blockDict = self.isBlock(eid, nx, ny, nz)
                    aargs = self.CreateEventData()
                    aargs["blockName"] = blockDict["name"]
                    aargs["x"] = nx
                    aargs["y"] = ny
                    aargs["z"] = nz
                    self.NotifyToClient(eid, "ToClient", aargs)

    #获取当前坐标
    def getPos(self, eid):
        comp = self.CreateComponent(eid, "Minecraft", "pos")
        return comp.GetPos()

    #检测方块
    def isBlock(self, pid, x, y, z):
        comp = self.CreateComponent(pid, "Minecraft", "blockInfo")
        blockDict = comp.GetBlockNew((x, y, z))
        return blockDict

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        print "===== TutorialServerSystem Destroy ====="
        # 调用上面的反监听函数来销毁
        self.UnListenEvent()
