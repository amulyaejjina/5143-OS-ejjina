import os,sys,json
'''
--------------------------------------------------------------
LS : Used to display listing of directories
Usage: ls 
       ls -lah
	   ls -l/-a/-h/-lh/-la/-hl
--------------------------------------------------------------
'''
import cmd
import os
import time
from stat import *
import sys
from pwd import getpwuid
from grp import getgrgid
with open(os.getcwd()+'/'+'Resources.json','r') as d:	# load keys from json module
    strings = json.load(d)								# store it in a variable for further use

def size_convert(size):
	suffixes=['B','KB','MB','GB','TB']
	precision=1
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1 								# increment the index of the suffix
		size = size/1024.0 								# apply the division
	return "%.*f%s"%(precision,size,suffixes[suffixIndex])

def octal_to_string(octal):
    result = ""
    value_letters = [(4,"r"),(2,"w"),(1,"x")]
    # Iterate over each of the digits in octal
    for digit in [int(n) for n in str(octal)]:
        # Check for each of the permissions values
        for value, letter in value_letters:
            if digit >= value:
                result += letter
                digit -= value
            else:
                result += '-'
    return result

def get_file_ownership(filename):
    return (
		# this is to get file group
        getpwuid(os.stat(filename).st_uid).pw_name,
        getgrgid(os.stat(filename).st_gid).gr_name
    )

def ls(**kwargs):
	command=["ls"]
	pipe_str=''
	output=''
	ishidden=False
	# keeping all possible combinations handy in a list
	test_list = ['-l','-lh','-hl','-ahl','-alh','-hla','-hal','-lah','-lha','-la','-al']
	if 'params' in kwargs:
		params = kwargs['params']
	if kwargs['ispiping']:
		output = kwargs['ispiping']
	# For long listing - command with 'l' combination in it
	if len(params)==1 and params[0].startswith('-') and params[0][1:].isalpha() and params[0] != '-h' and params[0] != '-ah':
		# if not 'a',remove hidden files
		if 'a' not in params[0]:
			a=os.listdir(os.getcwd())
			for item in a:
				if item.startswith('.'):
					a.remove(item)
			list = a
		else:
			list=os.listdir(os.getcwd())
		# show all hidden files if :ls -a
		if params[0] == '-a':
			a=os.listdir(os.getcwd())
			b = ('\n'.join(a))
			if output:
				return b
			else:
				return a
		# if the params are in the test_list written above, which has 'l' in it - 
		if params[0] in test_list:
			list.sort()
			print('\r')
			for k in list:
				f=os.stat(os.getcwd()+"/%s"%k)
				st1=os.stat(k)
				# get file size
				if params[0] in test_list[1:]:
					Size=size_convert(f.st_size)
				else:
					Size = str(f.st_size)
				Perm=int(oct(os.stat(k)[ST_MODE])[-3:])
				# get permissions & convert them to rwx
				Perm=octal_to_string(Perm)
				ownderName,groupName = get_file_ownership(k)
				# get file modification time
				Atime=time.asctime(time.localtime(st1[ST_ATIME]))
				Mtime=time.asctime(time.localtime(st1[ST_MTIME]))
				Ctime=time.asctime(time.localtime(st1[ST_CTIME]))
				if output:
					# if piping it to wc/other command,pass the output as a string
					pipe_str = pipe_str+Perm+ownderName+groupName+Size+Mtime+k+'\n'
				else:
					# formatting the display with enough spaces
					print('  {0:8s}  {1:8s}  {2:8s}  {3:8s}  {4:12s}  {5:24s} '.format(Perm,ownderName,groupName,Size,Mtime,k))
			if output:
				return pipe_str

	# No long listing - combination of 'a','h' and no 'l'
	elif (len(params)==1 and (params[0]=='-h' or params[0]=='-ah')) or not params:
		# first get all files,remove the ones which are hidden from that list
		a=os.listdir(os.getcwd())
		for item in a:
			if item[0]=='.':
				a.remove(item)
		b = ('\n'.join(a))
		if output:
			return b
		else:
			return a
	else:
		return strings['format'] # if wrong format,display message
