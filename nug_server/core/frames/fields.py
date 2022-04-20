from abc import abstractmethod


# https://docs.python.org/3/library/struct.html
from struct import pack


class Field:
    def __init__(self, fmt: str, value=None, read_only=False):
        self._value = value
        self._read_only = read_only
        self._fmt = fmt

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._read_only:
            raise Exception("Read-only field!")
        self._value = value

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractmethod
    def from_bytes(self, data: bytes):
        pass


class String(Field):
    def __init__(self, value=None, read_only=False):
        super().__init__("s", value, read_only)

    def from_bytes(self, data: bytes):
        self.value = data.decode()

    def to_bytes(self) -> bytes:
        return self._value.encode()


class Padding(Field):
    def __init__(self, size: int):
        self._size = size
        super().__init__(f"{self._size}s", read_only=True)

    def from_bytes(self, data: bytes):
        pass

    def to_bytes(self) -> bytes:
        return pack(self._fmt, bytearray([0] * self._size))
