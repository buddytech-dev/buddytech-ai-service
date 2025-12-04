import unittest
from core.sentiment import classify_text

class TestSentiment(unittest.TestCase):

    def test_positive(self):
        text = "I love this product!"
        result = classify_text(text)
        self.assertEqual(result, "positive")

    def test_negative(self):
        text = "This project is a disaster."
        result = classify_text(text)
        self.assertEqual(result, "negative")

    def test_neutral(self):
        text = "I went to the store."
        result = classify_text(text)
        self.assertEqual(result, "neutral")

if __name__ == "__main__":
    unittest.main()
