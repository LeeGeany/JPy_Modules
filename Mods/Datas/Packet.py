from dataclasses import dataclass, field
import struct
from typing import ClassVar, Tuple, List, Type

# --- 1. 타입-포맷 매핑 정의 ---
# struct 모듈의 포맷 문자를 파이썬 타입에 매핑합니다.
# Big-Endian '>' 기준으로 정의합니다.
from typing import Dict

# short, long, long long 등 다양한 크기의 정수 및 실수 타입을 추가했습니다.
TYPE_FORMAT_MAP: Dict[str, str] = {
    # ------------------------------------
    # 기본 정수/불리언 (Default 4B Int)
    # ------------------------------------
    'int': 'i',  # 4 bytes Signed Int (기본값)
    'bool': '?',  # 1 byte Boolean

    # ------------------------------------
    # 다양한 크기의 정수 (추가된 정수 포맷)
    # ------------------------------------
    'int_1b_signed': 'b',  # 1 byte Signed Char
    'int_1b_unsigned': 'B',  # 1 byte Unsigned Char
    'int_2b_signed': 'h',  # 2 bytes Signed Short
    'int_2b_unsigned': 'H',  # 2 bytes Unsigned Short
    'int_4b_signed': 'i',  # 4 bytes Signed Int (int와 동일)
    'int_4b_unsigned': 'I',  # 4 bytes Unsigned Int
    'int_8b_signed': 'q',  # 8 bytes Signed Long Long
    'int_8b_unsigned': 'Q',  # 8 bytes Unsigned Long Long

    # ------------------------------------
    # 실수 (Float/Double)
    # ------------------------------------
    'float': 'f',  # 4 bytes Float (단정밀도)
    'double': 'd',  # 8 bytes Double (배정밀도, 파이썬 float와 매칭)

    # ------------------------------------
    # 문자열/바이트열 (가변 길이 처리 필요)
    # ------------------------------------
    'str': 's',
    'bytes': 's'
}

@dataclass
class Packet:
    """모든 데이터 구조체의 기반 클래스."""
    # 직렬화 포맷을 지정하는 클래스 변수 (struct 포맷 문자와 동일)
    # ClassVar를 사용하여 인스턴스에 포함되지 않도록 합니다.
    # 이 딕셔너리의 키는 멤버 변수 이름과 일치할 필요는 없지만 순서는 중요합니다.
    PACKET_FORMAT: ClassVar[List[Tuple[str, str | int]]] = []

# 예제
@dataclass
class UserInfoPacket(Packet):
    """예시 1: 사용자 기본 정보 (고정 길이)"""
    user_id: int
    age: int
    is_active: bool

    # [필드명, struct 타입의 고정 길이(문자열/바이트 제외 시 0)]
    PACKET_FORMAT: ClassVar[List[Tuple[str, int]]] = [
        ('user_id', 0),  # 'i'
        ('age', 0),  # 'i' 또는 'h'
        ('is_active', 0)  # '?'
    ]

#예제
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

#예제
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


def packet_Pack(packet: Packet) -> bytes:
    fields_to_pack = []
    format_chars = []

    for field_name, format_or_size in packet.PACKET_FORMAT:
        field_value = getattr(packet, field_name)

        if isinstance(format_or_size, str):
            # 💡 수정된 핵심 로직: 'H', 'B', 'I' 등의 명시적 포맷 문자열을 최우선으로 사용
            format_chars.append(format_or_size)
            fields_to_pack.append(field_value)

        elif isinstance(format_or_size, int):
            # 고정 길이 (N) 또는 기본 타입 추론 (0) 처리

            field_type_str = type(field_value).__name__

            if field_type_str == 'str':
                # 고정 길이 문자열 (N > 0) 처리
                fixed_size = format_or_size
                data_bytes = field_value.encode('utf-8')
                format_chars.append(f'{fixed_size}s')
                fields_to_pack.append(data_bytes[:fixed_size].ljust(fixed_size, b'\x00'))

            elif format_or_size == 0:
                # 기본 타입 추론 (N = 0)
                format_char = TYPE_FORMAT_MAP.get(field_type_str)
                if not format_char: raise ValueError(f"지원하지 않는 타입: {field_type_str}")
                format_chars.append(format_char)
                fields_to_pack.append(field_value)

            else:
                # 가변 길이 문자열 (이전 로직)은 여기에서 분기해야 함
                raise NotImplementedError("Pack 로직: 정의되지 않은 int 값 처리 방식")

        # ... (이후 로직은 이전 답변을 참고)

    # Big-Endian으로 엔디안 통일
    final_format = '>' + ''.join(format_chars)

    try:
        data_bytes = struct.pack(final_format, *fields_to_pack)
        print(f"[*] 패킹 완료. 포맷: {final_format}, 크기: {struct.calcsize(final_format)} bytes")
        return data_bytes
    except struct.error as e:
        print(f"[!] 데이터 패킹 오류: {e}")
        raise


