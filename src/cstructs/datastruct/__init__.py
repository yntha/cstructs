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
import dataclasses
import typing
import io

from cstructs.exc import InvalidByteOrder, InvalidTypeDef
from cstructs.datastruct.metadata import StructMeta, MetadataItem
from cstructs.nativetypes import NativeType


_byteorder_map = {"native": "@", "little": "<", "network": "!", "big": ">"}


class DataStruct(type):
    on_read: typing.ClassVar[typing.Callable] = None
    on_write: typing.ClassVar[typing.Callable] = None
    meta: typing.ClassVar[StructMeta] = None
    byteorder: typing.ClassVar[str] = None
    size: typing.ClassVar[int] = None
    _source_class: typing.ClassVar[type] = None

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, cls.__name__, cls.__bases__, dict(vars(cls)))

    def __call__(cls, stream: typing.BinaryIO, *args):
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected file-like object, got {type(stream)}")


def datastruct(cls=None, /, *, byteorder: str = "native"):
    if byteorder not in _byteorder_map:
        raise InvalidByteOrder(f"Invalid byteorder: {byteorder}")

    def decorator(struct_cls: type):
        # noinspection PyTypeChecker
        dataclass_cls = dataclasses.dataclass(struct_cls)

        dataclass_cls.byteorder = byteorder
        dataclass_cls._source_class = struct_cls
        dataclass_cls.meta = StructMeta()

        for field in dataclasses.fields(dataclass_cls):
            if not isinstance(field.type, NativeType):
                raise InvalidTypeDef(
                    f"Invalid type definition for {field.name}: {field.type}"
                )

            item_name = field.name
            item_size = field.type.size
            item_typedef = field.type

            dataclass_cls.meta.add_item(
                MetadataItem(item_name, item_typedef, item_size)
            )

        dataclass_cls.size = sum([item.size for item in dataclass_cls.meta])
        dataclass_cls.__qualname__ = f"cstructs.datastruct.{dataclass_cls.__name__}"

        return dataclass_cls

    if cls is None:
        return decorator

    return decorator(cls)
