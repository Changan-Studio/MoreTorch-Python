# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
# 获取客户端system的基类ClientSystem
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


#UI端类
class demoUiScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.mPlayerId = clientApi.GetLocalPlayerId()
        print "666"

    #当按下按钮on时执行
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def on_click(self, args):
        print "按下开"
        comp = clientApi.GetComponent(self.mPlayerId, "MoreTorch", "state")
        comp.switch = True
        return ViewRequest.Refresh | ViewRequest.Exit

    # 当按下按钮off时执行
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def off_click(self, args):
        print "按下关"
        comp = clientApi.GetComponent(self.mPlayerId, "MoreTorch", "state2")
        comp.switch = True
        return ViewRequest.Refresh | ViewRequest.Exit