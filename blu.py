from mojo import context

from config import BLU, TP_LIST
from lib.blucontroller import BluController
from lib.buttonhandler import ButtonHandler
from lib.lib_tp import (
    tp_add_watcher_ss,
    tp_send_level_ss,
    tp_set_button_ss,
    tp_set_button_text_ss,
)

# ---------------------------------------------------------------------------- #
BLU_PATH_GAIN = [
    ("AMX MAIN SPEAKER GAIN", "Master"),
    ("AMX CEILLING GAIN", "Gain"),
    ("AMX OUTDOOR GAIN", "Gain"),
]
BLU_PATH_MUTE = [
    ("AMX MAIN SPEAKER GAIN", "Override Mute"),
    ("AMX CEILLING GAIN", "Mute"),
    ("AMX OUTDOOR GAIN", "Mute"),
]
# ---------------------------------------------------------------------------- #
# SECTION - 제어 장비
# ---------------------------------------------------------------------------- #
blu_controller = BluController(BLU)  # INFO - 제어 장비 인스턴스


def handle_blu_controller_online():
    blu_controller.init(BLU_PATH_GAIN, BLU_PATH_MUTE)


BLU.online(lambda evt: handle_blu_controller_online())
# ---------------------------------------------------------------------------- #
# SECTION - TP
# ---------------------------------------------------------------------------- #
TP_PORT_BLU = 2


def refresh_tp_by_path(path):
    if path in BLU_PATH_GAIN:
        idx = BLU_PATH_GAIN.index(path)
        lvl_index = 101 + idx
        val = blu_controller.states.get_state(path)
        if val is not None:
            tp_send_level_ss(TP_LIST, 2, lvl_index, int(round(blu_controller.db_to_tp(float(val)), 0)))
            tp_set_button_text_ss(TP_LIST, 2, lvl_index, f"{round(val, 1)} db")
    elif path in BLU_PATH_MUTE:
        idx = BLU_PATH_MUTE.index(path)
        ch_index = 101 + idx
        val = blu_controller.states.get_state(path)
        if val is not None:
            tp_set_button_ss(TP_LIST, 2, ch_index, val == "Muted")


blu_controller.states.subscribe(refresh_tp_by_path)


def add_tp_blu():
    # ---------------------------------------------------------------------------- #
    for idx, path in enumerate(BLU_PATH_GAIN):
        vol_up_button = ButtonHandler(repeat_interval=0.3)
        vol_down_button = ButtonHandler(repeat_interval=0.3)
        vol_up_button.add_event_handler("push", lambda path=path: blu_controller.vol_up(path))
        vol_up_button.add_event_handler("repeat", lambda path=path: blu_controller.vol_up(path))
        vol_down_button.add_event_handler("push", lambda path=path: blu_controller.vol_down(path))
        vol_down_button.add_event_handler("repeat", lambda path=path: blu_controller.vol_down(path))
        tp_add_watcher_ss(TP_LIST, TP_PORT_BLU, 201 + idx, vol_up_button.handle_event)
        tp_add_watcher_ss(TP_LIST, TP_PORT_BLU, 301 + idx, vol_down_button.handle_event)
    # ---------------------------------------------------------------------------- #
    for idx, path in enumerate(BLU_PATH_MUTE):
        mute_toggle_button = ButtonHandler()
        mute_toggle_button.add_event_handler("push", lambda path=path: blu_controller.toggle_muted_unmuted(path))
        tp_add_watcher_ss(TP_LIST, TP_PORT_BLU, 101 + idx, mute_toggle_button.handle_event)
    context.log.info("add_tp_blu 등록 완료")


def add_evt_blu():
    def refresh_all():
        for path in BLU_PATH_GAIN + BLU_PATH_MUTE:
            refresh_tp_by_path(path)

    BLU.online(lambda evt: refresh_all())
    for _, dv_tp in enumerate(TP_LIST):
        dv_tp.online(lambda evt: refresh_all())
        dv_tp.online(lambda evt: refresh_all())
    context.log.info("add_evt_blu 등록 완료")
