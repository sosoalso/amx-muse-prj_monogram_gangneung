from mojo import context

from config import CAM_IP, NUM_CAM, TP_LIST
from lib.buttonhandler import ButtonHandler
from lib.lib_tp import (
    tp_add_watcher,
    tp_set_button,
    tp_set_button_text_unicode,
    tp_show_popup,
)
from lib.simpleurlrequests import url_get


# ---------------------------------------------------------------------------- #
# SECTION : 제어 장비
# ---------------------------------------------------------------------------- #
class CanonCam:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.is_fast = False
        self.last_recall_preset = 0

    def logger(self, result):
        print(result)

    def toggle_speed(self):
        self.is_fast = not self.is_fast

    def set_speed(self, speed):
        self.is_fast = speed is True

    def get_speed(self):
        return "5000" if self.is_fast else "2500"

    def get_tilt_speed(self):
        return "5000" if self.is_fast else "2500"

    def get_pan_speed(self):
        return "5000" if self.is_fast else "2500"

    # ---------------------------------------------------------------------------- #
    def move_up(self):
        url_get(
            f"http://{self.ip_address}/-wvhttp-01-/control.cgi?tilt=up&tilt.speed={self.get_speed()}",
        )

    def move_down(self):
        url_get(
            f"http://{self.ip_address}/-wvhttp-01-/control.cgi?tilt=down&tilt.speed={self.get_speed()}",
        )

    def move_left(self):
        url_get(
            f"http://{self.ip_address}/-wvhttp-01-/control.cgi?pan=left&pan.speed={self.get_speed()}",
        )

    def move_right(self):
        url_get(
            f"http://{self.ip_address}/-wvhttp-01-/control.cgi?pan=right&pan.speed={self.get_speed()}",
        )

    def move_stop(self):
        url_get(f"http://{self.ip_address}/-wvhttp-01-/control.cgi?pan=stop&tilt=stop")

    def zoom_in(self):
        url_get(f"http://{self.ip_address}/-wvhttp-01-/control.cgi?zoom=tele")

    def zoom_out(self):
        url_get(f"http://{self.ip_address}/-wvhttp-01-/control.cgi?zoom=wide")

    def zoom_stop(self):
        url_get(f"http://{self.ip_address}/-wvhttp-01-/control.cgi?zoom=stop")

    def recall_preset(self, preset_no):
        url_get(f"http://{self.ip_address}/-wvhttp-01-/control.cgi?p={preset_no}")
        self.last_recall_preset = preset_no

    def store_preset(self, preset_no):
        url_get(f"http://{self.ip_address}/-wvhttp-01-/preset/set?p={preset_no}&all=enabled")


cam_instance_list = [CanonCam(ip) for ip in CAM_IP]  # INFO : 제어 장비 인스턴스
# ---------------------------------------------------------------------------- #
# SECTION : TP
# ---------------------------------------------------------------------------- #
TP_PORT_CAM = 6


class var:
    sel_cam = [0] * len(TP_LIST)


def refresh_cam_sel_btn(idx_tp):
    for index, btn in enumerate([111, 112, 113, 114]):
        tp_set_button(TP_LIST[idx_tp], TP_PORT_CAM, btn, var.sel_cam[idx_tp] == index + 1)


def refresh_cam_prst_btn(idx_tp):
    for index in range(1, 10 + 1):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            tp_set_button(
                TP_LIST[idx_tp],
                TP_PORT_CAM,
                index,
                cam_instance_list[var.sel_cam[idx_tp] - 1].last_recall_preset == index,
            )
        else:
            tp_set_button(TP_LIST[idx_tp], TP_PORT_CAM, index, False)


def refresh_cam_speed_button():
    for idx_tp, _ in enumerate(TP_LIST):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            tp_set_button(TP_LIST[idx_tp], TP_PORT_CAM, 107, cam_instance_list[var.sel_cam[idx_tp] - 1].is_fast)
        else:
            tp_set_button(TP_LIST[idx_tp], TP_PORT_CAM, 107, False)


def refresh_cam_all_button(*args):
    for idx_tp, _ in enumerate(TP_LIST):
        refresh_cam_sel_btn(idx_tp)
        refresh_cam_prst_btn(idx_tp)
    refresh_cam_speed_button()


def show_cam_popup(idx_tp, idx_cam, idx):
    tp_set_button_text_unicode(
        TP_LIST[idx_tp], 1, 51, f"{var.sel_cam[idx_cam]}번 카메라 {idx + 1}번 프리셋이 저장되었습니다."
    )
    tp_show_popup(TP_LIST[idx_tp], "popup_notification")


