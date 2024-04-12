class Pin:
    def __init__(self, id: int, title: str, url: str, image: str):
        self.id = id
        self.title = title
        self.url = url
        self.image = image

def to_pin(pin: dict):
    '''
    Converts a pin into the Pin class

            Parameters:
                    pin (dict): The pin

            Returns:
                    pin (Pin): A proper instance of the Pin class
    '''
    return Pin(
        id = pin['id'],
        title = pin['title'],
        url = pin['url'],
        image = pin['image']
    )