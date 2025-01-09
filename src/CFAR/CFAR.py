from abc import ABCMeta, abstractmethod

from common.load_yaml import load_yaml


class CFAR(metaclass=ABCMeta):
    @abstractmethod
    def calculate_average():
        pass

    @abstractmethod
    def judgment_threshold(after_cfar_data):
        pass
