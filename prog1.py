#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2012 d0nin380 <d0nin380@homeserver>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.



#Please not that this program is far from perfect. I can solve this mission on commandline.
#I will leave the optimization of this program up to you. 
#Enjoy!

import htsmain, re, os, platform
from inspect import stack

class htsprog1:
	"""
	Program to complete hackthissite programming mission 1
	Functions needed by this script in htsmain.py
	"""
	def __init__(self):
		"""
		call in some help from the htsmain.
		"""
		self.hts = htsmain.hts()
		self.hts.Login()
		self.content = self.hts.getMissionInfo('prog', 1)
		if not os.path.isfile('wordlist.txt'): self.hts.getFile('prog', 1,'wordlist.zip'), self.hts.unZipWordList()
		self.solveMission()
		
	def getWordList(self):
		"""
		Just downloading the wordlist...
		This function is no longer needed. use getFile from htsmain.hts
		"""
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		url = self.cfgParser.get('settings','missionUrl')+self.cfgParser.get('settings','wordfile')
		wl = urlopen(url)
		with open(os.path.basename(self.cfgParser.get('settings','wordfile')), 'wb') as local_file:
			local_file.write(wl.read())
			local_file.close()	
	
	def getMissionWords(self, content):
		"""
		We use the re module to get the words out of the html tag hell
		"""
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		reg = re.compile(r'<td><li>(\w+)</li></td>')
		words = re.findall(reg, content)
		return words
		
		
	def solveMission(self):
		"""
		This method will read the wordlist.txt
		Find the answer and send it back to the mission...
		"""
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		_result = []
		f=open('wordlist.txt','r')
		words = self.getMissionWords(self.content)
		data = f.readlines()
		for word in words:
			sword = sorted(word)
			for line in data:
				###This is the easyway...
				#line = (line.rstrip())
				#sline = sorted(line)
				###end of the easy way...
				###This is just done so we can use the platform module :p
				#windows line endings are different...
				if platform.system()=='Windows':
					sline = sorted(line[:-1])
				else:
					sline = sorted(line[:-2])
				if sword == sline:
					self.hts.verbose('matched %s to %s' % (word, line))
					if platform.system() == 'Windows':
						_result.append(line[:-1])
					else:
						_result.append(line[:-2])
					###This is part of the easy way too...
					#_result.append(line)
					###
					
		if len(_result) == 10:
			solution = dict(name='submitform', solution=', '.join(_result))
			self.hts.sendMissionInfo('prog', 1, solution)
			print solution
		else:
			print 'Couldnt solve the mission, Try again...'
		
if __name__ == '__main__':
	hack = htsprog1()	
