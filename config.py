from lib.lib_yeoul import get_device
from lib.networkmanager import TcpClient

BLU = get_device("SoundwebLondonBLU-100-1")
NUM_CAM = 4
CAM_IP = (
    "192.168.0.31",
    "192.168.0.32",
    "192.168.0.33",
    "192.168.0.34",
)
VIDMTX = TcpClient(name="vidmtx", ip="192.168.0.41", port=9990, buffer_size=2048)
VIDPRJ_01 = TcpClient(name="vidprj_01", ip="192.168.0.51", port=4352)
VIDPRJ_02 = TcpClient(name="vidprj_02", ip="192.168.0.52", port=4352)
VIDPRJ_03 = TcpClient(name="vidprj_03", ip="192.168.0.53", port=4352)
VIDPRJ = (VIDPRJ_01, VIDPRJ_02, VIDPRJ_03)
VIDREC = TcpClient(name="vidrec", ip="192.168.0.43", port=9993)
MUSE = get_device("idevice")
CE_REL_8_01 = get_device("CE-REL8-AC01E5")
CE_REL_8_02 = get_device("CE-REL8-AC0201")
REL_01 = MUSE.relay[0]
REL_02 = MUSE.relay[1]
REL_03 = MUSE.relay[2]
REL_04 = MUSE.relay[3]
REL_05 = MUSE.relay[4]
REL_06 = MUSE.relay[5]
REL_07 = MUSE.relay[6]
REL_08 = MUSE.relay[7]
REL_09 = CE_REL_8_01.relay[0]
REL_10 = CE_REL_8_01.relay[1]
REL_11 = CE_REL_8_01.relay[2]
REL_12 = CE_REL_8_01.relay[3]
REL_13 = CE_REL_8_01.relay[4]
REL_14 = CE_REL_8_01.relay[5]
REL_15 = CE_REL_8_01.relay[6]
REL_16 = CE_REL_8_01.relay[7]
REL_17 = CE_REL_8_02.relay[0]
REL_18 = CE_REL_8_02.relay[1]
REL_19 = CE_REL_8_02.relay[2]
REL_20 = CE_REL_8_02.relay[3]
REL_21 = CE_REL_8_02.relay[4]
REL_22 = CE_REL_8_02.relay[5]
REL_23 = CE_REL_8_02.relay[6]
REL_24 = CE_REL_8_02.relay[7]
REL = (
    REL_01,
    REL_02,
    REL_03,
    REL_04,
    REL_05,
    REL_06,
    REL_07,
    REL_08,
    REL_09,
    REL_10,
    REL_11,
    REL_12,
    REL_13,
    REL_14,
    REL_15,
    REL_16,
    REL_17,
    REL_18,
    REL_19,
    REL_20,
    REL_21,
    REL_22,
    REL_23,
    REL_24,
)
# # ---------------------------------------------------------------------------- #
IR_01 = MUSE.ir[0]
IR_02 = MUSE.ir[1]
IR_03 = MUSE.ir[2]
IR_04 = MUSE.ir[3]
IR_05 = MUSE.ir[4]
IR_06 = MUSE.ir[5]
IR_07 = MUSE.ir[6]
IR_08 = MUSE.ir[7]
IR_09 = None
IR_10 = None
IR_11 = None
IR_12 = None
IR_13 = None
IR_14 = None
IR_15 = None
IR_16 = None
IR = (
    IR_01,
    IR_02,
    IR_03,
    IR_04,
    IR_05,
    IR_06,
    IR_07,
    IR_08,
    IR_09,
    IR_10,
    IR_11,
    IR_12,
    IR_13,
    IR_14,
    IR_15,
    IR_16,
)


def init_ir():
    for ir in IR:
        if ir is not None:
            ir.mode.value = "IR"
            ir.carrier.value = True


# ---------------------------------------------------------------------------- #
TP_10001 = get_device("AMX-10001")
TP_10002 = get_device("AMX-10002")
TP_10003 = get_device("AMX-10003")
TP_LIST = (TP_10001, TP_10002, TP_10003)


# ---------------------------------------------------------------------------- #
def init_tcp_client_connect():
    VIDMTX.connect()
    VIDPRJ_01.connect()
    VIDPRJ_02.connect()
    VIDPRJ_03.connect()
    VIDREC.connect()
