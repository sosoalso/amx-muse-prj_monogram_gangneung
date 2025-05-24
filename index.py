from blu import add_evt_blu, add_tp_blu
from cam import add_evt_cam, add_tp_cam
from config import TP_LIST, init_tcp_client_connect
from lib.uimenu import UIMenu
from mojo import context
from relay import add_tp_relay
from vidmtx import add_evt_vidmtx, add_tp_vidmtx
from vidprj import add_evt_vidprj, add_tp_vidprj

# ---------------------------------------------------------------------------- #
context.log.level = "ERROR"
# ---------------------------------------------------------------------------- #
# INFO : UI 메뉴
UI_MENU = tuple(UIMenu(tp) for tp in TP_LIST)
# ---------------------------------------------------------------------------- #
# INFO : 장비 별 터치판넬 이벤트 등록
add_tp_blu()
add_tp_cam()
add_tp_relay()
add_tp_vidmtx()
add_tp_vidprj()
# ---------------------------------------------------------------------------- #
# INFO : 장비 별 이벤트 핸들러 등록
add_evt_blu()
add_evt_cam()
add_evt_vidmtx()
add_evt_vidprj()
# ---------------------------------------------------------------------------- #
# INFO : 소켓 연결 초기화
init_tcp_client_connect()
# ---------------------------------------------------------------------------- #
# INFO : MUSE 프로그램 실행
context.run(globals())
