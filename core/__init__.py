import datetime

class SystemInfo:
    def __init__(self):
        pass
    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        answer = 'It is now {} {}'.format(now.hour, now.minute)
        return answer