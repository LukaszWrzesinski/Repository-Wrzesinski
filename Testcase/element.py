class BaseElement:
    def __init__(self, driver, by, value):
        self.driver = driver
        self.by = by
        self.value = value

    def find(self):
        return self.driver.find_element(self.by, self.value)

    def click(self):
        element = self.find()
        element.click()

    def send_keys(self, keys):
        element = self.find()
        element.send_keys(keys)