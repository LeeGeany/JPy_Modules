import sys
import time

import pyvisa

class CVISA_Keysight_N9040B:
    def __init__(self, _vxg):
        self.m_vxg = _vxg

    # 스펙트럼 모드로 변경한다.
    def setModeSpectrum(self):
        try:
            self.m_vxg.write(f":INST:SEL SA:")
        except pyvisa.VisaIOError as e:
            print(e)

    # 싱글 스윕을 설정한다.
    def setModeSingleSweep(self, _is : str):
        try:
            if _is == "ON":
                self.m_vxg.write(f":INIT:CONT OFF:")
            else:
                self.m_vxg.write(f":INIT:CONT OFF:")
        except pyvisa.VisaIOError as e:
            print(e)

    # 데이터 포멧을 설정
    def setDataFormat(self, _format : str):
        try:
            if _format == "ASCII":
                self.m_vxg.write(f":FORM:DATA ASC,0")
            else:
                self.m_vxg.write(f":FORM:DATA ASC,0")
        except pyvisa.VisaIOError as e:
            print(e)

    # 내부소스 출력 설정
    def setRefSrc(self, _is : bool):
        try:
            if _is == True:
                self.m_vxg.write(":OUTP:STAT ON:")
            else:
                self.m_vxg.write(":OUTP:STAT OFF:")
        except pyvisa.VisaIOError as e:
            print(e)

    # 중심주파수를 이동한다.
    def setCentralFrequency(self, _where):
        try:
            self.m_vxg.write(f":SENS:FREQ:CENT {_where}Hz")
        except pyvisa.VisaIOError as e:
            print(e)

    # 시작주파수를 설정한다.
    def setStartFrequency(self, _where):
        try:
            self.m_vxg.write(f":SENS:FREQ:START {_where}Hz")
        except pyvisa.VisaIOError as e:
            print(e)

    # 종료주파수를 설정한다.
    def setStopFrequency(self, _where):
        try:
            self.m_vxg.write(f":SENS:FREQ:STOP {_where}Hz")
        except pyvisa.VisaIOError as e:
            print(e)

    # 스팬을 설정한다.
    def setSpanFrequency(self, _where):
        try:
            self.m_vxg.write(f":SENS:FREQ:SPAN {_where}Hz")
        except pyvisa.VisaIOError as e:
            print(e)

    # FULL SPAN 설정한다.
    def setFullSpanFrequency(self):
        try:
            self.m_vxg.write(":SENS:FREQ:SPAN:FULL")
        except pyvisa.VisaIOError as e:
            print(e)

    # 마커의 위치 설정
    def setMarkerFrequency(self, _where, _freq):
        try:
            self.m_vxg.write(f":CALC:MARK{_where}:X {_freq}Hz")
        except Exception as e:
            print(e)

    # 마커를 활성화 한다.
    def setMarkerOnOff(self, _where, _is: bool):
        try:
            if _is == True:
                self.m_vxg.write(f":CALC:MARK{_where}:STAT ON")
            else:
                self.m_vxg.write(f":CALC:MARK{_where}:STAT OFF")
        except Exception as e:
            print(e)

    # 마커를 피크 지점으로 이동
    def setMarkerPeak(self, _where):
        try:
            self.m_vxg.write(f":CALC:MARK{_where}:MAX")
        except pyvisa.VisaIOError as e:
            print(e)

    # 마커의 주파수 값 읽기
    def getMarkerFrequency(self, _where : int) -> int:
        try:
            return self.m_vxg.query(f":CALC:MARK{_where}:X?")
        except pyvisa.VisaIOError as e:
            print(e)

    # 마커의 진폭 값 읽기
    def getMarkerAmp(self, _where : int) -> int:
        try:
            return self.m_vxg.query(f":CALC:MARK{_where}:Y?")
        except pyvisa.VisaIOError as e:
            print(e)

    # 스윕 및 트리거
    def getSpectrumData(self):
        try:
            self.m_vxg.write(f":INIT:IMM")
            time.sleep(0.05)
            status = self.m_vxg.query("*OPC?").strip()
            time.sleep(0.05)

            if status == "1":
                raw_data = self.m_vxg.query(":TRAC? TRACE1")
                data_list = [float(val) for val in raw_data.split(',')]
                return data_list
        except Exception as e:
            print(e)



