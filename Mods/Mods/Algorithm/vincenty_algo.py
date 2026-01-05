import math

def vincenty_inverse(lat1, lon1, lat2, lon2):
    """
    Vincenty inverse formula (WGS-84)
    - 입력: 위도, 경도 (degrees)
    - 출력: 거리(m), 출발 방위각(deg), 도착 방위각(deg)
    """

    # WGS-84 타원체 상수
    a = 6378137.0  # 장반경 (m)
    f = 1 / 298.257223563  # 편평률
    b = (1 - f) * a

    # radian 변환
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    L = math.radians(lon2 - lon1)

    # U 값 (보조 구면상의 위도)
    U1 = math.atan((1 - f) * math.tan(φ1))
    U2 = math.atan((1 - f) * math.tan(φ2))

    sinU1, cosU1 = math.sin(U1), math.cos(U1)
    sinU2, cosU2 = math.sin(U2), math.cos(U2)

    # 초기값 설정
    λ = L
    λ_prev = 0.0
    iter_limit = 200  # 반복 제한
    for i in range(iter_limit):
        sinλ = math.sin(λ)
        cosλ = math.cos(λ)
        sinσ = math.sqrt(
            (cosU2 * sinλ) ** 2 +
            (cosU1 * sinU2 - sinU1 * cosU2 * cosλ) ** 2
        )
        if sinσ == 0:
            return 0.0, 0.0, 0.0  # 같은 지점

        cosσ = sinU1 * sinU2 + cosU1 * cosU2 * cosλ
        σ = math.atan2(sinσ, cosσ)

        sinα = cosU1 * cosU2 * sinλ / sinσ
        cos2α = 1 - sinα ** 2

        if cos2α == 0:
            cos2σm = 0  # 적도에 가까운 경우
        else:
            cos2σm = cosσ - 2 * sinU1 * sinU2 / cos2α

        C = f / 16 * cos2α * (4 + f * (4 - 3 * cos2α))
        λ_prev = λ
        λ = L + (1 - C) * f * sinα * (
            σ + C * sinσ * (cos2σm + C * cosσ *
                            (-1 + 2 * cos2σm ** 2))
        )

        if abs(λ - λ_prev) < 1e-12:
            break
    else:
        raise ValueError("Vincenty formula failed to converge")

    u2 = cos2α * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 *
                                       (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 *
                                 (74 - 47 * u2)))
    Δσ = B * sinσ * (
        cos2σm + B / 4 * (
            cosσ * (-1 + 2 * cos2σm ** 2) -
            B / 6 * cos2σm * (-3 + 4 * sinσ ** 2) *
            (-3 + 4 * cos2σm ** 2)
        )
    )

    s = b * A * (σ - Δσ)  # 거리 (m)

    α1 = math.atan2(cosU2 * math.sin(λ),
                    cosU1 * sinU2 - sinU1 * cosU2 * math.cos(λ))
    α2 = math.atan2(cosU1 * math.sin(λ),
                    -sinU1 * cosU2 + cosU1 * sinU2 * math.cos(λ))

    α1 = (math.degrees(α1) + 360) % 360
    α2 = (math.degrees(α2) + 360) % 360

    return s, α1, α2
