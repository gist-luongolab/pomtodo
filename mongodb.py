import pymongo

class DBManager:
	
	_connection = None
	_dbInstance = None

	def __init__(self, dbName):
		self._connection = pymongo.Connection()
		self.__openConnection(dbName)
		
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
	
	def __openConnection(self, dbName):
		self._dbInstance = self._connection[dbName]
		
	
