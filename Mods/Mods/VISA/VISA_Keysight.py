import pyvisa
import time

from Mods.VISA.VISA_Keysight_M9484C import CVISA_keysight_M9484C
from Mods.VISA.VISA_Keysight_N9040B import CVISA_Keysight_N9040B

class CVISA_Keysight:
    def __init__(self):
        self.m_ResourceManger = pyvisa.ResourceManager()
        self.m_vxg = None
        self.m_ctrl = None

    def OpenKeysight(self, _ip):
        try:
            self.m_vxg = self.m_ResourceManger.open_resource(
                f"TCPIP0::{_ip}::inst0::INSTR"
            )

            equip_  = str(self.WhoAreYou())
            name_   = self.FindEquipKeysight(equip_)

            if name_ == "M9484C":
                self.m_ctrl = CVISA_keysight_M9484C(self.m_vxg)
            elif name_ == "N9040B":
                self.m_ctrl = CVISA_Keysight_N9040B(self.m_vxg)
            else:
                print("Equipment not recognized")
        except pyvisa.VisaIOError as e:
            print(e)


    def WhoAreYou(self) -> str:
        self.m_vxg.write("*CLS")
        info_ = None
        try:
            info_ = str(self.m_vxg.query("*IDN?"))
        except pyvisa.VisaIOError as e:
            print(e)
        return info_


    def FindEquipKeysight(self, _name: str) -> str:
        if _name.find('M9484C') != -1:
            return "M9484C"
        elif _name.find('N9040B') != -1:
            return "N9040B"
        else:
            return "Equipment not recognized"

    def ResetKeysight(self):
        self.m_vxg.write("&RST")
        time.sleep(1)


    def ClearKeysight(self):
        self.m_vxg.write("*CLS")


    def TimeoutKeysight(self, _timeout):
        self.m_vxg.timeout = _timeout