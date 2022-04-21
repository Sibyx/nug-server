from abc import abstractmethod

from enum import Enum
from struct import pack, unpack
from typing import Type


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractmethod
    def from_bytes(self, data: bytes):
        pass


class StringField(Field):
    def from_bytes(self, data: bytes):
        self.value = data.decode()

    def to_bytes(self) -> bytes:
        return self.value.encode()


class EnumField(StringField):
    def __init__(self, enum_type: Type[Enum], value=None):
        self._enum = enum_type
        super().__init__(value)

    def to_bytes(self) -> bytes:
        return self.value.value.encode()

    def from_bytes(self, data: bytes):
        self.value = self._enum(data.decode())


class StructField(Field):
    def __init__(self, fmt: str, value=None):
        self._fmt = fmt
        super().__init__(value)

    def to_bytes(self) -> bytes:
        return pack(self._fmt, self.value)

    def from_bytes(self, data: bytes):
        self._value = unpack(self._fmt, data)


class PaddingField(StructField):
    def __init__(self, size: int):
        self._size = size
        super().__init__(f"{self._size}s")
        self._value = bytearray([0] * self._size)

    def from_bytes(self, data: bytes):
        pass


class ArrayField(Field):
    def __init__(self, field_type: Type[Field], value=None):
        super().__init__(value)
        self._field_type = field_type

    def to_bytes(self) -> bytes:
        result = bytearray()
        for i in self.value:
            result += i.to_bytes()
        return result

    def from_bytes(self, data: bytes):
        pass
