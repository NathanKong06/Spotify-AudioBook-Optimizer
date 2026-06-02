from planners.strict_planner import StrictPlanner
from planners.overflow_planner import OverflowPlanner

def generate_schedule(books, mode):
    if mode == "Complete-in-Month":
        return StrictPlanner().build(books)
    return OverflowPlanner().build(books)