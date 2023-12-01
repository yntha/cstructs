# --------------------------------------------------------------------------------------
#  Copyright(C) 2023 yntha                                                             -
#                                                                                      -
#  This program is free software: you can redistribute it and/or modify it under       -
#  the terms of the GNU General Public License as published by the Free Software       -
#  Foundation, either version 3 of the License, or (at your option) any later          -
#  version.                                                                            -
#                                                                                      -
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY     -
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A     -
#  PARTICULAR PURPOSE. See the GNU General Public License for more details.            -
#                                                                                      -
#  You should have received a copy of the GNU General Public License along with        -
#  this program. If not, see <http://www.gnu.org/licenses/>.                           -
# --------------------------------------------------------------------------------------
import struct
import typing

from cstructs.exc import InvalidByteOrder
from cstructs.datastruct.metadata import StructMeta


_byteorder_map = {"native": "@", "little": "<", "network": "!", "big": ">"}


class DataStruct(type):
    on_read: typing.Callable = None
    on_write: typing.Callable = None
    meta: StructMeta = None
    byteorder: str = None
    size: int = None
    _source_class = None

    def __call__(cls, stream: typing.BinaryIO, *args):
        if not hasattr(stream, "read"):
            raise TypeError("Expected stream to have a read method")

    def __qualname__(cls):
        return f"cstructs.datastruct.{cls._source_class.__name__}"


def datastruct(cls=None, /, *, byteorder: str = "native"):
    if byteorder not in _byteorder_map:
        raise InvalidByteOrder(f"Invalid byteorder: {byteorder}")

    def decorator(struct_cls: type):
        struct_cls.byteorder = byteorder
        struct_cls._source_class = struct_cls

        return struct_cls

    if cls is None:
        return decorator

    return decorator(cls)
