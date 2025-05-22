from config import REL, TP_LIST
from lib.buttonhandler import ButtonHandler
from lib.lib_tp import tp_add_watcher
from lib.lib_yeoul import pulse
from mojo import context


# ---------------------------------------------------------------------------- #
# SECTION : 제어 장비
# ---------------------------------------------------------------------------- #
def set_relay(idx, state):
    REL[idx].state.value = state


def on_relay(idx):
    set_relay(idx, True)


def off_relay(idx):
    set_relay(idx, False)


def pulse_relay(idx, pulse_time=1.0):
    @pulse(pulse_time, off_relay, idx)
    def wrapper():
        on_relay(idx)

    wrapper()


def get_relay_state(idx):
    if idx < 0 or idx >= len(REL):
        context.log.error("릴레이 인덱스 범위 초과")
        raise IndexError
    return REL[idx].state.value


# ---------------------------------------------------------------------------- #
# SECTION : TP
# ---------------------------------------------------------------------------- #
TP_PORT_RELAY = 5


# ---------------------------------------------------------------------------- #
def add_event_relay():
    for tp_instance in TP_LIST:
        for index in range(1, len(REL) + 1):
            button = ButtonHandler()
            button.add_event_handler("push", lambda idx=index - 1: pulse_relay(idx))
            tp_add_watcher(tp_instance, TP_PORT_RELAY, index + 200, button.handle_event)
    context.log.info("tp_relay 등록 완료")


# NOTE : 테스트
# def handle_relay_state(*args):
#     context.log.info(f"{args[0].path} {args[0].value}")


# for rel in REL:
#     if rel:
#         rel.state.watch(handle_relay_state)
# # ---------------------------------------------------------------------------- #
