from app.models import Event
from datetime import datetime, timedelta

class Schedule:
	def __init__(self, event):
		dates = event.dates.split(",")
		self.days = [datetime.strftime(date, "%a") for date in (datetime.strptime(date, "%m/%d/%Y") for date in dates)]
		self.dates = [datetime.strftime(date, "%m/%d") for date in (datetime.strptime(date, "%m/%d/%Y") for date in dates)]
	
		start_time_parsed = datetime.strptime(event.start, "%I:%M %p")
		end_time_parsed = datetime.strptime(event.end, "%I:%M %p")

		self.times = [datetime.strftime(date, "%I:%M %p") for date in 
					 		datetime_range(start_time_parsed, end_time_parsed,
					 		timedelta(minutes=15))]

def datetime_range(start, end, delta):
	current = start
	while current < end:
		yield current
		current += delta