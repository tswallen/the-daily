class Message:
    def __init__(self, author: str, media: str = None, content: str = None):
        self.author = author
        self.media = media
        self.content = content