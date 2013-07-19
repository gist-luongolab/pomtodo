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
	@staticmethod
	def updateTaskToComplete(taskid):
		Tasks.dbmng.updateTaskSettingCompleted(taskid)
		
	"""
		Find methods on DB
	"""
	@staticmethod
	def findAllTasks():
		return Tasks.dbmng.findAll()

	@staticmethod
	def findAllTodaySheets(tagname):
		for task in Tasks.dbmng.findAllTodaySheets():
			task_description = Tasks.dbmng.getTaskFromTaskid(task['taskid'])['todo']
			tags = Tasks.dbmng.getTaskFromTaskid(task['taskid'])['tags']
			if (tagname in tags):
				print 
				print "%-130s (%s) %+50s" % (task_description, task['npomodoroCurrent'],('COMPLETATO' if task['completed'] else 'NON COMPLETATO'))
				print "%+200s" % (tags)
				print "-" * 200


			
		
	@staticmethod
	def findTaskWithTagname(tagname):
		return Tasks.dbmng.findTaskWithTag(tagname)
	
	@staticmethod
	def moveTasksFromTodaySheetToTasksList():
		Tasks.dbmng.moveTasksFromTodaySheetToTasksList()
		

	@staticmethod
	def listTodayTasks(viewCompleteTasks = False):
		tasksTodaySheet = Tasks.dbmng.getTodayTasksByTodaySheet()[0]
		tasks = Tasks.dbmng.getTodayTasksByTodaySheet()[1]
		for task in tasks :
			if viewCompleteTasks:
				print "%-100s (%s) %+50s" % (task['todo'], tasksTodaySheet[str(task['_id'])]['npomodoroCurrent'],('COMPLETATO' if task['completed'] else 'NON COMPLETATO'))
			else:
				if (not task['completed']):
					print "%s) %-100s" % (task['_id'],task['todo'])	
			
	
	@staticmethod
	def getTodayTasks():
		tasks = []
		for task in Tasks.dbmng.getTodayTasksByTodaySheet():
			if (not task['completed']):
				tasks.append({'taskid': task['_id'], 'task': task['todo']})
		return tasks
		
	@staticmethod
	def getNextTask(taskid):
		tasks = Tasks.getTodayTasks()
		for task in tasks:
			if int(taskid) == task['taskid']:
				return task
			
	@staticmethod
	def updatePomodoroByTodayTask(taskid, npomodoro):
		Tasks.dbmng.updateNumberOfPomodoroTodaySheet(taskid, npomodoro)

	@staticmethod
	def updateTaskFromTodoTxtFile(taskid, taskModified):
		Tasks.dbmng.updateTaskFromTodoTxtFile(taskid, taskModified)
	