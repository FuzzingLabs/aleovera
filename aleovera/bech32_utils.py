# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for bech32/bech32m decoding/encoding.

References:
    https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
    https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
    https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py
"""

# Imports
from enum import Enum, auto, unique
from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict

class Bech32BaseConst:
    """Class container for Bech32 constants."""

    # Character set
    CHARSET: str = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


class Bech32BaseUtils:
    """Class container for Bech32 utility functions."""

    @staticmethod
    def ConvertToBase32(data: Union[List[int], bytes]) -> List[int]:
        """
        Convert data to base32.

        Args:
            data (list[int] or bytes): Data to be converted

        Returns:
            list[int]: Converted data

        Raises:
            ValueError: If the string is not valid
        """

        # Convert to base32
        conv_data = Bech32BaseUtils.ConvertBits(data, 8, 5)
        if conv_data is None:
            raise ValueError("Invalid data, cannot perform conversion to base32")

        return conv_data

    @staticmethod
    def ConvertFromBase32(data: Union[List[int], bytes]) -> List[int]:
        """
        Convert data from base32.

        Args:
            data (list[int] or bytes): Data to be converted

        Returns:
            list[int]: Converted data

        Raises:
            ValueError: If the string is not valid
        """

        # Convert from base32
        conv_data = Bech32BaseUtils.ConvertBits(data, 5, 8, False)
        if conv_data is None:
            raise ValueError("Invalid data, cannot perform conversion from base32")

        return conv_data

    @staticmethod
    def ConvertBits(data: Union[bytes, List[int]],
                    from_bits: int,
                    to_bits: int,
                    pad: bool = True) -> Optional[List[int]]:
        """
        Perform bit conversion.
        The function takes the input data (list of integers or byte sequence) and convert every value from
        the specified number of bits to the specified one.
        It returns a list of integer where every number is less than 2^to_bits.

        Args:
            data (list[int] or bytes): Data to be converted
            from_bits (int)          : Number of bits to start from
            to_bits (int)            : Number of bits to end with
            pad (bool, optional)     : True if data must be padded with zeros, false otherwise

        Returns:
            list[int]: List of converted values, None in case of errors
        """
        max_out_val = (1 << to_bits) - 1
        max_acc = (1 << (from_bits + to_bits - 1)) - 1

        acc = 0
        bits = 0
        ret = []

        for value in data:
            # Value shall not be less than zero or greater than 2^from_bits
            if value < 0 or (value >> from_bits):
                return None
            # Continue accumulating until greater than to_bits
            acc = ((acc << from_bits) | value) & max_acc
            bits += from_bits
            while bits >= to_bits:
                bits -= to_bits
                ret.append((acc >> bits) & max_out_val)
        if pad:
            if bits:
                # Pad the value with zeros to reach to_bits
                ret.append((acc << (to_bits - bits)) & max_out_val)
        elif bits >= from_bits or ((acc << (to_bits - bits)) & max_out_val):
            return None

        return ret


class Bech32EncoderBase(ABC):
    """
    Bech32 encoder base class.
    It provides methods for encoding to Bech32 format.
    """

    @classmethod
    def _EncodeBech32(cls,
                      hrp: str,
                      data: List[int],
                      sep: str) -> str:
        """
        Encode a Bech32 string from the specified HRP and data.

        Args:
            hrp (str)       : HRP
            data (list[int]): Data part
            sep (str)       : Bech32 separator

        Returns:
            str: Encoded data
        """

        # Add checksum to data
        data += cls._ComputeChecksum(hrp, data)
        # Encode to alphabet
        return hrp + sep + "".join([Bech32BaseConst.CHARSET[d] for d in data])

    @staticmethod
    @abstractmethod
    def _ComputeChecksum(hrp: str,
                         data: List[int]) -> List[int]:
        """
        Compute the checksum from the specified HRP and data.

        Args:
            hrp (str)       : HRP
            data (list[int]): Data part

        Returns:
            list[int]: Computed checksum
        """


@unique
class Bech32Encodings(Enum):
    """Enumerative for Bech32 encoding types."""

    BECH32 = auto()
    BECH32M = auto()


class Bech32Const:
    """Class container for Bech32 constants."""

    # Separator
    SEPARATOR: str = "1"
    # Checksum length
    CHECKSUM_STR_LEN: int = 6
    # Encoding checksum constants
    ENCODING_CHECKSUM_CONST: Dict[Bech32Encodings, int] = {
        Bech32Encodings.BECH32: 1,
        Bech32Encodings.BECH32M: 0x2bc830a3,
    }


class Bech32Utils:
    """Class container for Bech32 utility functions."""

    @staticmethod
    def PolyMod(values: List[int]) -> int:
        """
        Computes the polynomial modulus.

        Args:
            values (list[int]): List of polynomial coefficients

        Returns:
            int: Computed modulus
        """

        # Generator polynomial
        generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]

        # Compute modulus
        chk = 1
        for value in values:
            top = chk >> 25
            chk = (chk & 0x1ffffff) << 5 ^ value
            for i in range(5):
                chk ^= generator[i] if ((top >> i) & 1) else 0
        return chk

    @staticmethod
    def HrpExpand(hrp: str) -> List[int]:
        """
        Expand the HRP into values for checksum computation.

        Args:
            hrp (str): HRP

        Returns:
            list[int]: Expanded HRP values
        """
        # [upper 3 bits of each character] + [0] + [lower 5 bits of each character]
        return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 0x1f for x in hrp]

    @staticmethod
    def ComputeChecksum(hrp: str,
                        data: List[int],
                        encoding: Bech32Encodings = Bech32Encodings.BECH32M) -> List[int]:
        """
        Compute the checksum from the specified HRP and data.

        Args:
            hrp (str)                           : HRP
            data (list[int])                    : Data part
            encoding (Bech32Encodings, optional): Encoding type (BECH32 by default)

        Returns:
            list[int]: Computed checksum
        """
        values = Bech32Utils.HrpExpand(hrp) + data
        polymod = Bech32Utils.PolyMod(values + [0, 0, 0, 0, 0, 0]) ^ Bech32Const.ENCODING_CHECKSUM_CONST[encoding]
        return [(polymod >> 5 * (5 - i)) & 0x1f for i in range(Bech32Const.CHECKSUM_STR_LEN)]

    @staticmethod
    def VerifyChecksum(hrp: str,
                       data: List[int],
                       encoding: Bech32Encodings = Bech32Encodings.BECH32M) -> bool:
        """
        Verify the checksum from the specified HRP and converted data characters.

        Args:
            hrp  (str)                          : HRP
            data (list[int])                    : Data part
            encoding (Bech32Encodings, optional): Encoding type (BECH32 by default)

        Returns:
            bool: True if valid, false otherwise
        """
        polymod = Bech32Utils.PolyMod(Bech32Utils.HrpExpand(hrp) + data)
        return polymod == Bech32Const.ENCODING_CHECKSUM_CONST[encoding]


class Bech32Encoder(Bech32EncoderBase):
    """
    Bech32 encoder class.
    It provides methods for encoding to Bech32 format.
    """

    @classmethod
    def Encode(cls,
               hrp: str,
               data: bytes) -> str:
        """
        Encode to Bech32.

        Args:
            hrp (str)   : HRP
            data (bytes): Data

        Returns:
            str: Encoded address

        Raises:
            ValueError: If the data is not valid
        """
        return cls._EncodeBech32(hrp,
                                 Bech32BaseUtils.ConvertToBase32(data),
                                 Bech32Const.SEPARATOR)

    @staticmethod
    def _ComputeChecksum(hrp: str,
                         data: List[int]) -> List[int]:
        """
        Compute the checksum from the specified HRP and data.

        Args:
            hrp (str)       : HRP
            data (list[int]): Data part

        Returns:
            list[int]: Computed checksum
        """

        # Same as Segwit
        return Bech32Utils.ComputeChecksum(hrp, data)