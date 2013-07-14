class Tasks:
	taskid = 0
	tasks = []
	dbmng = None

	@staticmethod
	def addTasks(words):
		tags = []
		phrase = ""
		estimated_pomodori = 0
		for word in words:
			if ('+' in word):
				tags.append(word)
			elif ('#' in word):
				estimated_pomodori = int(word[1:])
			else:
				phrase += " " + word	
		
		Tasks.taskid += 1
		Tasks.tasks.append({"_id": Tasks.taskid,'tags': tags, 'todo': phrase.lstrip(), 'deletesoft': 0, 'completed': 0, 'npomodoroEstimated': estimated_pomodori})

	"""
		Write methods on DB
	"""
	@staticmethod 
	def writeTaskWithTags():
		for task in Tasks.tasks:
			Tasks.dbmng.insertTaskWithTags(task)
	@staticmethod
	def writeTasksInTodaySheet(todaySheet):
		Tasks.dbmng.insertTasksInTodaySheet(todaySheet)
	
	@staticmethod
	def deleteSoftFromTasksInventory(taskid):
		Tasks.dbmng.updateTaskSettingDeleteSoft(taskid)

	"""
		Find methods on DB
	"""
	@staticmethod
	def findAllTasks():
		return Tasks.dbmng.findAll()


	@staticmethod
	def findTaskWithTagname(tagname):
		return Tasks.dbmng.findTaskWithTag(tagname)
			

	@staticmethod
	def listTodayTasks(viewCompleteTasks = False):
		for task in Tasks.dbmng.getTodayTasksByTodaySheet():
			if viewCompleteTasks:
				print "%-100s %-50s" % (task['todo'], ('COMPLETATO' if task['completed'] else 'NON COMPLETATO'))
			else:
				if (not task['completed']):
					print "%-100s" % (task['todo'])	
			
	
	@staticmethod
	def getTodayTasks():
		tasks = []
		for task in Tasks.dbmng.getTodayTasksByTodaySheet():
			if (not task['completed']):
				tasks.append({'taskid': task['_id'], 'task': task['todo']})
		return tasks
			
	@staticmethod
	def updatePomodoroByTodayTask(taskid, npomodoro):
		Tasks.dbmng.updateNumberOfPomodoroTodaySheet(taskid, npomodoro)

	