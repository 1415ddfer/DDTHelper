import os
import importlib
from multiprocessing import Manager


class LoadPlugin:
    path = 'gamePlugin'

    def __init__(self):
        manager = Manager()
        self.plugin_dic = manager.dict()
        self.getFile()

    def getFile(self):
        try:
            for i in os.listdir(self.path):
                if i.endswith('.py'):
                    print(i)
                    self.check_mode(i.split('.')[0])
        except Exception as e:
            print(e)

    def check_mode(self, mode):
        metaclass = importlib.import_module(self.path + '.' + mode)
        try:
            _plugin = metaclass._main()

            self.plugin_dic[_plugin.name] = _plugin
        except Exception as e:
            print(e)
        pass
