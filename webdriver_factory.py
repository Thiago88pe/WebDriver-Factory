import os
from abc import ABC, abstractmethod

from selenium.webdriver.chrome.options import Options as ChromeOptions

class WebDriverOptions(ABC):
    """Interface para configuração de opções e preferências do navegador."""

    @abstractmethod
    def get_prefs(self):

    @abstractmethod
    def get_options(self):

class ChromeWebDriverOptions(WebDriverOptions):
    """Configuração de opções e preferências do navegador Chrome."""
    def get_prefs(self):

        diretorio_download = os.getcwd()

        prefs = {
            "download.default_directory": diretorio_download,
            "savefile.default_directory": diretorio_download,

        }
        return prefs
    
    def get_options(self):

        options = ChromeOptions()

        options.add_experimental_option(name="prefs", value=self.get_prefs())
        return options
