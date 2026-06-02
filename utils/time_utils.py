def to_minutes(hour:int, minutes:int) -> int:
    """
    Converts hours and minutes into total minutes.
    Args:
        hour (int): The number of hours.
        minutes (int): The number of minutes.
    Returns:
        int: Total minutes calculated from hours and minutes.
    """
    return hour * 60 + minutes

def to_hours(minutes:int) -> tuple[int, int]:
    """
    Converts total minutes into hours and remaining minutes.
    Args:
        minutes (int): Total minutes to convert.
    Returns:
        tuple[int, int]: A tuple containing hours and remaining minutes.
    """
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour}h {minute:02d}m"