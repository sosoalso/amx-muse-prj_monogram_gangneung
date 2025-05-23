import re

from config import TP_LIST, VIDMTX
from lib.buttonhandler import ButtonHandler
from lib.eventmanager import EventManager
from lib.lib_tp import (
    tp_add_watcher,
    tp_set_button,
    tp_set_button_text_unicode,
    tp_set_button_text_unicode_ss,
)
from mojo import context


# ---------------------------------------------------------------------------- #
# SECTION : 제어 장비
# ---------------------------------------------------------------------------- #
class Vidmtx(EventManager):
    def __init__(self, dv):
        super().__init__("route")
        self.dv = dv
        self.routes = {key: 0 for key in range(1, 20 + 1)}
        self.init()

    def init(self):
        self.dv.receive.listen(self.parse_response)

    def parse_response(self, *args):
        try:
            data_text = args[0].arguments["data"].decode("utf-8")
            context.log.debug(data_text)
            parsed_data_text_chunks = data_text.split("\n\n")
            for parsed_data_text in parsed_data_text_chunks:
                splitted_message = parsed_data_text.split("\n")
                if "VIDEO OUTPUT ROUTING:" in splitted_message[0]:
                    for msg in splitted_message[1:]:
                        match = re.search(r"\d+ \d+", msg)
                        if match:
                            line = match.group(0)
                            try:
                                idx_out, idx_in = map(int, line.split())
                                self.routes[idx_out + 1] = idx_in + 1
                                self.trigger_event("route", idx_in=idx_in, idx_out=idx_out, this=self)
                            except ValueError as e:
                                context.log.error(f"{e}")
        except (AttributeError, KeyError, UnicodeDecodeError) as e:
            context.log.error(f"Error decoding data: {e}")
            return

    def set_route(self, idx_in, idx_out):
        self.dv.send(f"VIDEO OUTPUT ROUTING:\n{idx_out} {idx_in}\n\n")
        self.routes[idx_out + 1] = idx_in + 1
        self.trigger_event("route", idx_in=idx_in, idx_out=idx_out, routes=self.routes, this=self)

    def set_routes(self, route_dict):
        route_str = "\n".join(f"{idx_in} {idx_out}" for idx_in, idx_out in route_dict.items())
        self.dv.send(f"VIDEO OUTPUT ROUTING:\n{route_str}\n")
        for idx_in, idx_out in route_dict.items():
            self.trigger_event("route", idx_in=idx_in, idx_out=idx_out, routes=self.routes, this=self)


vidmtx_instance = Vidmtx(VIDMTX)
# ---------------------------------------------------------------------------- #
# SECTION : TP
# ---------------------------------------------------------------------------- #
TP_PORT_VIDMTX = 3
NUM_VIDMTX_IN = 20
NUM_VIDMTX_OUT = 20
NAME_VIDMTX_IN = (
    "카메라 1",
    "카메라 2",
    "카메라 3",
    "카메라 4",
    "입력 05",
    "입력 06",
    "입력 07",
    "입력 08",
    "입력 09",
    "입력 10",
    "입력 11",
    "입력 12",
    "입력 13",
    "입력 14",
    "입력 15",
    "입력 16",
    "입력 17",
    "입력 18",
    "입력 19",
    "입력 20",
)
NAME_VIDMTX_OUT = (
    "출력 01",
    "출력 02",
    "출력 03",
    "출력 04",
    "출력 05",
    "출력 06",
    "출력 07",
    "출력 08",
    "출력 09",
    "출력 10",
    "출력 11",
    "출력 12",
    "출력 13",
    "출력 14",
    "출력 15",
    "출력 16",
    "출력 17",
    "출력 18",
    "출력 19",
    "출력 20",
)


# ---------------------------------------------------------------------------- #
class var:
    sel_in = [0] * len(TP_LIST)


# ---------------------------------------------------------------------------- #
def refresh_input_button(idx_tp):
    for idx_in in range(1, NUM_VIDMTX_IN + 1):
        tp_set_button(TP_LIST[idx_tp], TP_PORT_VIDMTX, idx_in + 100, var.sel_in[idx_tp] == idx_in)
        tp_set_button(
            TP_LIST[idx_tp],
            TP_PORT_VIDMTX,
            idx_in + 200,
            var.sel_in[idx_tp] and vidmtx_instance.routes[idx_in] == var.sel_in[idx_tp],
        )


def refresh_output_button(idx_tp):
    for idx_out in range(1, NUM_VIDMTX_OUT + 1):
        tp_set_button(
            TP_LIST[idx_tp],
            TP_PORT_VIDMTX,
            idx_out + 200,
            var.sel_in[idx_tp] and vidmtx_instance.routes[idx_out] == var.sel_in[idx_tp],
        )


def refresh_input_button_name(idx_tp):
    for idx_in in range(1, NUM_VIDMTX_IN + 1):
        tp_set_button_text_unicode(TP_LIST[idx_tp], TP_PORT_VIDMTX, idx_in + 100, NAME_VIDMTX_IN[idx_in - 1])


