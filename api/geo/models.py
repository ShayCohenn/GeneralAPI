class City:
    def __init__(
            self, 
            city: str,
            country: str, 
            flag: str = None, 
            dial_code: str = None, 
            emoji: str = None):
        self.city = city
        self.country = country
        self.flag = flag if flag is not None else None
        self.dial_code = dial_code if dial_code is not None else None
        self.emoji = emoji if emoji is not None else None
    
    def to_dict(self):
        data = {attr: getattr(self, attr) 
                for attr in self.__dict__ if getattr(self, attr) is not None 
                and attr not in ['city', 'country']}
        data['city'] = self.city
        data['country'] = self.country
        return data
    
class Country:
    def __init__(
            self, 
            country: str, 
            flag: str = None, 
            dial_code: str = None, 
            emoji: str = None):
        self.country = country
        self.flag = flag if flag is not None else None
        self.dial_code = dial_code if dial_code is not None else None
        self.emoji = emoji if emoji is not None else None
    
    def to_dict(self):
        data = {attr: getattr(self, attr) 
                for attr in self.__dict__ if getattr(self, attr) is not None 
                and attr not in ['country']}
        data['country'] = self.country
        return data