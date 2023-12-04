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
import pytest
import io

from cstructs import datastruct, NativeTypes, DataStruct


def test_read_basic():
    @datastruct
    class Test(DataStruct):
        a: NativeTypes.uint8
        b: NativeTypes.uint8

    stream = io.BytesIO(bytes.fromhex("01 02"))
    test = Test(stream)

    assert test.a == 1
    assert test.b == 2


def test_read_complex():
    @datastruct(byteorder="big")
    class Test(DataStruct):
        a: NativeTypes.uint16
        b: NativeTypes.uint32
        c: NativeTypes.i32
        d: NativeTypes.uint64
        e: NativeTypes.bytestring(4)
        f: NativeTypes.char(12)

    stream = io.BytesIO()

    stream.write(bytes.fromhex("0001"))
    stream.write(bytes.fromhex("00000002"))
    stream.write(bytes.fromhex("fffffffd"))
    stream.write(bytes.fromhex("0000000000000004"))
    stream.write(bytes.fromhex("01020304"))
    stream.write(b"Hello World!")

    stream.seek(0)

    test = Test(stream)

    assert test.a == 1
    assert test.b == 2
    assert test.c == -3
    assert test.d == 4
    assert test.e == b"\x01\x02\x03\x04"
    assert test.f == "Hello World!"
