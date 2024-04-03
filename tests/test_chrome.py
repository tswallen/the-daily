from .context import daily

import unittest


class ChromeQuotesTestSuite(unittest.TestCase):

    chrome = daily.Chrome()

    # def test_print_first_three_tab_urls(self):
    #     self.assertIsNotNone(self.chrome.print_first_three_tab_urls())

    # def test_screenshot_first_tab(self):
    #     self.assertIsNone(self.chrome.screenshot_first_tab())

    # def test_capture_tabs_info(self):
    #     self.assertIsNotNone(self.chrome.capture_tabs_info())

    def test_find_bookmarks_in_nested_folder(self):
        self.assertIsNotNone(self.chrome.find_bookmarks_in_nested_folder())

if __name__ == '__main__':
    unittest.main()