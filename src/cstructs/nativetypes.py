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
from cstructs.exc import InvalidTypeDef


class NativeType:
    def __init__(self, name: str, size: int, python_type: type):
        self.name = name
        self.size = size
        self.python_type = python_type

        # repeat length is set in the __call__ method
        self.repeat_length = 1

    # this function allows for the user to specify the repeat length
    # of a native type by calling the NativeType instance. Ex:
    # NativeType.uint64(5) will invoke this function and set the repeat
    # length to 5.
    def __call__(self, repeat_length: int):
        if repeat_length <= 0:
            raise InvalidTypeDef(
                f"repeat length must be greater than 0, got {repeat_length}"
            )

        self.repeat_length = repeat_length

        if self.size == -1:
            self.size = repeat_length

        return self

    def __repr__(self):
        return f"NativeType({self.name}, {self.size})"

    def __str__(self):
        return self.name


class NativeTypes:
    # long typedef names
    uint64 = NativeType("uint64", 8, int)
    uint32 = NativeType("uint32", 4, int)
    uint16 = NativeType("uint16", 2, int)
    uint8 = NativeType("uint8", 1, int)
    int64 = NativeType("int64", 8, int)
    int32 = NativeType("int32", 4, int)
    int16 = NativeType("int16", 2, int)
    int8 = NativeType("int8", 1, int)
    double = NativeType("double", 8, float)
    float = NativeType("float", 4, float)
    char = NativeType("char", 1, str)
    bool = NativeType("bool", 1, bool)

    # bytestring is a special case, it's size is variable
    # and is specified by the user. The size is set in the
    # __call__ method of the NativeType class.
    bytestring = NativeType("bytestring", -1, bytes)

    # short typedef names
    u64 = uint64
    u32 = uint32
    u16 = uint16
    u8 = uint8
    i64 = int64
    i32 = int32
    i16 = int16
    i8 = int8