def refresh_output_button_name(idx_tp):
    for idx_out in range(1, NUM_VIDMTX_OUT + 1):
        tp_set_button_text_unicode(TP_LIST[idx_tp], TP_PORT_VIDMTX, idx_out + 200, NAME_VIDMTX_OUT[idx_out - 1])


def refresh_output_route_name_all():
    for idx_out in range(1, NUM_VIDMTX_OUT + 1):
        refresh_output_route_name(idx_out)


def refresh_output_route_name(idx_out):
    if 0 < idx_out <= NUM_VIDMTX_OUT:
        if 0 < vidmtx_instance.routes[idx_out] <= NUM_VIDMTX_IN:
            tp_set_button_text_unicode_ss(
                TP_LIST, TP_PORT_VIDMTX, idx_out + 300, NAME_VIDMTX_IN[vidmtx_instance.routes[idx_out] - 1]
            )
        else:
            tp_set_button_text_unicode_ss(TP_LIST, TP_PORT_VIDMTX, idx_out + 300, "")


# ---------------------------------------------------------------------------- #
def add_tp_vidmtx():
    for idx_tp, dv_tp in enumerate(TP_LIST):
        # INFO : 입력 선택 버튼 | ch 101-120
        for idx_in in range(1, 20 + 1):

            def set_selected_input(idx_tp=idx_tp, idx_in=idx_in):
                var.sel_in[idx_tp] = idx_in
                refresh_input_button(idx_tp)
                refresh_output_button(idx_tp)

            input_select_button = ButtonHandler()
            input_select_button.add_event_handler("push", set_selected_input)
            tp_add_watcher(dv_tp, TP_PORT_VIDMTX, idx_in + 100, input_select_button.handle_event)
        # INFO : 출력 버튼 - 라우팅 | ch 201-220
        for idx_out in range(1, 20 + 1):

            def set_route(idx_tp=idx_tp, idx_out=idx_out):
                if var.sel_in[idx_tp] and idx_out:
                    vidmtx_instance.set_route(var.sel_in[idx_tp] - 1, idx_out - 1)
                    refresh_output_button(idx_tp)

            output_route_button = ButtonHandler()
            output_route_button.add_event_handler("push", set_route)
            tp_add_watcher(dv_tp, TP_PORT_VIDMTX, idx_out + 200, output_route_button.handle_event)
    context.log.info("add_tp_vidmtx 등록 완료")


def add_evt_vidmtx():
    # INFO : 매트릭스 이벤트 피드백
    def refresh_button_on_route_event(**kwargs):
        for idx_evt, _ in enumerate(TP_LIST):
            refresh_output_button(idx_evt)
            refresh_output_route_name(kwargs["idx_out"] + 1)

    vidmtx_instance.add_event_handler("route", refresh_button_on_route_event)
    # ---------------------------------------------------------------------------- #
    # INFO : TP 온라인 피드백
    for tp_idx, tp_online in enumerate(TP_LIST):
        tp_online.online(lambda evt, idx=tp_idx: refresh_input_button(idx))
        tp_online.online(lambda evt, idx=tp_idx: refresh_output_button(idx))
        tp_online.online(lambda evt, idx=tp_idx: refresh_input_button_name(idx))
        tp_online.online(lambda evt, idx=tp_idx: refresh_output_button_name(idx))
        tp_online.online(lambda evt: refresh_output_route_name_all())
    context.log.info("add_evt_vidmtx 등록 완료")


# ---------------------------------------------------------------------------- #
# import unittest
# class TestVidmtx(unittest.TestCase):
#     def setUp(self):
#         self.vidmtx = Vidmtx()
#     def test_parse_response_valid_data(self):
#         data_text = "VIDEO OUTPUT ROUTING:\n1 2\n3 4\n\n"
#         self.vidmtx.parse_response(data_text)
#         self.assertEqual(self.vidmtx.routes, {1: 2, TP_PORT_VIDMTX: 4})
#     def test_parse_response_no_video_output_routing(self):
#         data_text = "SOME OTHER HEADER:\n1 2\n3 4\n\n"
#         self.vidmtx.parse_response(data_text)
#         self.assertEqual(self.vidmtx.routes, {})
#     def test_parse_response_empty_data(self):
#         data_text = ""
#         self.vidmtx.parse_response(data_text)
#         self.assertEqual(self.vidmtx.routes, {})
#     def test_parse_response_no_double_newline(self):
#         data_text = "VIDEO OUTPUT ROUTING:\n1 2\n3 4"
#         self.vidmtx.parse_response(data_text)
#         self.assertEqual(self.vidmtx.routes, {})
#     def test_parse_response_invalid_format(self):
#         data_text = "VIDEO OUTPUT ROUTING:\n1 A\n3 4\n\n"
#         self.assertEqual(self.vidmtx.routes, {})
# if __name__ == "__main__":
#     unittest.main()
