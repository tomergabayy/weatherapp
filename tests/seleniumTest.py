import unittest, os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class WeatherappSearchtest(unittest.TestCase):

    def setUp(self):
        os.system('docker-compose up -d')
        self.driver = webdriver.Firefox()

    def test_positive(self):
        driver = self.driver
        driver.get("http://127.0.0.1:9090")
        self.assertIn("Weather App", driver.title)
        search_box = driver.find_element(By.NAME, "place")
        search_query = "ashdod"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(0.9)
        result = driver.find_element(By.NAME, "city")
        self.assertTrue(result.is_enabled())
    
    def test_negetive(self):
        driver = self.driver
        driver.get("http://127.0.0.1:9090")
        self.assertIn("Weather App", driver.title)
        search_box = driver.find_element(By.NAME, "place")
        search_query = "beer tuvia"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(0.4)
        result = driver.find_element(By.NAME, "img")
        self.assertTrue(result.is_enabled())


    def tearDown(self):
        self.driver.close()
        os.system('docker-compose kill')

if __name__ == "__main__":
    unittest.main()