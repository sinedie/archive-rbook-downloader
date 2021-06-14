from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class BaseElement:
    def __init__(self, driver, locate_by, locate_value, multiple=False):
        self.driver = driver
        locator = (getattr(By, locate_by.upper(), "ID"), locate_value)
        find_element = driver.find_elements if multiple else driver.find_element
        WebDriverWait(driver, 100).until(lambda driver: find_element(*locator))
        self.element = find_element(*locator)


class Text(BaseElement):
    @property
    def text(self):
        return self.element.text
    
    @property
    def width(self):
        return self.element.size['width']

    @property
    def height(self):
        return self.element.size['height']

class TextInput(BaseElement):
    def write(self, value):
        self.element.clear()
        self.element.send_keys(*value)

    @property
    def value(self):
        return self.element.get_attribute("value")


class Button(BaseElement):
    def click(self):
        try:
            can_click = getattr(self.element, "click", None)
            if callable(can_click):
                self.element.click()
        except:
            # Using javascript if usual click function does not work
            self.driver.execute_script("arguments[0].click();", self.element)


class Image(BaseElement):
    @property
    def src(self):
        return [img.get_attribute("src") for img in self.element]