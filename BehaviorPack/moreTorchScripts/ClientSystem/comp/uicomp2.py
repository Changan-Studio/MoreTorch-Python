# -*- coding: utf-8 -*-

import client.extraClientApi as clientApi
ComponentCls = clientApi.GetComponentCls()

# Component要继承于基类才能生效
class uicompClient2(ComponentCls):
    def __init__(self, entityId):
        ComponentCls.__init__(self, entityId)
        # 这里设置了一个开关来开关更新射击
        self.mState = False

    @property
    def switch(self):
        return self.mState

    @switch.setter
    def switch(self, val):
        self.mState = val