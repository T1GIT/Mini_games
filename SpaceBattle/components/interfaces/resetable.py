class Resetable:
    """
    Interface.
    Owner can erase its internal state, using <Resetable.Object>.reset()
    """
    def reset(self) -> None:
        """ Erasing class'es child's state """
        self.__init__()
