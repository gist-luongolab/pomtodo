import datetime
class TodaySheet:
	
	_todayDate = ""
	_time = ""
	_tasks = []
	_tasks_completed = []
	
	def __init__(self, taskid):
		self._tasks = taskid
		today = datetime.datetime.now()

		self._todayDate = today.strftime("%d/%m/%Y")
		self._time = today.strftime("%H:%M")

	def getTaskIds(self):
		return self._tasks
	def makeRecordToWriteOnDB(self):
		return {'date': self._todayDate, 'time': self._time, 'taskids': self._tasks}