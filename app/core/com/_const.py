class ConstError(TypeError):
   pass
class _const(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError(f'Can\'t rebind const ({name})')
        else:
            self.__setattr__(name, value)