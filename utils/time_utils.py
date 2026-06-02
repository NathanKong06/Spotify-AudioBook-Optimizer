def to_minutes(hour:int, minutes:int) -> int:
    return hour * 60 + minutes

def to_hours(minutes:int) -> tuple[int, int]:
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour}h {minute:02d}m"