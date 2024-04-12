from bson.binary import Binary
#from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Specify the URL of your Selenium Standalone Chrome container


# Connect to the remote WebDriver



# TODO: keep these?
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service = service)

class Bookmark:
    def __init__(self, title: str, url: str, screenshot: Binary | bytes | None): # Might need to change to bytes
        self.title = title
        self.url = url
        self.screenshot = screenshot if screenshot is not None else self.capture_screenshot()

    def capture_screenshot(self) -> Binary:
        '''
        Captures a screenshot of the bookmark

                Returns:
                        screenshot (Binary): A binary representation of the screenshot
        '''
        #service = Service(ChromeDriverManager().install())
        #driver = webdriver.Chrome(service = service)
        selenium_url = 'http://selenium-chrome:4444/wd/hub'  # Adjust this as necessary

        # Set up Chrome options
        chrome_options = ChromeOptions()
        # Add any Chrome-specific options here, e.g., chrome_options.add_argument('--headless')

        # Connect to the remote WebDriver
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=chrome_options
        )
        try:
            driver.get(self.url)
            screenshot_data = driver.get_screenshot_as_png()
        finally:
            driver.quit()

        return Binary(screenshot_data)

def to_bookmark(bookmark: dict):
    '''
    Converts a bookmark into the Bookmark class

            Parameters:
                    bookmark (dict): The bookmark

            Returns:
                    bookmark (Bookmark): A proper instance of the Bookmark class
    '''
    return Bookmark(
        title = bookmark['title'],
        url = bookmark['url'],
        screenshot = bookmark.get('screenshot')
    )