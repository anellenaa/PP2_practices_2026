from datetime import datetime, timedelta

# 1. Current date minus 5 days
now = datetime.now()
print("5 days ago:", now - timedelta(days=5))

# 2. Yesterday, today, tomorrow
today = datetime.now().date()
print("Yesterday:", today - timedelta(days=1))
print("Today:    ", today)
print("Tomorrow: ", today + timedelta(days=1))

# 3. Drop microseconds
print("Without microseconds:", datetime.now().replace(microsecond=0))

# 4. Difference between two dates in seconds
date1 = datetime(2026, 1, 1, 12, 0, 0)
date2 = datetime(2026, 9, 30, 18, 30, 0)
print("Difference in seconds:", (date2 - date1).total_seconds())