from config import TP_LIST, VIDPRJ
from lib.buttonhandler import ButtonHandler
from lib.eventmanager import EventManager
from lib.lib_tp import tp_add_watcher_ss, tp_set_button_ss
from lib.scheduler import Scheduler
from mojo import context


# ---------------------------------------------------------------------------- #
# SECTION : 제어 장비
# ---------------------------------------------------------------------------- #
class EpsonVidprj(EventManager):
    def __init__(self, dv, name="EpsonVidprj"):
        super().__init__("power", "poweron", "poweroff", "mute", "muted", "unmuted", "poll")
        self.dv = dv
        self.poll = Scheduler(max_workers=3, name="EpsonVidprjPoll")
        self.power = False
        self.mute = False
        self.source = "0"
        self.name = name
        self.init()

    def init(self):
        self.dv.receive.listen(self.parse_response)
        self.dv.connect()
        self.start_poll()

    def start_poll(self, *args):
        def query_power():
            context.log.info("전원 물어보는 중")
            # print(self.poll.scheduled_tasks)
            self.dv.send("%1POWR ?\r")

        def query_mute():
            context.log.info("뮤트 물어보는 중")
            self.dv.send("%1AVMT ?\r")

        self.poll.set_timeout(lambda: self.poll.set_interval(query_power, 10.0), 1.0)
        self.poll.set_timeout(lambda: self.poll.set_interval(query_mute, 10.0), 2.0)

    def parse_response(self, *args):
        if not args or not hasattr(args[0], "arguments") or "data" not in args[0].arguments:
            context.log.error(f"수신 응답은 잘못된 형식입니다. {args=}")
        else:
            try:
                data_text = args[0].arguments["data"].decode("utf-8")
                response = data_text.split("\r")[0]
                context.log.debug(f"EpsonVidprj {self.name=} parse_response {response=}")
                if "%1POWR=" in response:
                    res = response.partition("=")[2]
                    if res == "1":
                        self.power = True
                    elif res == "0":
                        self.power = False
                    context.log.debug(f"{self.power=}")
                    self.trigger_event("power", value=self.power, this=self)
                elif "%1AVMT=" in response:
                    res = response.partition("=")[2]
                    if res == "11":
                        self.mute = True
                    elif res == "10":
                        self.mute = False
                    self.trigger_event("mute", value=self.mute, this=self)
                    context.log.debug(f"{self.mute=}")
            except (AttributeError, KeyError, UnicodeDecodeError) as e:
                context.log.error(f"EpsonVidprj {self.name=} Error decoding data: {e}")

    def set_power(self, value):
        self.dv.send("%1POWR 1\r" if value else "%1POWR 0\r")
        self.power = value
        self.trigger_event("power", value=value, this=self)

    def power_on(self):
        self.set_power(True)

    def power_off(self):
        self.set_power(False)

    def set_mute(self, value):
        self.dv.send("%1AVMT 11\r" if value else "%1AVMT 10\r")
        self.mute = value
        self.trigger_event("mute", value=value, this=self)

    def mute_on(self):
        self.set_mute(True)

    def mute_off(self):
        self.set_mute(False)


vidprj_instance_list = tuple(EpsonVidprj(dv, name=f"vidprj_0{idx}") for idx, dv in enumerate(VIDPRJ))
# ---------------------------------------------------------------------------- #
# SECTION : TP
# ---------------------------------------------------------------------------- #
TP_PORT_VIDPRJ = 4


def refresh_vidprj_power_button(idx):
    tp_set_button_ss(TP_LIST, TP_PORT_VIDPRJ, 11 + idx, vidprj_instance_list[idx].power)
    tp_set_button_ss(TP_LIST, TP_PORT_VIDPRJ, 21 + idx, not vidprj_instance_list[idx].power)


def refresh_vidprj_mute_button(idx):
    tp_set_button_ss(TP_LIST, TP_PORT_VIDPRJ, 31 + idx, vidprj_instance_list[idx].mute)
    tp_set_button_ss(TP_LIST, TP_PORT_VIDPRJ, 41 + idx, not vidprj_instance_list[idx].mute)


def add_event_vidprj():
    # ---------------------------------------------------------------------------- #
    # INFO : 전원 On/Off | ch 11-13 21-23 : 뮤트 On/Off | ch 31-33 41-43
    for idx_vidprj, vidprj_instance in enumerate(vidprj_instance_list):
        power_on_button = ButtonHandler()
        power_off_button = ButtonHandler()
        mute_button = ButtonHandler()
        unmute_button = ButtonHandler()
        power_on_button.add_event_handler("push", vidprj_instance.power_on)
        power_off_button.add_event_handler("push", vidprj_instance.power_off)
        mute_button.add_event_handler("push", vidprj_instance.mute_on)
        unmute_button.add_event_handler("push", vidprj_instance.mute_off)
        tp_add_watcher_ss(TP_LIST, TP_PORT_VIDPRJ, 11 + idx_vidprj, power_on_button.handle_event)
        tp_add_watcher_ss(TP_LIST, TP_PORT_VIDPRJ, 21 + idx_vidprj, power_off_button.handle_event)
        tp_add_watcher_ss(TP_LIST, TP_PORT_VIDPRJ, 31 + idx_vidprj, mute_button.handle_event)
        tp_add_watcher_ss(TP_LIST, TP_PORT_VIDPRJ, 41 + idx_vidprj, unmute_button.handle_event)
    # ---------------------------------------------------------------------------- #
    # INFO : 비디오 프로젝터 이벤트 피드백
    for idx_vidprj, vidprj_instance in enumerate(vidprj_instance_list):
        vidprj_instance.add_event_handler("power", lambda idx=idx, **kwarg: refresh_vidprj_power_button(idx))
        vidprj_instance.add_event_handler("mute", lambda idx=idx, **kwarg: refresh_vidprj_mute_button(idx))
    # ---------------------------------------------------------------------------- #
    # INFO : TP 온라인 피드백
    # ---------------------------------------------------------------------------- #
    for idx, tp in enumerate(TP_LIST):
        for idx in range(len(vidprj_instance_list)):
            tp.online(lambda evt, idx=idx,: refresh_vidprj_power_button(idx))
            tp.online(lambda evt, idx=idx,: refresh_vidprj_mute_button(idx))
    # ---------------------------------------------------------------------------- #
    context.log.info("add_event_vidprj 등록 완료")
    # ---------------------------------------------------------------------------- #
