Date - Feb 14th 2022

## Project Title - 5143 Shell Project

### **Project description** - Mimicking basic shell behavior using python<br />
#### **Concepts Used -** 
1. Recursion<br />
2. Dictionaries<br />
3. String & Array operations<br />
4. Creating Package to pack multiple modules into a single folder<br />

#### **Modules used -** <br />
1. Termcolor for coloring output(grep)<br />
2. Json module for all strings needed(man pages,error messages)<br />
3. Regex expressions (grep,wc)<br />
4. Itertools(head,tail - slicing)<br />
5. Pyautogui for cursor(less)

#### List of commands implemented - 

1. ls/ls -l/ls -la/ls -lah	

2. mkdir bananas

3. cd bananas

4. cd ../cd .. ..

5. cd ~/cd		

6. pwd		

7. mv somefile.txt bananas	

8. cp bananas/somefile.txt somefile/otherfile.txt	

9. rm -rf bananas rm bananas

10.	cat somefile	/cat file1 file2

11.	less somefile

12.	head -n 20 somefile/head -20 somefile

13.	tail -n 20 somefile/tail -20 somefile

14.	grep -l bacon bacon.txt	

15.	wc -w bacon.txt/wc -w -l bacon.txt	

16.	history	

17.	!x

18.	chmod 777 somefile.txt

19.	sort bacon.txt

20.	clear

21.	REDIRECTION : cat file1 file2 > file0 (OR) cat file1 >> file0 

22. PIPING: grep bacon bacon.txt | wc -l 

23. MULTIPLE PIPING + REDIRECTION : grep blob a.py | head -4 | wc > a.txt 

24.  man grep (man pages for all commands)

#### Not working
Left and Right arrow presses

#### References
1. Stackoverflow for aligned printing in cd command

#### NOTE
  This program creates a file named 'history.txt' in your home,once you run it in your local.
  Please keep a track to delete that file once you close the program at the end.
