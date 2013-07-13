import argparse
import os
import cmd
import sys
from constants import Constants
from tasks import Tasks

class Parser(cmd.Cmd):

	_arg = {}
	_parser = None
	

	def __init__(self, arg):
		self._arg = arg
	
		
	def parseCmdLine(self):
		self._parser = argparse.ArgumentParser(description='Pomodoro activities')
		self._parser.add_argument('-a', '--add', dest="words", nargs="+")
		self._parser.add_argument('-l', '--list', dest="typeOfList", nargs="+")
		self._parser.add_argument('-i', '--interactive', action="store_true", )
		args = self._parser.parse_args()
		
		if (args.words):
			return self.__parseAddTaskCmd(args.words)
		elif (args.typeOfList):
			if (args.typeOfList[0] == "all"):
				return {'constReturnValue':Constants.LIST_ALL_TASK}
			else:
				return {'constReturnValue':Constants.LIST_TASK_BY_TAGNAME, 'tagname': args.typeOfList[0]}
		elif (args.interactive):
			return {'constReturnValue': Constants.SHELL_INTERACTIVE_MODE}

	
	def __parseAddTaskCmd(self, words):
		return {'constReturnValue': Constants.ADD_TASK, 'words': words}
	
	def __parseMoveCmd(self, listTaskId):
		return listTaskId
	