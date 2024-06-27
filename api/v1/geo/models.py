from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class City:
    city: str
    country: str
    flag: str = None
    dial_code: str = None
    emoji: str = None

    def __iter__(self):
        for attr in self.__slots__:
            value = getattr(self, attr)
            if value is not None:
                yield attr, value

@dataclass(frozen=True, slots=True)
class Country:
    country: str
    flag: str = None
    dial_code: str = None
    emoji: str = None

    def __iter__(self):
        for attr in self.__slots__:
            value = getattr(self, attr)
            if value is not None:
                yield attr, value