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

import htsmain, re, HTMLParser
from inspect import stack

class htsbasic6:
	"""
	This will solve the basic mission 6
	The intention of this program is to give you an idea
	how this hts python lib works.
	"""
	def __init__(self):
		"""
		call in the main program.
		Used to login, get and send the mission data and files.
		"""
		self.hts = htsmain.hts()
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		self.h = HTMLParser.HTMLParser()
		self.hts.Login()
		self.content = self.hts.getMissionInfo('basic', 6)
		self.solveBasic6(self.content)
		
		
		
	def solveBasic6(self, content):
		"""
		This function will simply solve the basic mission6
		"""
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		chars = []
		word = re.findall(r'<br /><br /><b>(.*)</b><br /><br />', content)
		word = self.h.unescape(word[0])
		count = 0
		for i in word:
			chars.append(chr(ord(i)-count))
			count +=1
			
		decword = ''.join(chars)
		solution = dict(password=decword)
		self.hts.verbose('Sending: "%s" to the mission.' % decword)
		self.hts.sendMissionInfo('basic', 6, solution)
					
			
if __name__ == '__main__':
	htsbasic6()
