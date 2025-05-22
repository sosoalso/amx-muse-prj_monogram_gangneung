class Event:
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"Event(id={self.id})"


# 이벤트 핸들러 데코레이터
def on_event(func):
    def wrapper(*args, **kwargs):
        # 이벤트 객체 생성 (예: 이벤트 발생 시 자동 생성)
        evt = Event(id=42)  # id는 예시 값
        print("[Event Triggered] Injecting evt into the function...")
        return func(evt, *args, **kwargs)  # evt를 첫 번째 인수로 주입

    return wrapper


# 이벤트가 발생하면 자동으로 evt가 주입되는 함수
@on_event
def handle_event(*args):
    print(f"Handling event: {args[0]}")
    print(f"Message: {args[1]}")


# 함수 호출 (이벤트 발생 시 자동으로 evt가 주입됨)
handle_event("Hello, World!")
