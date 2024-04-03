import logging
from logging import INFO, DEBUG, ERROR

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import csv

import json

class Chrome:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service = self.service, options = self.options)

    def print_first_three_tab_urls(self):
        test = []
        for handle in self.driver.window_handles[:3]:
            self.driver.switch_to.window(handle)
            print(INFO, f'Url in tab: {self.driver.current_url}')
            logging.log(INFO, f'Url in tab: {self.driver.current_url}')
            test.append(self.driver.current_url)
        return test
    
    def screenshot_first_tab(self):

        # Assuming you've already navigated to your tabs, we just switch and take screenshots
        for tab_index, handle in enumerate(self.driver.window_handles):
            self.driver.switch_to.window(handle)
            time.sleep(2)  # Give some time for the tab to load or become active
            screenshot_filename = f"tab_{tab_index + 1}_screenshot.png"
            self.driver.get_screenshot_as_file(screenshot_filename)
            print(f"Screenshot saved for tab {tab_index + 1}: {screenshot_filename}")

        # url = "https://google.com"
        # jpeg_path='screenshot.png'

        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")  # Optional on Windows, mandatory on Linux
        # chrome_options.add_argument("--window-size=1920x1080")  # Set the window size

        # # Set up the WebDriver
        # service = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service, options=chrome_options)

        # # Navigate to the URL and take a screenshot
        # driver.get(url)
        # driver.get_screenshot_as_file(jpeg_path)
        # print(f"Screenshot saved as {jpeg_path}")

        # jpeg_path='screenshot.png'
        # first_tab = self.driver.window_handles[0]
        # self.driver.switch_to.window(first_tab)
        
        # # Take a screenshot and save it
        # self.driver.get_screenshot_as_file(jpeg_path)
        
        # print(f"Screenshot saved as {jpeg_path}")

        # Optional: Close the driver if you don't need it anymore
        # driver.quit()
            
    def capture_tabs_info(self):
        urls = []
        screenshots = []

        tabs_info = []

        for index, handle in enumerate(self.driver.window_handles):
            self.driver.switch_to.window(handle)
            time.sleep(2)  # Wait for the tab to fully load

            # Save the URL
            urls.append(self.driver.current_url)

            # Take a screenshot
            screenshot_filename = f"C:\\Screenshots\\tab_{index}_screenshot.png"
            self.driver.get_screenshot_as_file(screenshot_filename)
            screenshots.append(screenshot_filename)
            tabs_info.append([self.driver.current_url, self.driver.title, screenshot_filename])

            print(f"Tab {index}: Title = \"{self.driver.title}\", Screenshot = {screenshot_filename}")

        # Write to CSV
        with open('tabs_info.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Title', 'Screenshot Filename'])
            writer.writerows(tabs_info)

        # Optionally, close the driver if you don't need the session anymore
        # driver.quit()
        
        return urls, screenshots
    
    def find_bookmarks_in_nested_folder(self):
        bookmarks_file = 'C:\\Users\\tswal\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks'  # Update this path
        folder_path = ['Old Stuff', 'New folder']   # The name of the folder you want to extract bookmarks from
        with open(bookmarks_file, 'r', encoding='utf-8') as file:
            bookmarks_data = json.load(file)

        def find_folder(bookmarks, folder_path):
            # Base case: If the folder path is empty, return the current bookmarks
            if not folder_path:
                return bookmarks
            current_folder_name = folder_path.pop(0)
            for item in bookmarks:
                if item['type'] == 'folder' and item['name'] == current_folder_name:
                    return find_folder(item['children'], folder_path)
            return []

        bookmarks_list = []
        # Start the search from the root. Adjust the root keys as necessary.
        for root_key in ['bookmark_bar', 'other', 'synced']:
            root_bookmarks = bookmarks_data['roots'].get(root_key, {}).get('children', [])
            bookmarks_list.extend(find_folder(root_bookmarks, folder_path.copy()))

        print(bookmarks_list[0])

        # Filter out to keep only URLs
        bookmarks = [{'title': bookmark['name'], 'url': bookmark['url']} for bookmark in bookmarks_list if bookmark.get('type') == 'url']


        with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
            # Create a CSV writer object
            writer = csv.DictWriter(file, fieldnames=bookmarks[0].keys())
            
            # Write the header (dictionary keys)
            writer.writeheader()
            
            # Write the rows (dictionary values)
            writer.writerows(bookmarks[:10])
        print(bookmarks[0])
        
        return bookmarks