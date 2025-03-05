from abc import ABC, abstractmethod


class WebDriverOptions(ABC):
    """Interface para configuração de opções e preferências do navegador."""

    @abstractmethod
    def get_prefs(self):

    @abstractmethod
    def get_options(self):
