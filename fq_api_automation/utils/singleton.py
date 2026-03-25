class Singleton(type):

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            # 如果 __instance 不存在，创建新的实例
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            # 如果存在，直接返回
            return self.__instance