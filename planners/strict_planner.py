MONTHLY_LIMIT = 15 * 60

class StrictPlanner:
    def build(self, books: list) -> dict:
        """
        Builds a schedule using a strict knapsack approach, maximizing the total minutes without exceeding the monthly limit.
        Args:
            books (list): A list of book objects, each with a 'minutes' attribute.
        Returns:
            dict: A dictionary containing the 'schedule' (list of months with entries) and 'unscheduled' (list of books that couldn't be scheduled).
        """
        remaining_books = books[:] # Copy of books list
        schedule = []
        month = 1
        while remaining_books:
            # Find the best combination of books for the current month without exceeding the monthly capacity
            chosen = self.best_subset( remaining_books, MONTHLY_LIMIT )
            if not chosen:
                # No valid subset can be found, so scheduling is complete
                break
            schedule.append(
                {
                    "month": month,
                    "entries": [
                        {
                            "title": b.title,
                            "minutes": b.minutes,
                            "partial": False
                        }
                        for b in chosen
                    ]
                }
            )
            for book in chosen:
                # Remove chosen books
                remaining_books.remove(book)
            month += 1
        # Books longer than monthly limit cannot be scheduled in this mode
        unscheduled = [
            b for b in remaining_books
            if b.minutes > MONTHLY_LIMIT
        ]
        return {
            "schedule": schedule,
            "unscheduled": unscheduled
        }

    def best_subset(self, books: list, capacity: int) -> list:
        """
        Uses a dynamic programming approach to find the best subset of books that maximizes total minutes without exceeding the capacity.
        Args:
            books (list): A list of book objects, each with a 'minutes' attribute.
            capacity (int): The maximum total minutes allowed for the subset.
        Returns:
            list: A list of book objects that form the best subset.
        """
        n = len(books)
        # dp[i][c] = maximum minutes achievable using the first i books with capacity c
        dp = [[0] * (capacity + 1)
              for _ in range(n + 1)]
        # Build the DP table one book at a time
        for i in range(1, n + 1):
            # Treat audiobook length as the knapsack weight/value
            weight = books[i - 1].minutes
            # Evaluate every possible remaining capacity
            for c in range(capacity + 1):
                dp[i][c] = dp[i - 1][c]
                if weight <= c:
                    dp[i][c] = max(
                        dp[i][c],
                        dp[i - 1][c - weight] + weight )
        # Reconstruct the chosen subset by walking backwards through the DP table
        chosen = []
        c = capacity
        # If the value changed from the previous row, the current book was included in the optimal solution
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                chosen.append(books[i - 1])
                c -= books[i - 1].minutes
        return chosen