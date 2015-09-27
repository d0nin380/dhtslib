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
		# we will need this for each and every script
		self.hts = htsmain.hts()
		
		# verbose is only displayed with -v flag "python basic6.py -v"
		# stack() outputs list of tuples and we can find the name of the current running function
		# as the 4th item in the first tuple
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		
		# I really don't remember why we even used HTMLParser in this script 
		# It's later used to unescape the password. Might have had a case of special characters...
		self.h = HTMLParser.HTMLParser()
		
		# if you have your username and password set in the config file, you can call Login
		self.hts.Login()
		
		# fetch the whole mission info
		self.content = self.hts.getMissionInfo('basic', 6)
		
		# here were calling the function defined below
		self.solveBasic6(self.content)
		
		
		
	def solveBasic6(self, content):
		"""
		This function will simply solve the basic mission6
		"""
		self.hts.verbose('\nNow Running: %s\n' % stack()[0][3])
		# creating a list for the decrypted characters
		chars = []
		# Not really an expert on anything but regular expressions were never my strong point..
		word = re.findall(r'<br /><br /><b>(.*)</b><br /><br />', content)
		# word[0] would do here unless the password contained special characters
		word = self.h.unescape(word[0])
		
		count = 0
		# the word is decrypted so each letter will go up by the amount of its place in the word.
		# password 'aaa' would be encrypted as 'abc' and 'cde' would be encrypted 'ceg'.
		# So we loop through each letter in the word and add one to the 'count'.
		# we then need to substract the count of each character and the easiest way to do that
		# is to convert the letter to it's ASCII value and back to a 'letter'
		# we can do this all in oneliner, append the character that has the count substracted from it
		# to the list callet 'chars'
		for i in word:
			chars.append(chr(ord(i)-count))
			count +=1
			
		# we're creating a decrypted word by joining all the items(letters) in the list 'chars' together.
		decword = ''.join(chars)
		
		# send the solution as a dictionary back to HTS
		solution = dict(password=decword)
		self.hts.verbose('Sending: "%s" to the mission.' % decword)
		self.hts.sendMissionInfo('basic', 6, solution)
					

# this thing down here gets run only if the file is run, not if the file is imported to another file.		
if __name__ == '__main__':
	htsbasic6()
