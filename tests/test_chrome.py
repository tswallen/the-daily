from .context import daily

import unittest


class ChromeTestSuite(unittest.TestCase):

    chrome = daily.Chrome()

    def test_log_bookmarks(self):
        self.assertIsNone(self.chrome.log_bookmarks(2))

    def test_get_bookmarks(self):
        bookmarks = self.chrome.get_bookmarks()
        self.assertIsNotNone(bookmarks) # Assumes we have bookmarks

    # def test_get_bookmarks_with_screenshot(self):
    #     bookmarks = self.chrome.get_bookmarks(with_screenshot = True)
    #     self.assertIsNotNone(bookmarks) # Assumes we have bookmarks
    #     self.assertIsInstance(bookmarks, list)
    #     self.assertIsInstance(bookmarks[0], daily.Bookmark)
    #     self.assertIsNotNone(bookmarks[0].screenshot)

if __name__ == '__main__':
    unittest.main()