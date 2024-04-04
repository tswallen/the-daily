from .context import daily

import unittest


class ChromeQuotesTestSuite(unittest.TestCase):

    chrome = daily.Chrome()

    # def test_log_bookmarks(self):
    #     self.assertIsNone(self.chrome.log_bookmarks(2))
    #     documents = list(self.chrome.mongo.find({}))
    #     self.assertIsNotNone(documents) # Assumes we have bookmarks
    #     self.assertIsInstance(documents, list)

    # def test_get_bookmarks(self):
    #     bookmarks = self.chrome.get_bookmarks()
    #     self.assertIsNotNone(bookmarks) # Assumes we have bookmarks
    #     self.assertIsInstance(bookmarks, list)
    #     self.assertIsInstance(bookmarks[0], daily.Bookmark)
    #     self.assertIsNotNone(bookmarks[0].screenshot)

    def test_clear_bookmarks(self):
         #self.chrome.mongo.delete_many({})
         documents = list(self.chrome.mongo.find({}))
         print(documents)

if __name__ == '__main__':
    unittest.main()