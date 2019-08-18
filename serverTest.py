import unittest
import requests


class TestStringMethods(unittest.TestCase):

    def test_create_ai(self):
        url = 'http://localhost:5000/ai-server/script-bot/Intellectual000/new?gameId=1&playerId=1'
        res = requests.get(url)
        response = "/ai-server/Intellectual000/script-bot/1/1"
        self.assertEqual(res.text, response)

    def test_update_ai(self):
        url = 'http://127.0.0.1:5000/ai-server/1/1/'
        data = ({"id": 1, "users": {"1": {}}})
        res = requests.post(url, json=data)
        response = """[
  {
    "arguments": {
      "arg1": "value1"
    }, 
    "commandName": "moveOrAttack"
  }
]
"""
        self.assertEqual(res.text, response)




if __name__ == '__main__':
    unittest.main()
