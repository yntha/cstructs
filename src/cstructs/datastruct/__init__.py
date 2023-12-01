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

from cstructs.exc import InvalidByteOrder, InvalidFormatString


_byteorder_map = {
    "native": "@",
    "little": "<",
    "network": "!",
    "big": ">"
}


def datastruct(format_str: str = "", byteorder: str = "native"):
    if byteorder not in _byteorder_map:
        raise InvalidByteOrder(f"Invalid byteorder: {byteorder}")

    try:
        struct.calcsize(format_str)
    except struct.error:
        raise InvalidFormatString(f"Invalid format string: {format_str}")

    def decorator(cls):
        return cls

    return decorator
