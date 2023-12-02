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
import enum
import typing

from dataclasses import dataclass
from cstructs.nativetypes import NativeType
from cstructs.util import is_datastruct


@dataclass
class MetadataItem:
    name: str
    type: NativeType
    size: int

    # these fields are set later on
    offset: int = None
    value: typing.Any = None

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        value_str = f"{self.value}"

        if is_datastruct(self.value.__class__):
            value_str = "\n" + str(self.value)
            value_str += "\n" + "-" * max(
                map(lambda s: len(s) - 1, value_str.split("\n"))
            )

        if isinstance(self.value, enum.Enum):
            value_str = repr(self.value)

        return f"{self.type.name} ({self.size} bytes) = {value_str}"


class StructMeta:
    def add_item(self, item: MetadataItem):
        setattr(self, item.name, item)

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield getattr(self, attr)

    def __getitem__(self, item):
        return (
            getattr(self, item)
            if isinstance(item, str)
            else [*self.__dict__.values()][item]
        )

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "\n".join([f"{key}: {value}" for key, value in self.__dict__.items()])
