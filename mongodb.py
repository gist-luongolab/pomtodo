import pymongo
import datetime

class DBManager:
	
	_connection = None
	_dbInstance = None
	_today = ""
	def __init__(self, dbName):
		self._connection = pymongo.Connection()
		self.__openConnection(dbName)
		self._today = datetime.datetime.now().strftime("%d/%m/%Y")
		
		
	def __openConnection(self, dbName):
		self._dbInstance = self._connection[dbName]

	def createCollectionByName(self, collectionName):
		self._dbInstance[collectionName]

	def insertTaskWithTags(self, taskWithTags):
		self._dbInstance.tasks.insert(taskWithTags)
	
	def updateTaskSettingDeleteSoft(self, taskid):
		task = self._dbInstance.tasks.find_one({'_id': int(taskid)})
		task['deletesoft'] = 1
		self._dbInstance.tasks.save(task)

	def updateTaskSettingCompleted(self, taskid):
		task = self._dbInstance.tasks.find_one({'_id': int(taskid)})
		task['completed'] = 1
		self._dbInstance.tasks.save(task)

	def findAll(self):
		return self._dbInstance.tasks.find({'$and':[{'deletesoft': {'$not': { '$gt': 0}}}, {'completed': {'$not': { '$gt': 0}}}]})

	def findAllTodaySheets(self):
		return self._dbInstance.todaySheets.find();
	def countAllTasks(self):
		return self._dbInstance.tasks.count()
	
	def findTaskWithTag(self, tagName):
		return self._dbInstance.tasks.find({'$and':[{'tags':tagName}, {'deletesoft': {'$not': {'$gt': 0}}}, {'completed': {'$not': { '$gt': 0}}}]})

	def getCollectionsName(self):
		return self._dbInstance.collection_names()
	
	def moveTasksFromTodaySheetToTasksList(self):
		tasks = self._dbInstance.todaySheets.find({'completed': 0})
		for task in tasks:
			self._dbInstance.todaySheets.remove({'taskid':str(task['taskid'])})
			taskWillUpdate = self._dbInstance.tasks.find_one({'_id':int(task['taskid'])})
			taskWillUpdate['deletesoft'] = 0
			self._dbInstance.tasks.save(taskWillUpdate) 
		 
	
	"""
		Today Sheet methods
	"""
	def insertTasksInTodaySheet(self, todaySheet):
		return self._dbInstance.todaySheets.insert(todaySheet)	
	
	def getTodayTasksByTodaySheet(self):
		today_taskids = []
		today_tasks = dict()
		for task in self._dbInstance.todaySheets.find({ 'date': self._today}, sort=[('taskid', pymongo.DESCENDING)]):
			today_taskids.append(task['taskid'])
			today_tasks[task['taskid']] = task
		
		return [ today_tasks , self._dbInstance.tasks.find( {'_id': {'$in': map(int, today_taskids)} } )]
	
	def getTaskFromTaskid(self, taskid):
		return self._dbInstance.tasks.find_one( {'_id': int(taskid) } )
	
	def updateNumberOfPomodoroTodaySheet(self, taskid, numberOfPomodoro):
		taskWillUpdate = self._dbInstance.todaySheets.find_one({'taskid': str(taskid)})
		taskWillUpdate['npomodoroCurrent'] = numberOfPomodoro
		taskWillUpdate['completed'] = 1
		self._dbInstance.todaySheets.save(taskWillUpdate)
		
		taskWillUpdate = dict()
		taskWillUpdate = self._dbInstance.tasks.find_one({'_id': int(taskid)})
		taskWillUpdate['completed'] = 1
		self._dbInstance.tasks.save(taskWillUpdate)
		
	def updateTaskFromTodoTxtFile(self, taskid, taskModified):
		taskWillUpdate = dict()
		taskWillUpdate = self._dbInstance.tasks.find_one({'_id': int(taskid)})
		taskWillUpdate['todo'] = taskModified
		self._dbInstance.tasks.save(taskWillUpdate)
		
		

	def dropdb(self, dbname):
		self._connection.drop_database(dbname)
