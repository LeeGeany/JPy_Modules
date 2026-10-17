from dataclasses import dataclass, make_dataclass
import struct
from typing import ClassVar, List, Tuple, Any,  Type
from typing import Dict

TYPE_FORMAT_MAP: Dict[str, str] = {
    'int': 'i',  # 4 bytes Signed Int (기본값)
    'bool': '?',  # 1 byte Boolean

    'int_1b_signed': 'b',  # 1 byte Signed Char
    'int_1b_unsigned': 'B',  # 1 byte Unsigned Char
    'int_2b_signed': 'h',  # 2 bytes Signed Short
    'int_2b_unsigned': 'H',  # 2 bytes Unsigned Short
    'int_4b_signed': 'i',  # 4 bytes Signed Int (int와 동일)
    'int_4b_unsigned': 'I',  # 4 bytes Unsigned Int
    'int_8b_signed': 'q',  # 8 bytes Signed Long Long
    'int_8b_unsigned': 'Q',  # 8 bytes Unsigned Long Long

    'float': 'f',  # 4 bytes Float (단정밀도)
    'double': 'd',  # 8 bytes Double (배정밀도, 파이썬 float와 매칭)

    'str': 's',
    'bytes': 's'
}

# ============================================================
# Packet Base
# ============================================================
@dataclass
class Packet:
    PACKET_FORMAT: ClassVar[List[Tuple[str, str | int]]] = []

# ============================================================
# Example Packet
# ============================================================
@dataclass
class CDataTCPHeader(Packet):
    source: int
    dest: int
    cmd: int
    type: int
    time: int
    size: int

    PACKET_FORMAT: ClassVar[
        List[Tuple[str, str]]
    ] = [
        ("source", "I"),
        ("dest",   "I"),
        ("cmd",    "I"),
        ("type",   "I"),
        ("time",   "I"),
        ("size",   "I"),
    ]

# ============================================================
# Example
# 4 byte integer × 1024
# ============================================================
@dataclass
class CDataPacket(Packet):
    source: int
    dest: int
    cmd: int
    type: int
    time: int
    size: int
    data: List[int]

    PACKET_FORMAT: ClassVar[
        List[Tuple[str, str]]
    ] = [
        ("source", "I"),
        ("dest",   "I"),
        ("cmd",    "I"),
        ("type",   "I"),
        ("time",   "I"),
        ("size",   "I"),
        ("data",   "1024I"),
    ]

@dataclass
class TextMessagePacket(Packet):
    """예시 2: 가변 길이 문자열을 포함한 메시지 (가변 길이 처리 필요)"""
    sender_id: int
    message: str  # 가변 길이 필드

    # 주의: 가변 길이 문자열은 '길이 정보(int)'와 '실제 데이터(bytes)' 두 부분으로 직렬화해야 합니다.
    PACKET_FORMAT: ClassVar[List[Tuple[str, int]]] = [
        ('sender_id', 0),
        # message 필드는 전송 시 길이를 헤더로 추가할 것입니다.
    ]

@dataclass
class FixedNamePacket(Packet):
    """예시 3: 고정 길이 문자열을 포함한 패킷"""
    session_id: int
    name: str

    # name을 10바이트 고정 길이 문자열로 처리
    PACKET_FORMAT: ClassVar[List[Tuple[str, int]]] = [
        ('session_id', 0),
        ('name', 10)  # '10s'
    ]


# ============================================================
# Dynamic Packet
# ============================================================
def create_dynamic_packet_class(class_name: str, fields_info: Dict[str, Any]) -> Type[Packet]:

    ds_fields = []
    packet_format = []

    for name, (f_type, f_format) in fields_info.items():
        ds_fields.append((name, f_type))
        packet_format.append((name, f_format))

    dynamic_class = make_dataclass(
        class_name,
        fields=ds_fields,
        bases=(Packet,),
        namespace={
            "PACKET_FORMAT": packet_format
        }
    )

    return dynamic_class


