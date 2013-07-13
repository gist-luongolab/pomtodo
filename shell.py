import os
import cmd
import sys
from constants import Constants
from tasks import Tasks

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
			print task['todo']
	def do_EOF(self, line):
		return True
	def do_exit(self, args):
		return True