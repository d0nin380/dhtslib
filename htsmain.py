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

import sys, os,re, ConfigParser, zipfile
try:
	from httplib2 import Http
	from urllib import urlencode
	from urllib2 import urlopen
	from optparse import OptionParser
	from inspect import stack
except ImportError, err:
	sys.exit('Download missing libraries: %snNow exiting..') %err
	
class hts:
	"""
	A python program written by d0nin380 to solve hackthissite.org programming mission.
	So far can only solve mission 1.
	Other missions todo.
	"""
	
	def __init__(self):
		"""
		Here we basically only read the config file...
		check command line help...
		"""
		#lets check if the current path is writable... this is so we can write the wordlist.txt file on the disk
		if not os.access(os.getcwd(),os.W_OK):
			sys.exit('The current directory is not writable.\nMake the directory writable or choose a different path.\nNow exiting...')
		
		
		#parsing command line options (for now, only config location if different than default.
		self.argv_parser = OptionParser()
		self.argv_parser.add_option('-c', '--conf', dest='filename', action='store', help='Default=config.cfg Config file containing the needed info Check the default config file for details', default='config.cfg')
		self.argv_parser.add_option('-v', dest='verbose', action='store_true', help='Print runtime info')
		
		#saving the options.
		(self.options, self.args) = self.argv_parser.parse_args()
		
		#This is usually right after the function docstring
		#Print only if -v flag set at commandline.
		#helps to give you an idea...		
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		
		#loading the config.
		self.loadconfig(self.options.filename)
		
		#setting up the httplib
		self.h=Http()
		self.stack = stack
		
		#just some testing happenin in here... nothing to worry about...	
		#self.Login()
		#self.getWordList()
		#self.unZipWordList()
		#self.getMissionInfo(1)
		
	def loadconfig(self, config):
		"""
		Loading the config.
		"""
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		self.cfgParser = ConfigParser.SafeConfigParser()
		self.cfgParser.read(self.options.filename)
		if self.cfgParser.get('login', 'user') == 'ChangeMe' or self.cfgParser.get('login', 'password') == 'ChangeMe':
			sys.exit('You have not edited the config file so we don\'t know what username and password to use...\nNow exiting...')	
				
	
	def Login(self):
		"""
		This method will log you in to the site.
		"""
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		loginInfo = dict(username = self.cfgParser.get('login','user'), password = self.cfgParser.get('login','password'))
		self.headers = {'host':self.cfgParser.get('headers','host'), 'User-Agent':self.cfgParser.get('headers','ua'), 'Referer':self.cfgParser.get('headers','ref'), 'Content-Type':self.cfgParser.get('headers','ct'), 'Accept-Encoding':self.cfgParser.get('headers','ae')}
		self.response, self.content = self.h.request(self.cfgParser.get('login','loginUrl'), 'POST', headers=self.headers, body=urlencode(loginInfo))
		self.headers['Cookie'] = self.response['set-cookie']
		print self.content
		if 'Logging in on this account requires use of a CAPTCHA.  Please follow the instructions below for the image shown.' in re.findall('<div class="login-form-error">(.+)</div>', self.content):
			print 'Could not login. This account requires captcha validation.'
		elif 'Invalid Password' in re.findall('<div class="login-form-error">(.+)</div>', self.content):
			print 'Could not login. Invalid username or password.'
		else:
			self.verbose('Login successful')
					
		
	def getMissionInfo(self, missionCID, missionID, ref=None):
		"""
		Getting the mission info.
		missionCID = the category of the mission
		'prog', 'basic', 'realistic'
		and the missionID is obviously the number of the mission.	
		Must be logged in..
		"""
		if ref: self.headers['Referer'] = ref
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		mission = self.cfgParser.get('settings','missionUrl')+missionCID+'/'+str(missionID)
		self.response, self.content = self.h.request(mission, 'GET', headers=self.headers)
		if '<!-- login form start -->' in self.content:
			sys.exit('You have not logged in... Wrong username or password?\nNow exiting...')
		else:
			self.verbose('Mission %s retrived...' % missionID)
			return self.content
		
	def sendMissionInfo(self, missionCID, missionID, solution, ref=None):
		url = self.cfgParser.get('settings', 'missionUrl')+missionCID+'/'+str(missionID)+'/index.php'
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		if ref: self.headers['Referer'] = ref
		self.response, self.content = self.h.request(url, 'POST', headers=self.headers, body=urlencode(solution))
		confirm = re.findall(r'<h2>(.*)</h2></div><div class="light-td">(.*)<br /></div>', self.content)
		for i in confirm:
			print 'Mission confirmation:\n%s %s' % (i[0], i[1])
			
	def unZipWordList(self):
		"""
		Unzipping the wordlist.zip in to the cwd
		"""
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		try:
			zipfile.ZipFile('wordlist.zip').extractall()
		except zipfile.BadZipfile, err:
			self.verbose(err)
			self.verbose('Trying to fix BadZipfile...')
			self.fixBadZipfile(self.cfgParser.get('settings','wordfile'))
			
	def fixBadZipfile(self, zipFile):
		"""
		Fixing the bad zipfile created by 'hts-somebody'
		Python cant handle zipfiles with comments at the end.
		This method will find the end of central directory record	
		and get rid of everything after that. ('\n' in this case...)
		Thank you uri-cohen at stackoverflow.com on
		http://stackoverflow.com/questions/4923142/zipfile-cant-handle-some-type-of-zip-data
		"""
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		f = open(zipFile, 'r+b')  
		data = f.read()  
		pos = data.find('\x50\x4b\x05\x06') # End of central directory signature  
		if (pos > 0):  
			f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
			f.truncate()  
			f.close()
			self.verbose('BadZipfile fixed...\n\nNow resuming to unzip the wordlist...')
			self.unZipWordList()
		else:  
			print 'Something is still fucked up... cannot fix... givin up....'
			
	def getFile(self, mCID, mID, f, ref=None):
		"""
		Download a file from the server if you know the filename and the extension
		"""
		if ref: self.headers['Referer'] = ref
		self.verbose('\nNow Running: %s\n' % stack()[0][3])
		url = self.cfgParser.get('settings','missionUrl')+mCID+'/'+str(mID)+'/'+f
		wl = urlopen(url)
		with open(os.path.basename(f), 'wb') as local_file:
			local_file.write(wl.read())
			local_file.close()	

			
	def verbose(self, msg):
		"""
		Print if verbose flag is set.
		"""
		if self.options.verbose:
			print msg
	
if __name__ == '__main__':
	hack = hts()
