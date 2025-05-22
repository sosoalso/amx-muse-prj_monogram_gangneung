from config import IR, TP_LIST
from lib.buttonhandler import ButtonHandler
from lib.lib_tp import tp_add_watcher
from mojo import context


# ---------------------------------------------------------------------------- #
# SECTION : 제어 장비
# ---------------------------------------------------------------------------- #
def handle_ir(index):
    context.log.info(f"handle_ir: {index}")
    IR[0].clearAndSendIrCode(index)  # Send the IR command using the first IR device


# ---------------------------------------------------------------------------- #
# SECTION : TP
# ---------------------------------------------------------------------------- #
TP_PORT_BLU_RAY = 8


# ---------------------------------------------------------------------------- #
def add_tp_ir():
    for idx, tp in enumerate(TP_LIST):
        # for code in [1, 2, 3, 4, 5, 6, 7, 9, 44, 45, 46, 47, 48, 49, 50, 51, 58]:
        for code in [27, 28]:
            ir_button = ButtonHandler()
            ir_button.add_event_handler("push", lambda code=code: handle_ir(code))
            tp_add_watcher(tp, TP_PORT_BLU_RAY, code, ir_button.handle_event)
    context.log.info("tp_ir 등록 완료")
