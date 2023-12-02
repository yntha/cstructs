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

from cstructs.exc import InvalidByteOrder, InvalidTypeDef
from cstructs.datastruct.metadata import StructMeta, MetadataItem
from cstructs.nativetypes import NativeType


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


def datastruct(cls=None, /, *, byteorder: str = "native"):
    if byteorder not in _byteorder_map:
        raise InvalidByteOrder(f"Invalid byteorder: {byteorder}")

    def decorator(struct_cls: type):
        struct_cls.byteorder = byteorder
        struct_cls._source_class = struct_cls
        struct_cls.meta = StructMeta()

        # add all annotations to the meta
        for name, type_ in struct_cls.__annotations__.items():
            if not isinstance(type_, NativeType):
                raise InvalidTypeDef(f"Invalid type definition for {name}: {type_}")

            item_name = type_.name
            item_size = type_.size
            item_typedef = type_

            struct_cls.meta.add_item(MetadataItem(item_name, item_typedef, item_size))

        struct_cls.size = struct_cls.meta.size
        struct_cls.__qualname__ = f"cstructs.datastruct.{struct_cls.__name__}"

        return struct_cls

    if cls is None:
        return decorator

    return decorator(cls)
