import array
import bz2

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AutoGrowingList(list):
    """ A class to hold auto growing lists with a configurable index offset """
    EMPTY = -1
    INDEX_OFFSET = 1

    def __setitem__(self, index, value):
        index = index - self.INDEX_OFFSET
        if index >= len(self):
            self.extend([self.EMPTY] * (index + self.INDEX_OFFSET - len(self)))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if type(index) == int and index >= 0:
            index = index - self.INDEX_OFFSET
        elif type(index) == slice:
            new_start, new_stop = index.start, index.stop
            if new_start >= 0:
                new_start = new_start - self.INDEX_OFFSET
            if new_stop >= 0:
                new_stop = new_stop - self.INDEX_OFFSET

            index = slice(new_start, new_stop, index.step)
        try:
            return list.__getitem__(self, index)
        except IndexError:
            return self.EMPTY


class CompressedListField(models.BinaryField):
    """ A field to hold compressed lists """

    description = _("Compressed list")
    empty_values = [None, b'']
    type_code = 'l'

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        kwargs['null'] = True
        if 'type_code' in kwargs:
            self.type_code = str(kwargs['type_code'])
            del kwargs['type_code']
        if 'default' in kwargs:
            kwargs['default'] = AutoGrowingList(kwargs['default'])
        super(CompressedListField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CompressedListField, self).deconstruct()
        if 'editable' in kwargs:
            del kwargs['editable']
        if 'null' in kwargs:
            del kwargs['null']
        return name, path, args, kwargs

    def get_default(self):
        return AutoGrowingList([])

    def get_db_prep_value(self, value, connection, prepared=False):
        if value:
            value = bz2.compress(array.array(self.type_code, list(value)))
        else:
            value = b''
        return super(CompressedListField, self).get_db_prep_value(
            value, connection, prepared)

    def from_db_value(self, value, expression, connection, context):
        if value:
            compressed = super(CompressedListField, self).to_python(value)
            data = bz2.decompress(compressed)
            return AutoGrowingList(array.array(self.type_code, data))
        else:
            return self.get_default()

    def value_to_string(self, obj):
        """Binary data is serialized as base64"""
        return models.Field.value_to_string(self, obj)

    def to_python(self, value):
        if isinstance(value, AutoGrowingList):
            return value

        if value:
            compressed = super(CompressedListField, self).to_python(value)
            data = bz2.decompress(compressed)
            return AutoGrowingList(array.array(self.type_code, data))
        else:
            return self.get_default()
