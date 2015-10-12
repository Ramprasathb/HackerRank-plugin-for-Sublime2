import sublime, sublime_plugin
import urllib2 as url2, httplib as http, urllib as url1
import json, re, base64


# re - for checking the regular expressions
# base64 - Encoding during the process of authentication

hackerrank_url = 'https://www.hackerrank.com/rest/contests/'

lang = {'py':'python'}

class HackerrankCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		try:
			f = open('credentials.in', 'r')
			credentials = f.readlines()
			username = credentials[0].strip('\n')
			password = credentials[1].strip('\n')
	  	except IOError:
			print 'credentials file missing in the directory \n'
			return
  		
  		authentication = HRBasicAuthHandler()
	  	authentication.add_password( realm=None, uri=hackerrank_url, user=username, passwd=password)
	  	opener = url2.build_opener(authentication)
	  	url2.install_opener(opener)
	   	
	   	language, code, custom_testcase, additional_url = self.getDetails()

	   	if language is None:
	   		return
	   	else:
	   		if custom_testcase is None:
	   			payload = {'code':code, 'customtestcase':'false', 'language':language}
	   		else:
		  		payload = {'code':code, 'customtestcase':'true', 'language':language, 'custominput':custom_testcase}
			url = hackerrank_url+additional_url
		
		request = url2.Request(url+'compile_tests', url1.urlencode(payload))
	 	response = url2.urlopen(request)
	 	header = response.read()
	 	header_ = json.loads(header)
	 	submission_id =  header_['model']['id']
	 	request = url2.Request(url+'compile_tests/'+str(submission_id)+'?')
	 	response = url2.urlopen(request)
	 	response = url2.urlopen(request)
	 	result = response.read()
	 	#print result
	 	if custom_testcase is None:
	 		self.printOutput(json.loads(result))
	 	else:
	 		self.printCustomOutput(json.loads(result))

	def getDetails(self):

		file_name = self.view.file_name()
 	  	actual_file_name = file_name.split('/')[-1]
 	  	file_extension = file_name.split('.')[-1]
 	  	language = lang[file_extension]
 	  	code, custom_testcase = self.getCodeFromFile(language)
 	  	submission_url = code.split('\n')[-1] 	  
 	  	contest_link = map(str, submission_url.split())[-1]
 	  	contest_link = contest_link.split('/')
 	  	if contest_link[3] == 'challenges':
 	  		additional_url = "master/challenges/"+contest_link[-1]+"/"
 	  	else:
 			return None, None, None, None
 	  	return language, code, custom_testcase, additional_url
		
	def getCodeFromFile(self, language):

		code = self.view.substr(sublime.Region(0, self.view.size()))
 	  	testcases = self.load_tests(code)
 	  	if testcases is not None:
	 	  	print testcases
 		  	return code, testcases
 	  	return code, None

 	def load_tests(self, content):
	    m = re.findall('""""I\n(.*?)\nI"""', content, re.DOTALL)
	    if len(m):
	    	return m[0]
	    return None


	def printCustomOutput(self, result):
		print "Custom Testcase\n"
		print "INPUT"
		for each in result['model']['stdin']:
			print str(each)
		print "OUTPUT"
		for each in result['model']['stdout']:
			print str(each)
		print "Errors"
		for each in result['model']['censored_stderr']:
			print str(each)
	def printOutput(self, result):
		result_list = result['model']['testcase_message']
		maxTestcase = len(result_list)
		#print maxTestcase
		count = 0
		for i in result_list:
			if i == 'Success':
				count+=1
		print 'You have passed ( '+str(count)+'/'+str(maxTestcase)+' ) testcases'
		print ''.join('	Testcase '+str(index+1)+": "+str(each)+'\n' for index, each in enumerate(result_list))


class HRBasicAuthHandler(url2.HTTPBasicAuthHandler):
	def http_request(self, req):
		url = req.get_full_url()
		realm = None
		r_username, r_passwd = self.passwd.find_user_password(realm, url)
		if r_passwd:
			raw = "%s:%s" % (r_username, r_passwd)
			auth = 'Basic %s' % base64.b64encode(raw).strip()
			req.add_unredirected_header(self.auth_header, auth)
		return req

	https_request = http_request
