import unittest, requests, os, time

class WeatherAppTests(unittest.TestCase):

    def setUp(self):
        os.system('docker run -d -p 7070:8000 --name test tomergabayy/weatherapp gunicorn -w 3 --bind 0.0.0.0:8000 app:app')
        time.sleep(5)

    def tearDown(self):
        os.system('docker rm -f test')
    
    def test_smoke(self):
        self.response = requests.get("http://127.0.0.1:7070")
        self.status = self.response.status_code
        self.assertEqual(self.status,200,msg="app is not reachable")


if __name__=="__main__":
    unittest.main()
