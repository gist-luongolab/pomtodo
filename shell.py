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
		for task in Tasks.findAllTasks():
			print "%d) %s " % (task['_id'],task['todo'])
	
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

	def do_start(self, line):
		"""
		Avvia sessione pomodoro
		"""
		tasks = Tasks.getTodayTasks()
		firstTodayTask = tasks.pop(0)
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
				breakPomodoroSession = TimerCountdown(2, "Pausa breve di 5'", 3)
				breakPomodoroSession.daemon = True
				breakPomodoroSession.start()
				breakPomodoroSession.join()
				print
				user_input = raw_input("Vuoi continuare con il prossimo task? [s/n]")
				if (user_input == 's'):
					if (tasks):
						firstTodayTask = tasks.pop(0)
						numberOfPomodoro = 1
					else:
						break
				else:	
					break
				

		
		#Tasks.updatePomodoroByTodayTask(firstTodayTask['taskid'], numberOfPomodoro)
		
	def do_clear(self, line):
		Tasks.dbmng.dropdb("pomodoroDB")
		sys.exit()
	
	def do_EOF(self, line):
		return True
	def do_exit(self, args):
		return True


