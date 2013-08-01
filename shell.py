import cmd
import sys
import time
from timerCountdown import TimerCountdown
from constants import Constants
from tasks import Tasks
from todaysheet import TodaySheet

class Shell(cmd.Cmd):
	_commands = ['add']

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = Constants.PROMPT_SHELL
		self.completekey = '<tab>'
		self.__importTasksFromFile()


		
	def callShellPrompt(self):
		self.cmdloop()

	"""
		Command line parser methods in interactive mode
	"""
	def do_add(self, line):
		"""
		Aggiunge un nuovo task add <task> <numero_pomodori> <tags>
		"""
		words = line.split(' ')
		Tasks.addTasks(words)
		Tasks.writeTaskWithTags()
	
	
	def do_list(self, line):
		"""
		Elenca tutti i task inseriti
		"""
		sub_command = line.split(' ')
		if (len(sub_command[0]) > 0):
			strSearch = ""
			if ('+' not in sub_command[0]):
				strSearch = '+' + sub_command[0]

			tasks = Tasks.findTaskWithTagname(strSearch)

			for task in tasks:
				print "%d) %-100s" % (task['_id'],task['todo'])
		else:
			tasks = Tasks.findAllTasks()
			
			for task in tasks:
				print "%d) %-100s %-50s" % (task['_id'],task['todo'], task['tags'])
		

			
				
	
	def do_mv(self, line):
		"""
		Sposta i task dall'inventario al todaySheet (rappresenta i task presi in carico)
		"""
		tasksid = line.split(',')
		for taskid in tasksid:
			self._todaySheet = TodaySheet(taskid)
			Tasks.writeTasksInTodaySheet(self._todaySheet.makeRecordToWriteOnDB())
			Tasks.deleteSoftFromTasksInventory(taskid)
	
	def do_now(self, line):
		 """
		 Visualizza i task da svolgere oggi
		 """
		 Tasks.listTodayTasks(False)
	
	def do_tt(self, line):
		"""
		Visualizza tutti i task completati e non completati oggi
		"""
		Tasks.listTodayTasks(True)

	def do_ta(self, line):
		"""
		Visualizza tutti i task completati nei giorni precedenti
		"""
		strSearch = ""
		find_tag = line.split(' ')

		if (len(find_tag[0]) > 0):
			if ('+' not in find_tag[0]):
				strSearch = '+' + find_tag[0]

		Tasks.findAllTodaySheets(strSearch)

	def do_c(self, line):
		"""
		Task completati 
		"""
		task_ids = line.split(',')
		for task_id in task_ids:
			Tasks.updateTaskToComplete(task_id)
	
	def do_start(self, line):
		"""
		Avvia sessione pomodoro
		"""
		task_ids = line.split(',')
		if not task_ids[0]:
			print "Devi inserire un task da cui vuoi partire"
			return
		firstTodayTask = Tasks.getNextTask(task_ids.pop(0))
		
		numberOfPomodoro = 1
		
		while True:	
			pomodoroTimer = TimerCountdown(1, firstTodayTask['task'], 15)
			pomodoroTimer.daemon = True
			pomodoroTimer.start()
			
			pomodoroTimer.join()
			print
			user_input = raw_input("Ti serve altro tempo per completare il task? [s/n]")
			if (user_input == 's'):
				numberOfPomodoro += 1
			else:
				Tasks.updatePomodoroByTodayTask(firstTodayTask['taskid'], numberOfPomodoro)
				break

		
		
	#def do_clear(self, line):
	#	Tasks.dbmng.dropdb("pomodoroDB")
	#	sys.exit()
	
	def do_export(self, line):
		"""
			Export Task from TODO to File in Dropbox
		"""
		self.__exportTasksToFile()

	def do_import(self, line):
		"""
		Import Tasks from file
		"""
		self.__importTasksFromFile()

	def do_EOF(self, line):
		return True
	
	def do_exit(self, args):
		self.__exportTasksToFile();	
		Tasks.moveTasksFromTodaySheetToTasksList()
		return True

	def __exportTasksToFile(self):
		out_file = open("/Users/luigi/Dropbox/todo/td.txt","w+")
		tasks = Tasks.findAllTasks()
		if tasks:
			for task in tasks:
				taskRecord = str(task['_id']) + " $ " + task['todo'] + "\n"
				out_file.write(taskRecord)
		
		out_file.close()

	def __importTasksFromFile(self):
		
		try:
			in_file = open("/Users/luigi/Dropbox/todo/td.txt","r")
   			pass
   		except IOError:
   			return

		if in_file:
			for line in in_file.readlines():
				splitRecord = line.split('$')
				taskid = splitRecord[0].strip()
				task = splitRecord[1].strip()
				Tasks.updateTaskFromTodoTxtFile(taskid, task)

				
		in_file.close()

