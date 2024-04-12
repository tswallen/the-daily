from dotenv import load_dotenv

load_dotenv()

from .classes.bookmark import Bookmark, to_bookmark
from .classes.message import Message
from .classes.pin import Pin
from .classes.post import Post
from .classes.quote import Quote

from .chrome import Chrome
from .discord import Discord
# Instagram
from .pinterest import Pinterest
from .quotes import Quotes
from .reddit import Reddit
# Tasks
# Weather
