class Tasks:
	taskid = 0
	tasks = []
	dbmng = None

	@staticmethod
	def addTasks(words):
		tags = []
		phrase = ""
		for word in words:
			if ('+' in word):
				tags.append(word)
			else:
				phrase += " " + word	
		
		Tasks.taskid += 1
		Tasks.tasks.append({"_id": Tasks.taskid,'tags': tags, 'todo': phrase.lstrip()})

	
	@staticmethod 
	def writeTaskWithTags():
		for task in Tasks.tasks:
			Tasks.dbmng.insertTaskWithTags(task)
	@staticmethod
	def findAllTasks():
		return Tasks.dbmng.findAll()


	@staticmethod
	def findTaskWithTagname(tagname):
		return Tasks.dbmng.findTaskWithTag(tagname)
			