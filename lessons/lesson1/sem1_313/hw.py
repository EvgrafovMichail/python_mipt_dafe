import time

class Hacker:
    def __init__(self) -> None:
        pass

    @staticmethod
    def hack_you_ass() -> None:
        print("Взлом очка начинается...")
        i = 0
        while i < 101:
            try:
                print(f"{i}%")
                i += 1
                time.sleep(1)
            except KeyboardInterrupt:
                print("Ты не уйдешь")


print("hello world")
Hacker.hack_you_ass()
