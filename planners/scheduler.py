from planners.strict_planner import StrictPlanner
from planners.overflow_planner import OverflowPlanner

def generate_schedule(books: list, mode: str) -> list:
    """Generates a listening schedule based on the selected mode.
    Args:
        books (list): List of Audiobook objects to schedule.
        mode (str): Scheduling mode, either "Complete-in-Month" or "Carry-Over".
    Returns:
        list: A month-by-month schedule of listening sessions.
    """
    if mode == "Complete-in-Month":
        return StrictPlanner().build(books)
    return OverflowPlanner().build(books)