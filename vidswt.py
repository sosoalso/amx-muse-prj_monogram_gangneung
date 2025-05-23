from config import TP_LIST, VIDSWT
from lib.buttonhandler import ButtonHandler
from lib.eventmanager import EventManager
from lib.lib_tp import tp_add_watcher_ss, tp_set_button_ss
from mojo import context


# ---------------------------------------------------------------------------- #
# SECTION : 제어 장비
# ---------------------------------------------------------------------------- #
class Vidswt(EventManager):
    def __init__(self, dv):
        super().__init__("switch_pgm", "switch_pvw")
        self.dv = dv
        self.pvw_in = 0
        self.pgm_in = 0

    def switch_pvw(self, ch_in):
        self.dv.setPreviewInputVideoSource(0, ch_in)
        self.pvw_in = ch_in
        self.trigger_event("switch_pvw", idx_in=self.pvw_in)

    def switch_pgm(self, ch_in):
        self.dv.setProgramInputVideoSource(0, ch_in)
        self.pgm_in = ch_in
        self.trigger_event("switch_pgm", idx_in=self.pgm_in)

    def transition_cut(self):
        self.dv.execCutME(0)

    def transition_auto(self):
        self.dv.execAutoME(0)


vidswt_instance = Vidswt(VIDSWT)
# ---------------------------------------------------------------------------- #
# SECTION : TP
# ---------------------------------------------------------------------------- #
TP_PORT_VIDSWT = 9


# ---------------------------------------------------------------------------- #
def refresh_pvw_switch_button():
    for idx in range(1, 10 + 1):
        tp_set_button_ss(TP_LIST, TP_PORT_VIDSWT, idx + 100, vidswt_instance.pvw_in == idx - 1)


def refresh_pgm_switch_button():
    for idx in range(1, 10 + 1):
        tp_set_button_ss(TP_LIST, TP_PORT_VIDSWT, idx + 200, vidswt_instance.pgm_in == idx - 1)


def add_tp_vidswt():
    # ---------------------------------------------------------------------------- #
    for idx in range(1, 10 + 1):
        pvw_switch_button = ButtonHandler()
        pvw_switch_button.add_event_handler("push", lambda idx=idx: vidswt_instance.switch_pvw(idx))
        tp_add_watcher_ss(TP_LIST, TP_PORT_VIDSWT, idx + 100, pvw_switch_button.handle_event)
        pgm_switch_button = ButtonHandler()
        pgm_switch_button.add_event_handler("push", lambda idx=idx: vidswt_instance.switch_pgm(idx))
        tp_add_watcher_ss(TP_LIST, TP_PORT_VIDSWT, idx + 200, pgm_switch_button.handle_event)
    # ---------------------------------------------------------------------------- #
    context.log.info("add_tp_vidswt 등록 완료")


def add_evt_vidswt():
    # INFO : 비디오 스위처 이벤트 피드백
    vidswt_instance.add_event_handler("switch_pvw", lambda **kwargs: refresh_pvw_switch_button())
    vidswt_instance.add_event_handler("switch_pgm", lambda **kwargs: refresh_pgm_switch_button())
    # ---------------------------------------------------------------------------- #
    context.log.info("add_evt_vidswt 등록 완료")
