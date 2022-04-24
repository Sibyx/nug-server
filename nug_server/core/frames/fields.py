from abc import abstractmethod

from enum import Enum
from io import BytesIO
from struct import pack, unpack, calcsize
from typing import Type, Optional


class Field:
    def __init__(self, value=None):
        self._value = value

    def __call__(self, value) -> 'Field':
        self._value = value
        return self

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @abstractmethod
    def read(self, buffer: BytesIO):
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractmethod
    def from_bytes(self, data: bytes):
        pass


class StringField(Field):
    def from_bytes(self, data: bytes):
        self.value = data.decode()

    def read(self, buffer: BytesIO):
        self.from_bytes(buffer.read())

    def to_bytes(self) -> bytes:
        return self.value.encode()


class EnumField(StringField):
    def __init__(self, enum_type: Type[Enum], value=None):
        self._enum = enum_type
        super().__init__(value)

    def to_bytes(self) -> bytes:
        return self.value.value.encode()

    def read(self, buffer: BytesIO):
        self.from_bytes(buffer.read())

    def from_bytes(self, data: bytes):
        self.value = self._enum(data.decode())


class StructField(Field):
    def __init__(self, fmt: str, value=None, scalar: bool = True):
        self._fmt = f"!{fmt}"
        self._scalar = scalar
        super().__init__(value)

    def read(self, buffer: BytesIO):
        size = calcsize(self._fmt)
        self.from_bytes(buffer.read(size))

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
    def __init__(self, field: Field, value=None, header: Optional[Field] = None, size: int = None):
        super().__init__(value)
        self._field = field
        self.length_header = header
        self.size = size

    def read(self, buffer: BytesIO):
        if not (self.length_header or self.size):
            raise ValueError("Length header or size have to be provided!")

        if self.length_header:
            self.length_header.read(buffer)
            self.size = self.length_header.value

        self.value = []
        for i in self.size:
            self.value.append(self._field.read(i).value)

    def to_bytes(self) -> bytes:
        result = bytes()

        if self.length_header:
            result += self.length_header(len(self.value)).to_bytes()

        for i in self.value:
            result += self._field(i).to_bytes()
        return result

    def from_bytes(self, data: bytes):
        pass


class FrameField(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def to_bytes(self) -> bytes:
        return self.value.get_value()

    def read(self, buffer: BytesIO):
        self.value.read(buffer)

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
