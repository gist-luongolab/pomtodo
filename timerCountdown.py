import threading
import time
import os
import sys

class TimerCountdown(threading.Thread):
	def __print_time(self,threadName, delay):
		counter = 0
		while counter <= delay:
			time.sleep(100)
			sys.stdout.write ('\r[{0}] {1}%'.format('#'*((counter * 7)), ((counter * 7) - 5)))
			sys.stdout.flush()
			counter += 1
		os.system('afplay /System/Library/Sounds/Glass.aiff')
	 
	def run(self):
		print "Inizio task: " + self.name
		threadLock = threading.Lock()
		
		threadLock.acquire()
		self.__print_time(self.name, self.delay)
		threadLock.release()

	def __init__(self, threadID, name, delay):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.delay = delay

    
    
	