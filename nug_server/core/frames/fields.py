import io
from abc import abstractmethod
from asyncio import StreamReader, StreamWriter

from struct import pack, unpack, calcsize
from typing import Optional

import copy


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
    async def read(self, buffer: StreamReader):
        pass

    def write(self, buffer: StreamWriter):
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @abstractmethod
    def from_bytes(self, data: bytes):
        pass


class StructField(Field):
    def __init__(self, fmt: str, value=None, scalar: bool = True):
        self._fmt = f"!{fmt}"
        self._scalar = scalar
        super().__init__(value)

    async def read(self, buffer: StreamReader):
        size = calcsize(self._fmt)
        self.from_bytes(await buffer.read(size))

    def write(self, buffer: StreamWriter):
        data = pack(self._fmt, self.value)
        buffer.write(data)

    def to_bytes(self) -> bytes:
        return pack(self._fmt, self.value)

    def from_bytes(self, data: bytes):
        payload = unpack(self._fmt, data)
        self._value = payload[0] if self._scalar else payload


class StringField(StructField):
    def __init__(self, size: int = None, header: Optional[Field] = None,):
        self.size = size
        self.header = header
        super().__init__(f"{self.size}s" if self.size is not None else "s")

    async def read(self, buffer: StreamReader):
        if not (self.header or self.size):
            raise ValueError("Length header or size have to be provided!")

        if self.header:
            await self.header.read(buffer)
            self.size = self.header.value

        self.value = (await buffer.read(self.size)).decode()

    def write(self, buffer: StreamWriter):
        if self.header:
            self.header.value = len(self.value)
            self.header.write(buffer)
        buffer.write(self.value.encode())

    def from_bytes(self, data: bytes):
        self.value = data.decode()

    def to_bytes(self) -> bytes:
        buffer = io.BytesIO()
        self.size = len(self.value)

        if self.header:
            self.header.value = len(self.value)
            self.header.write(buffer)
        buffer.write(self.value.encode())

        return buffer.getvalue()


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
        self.header = header
        self.size = size

    async def read(self, buffer: StreamReader):
        if not (self.header or self.size):
            raise ValueError("Length header or size have to be provided!")

        if self.header:
            await self.header.read(buffer)
            self.size = self.header.value

        self.value = []
        for i in range(self.size):
            await self._field.read(buffer)
            self.value.append(copy.deepcopy(self._field.value))

    def write(self, buffer: StreamWriter):
        if self.header:
            self.header.value = len(self.value)
            self.header.write(buffer)

        for i in self.value:
            self._field(i).write(buffer)

    def to_bytes(self) -> bytes:
        result = bytes()

        if self.header:
            result += self.header(len(self.value)).to_bytes()

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

    async def read(self, buffer: StreamReader):
        await self.value.read(buffer)

    def write(self, buffer: StreamWriter):
        self.value.write(buffer)

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
