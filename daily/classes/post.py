class Post:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

def to_post(post: dict):
    '''
    Converts a post into the Post class

            Parameters:
                    post (dict): The post

            Returns:
                    post (Post): A proper instance of the Post class
    '''
    return Post(
        title = post['title'],
        url = post['url']
    )