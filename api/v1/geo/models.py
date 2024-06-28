from dataclasses import dataclass

@dataclass(frozen=True)
class City:
    city: str
    country: str
    flag: str = None
    dial_code: str = None
    emoji: str = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if value is not None:
                yield attr, value

@dataclass(frozen=True)
class Country:
    country: str
    flag: str = None
    dial_code: str = None
    emoji: str = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if value is not None:
                yield attr, value