# ---------------------------------------------------------------------------- #
def add_tp_cam():
    def select_cam(idx_tp, idx_cam):  # 기본 매개변수로 idx_cam 캡처
        var.sel_cam[idx_tp] = idx_cam + 1
        refresh_cam_sel_btn(idx_tp)
        refresh_cam_prst_btn(idx_tp)
        refresh_cam_speed_button()

    def recall_preset(idx_tp, idx_prst):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].recall_preset(idx_prst + 1)
            refresh_cam_prst_btn(idx_tp)

    def store_preset(idx_tp, idx_prst):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].store_preset(idx_prst + 1)
            show_cam_popup(idx_tp, var.sel_cam[idx_tp], idx_prst)

    def move_up(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].move_up()

    def stop_move(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].move_stop()

    def move_down(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].move_down()

    def move_left(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].move_left()

    def move_right(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].move_right()

    def zoom_in(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].zoom_in()

    def zoom_out(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].zoom_out()

    def stop_zoom(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].zoom_stop()

    def toggle_speed(idx_tp):
        if 1 <= var.sel_cam[idx_tp] <= NUM_CAM:
            cam_instance_list[var.sel_cam[idx_tp] - 1].toggle_speed()
        refresh_cam_speed_button()

    # ---------------------------------------------------------------------------- #
    for idx_tp, dv_tp in enumerate(TP_LIST):
        # NOTE : 카메라 선택 버튼 | ch 111-113
        for idx, btn in enumerate([111, 112, 113, 114]):
            cam_sel_btn = ButtonHandler()
            cam_sel_btn.add_event_handler("push", lambda idx_tp=idx_tp, idx=idx: select_cam(idx_tp, idx))
            tp_add_watcher(dv_tp, TP_PORT_CAM, btn, cam_sel_btn.handle_event)
        # NOTE : 카메라 프리셋 버튼 | ch 1-10
        for idx, btn in enumerate(range(1, 10 + 1)):
            prst_btn = ButtonHandler(hold_time=1.5)
            prst_btn.add_event_handler("release", lambda idx_tp=idx_tp, idx=idx: recall_preset(idx_tp, idx))
            prst_btn.add_event_handler("hold", lambda idx_tp=idx_tp, idx=idx: store_preset(idx_tp, idx))
            tp_add_watcher(dv_tp, TP_PORT_CAM, btn, prst_btn.handle_event)
        # NOTE : 카메라 각종 버튼 | ch 101-107
        up_btn = ButtonHandler()
        dn_btn = ButtonHandler()
        tl_btn = ButtonHandler()
        rt_btn = ButtonHandler()
        zi_btn = ButtonHandler()
        zo_btn = ButtonHandler()
        tg_spd_btn = ButtonHandler()
        up_btn.add_event_handler("push", lambda idx_tp=idx_tp: move_up(idx_tp))
        up_btn.add_event_handler("release", lambda idx_tp=idx_tp: stop_move(idx_tp))
        dn_btn.add_event_handler("push", lambda idx_tp=idx_tp: move_down(idx_tp))
        dn_btn.add_event_handler("release", lambda idx_tp=idx_tp: stop_move(idx_tp))
        tl_btn.add_event_handler("push", lambda idx_tp=idx_tp: move_left(idx_tp))
        tl_btn.add_event_handler("release", lambda idx_tp=idx_tp: stop_move(idx_tp))
        rt_btn.add_event_handler("push", lambda idx_tp=idx_tp: move_right(idx_tp))
        rt_btn.add_event_handler("release", lambda idx_tp=idx_tp: stop_move(idx_tp))
        zi_btn.add_event_handler("push", lambda idx_tp=idx_tp: zoom_in(idx_tp))
        zi_btn.add_event_handler("release", lambda idx_tp=idx_tp: stop_zoom(idx_tp))
        zo_btn.add_event_handler("push", lambda idx_tp=idx_tp: zoom_out(idx_tp))
        zo_btn.add_event_handler("release", lambda idx_tp=idx_tp: stop_zoom(idx_tp))
        tg_spd_btn.add_event_handler("push", lambda idx_tp=idx_tp: toggle_speed(idx_tp))
        tp_add_watcher(dv_tp, TP_PORT_CAM, 101, up_btn.handle_event)
        tp_add_watcher(dv_tp, TP_PORT_CAM, 102, dn_btn.handle_event)
        tp_add_watcher(dv_tp, TP_PORT_CAM, 103, tl_btn.handle_event)
        tp_add_watcher(dv_tp, TP_PORT_CAM, 104, rt_btn.handle_event)
        tp_add_watcher(dv_tp, TP_PORT_CAM, 105, zi_btn.handle_event)
        tp_add_watcher(dv_tp, TP_PORT_CAM, 106, zo_btn.handle_event)
        tp_add_watcher(dv_tp, TP_PORT_CAM, 107, tg_spd_btn.handle_event)
    context.log.info("add_tp_cam 등록 완료")


def add_evt_cam():
    for idx, tp in enumerate(TP_LIST):
        tp.online(lambda evt, idx=idx: refresh_cam_sel_btn(idx))
        tp.online(lambda evt, idx=idx: refresh_cam_prst_btn(idx))
    context.log.info("add_evt_cam 등록 완료")