# ============================================================
# Pack
# ============================================================
def packet_Pack(packet: Packet) -> bytes:

    format_chars = []
    fields_to_pack = []

    for field_name, format_spec in packet.PACKET_FORMAT:

        field_value = getattr(packet, field_name)

        # ----------------------------------------
        # struct format
        # ----------------------------------------

        if isinstance(format_spec, str):

            format_chars.append(format_spec)

            # 배열
            if format_spec[0].isdigit():

                if not isinstance(field_value, (list, tuple)):
                    raise TypeError(
                        f"'{field_name}' must be list or tuple."
                    )

                # 예: 1024I
                count = int(
                    format_spec[:len(format_spec)
                    - len(format_spec.lstrip("0123456789"))]
                )

                if len(field_value) != count:
                    raise ValueError(
                        f"'{field_name}' requires {count} elements, "
                        f"but got {len(field_value)}."
                    )

                fields_to_pack.extend(field_value)

            else:
                fields_to_pack.append(field_value)

        # ----------------------------------------
        # Fixed string
        # ----------------------------------------

        elif isinstance(format_spec, int):

            if format_spec <= 0:
                raise ValueError(
                    f"Invalid fixed size: {format_spec}"
                )

            if not isinstance(field_value, str):
                raise TypeError(
                    f"'{field_name}' must be str."
                )

            data_bytes = field_value.encode("utf-8")

            format_chars.append(
                f"{format_spec}s"
            )

            fields_to_pack.append(
                data_bytes[:format_spec].ljust(
                    format_spec,
                    b"\x00"
                )
            )

        else:
            raise TypeError(
                f"Invalid format for '{field_name}'."
            )

    final_format = "<" + "".join(format_chars)

    try:

        data_bytes = struct.pack(
            final_format,
            *fields_to_pack
        )

    except struct.error as e:

        raise ValueError(
            f"Packet packing failed. "
            f"format={final_format}"
        ) from e

    return data_bytes


# ============================================================
# Unpack
# ============================================================
def packet_Unpack(packet_class: Type[Packet], data_bytes: bytes, _endian = ">") -> Packet:

    format_chars = []

    for field_name, format_spec in packet_class.PACKET_FORMAT:

        if isinstance(format_spec, str):

            format_chars.append(format_spec)

        elif isinstance(format_spec, int):

            if format_spec <= 0:
                raise ValueError(
                    f"Invalid fixed size: {format_spec}"
                )

            format_chars.append(
                f"{format_spec}s"
            )

        else:

            raise TypeError(
                f"Invalid format for '{field_name}'."
            )

    final_format = _endian + "".join(format_chars)

    packet_size = struct.calcsize(final_format)
    #print(f"packet_size {packet_size} : {len(data_bytes)}" )
    if len(data_bytes) != packet_size:

        raise ValueError(
            f"Packet size mismatch: "
            f"expected={packet_size}, "
            f"received={len(data_bytes)}"
        )

    unpacked_values = {}
    unpacked_tuple = struct.unpack(
        final_format,
        data_bytes
    )

    tuple_index = 0

    for field_name, format_spec in packet_class.PACKET_FORMAT:

        # ----------------------------------------
        # Array
        # ----------------------------------------

        if isinstance(format_spec, str) and format_spec[0].isdigit():

            count_str = format_spec[
                :len(format_spec)
                - len(format_spec.lstrip("0123456789"))
            ]

            count = int(count_str)

            unpacked_values[field_name] = list(
                unpacked_tuple[
                    tuple_index:
                    tuple_index + count
                ]
            )

            tuple_index += count

        # ----------------------------------------
        # Fixed string
        # ----------------------------------------

        elif isinstance(format_spec, int):

            value = unpacked_tuple[tuple_index]

            value = value.rstrip(
                b"\x00"
            ).decode(
                "utf-8"
            )

            unpacked_values[field_name] = value

            tuple_index += 1

        # ----------------------------------------
        # Normal field
        # ----------------------------------------

        else:

            unpacked_values[field_name] = (
                unpacked_tuple[tuple_index]
            )

            tuple_index += 1

    return packet_class(
        **unpacked_values
    )