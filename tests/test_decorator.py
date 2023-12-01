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

from cstructs import datastruct
from cstructs.exc import InvalidFormatString, InvalidByteOrder


def test_bare_decorator_call():
    @datastruct
    class Test:
        pass


def fn_decorator_call_with_byteorder(byteorder: str):
    @datastruct(byteorder=byteorder)
    class Test:
        pass


def test_decorator_call_with_byteorder():
    fn_decorator_call_with_byteorder("little")
    fn_decorator_call_with_byteorder("big")
    fn_decorator_call_with_byteorder("native")  # native is the default
    fn_decorator_call_with_byteorder("network")

    # test improper byteorder
    with pytest.raises(InvalidByteOrder):
        fn_decorator_call_with_byteorder("wrong")
