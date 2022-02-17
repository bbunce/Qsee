import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
class Testindex(unittest.TestCase):
    """class to test basic functionality of a web-based input form"""
    def setUp(self):
        """set up function to set the web driver, in this case chrome"""
        self.driver=webdriver.Chrome('./chromedriver')
    def test_input_form (self):

        """Please ensure server is running on local server before beginning test and
        that you have install the correct chromedriver version for your system..."""

        driver = self.driver
        driver.get('http://127.0.0.1:8000/test_input/8/3/')

        driver.find_element(By.ID, 'id_result').send_keys(random.randint(27, 30))
        driver.find_element(By.ID, 'id_test_date').send_keys('20/01/2023')
        driver.find_element(By.ID, 'id_operator').send_keys('GD')
        driver.find_element(By.ID, 'id_note').send_keys(random.randint(1, 30000))
        driver.find_element_by_name('save').click()
        driver.back()
        driver.refresh()

        driver.find_element(By.ID, 'id_result').send_keys(random.randint(27, 30))
        driver.find_element(By.ID, 'id_test_date').send_keys('20/01/2023')
        driver.find_element(By.ID, 'id_operator').send_keys('GD')
        driver.find_element(By.ID, 'id_note').send_keys(random.randint(1, 30000))
        driver.find_element_by_name('save').click()
        driver.back()
        driver.refresh()

        driver.find_element(By.ID, 'id_result').send_keys(random.randint(27, 30))
        driver.find_element(By.ID, 'id_test_date').send_keys('20/01/2023')
        driver.find_element(By.ID, 'id_operator').send_keys('GD')
        driver.find_element(By.ID, 'id_note').send_keys(random.randint(1, 30000))
        driver.find_element_by_name('save').click()
        driver.back()
        driver.refresh()

        driver.find_element(By.ID, 'id_result').send_keys(random.randint(27, 30))
        driver.find_element(By.ID, 'id_test_date').send_keys('20/01/2023')
        driver.find_element(By.ID, 'id_operator').send_keys('GD')
        driver.find_element(By.ID, 'id_note').send_keys(random.randint(1, 30000))
        driver.find_element_by_name('save').click()
        driver.back()
        driver.refresh()

        driver.find_element(By.ID, 'id_result').send_keys(random.randint(27, 30))
        driver.find_element(By.ID, 'id_test_date').send_keys('20/01/2023')
        driver.find_element(By.ID, 'id_operator').send_keys('GD')
        driver.find_element(By.ID, 'id_note').send_keys(random.randint(1, 30000))
        driver.find_element_by_name('save').click()
        driver.back()
        driver.refresh()

        driver.find_element(By.ID, 'id_result').send_keys(random.randint(27, 30))
        driver.find_element(By.ID, 'id_test_date').send_keys('20/01/2023')
        driver.find_element(By.ID, 'id_operator').send_keys('GD')
        driver.find_element(By.ID, 'id_note').send_keys(random.randint(1, 30000))
        driver.find_element_by_name('save').click()
        driver.back()
        driver.refresh()

if __name__=="__main__":
    unittest.main()