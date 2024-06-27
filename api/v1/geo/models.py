class City:
    def __init__(self, city: str, country: str, flag: str = None, dial_code: str = None, emoji: str = None):
        self.city = city
        self.country = country
        self.flag = flag
        self.dial_code = dial_code
        self.emoji = emoji

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if value is not None:
                yield attr, value

    
class Country:
    def __init__(self, country: str, flag: str = None, dial_code: str = None, emoji: str = None):
        self.country = country
        self.flag = flag
        self.dial_code = dial_code
        self.emoji = emoji

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if value is not None:
                yield attr, value