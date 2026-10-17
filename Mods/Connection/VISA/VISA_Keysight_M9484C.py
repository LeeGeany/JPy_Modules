import sys
import time

import pyvisa

class CVISA_keysight_M9484C:
    def __init__(self, _vxg):
        self.m_vxg = _vxg

    # Reference 관련 함수들
    def setReference(self, _where):
        if _where == "INT":
            self.m_vxg.write(":SOUR:ROSC:SOUR INT")
        elif _where == "EXT":
            self.m_vxg.write(":SOUR:ROSC:SOUR EXT")
        else:
            print("Nothing to do")
        time.sleep(0.1)

    ### 10MHz Reference clk 출력 시작
    def set10MhzRefOn(self):
        self.m_vxg.write(":ROUT:REF:ROUT F10")

    ### 10MHz Reference clk 출력 중지
    def set10MhzRefOff(self):
        print("Nothing to do")

    def isReference(self):
        print(self.m_vxg.query(":SOUR:ROSC:SOUR?"))

    # 10MHz 레퍼런스 신호를 받고 있는지 확인
    def is10MHzReference(self):
        ret = int(self.m_vxg.query("STAT:QUES:FREQ:COND?"))
        if(ret == 0):
            print("외부 참조 클럭에 성공적으로 Lock 되었습니다.")
        elif (ret == 2):
            print("외부 참조 잠금 손실 상태입니다.")
        else :
            print(f"ERROR CODE : {ret} 기타 주파수 관련 문제가 감지되었습니다.")

### RF 신호 출력 관련 함수
    # 1) RF 신호 출력 시작
    def setRFOn(self, _port, _freqMHz, _powdBm):
        self.m_vxg.write(f":SOUR:RF{_port}:FREQ {_freqMHz}MHz")
        self.m_vxg.write(f":SOUR:RF{_port}:POW {_powdBm} dBm")
        self.m_vxg.write(f":SOUR:RF{_port}:OUTP ON")
        time.sleep(0.1)

    # 2) RF 신호 출력 종료
    def setRFOff(self, _port):
        self.m_vxg.write(f":SOUR:RF{_port}:OUTP OFF")

    # 3) RF 신호 출력 여부 문의 1 : 출력 0 : 미출력
    def isRFOut(self, _port):
        return self.m_vxg.query(f":SOUR:RF{_port}:OUTP?")

### 위상 정렬 관련 함수들
    def setPhaseMod(self, _port, _phaseDeg):
        self.m_vxg.write(f":SOUR:RF{_port}:PHAS {_phaseDeg} DEG")
        time.sleep(0.1)

    def setPhaseCoh(self):
        self.m_vxg.write("PHAS:ADJ")
