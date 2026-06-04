MONTHLY_LIMIT = 15 * 60

class OverflowPlanner:
    def build(self, books: list) -> list:
        """
        Builds a schedule using a greedy approach that allows overflow, filling each month as much as possible before moving to the next.
        Args:
            books (list): A list of book objects, each with a 'minutes' attribute.
        Returns:
            list: A list of dictionaries, each representing a month with its entries and overflow details.
        """
        remaining_books = books[:] # Copy of books list
        schedule = []
        month_number = 1
        active_book = None # Book that has been started but not finished (in progress)
        active_remaining = 0 #Remaining minutes left in the active book

        while remaining_books or active_book:
            remaining_capacity = MONTHLY_LIMIT
            month_entries = []
            while remaining_capacity > 0:
                if active_book: # Always prioritize continuing a book already in progress
                    # Listen as much as possible of the current active book
                    listened = min(active_remaining, remaining_capacity)
                    month_entries.append(
                        {
                            "title": active_book.title,
                            "minutes": listened,
                            "partial": listened < active_remaining,
                            "book_total": active_book.minutes
                        }
                    )
                    active_remaining -= listened
                    remaining_capacity -= listened

                    if active_remaining == 0:
                        # Finished the active book
                        active_book = None
                    continue

                # Look for books that fit entirely in remaining capacity, preference is given to the largest book that fully fits
                # Greedy choice that tries to minimize splitting books
                fitting_books = [
                    b for b in remaining_books
                    if b.minutes <= remaining_capacity
                ]

                # Select best fitting full book (max duration that fits remaining time)
                if fitting_books:
                    chosen = max(fitting_books, key=lambda b: b.minutes)
                    month_entries.append(
                        {
                            "title": chosen.title,
                            "minutes": chosen.minutes,
                            "partial": False,
                            "book_total": chosen.minutes
                        }
                    )

                    remaining_capacity -= chosen.minutes
                    remaining_books.remove(chosen)
                    continue

                # If no book fits fully, start the largest remaining book
                if remaining_books:
                    chosen = max(remaining_books, key=lambda b: b.minutes)
                    remaining_books.remove(chosen)
                    active_book = chosen
                    active_remaining = chosen.minutes
                    continue
                break
            schedule.append(
                {
                    "month": month_number,
                    "entries": month_entries,
                    "used_minutes":
                        MONTHLY_LIMIT - remaining_capacity,
                    "unused_minutes":
                        remaining_capacity
                }
            )
            month_number += 1
        return schedule