import pymongo
import datetime

class DBManager:
	
	_connection = None
	_dbInstance = None
	_today = ""
	def __init__(self, dbName):
		self._connection = pymongo.Connection()
		self.__openConnection(dbName)
		self._today = datetime.datetime.now()
		
		
	def __openConnection(self, dbName):
		self._dbInstance = self._connection[dbName]

	def createCollectionByName(self, collectionName):
		self._dbInstance[collectionName]

	def insertTaskWithTags(self, taskWithTags):
		self._dbInstance.tasks.insert(taskWithTags)
	
	def findAll(self):
		return self._dbInstance.tasks.find()

	def countAllTasks(self):
		return self._dbInstance.tasks.count()
	def findTaskWithTag(self, tagName):
		return self._dbInstance.tasks.find({'tags':tagName})

	def getCollectionsName(self):
		return self._dbInstance.collection_names()
	
	
	def insertTasksInTodaySheet(self, todaySheet):
		return self._dbInstance.todaySheets.insert(todaySheet)	
	
	def getTodayTasksByTodaySheet(self):
		today_taskids = []
		for taskids in self._dbInstance.todaySheets.find({ 'date': self._today.strftime("%d/%m/%Y") }):
			today_taskids.extend(taskids['taskids'])
		return self._dbInstance.tasks.find( {'_id': {'$in': map(int, today_taskids)} } )
	

	def dropdb(self, dbname):
		self._connection.drop_database(dbname)
