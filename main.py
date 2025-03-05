from webdriver_factory import WebDriverFactory


factory = WebDriverFactory()
with factory.get_driver() as driver:
    driver.get("http://google.com.br")
