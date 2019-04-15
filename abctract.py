from six import add_metaclass
from abc import ABCMeta, abstractmethod, abstractproperty

@add_metaclass(ABCMeta)
class PublicTest():

    @abstractproperty
    def times(self):
        pass

    @abstractmethod
    def gendata(self):
        pass

    @abstractmethod
    def run(self):
        pass

