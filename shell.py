import os
import cmd
import sys
import time
from constants import Constants
from tasks import Tasks
from todaysheet import TodaySheet

class Shell(cmd.Cmd):
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = Constants.PROMPT_SHELL
		
	def callShellPrompt(self):
		self.cmdloop()

	"""
		Command line parser methods in interactive mode
	"""
	def do_add(self, line):
		words = line.split(' ')
		Tasks.addTasks(words)
		Tasks.writeTaskWithTags()
	
	def do_list(self, line):
		for task in Tasks.findAllTasks():
			print "%d) %s " % (task['_id'],task['todo'])
	
	def do_mv(self, line):
		taskid = line.split(',')
		self._todaySheet = TodaySheet(taskid)
		Tasks.writeTasksInTodaySheet(self._todaySheet.makeRecordToWriteOnDB())

	def do_now(self, line):
		 Tasks.getTodayTasks()
	
	def do_start(self, line):
		
	def do_EOF(self, line):
		return True
	def do_exit(self, args):
		return True