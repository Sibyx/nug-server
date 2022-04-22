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
    def __init__(self, fmt: str, value=None, scalar: bool = True):
        self._fmt = f"!{fmt}"
        self._scalar = scalar
        super().__init__(value)

    def to_bytes(self) -> bytes:
        return pack(self._fmt, self.value)

    def from_bytes(self, data: bytes):
        payload = unpack(self._fmt, data)
        self._value = payload[0] if self._scalar else payload


class PaddingField(StructField):
    def __init__(self, size: int):
        self._size = size
        super().__init__(f"{self._size}s")
        self._value = bytearray([0] * self._size)

    def from_bytes(self, data: bytes):
        pass


class ArrayField(Field):
    def __init__(self, field: Field, value=None):
        super().__init__(value)
        self._field = field

    def to_bytes(self) -> bytes:
        result = bytes()
        for i in self.value:
            self._field.value = i
            result += self._field.to_bytes()
        return result

    def from_bytes(self, data: bytes):
        pass


class FrameField(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def to_bytes(self) -> bytes:
        return self.value.get_value()

    def from_bytes(self, data: bytes):
        pass


class U8(StructField):
    def __init__(self, value=None):
        super().__init__("B", value, True)


class S8(StructField):
    def __init__(self, value=None):
        super().__init__("b", value, True)


class U16(StructField):
    def __init__(self, value=None):
        super().__init__("H", value, True)


class S16(StructField):
    def __init__(self, value=None):
        super().__init__("h", value, True)


class U32(StructField):
    def __init__(self, value=None):
        super().__init__("I", value, True)


class S32(StructField):
    def __init__(self, value=None):
        super().__init__("i", value, True)
