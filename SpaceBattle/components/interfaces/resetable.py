from abc import ABC, abstractmethod


class Resetable(ABC):
    """
    Interface.
    Owner can erase its internal state, using <Resetable.Object>.reset()
    """
    @abstractmethod
    def reset(self) -> None:
        """ Erasing class'es child's state """
        pass
