This is a small plugin for Sublime 2 that runs your code on the HackerRank platform

This plugin is completely written using Python.


Copy Paste all these files into the User folder of your .*\Sublime 2\Packages\User (Windows)
Steps to be followed :
1. Add the contents of "Default (Windows).sublime-keymap" to your sublime-keymap
2. Create a new python file and write your code. Insert the URL of the question in Hackerrank where the code is supposed to be run, in a comment.
	e.g) # https://www.hackerrank.com/challenges/solve-me-first
	For custom Input : please follow the format in "test_customInput.py"
3. Press Ctrl+R when you want to run the code on Hackerrank.
4. The output will be displayed on the console.


Difficulties Faced :
1. Understanding the working of Sublime plugins was challenging
2. Tried to make the call without authentication, but couldn't get the response of number of testcases passed using the given submission_id. Hence have included the authentication. When making a Get request with the submission ID couldn't get the response as Status : true, it was always false.
3. Given more time, I shall be able to understand more about it and try removing the authentication. 

References : 
1. Python Docs
2. Hackerrank 
3. Open Source examples for making authentication and sublime plugins