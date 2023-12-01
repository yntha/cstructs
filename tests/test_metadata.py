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

from cstructs.datastruct.metadata import StructMeta, MetaDataItem
from cstructs import datastruct, DataStruct, NativeTypes


def test_struct_meta_empty_class():
    @datastruct
    class Test(metaclass=DataStruct):
        pass

    # meta should NOT be None and should be an instance of StructMeta
    assert isinstance(Test.meta, StructMeta)

    # ensure that the metadata is iterable
    for item in Test.meta:
        pass


def test_struct_meta_class_with_fields():
    @datastruct
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.string

    # ensure that meta behaves like a sequence
    assert isinstance(Test.meta[0], MetaDataItem)
    assert isinstance(Test.meta[1], MetaDataItem)

    # ensure that the metadata also implements dict like behavior
    assert isinstance(Test.meta["a"], MetaDataItem)
    assert isinstance(Test.meta["b"], MetaDataItem)

    # ensure that the metadata fields are also instance fields
    assert isinstance(Test.a, MetaDataItem)
    assert isinstance(Test.b, MetaDataItem)

    # ensure that each metadata item has a name, type, and size
    # field
    assert Test.a.name == "a"
    assert Test.a.type in NativeTypes.uint32
    assert Test.a.size == NativeTypes.uint32.size

    assert Test.b.name == "b"
    assert Test.b.type in NativeTypes.string
    assert Test.b.size == NativeTypes.string.size


def test_native_types():
    @datastruct
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.u32
        c: NativeTypes.uint16
        d: NativeTypes.u16
        e: NativeTypes.uint8
        f: NativeTypes.u8
        g: NativeTypes.int32
        h: NativeTypes.i32
        i: NativeTypes.int16
        j: NativeTypes.i16
        k: NativeTypes.int8
        l: NativeTypes.i8
        m: NativeTypes.float
        n: NativeTypes.double
        o: NativeTypes.bool
        p: NativeTypes.char
        q: NativeTypes.bytestring
        r: NativeTypes.uint64
        s: NativeTypes.u64
        t: NativeTypes.int64
        u: NativeTypes.i64

    # ensure that the metadata fields are also instance fields
    assert isinstance(Test.a, MetaDataItem)
    assert isinstance(Test.b, MetaDataItem)

    # ensure that each metadata item has a name, type, and size
    # field
    assert Test.a.name == "a"

    # ensure that the type field can be either them long typedef or the short typedef
    assert Test.a.type in (NativeTypes.uint32, NativeTypes.u32)
    assert Test.a.size == NativeTypes.uint32.size

    # ensure that the native types have a field that represents this typedef as a
    # python primitive
    assert NativeTypes.uint32.python_type == int