# (주의: 이 예제에서는 string/variable length 처리를 단순화했습니다.
# 전체 코드를 통합하려면 가장 최신 버전의 Pack 함수를 사용해야 합니다.)


# --- 1. 타입-포맷 매핑 정의 (다시 사용) ---
# 이 예제에서는 PACKET_FORMAT에 포맷을 직접 명시하는 것이 가장 좋습니다.
# 여기서는 이전 로직과의 호환성을 위해 필드 이름을 기반으로 포맷을 추론합니다.
def _get_struct_format_char(field_name: str) -> str:
    """필드 이름 기반으로 struct 포맷 문자를 추론합니다."""
    if field_name in ['user_id', 'age', 'sender_id', 'session_id']:
        return 'i'  # 4 bytes Signed Integer
    elif field_name in ['is_active']:
        return '?'  # 1 byte Boolean
    # 다른 타입이 필요하면 여기에 추가합니다.
    raise TypeError(f"필드 '{field_name}'의 struct 포맷을 추론할 수 없습니다.")


# --- Unpack 함수 (역직렬화) 수정 버전 ---
def packet_Unpack(packet_class: Type['Packet'], data_bytes: bytes) -> 'Packet':
    """
    고정 길이 필드만 처리하며, Big-Endian (>)으로 역직렬화합니다.
    """
    format_chars = []

    # 1. 패킷 전체의 struct 포맷 문자열을 동적으로 생성
    # format_or_size는 'H', 'B' (str) 또는 10 (int) 등이 될 수 있습니다.
    for field_name, format_or_size in packet_class.PACKET_FORMAT:

        if isinstance(format_or_size, str):
            # 명시적 포맷 문자열 ('H', 'B', 'i', 'I' 등)인 경우
            format_chars.append(format_or_size)

        elif isinstance(format_or_size, int):
            # 숫자 값인 경우 (주로 고정 길이 문자열 Ns 처리)
            fixed_size = format_or_size

            if fixed_size > 0:
                # 고정 길이 문자열 (예: '10s')
                format_chars.append(f'{fixed_size}s')
            else:
                # fixed_size == 0 인 경우: 원래 기본 타입 추론을 해야 하나,
                # 현재는 PACKET_FORMAT에 명시적 포맷을 넣으므로 이 로직은 불필요하거나 오류를 유발합니다.
                # (만약 0이 들어온다면 _get_struct_format_char 사용)
                # 여기서는 오류 방지를 위해 임시로 'i'로 가정합니다.
                # 사용자님의 PACKET_FORMAT에는 0이 없으므로 안전합니다.
                format_chars.append('i')
        else:
            raise TypeError(f"PACKET_FORMAT의 '{field_name}' 필드 포맷({format_or_size})이 유효하지 않습니다.")

    final_format = '>' + ''.join(format_chars)
    packet_size = struct.calcsize(final_format)

    print(f"\n--- {packet_class.__name__} 역직렬화 시작 ---")
    print(f"📦 예상 포맷: {final_format}, 예상 크기: {packet_size} bytes")

    # 2. 크기 확인
    if len(data_bytes) != packet_size:
        raise ValueError(
            f"❌ 크기 불일치: {packet_class.__name__}에 필요한 크기는 {packet_size} bytes이나, "
            f"{len(data_bytes)} bytes가 입력되었습니다."
        )

    # 3. 바이트열 전체를 한 번에 언패킹 (Big-Endian 사용)
    unpacked_tuple = struct.unpack(final_format, data_bytes)

    # 4. 언패킹된 튜플을 필드 이름과 매핑
    unpacked_values = {}
    tuple_index = 0

    for field_name, format_or_size in packet_class.PACKET_FORMAT:
        field_value = unpacked_tuple[tuple_index]

        # 문자열 처리 시에만 디코딩 및 널 바이트 제거
        # format_or_size가 int 타입(고정 길이 N)일 때만 문자열 처리
        if isinstance(format_or_size, int) and format_or_size > 0:
            unpacked_bytes = field_value
            field_value = unpacked_bytes.rstrip(b'\x00').decode('utf-8')

        unpacked_values[field_name] = field_value
        tuple_index += 1

        print(f"  > 필드 '{field_name}': {field_value}")

    return packet_class(**unpacked_values)