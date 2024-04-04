class Post:
    def __init__(self, id: int, title: str, url: str, image: str):
        self.id = id
        self.title = title
        self.url = url
        self.image = image

def to_post(post: dict):
    '''
    Converts a post into the Post class

            Parameters:
                    post (dict): The post

            Returns:
                    post (Post): A proper instance of the Post class
    '''
    return Post(
        id = post['id'],
        title = post['title'],
        url = post['url'],
        image = post['image']
    )