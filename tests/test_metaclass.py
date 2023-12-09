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

from cstructs import datastruct, DataStruct
from cstructs.datastruct.metadata import StructMeta


def test_metaclass():
    @datastruct
    class Test(metaclass=DataStruct):
        pass

    # check that the metaclass transforms the class qualname
    # this serves as a marker for classes that have been transformed
    # by the metaclass.
    assert Test.__qualname__ == "cstructs.datastruct.Test"

    # check that the metaclass adds the following fields:
    # - on_read: a callback function that is called after the struct is read
    # - on_write: a callback function that is called after the struct is written
    # - meta: a collection of member metadata
    # - byteorder: the byteorder of the struct
    # - size: the size of the struct
    assert hasattr(Test, "on_read")
    assert hasattr(Test, "on_write")
    assert hasattr(Test, "meta")
    assert hasattr(Test, "byteorder")
    assert hasattr(Test, "size")

    # on_read and on_write should both be initialized to None if the user does not
    # provide a callback function.
    assert Test.on_read is None
    assert Test.on_write is None

    # byteorder should NOT be None.
    assert Test.byteorder is not None

    # size should always be 0 for now.
    assert Test.size == 0

    # ensure that the only argument of the read function is the stream we
    # want to read from.
    with pytest.raises(TypeError):
        Test.read()
    with pytest.raises(TypeError):
        Test.read(1, 2, 3)
    with pytest.raises(TypeError):
        Test.read(None)

    Test.read(io.BytesIO(b""))
