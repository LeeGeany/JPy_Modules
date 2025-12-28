import sys
import os
from geographiclib.geodesic import Geodesic

"""
    @brief  val 값이 max, min 사이에 있는지 확인하는 함수  
    @params max 범위의 최대 값 max 값은 포함하지 않음
    @params min 범위의 최소 값 min 값은 포함하지 않음
    @params val 비교할 대상
    @return 범위에 있으면 True, 없으면 False
"""
def isRange(max, min, val) -> bool:
    if val > max or val < min:
        return False
    else:
        return True

"""
    @brief  val 값이 소수인지 확인하는 함수
    @return 소수이면 True, 아니면 False
"""
def isFloat(s) -> bool:
    try:
        float(s)   # 정수 문자열도 float 변환 가능
        return True
    except ValueError:
        return False

"""
    @brief  ASCII를 바이트로 바꾸는 함수
    @params text ASCII 문자열
"""
def ASCII2Bytes(text: str):
    try:
        return text.encode("ascii")
    except UnicodeEncodeError:
        print("[!] 오류: 아스키 범위를 벗어나는 문자가 포함되어 있습니다.")
        return None

"""
    @brief  바이트를 ASCII로 바꾸는 함수
    @params byte_data 바이트 데이터
"""
def Bytes2ASCII(byte_data: bytes):
    try:
        return byte_data.decode('ascii')
    except UnicodeDecodeError:
        print("[!] 오류: 아스키로 해석할 수 없는 바이트 데이터가 포함되어 있습니다.")
        return None
    except AttributeError:
        print("오류: 입력값이 바이트(bytes) 타입이 아닙니다.")
        return None

"""
    @brief  바이트를 리스트로 바꾸는 함수
    @params byte_data 바이트 데이터
"""
def bytes_to_codes(byte_data: bytes):
    return list(byte_data)


def ASCII_to_codes(text : str) -> bytes:
    return bytes.fromhex(text)



def dms2degree(degrees, minutes, seconds, direction=None):
    decimal = abs(degrees) + minutes / 60 + seconds / 3600

    if direction in ('S', 'W'):
        decimal *= -1
    elif direction not in (None, 'N', 'E'):
        raise ValueError("direction은 N, S, E, W 중 하나여야 합니다.")

    if degrees < 0:
        decimal *= -1  # 음수 도 입력 처리

    return decimal

def degree2dms(self, degree):
    """
    십진각(decimal degrees)을 DMS(Degree-Minute-Second)로 변환
    반환: (도, 분, 초)
    """
    is_negative = degree < 0
    decimal = abs(degree)

    degrees = int(decimal)
    minutes_full = (decimal - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60

    if is_negative:
        degrees *= -1  # 음수면 부호 붙임

    return degrees, minutes, seconds

def geodesic_info(lat1, lon1, lat2, lon2):
    """
    두 좌표(lat1, lon1), (lat2, lon2)의
    거리(m)와 출발점/도착점 방위각(deg) 계산
    """
    geod = Geodesic.WGS84
    result = geod.InverseLine(lat1, lon1, lat2, lon2)
    pos = result.Position(result.s13)

    distance = result.s13      # 거리 (미터)
    initial_bearing = (pos['azi1'] + 360) % 360  # 출발점 방위각
    final_bearing   = (pos['azi2'] + 180) % 360

    return distance, initial_bearing, final_bearing

def resource_path(relative_path: str) -> str:
    """리소스 파일(.ui 등)의 절대 경로를 반환"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller로 빌드된 경우
        base_path = sys._MEIPASS
    else:
        # 개발(일반 python 실행) 환경
        base_path = os.path.abspath("../Algorithm")

    return os.path.join(base_path, relative_path)