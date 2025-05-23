from blu import add_evt_blu, add_tp_blu
from cam import add_evt_cam, add_tp_cam
from config import TP_LIST, init_tcp_client_connect
from lib.uimenu import UIMenu
from mojo import context
from relay import add_tp_relay
from vidmtx import add_evt_vidmtx, add_tp_vidmtx
from vidprj import add_evt_vidprj, add_tp_vidprj
from vidrec import add_evt_vidrec, add_tp_vidrec
from vidswt import add_evt_vidswt, add_tp_vidswt

# from vidswt import add_evt_vidswt, add_tp_vidswt
# def add_system_power_on_off_button(*args):
#     def power_on_event(wait_time):
#         tp_set_button_text_unicode_ss(TP_LIST, 1, 1, "시스템 전원을 켜는 중입니다...")
#         tp_set_page_ss(TP_LIST, "02")
#         set_relay(0, True)
#         for i in range(101):
#             time.sleep(wait_time / 100)
#             tp_send_level_ss(TP_LIST, 1, 1, i)
#         time.sleep(1.0)
#         tp_set_page_ss(TP_LIST, "03")
#     def power_off_event(wait_time):
#         tp_set_button_text_unicode_ss(TP_LIST, 1, 1, "시스템 전원을 끄는 중입니다...")
#         tp_set_page_ss(TP_LIST, "02")
#         set_relay(0, False)
#         for i in range(101):
#             time.sleep(wait_time / 100)
#             tp_send_level_ss(TP_LIST, 1, 1, 100 - i)
#         time.sleep(1.0)
#         tp_set_page_ss(TP_LIST, "01")
#     def power_on_button_event():
#         threading.Thread(target=power_on_event, args=(10,)).start()
#     def power_off_button_event():
#         threading.Thread(target=power_off_event, args=(10,)).start()
#     power_on_button = ButtonHandler()
#     power_off_button = ButtonHandler()
#     power_on_button.add_event_handler("push", power_on_button_event)
#     power_off_button.add_event_handler("push", power_off_button_event)
#     tp_add_watcher_ss(TP_LIST, 1, 201, power_on_button.handle_event)
#     tp_add_watcher_ss(TP_LIST, 1, 202, power_off_button.handle_event)
# ---------------------------------------------------------------------------- #
# INFO : 각종 설정
# ---------------------------------------------------------------------------- #
context.log.level = "ERROR"
# ---------------------------------------------------------------------------- #
# INFO : UI 메뉴
# ---------------------------------------------------------------------------- #
UI_MENU = tuple(UIMenu(tp) for tp in TP_LIST)
# ---------------------------------------------------------------------------- #
# INFO : 장비 별 이벤트 핸들러 등록
# ---------------------------------------------------------------------------- #
add_tp_blu()
add_tp_cam()
add_tp_relay()
add_tp_vidmtx()
add_tp_vidprj()
add_tp_vidrec()
add_tp_vidswt()
# ---------------------------------------------------------------------------- #
add_evt_blu()
add_evt_cam()
add_evt_vidmtx()
add_evt_vidprj()
add_evt_vidrec()
add_evt_vidswt()
# ---------------------------------------------------------------------------- #
init_tcp_client_connect()
# ---------------------------------------------------------------------------- #
context.run(globals())
# ---------------------------------------------------------------------------- #
