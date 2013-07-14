import datetime
class TodaySheet:
	
	_todayDate = ""
	_time = ""
	_estimate_number_pomodoro = 0
	_tasks_completed = []
	
	def __init__(self, taskid, estimate_pomodoro = 0):
		self._taskid = taskid
		today = datetime.datetime.now()

		self._todayDate = today.strftime("%d/%m/%Y")
		self._time = today.strftime("%H:%M")
		self._estimate_number_pomodoro = estimate_pomodoro


	def getTaskIds(self):
		return self._tasks

	def makeRecordToWriteOnDB(self):
		return {'date': self._todayDate, 'time': self._time, 'npomodoroCurrent': 0,'taskid': self._taskid, 'completed': 0}