"""

미리세컨드(ms)까지 나타내는 방법 -> %Y-%m-%d %H:%M:%S.%f

"""
import datetime

def time_stamp(_format : str = None) -> str:
    if format is None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    else:
        timestamp = datetime.datetime.now().strftime(f"{_format}")[:-3]
    return timestamp
