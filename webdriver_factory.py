import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv(override=True)


class WebDriverOptions(ABC):
    """Interface para configuração de opções e preferências do navegador."""

    @abstractmethod
    def get_prefs(self):
        pass

    @abstractmethod
    def get_options(self):
        pass

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
        if os.getenv(key="HEADLESS", default="false").lower() == "true":
            options.add_argument(argument="--headless")

        options.add_experimental_option(name="prefs", value=self.get_prefs())
        return options

class WebDriverFactory:
    """Factory para criar WebDriver de diferentes navegadores."""
    _browsers = {
        "chrome": (Chrome, ChromeWebDriverOptions, ChromeService, ChromeDriverManager),

    }
    def __init__(self) -> None:
        """Inicializa a fábrica de WebDriver, determinando o navegador a ser utilizado."""
        self.browser = os.getenv(key="BROWSER", default="chrome").lower()
        if self.browser not in self._browsers:
            raise ValueError(f"Navegador '{self.browser.upper()}' não suportado.")

    def get_driver(self):
        """Cria e retorna uma instância do WebDriver configurado para o navegador escolhido."""

        driver_class, webdriver_options, service, manager  = self._browsers[self.browser]

        # Configura as opções do navegador
        options = webdriver_options().get_options()

        # Configura o serviço do navegador
        service_instance = service(executable_path=manager().install())

        # Cria a instância do WebDriver
        driver = driver_class(options=options, service=service_instance)
        return driver
