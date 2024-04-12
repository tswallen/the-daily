from dotenv import load_dotenv

load_dotenv()

from .classes.bookmark import Bookmark, to_bookmark
from .classes.message import Message
from .classes.pin import Pin
from .classes.post import Post
from .classes.quote import Quote
from .classes.task import Task

from .chrome import Chrome
from .discord import Discord
# Instagram
from .pinterest import Pinterest
from .pocket import Pocket
from .quotes import Quotes
from .reddit import Reddit
from .tasks import Tasks
# Weather
