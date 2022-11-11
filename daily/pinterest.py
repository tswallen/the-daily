from py3pin.Pinterest import Pinterest
import ipywidgets as widgets
from IPython.display import Image

from dotenv import load_dotenv

from os import environ

# Define user variables

max_items = 100                        # This is the maximum number of images you want to view
slideshow_interval = 5000              # This is in milliseconds
target_boards = ['Board 1', 'Board 2'] # This is the list of boards you wish to view (case sensitive)

# Initialise Pinterest

load_dotenv()

pinterest = Pinterest(email = environ['PINTEREST_EMAIL'],
                      password = environ['PINTEREST_PASSWORD'],
                      username = environ['PINTEREST_USERNAME'],
                      cred_root = 'credentials')

boards = pinterest.boards()

# Populate urls

urls = []

for board in boards:
    if board['name'] in target_boards:
        rec_pins = []
        rec_batch = pinterest.board_recommendations(board_id = board['id'])
        while len(rec_batch) > 0 and len(rec_pins) < max_items:
            rec_pins += rec_batch
        for pin in rec_pins:
            if 'images' in pin:
                urls.append(pin['images']['orig']['url'])

def show_image(image):
    return Image(url = urls[image - 1])

widgets.interact(show_image, image = widgets.Play(interval = slideshow_interval, max = max_items))