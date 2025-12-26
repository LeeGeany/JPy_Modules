import sys
import os
from geographiclib.geodesic import Geodesic

def is_float(s):
    """
    문자열 s가 정수든 소수든 실수 형태면 True, 아니면 False
    """
    try:
        float(s)   # 정수 문자열도 float 변환 가능
        return True
    except ValueError:
        return False

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
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)