import unittest
from preprocess import remove_stopwords  # you'll write this function next

class TestTextPreprocessing(unittest.TestCase):

    def test_remove_some_stopwords(self):
        text = "this is a simple test"
        stopwords = ["is", "a"]
        result = remove_stopwords(text, stopwords)
        self.assertEqual(result, "this simple test")

    def test_remove_all_stopwords(self):
        text = "the and is"
        stopwords = ["the", "and", "is"]
        result = remove_stopwords(text, stopwords)
        self.assertEqual(result, "")

    def test_no_stopwords(self):
        text = "machine learning model"
        stopwords = []
        result = remove_stopwords(text, stopwords)
        self.assertEqual(result, "machine learning model")

    def test_empty_text(self):
        text = ""
        stopwords = ["the"]
        result = remove_stopwords(text, stopwords)
        self.assertEqual(result, "")

if __name__ == "__main__":
    unittest.main()
