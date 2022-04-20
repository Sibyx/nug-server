import copy
from asyncio import WriteTransport, ReadTransport

from nug_server.core.frames.fields import Field


# FROM: https://github.com/django/django/blob/main/django/forms/forms.py#L25
class DeclarativeFieldsMetaclass(type):
    """Collect Fields declared on the base classes."""

    def __new__(mcs, name, bases, attrs):
        attrs["declared_fields"] = {
            key: attrs.pop(key)
            for key, value in list(attrs.items())
            if isinstance(value, Field)
        }

        new_class = super().__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = {}
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, "declared_fields"):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class


class BaseFrame:
    def __init__(self, **kwargs):
        self.fields = copy.deepcopy(getattr(self, 'base_fields'))

        for key, value in kwargs.items():
            if key in self.fields and isinstance(self.fields[key], Field):
                self.fields[key].value = value

    def __getitem__(self, name):
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError(
                "Key '%s' not found in '%s'. Choices are: %s." % (
                    name,
                    self.__class__.__name__,
                    ', '.join(sorted(self.fields)),
                )
            )
        return field

    def __getattr__(self, name):
        return self.fields[name]

    def __iter__(self):
        for name in self.fields:
            yield self[name]

    def read(self, data: bytes):
        for key, field in self.fields.items():
            self.fields[key].from_bytes(data)

    def write(self, stream: WriteTransport):
        buffer = bytes()
        for key, field in self.fields.items():
            buffer += field.to_bytes()

        stream.write(buffer)


class Frame(BaseFrame, metaclass=DeclarativeFieldsMetaclass):
    pass
