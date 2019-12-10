from app.models import Event
from datetime import datetime, timedelta
from colour import Color

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

def create_overlap(schedule, avail_arr):
		id_list = []
		for time in schedule.times:
			for date in schedule.dates:
				id_list.append(date + " " + time)

		overall_avail = {}
		avail_max = 0
		for id1 in id_list:
			overall_avail[id1] = 0
		for availability in avail_arr:
			for id1 in id_list:
				if availability[id1]:
					overall_avail[id1] += 1
					if overall_avail[id1] > avail_max:
						avail_max = overall_avail[id1]

		full_avail = Color("#5f7eed")
		no_avail = Color("#f0f0f0")
		colors = list(no_avail.range_to(full_avail, avail_max))

		color_dict = {}
		for id1 in id_list:
			color_dict[id1] = colors[overall_avail[id1]]

		return color_dict



def datetime_range(start, end, delta):
	current = start
	while current < end:
		yield current
		current += delta