# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import client.extraClientApi as clientApi
# 获取客户端system的基类ClientSystem
ClientSystem = clientApi.GetClientSystemCls()
from moreTorchScripts.ClientSystem.coroutineMgrGas import CoroutineMgr

# 在modMain中注册的Client System类
class moreTorchClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        # 首先初始化TutorialClientSystem的基类ClientSystem
        super(moreTorchClientSystem, self).__init__(namespace, systemName)
        print "==== TutorialClientSystem Init ===="
        self.ListenEvent()
        self.destorySfxsId = []
        self.mPlayerId = clientApi.GetLocalPlayerId()

    #监听事件集合
    def ListenEvent(self):
        self.DefineEvent("toServer")
        self.ListenForEvent("MoreTorch", "moreTorchServerSystem", "ToClient", self, self.ToClient)
        #self.ListenForEvent("MoreTorch", "moreTorchServerSystem", "destory", self, self.destory)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.OnUiInit)

    #接收服务器消息并判断矿物
    def ToClient(self, args):

        if args["blockName"] == "minecraft:iron_ore":
            self.Sfx("textures/sfxs/t", args["x"], args["y"], args["z"])

        if args["blockName"] == "minecraft:coal_ore":
            self.Sfx("textures/sfxs/m", args["x"], args["y"], args["z"])

        if args["blockName"] == "minecraft:gold_ore":
            self.Sfx("textures/sfxs/hj", args["x"], args["y"], args["z"])

        if args["blockName"] == "minecraft:diamond_ore":
            self.Sfx("textures/sfxs/zs", args["x"], args["y"], args["z"])

        if args["blockName"] == "minecraft:emerald_ore":
            self.Sfx("textures/sfxs/lbs", args["x"], args["y"], args["z"])

        if args["blockName"] == "minecraft:lapis_ore":
            self.Sfx("textures/sfxs/qjs", args["x"], args["y"], args["z"])

        if args["blockName"] == "minecraft:redstone_ore":
            self.Sfx("textures/sfxs/hs", args["x"], args["y"], args["z"])

    #初始化UI事件，用于创建UI时用到
    def OnUiInit(self, args=None):
        clientApi.RegisterUI("MoreTorch", "demoUi", "moreTorchScripts.ClientSystem.ui.demoUi.demoUiScreen", "demoUi.main")
        clientApi.CreateUI("MoreTorch", "demoUi", {"isHud": 1})
        print "UI初始化成功"

        #初始化完毕隐藏off按钮
        uiNode = clientApi.GetUI("MoreTorch", "demoUi")
        uiNode.SetVisible("/panel/off_btn", False)

    #销毁序列帧图函数
    def destorySfxs(self):
        for id in self.destorySfxsId:
            self.DestroyEntity(id)

    #创建序列帧函数，并让其重复播放，透视，面朝相机视角
    def Sfx(self, data, x, y, z):
        frameEntityId = self.CreateEngineSfx(data)
        frameAniTransComp = self.CreateComponent(frameEntityId, "Minecraft", "frameAniTrans")
        frameAniTransComp.SetPos((x, y, z))
        frameAniTransComp.SetRot((0, 0, 0))
        frameAniTransComp.SetScale((0.2, 0.2, 0.2))
        frameAniControlComp = self.CreateComponent(frameEntityId, "Minecraft", "frameAniControl")
        frameAniControlComp.Play()
        frameAniControlComp.SetDeepTest(False)
        frameAniControlComp.SetLoop(True)
        frameAniControlComp.SetFaceCamera(True)
        self.destorySfxsId.append(frameEntityId)
        print "播放序列帧成功"


    #创建系统完毕1秒30次执行
    def Update(self):

        #创建自定义组件state，用于传递UI端和客户端信息操作
        comp = self.CreateComponent(self.mPlayerId, "MoreTorch", "state")
        if comp.switch:
            self.fs_on()
            CED = self.CreateEventData()
            CED["mPlayerId"] = self.mPlayerId
            self.NotifyToServer("toServer", CED)
            comp.switch = False

        #同上↑
        comp2 = self.CreateComponent(self.mPlayerId, "MoreTorch", "state2")
        if comp2.switch:
            self.fs_off()
            self.destorySfxs()
            comp2.switch = False

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        self.UnDefineEvent("toServer")
        self.UnListenForEvent("MoreTorch", "moreTorchServerSystem", "ToClient", self, self.ToClient)
        #self.UnListenForEvent("MoreTorch", "moreTorchServerSystem", "destory", self, self.destory)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self, self.OnTick)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.OnUiInit)

    #UI开关逻辑函数
    def fs_on(self):
        uiNode = clientApi.GetUI("MoreTorch", "demoUi")
        uiNode.SetVisible("/panel/on_btn", False)
        uiNode.SetVisible("/panel/off_btn", True)

    # UI开关逻辑函数
    def fs_off(self):
        uiNode = clientApi.GetUI("MoreTorch", "demoUi")
        uiNode.SetVisible("/panel/on_btn", True)
        uiNode.SetVisible("/panel/off_btn", False)