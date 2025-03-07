import json
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
        settings = {
                "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
                "selectedDestinationId": "Save as PDF",
                "version": 2,
            }

        prefs = {
            "printing.print_preview_sticky_settings.appState": json.dumps(obj=settings),
            "download.default_directory": diretorio_download,
            "savefile.default_directory": diretorio_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "ignore-certificate-errors": True,
            "ignore-ssl-errors=yes": True,
            "allow-running-insecure-content": True,
            "disable-web-security": True,
            "profile.accept_untrusted_certs": True,
            "safebrowsing.enabled": True,
            "plugins.plugins_disabled": ["Chrome PDF Viewer"],
            "safebrowsing.disable_download_protection": True,
            "profile.default_content_settings.popups": 0,
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
