try:
  from http.cookiejar import CookieJar
except ImportError:
  from cookielib import CookieJar

try:
  input = raw_input
except NameError:
  pass

try:
  from urllib.request import HTTPCookieProcessor, build_opener, install_opener, Request, urlopen
  from urllib.parse import urlencode
except ImportError:
  from urllib2 import HTTPCookieProcessor, build_opener, install_opener, Request, urlopen
  from urllib import urlencode

import re
import time
import webbrowser
from random import randrange



# Attempt login
def login():
  print('inside login')
  # Cookie / Opener holder
  cj = CookieJar()
  opener = build_opener(HTTPCookieProcessor(cj))

  # Login Header
  opener.addheaders = [('User-agent', 'UBC-Login')]

  # Install opener
  install_opener(opener)

  # Form POST URL
  postURL = "https://cas.id.ubc.ca/ubc-cas/login/"

  # First request form data
  formData = {
    'username': cwl_username,
    'password': cwl_password,
    'execution': 'e1s1',  #e5s1
    '_eventId': 'submit',
    'lt': 'xxxxxx',
    'submit': 'Continue >'
    }

  # Encode form data
  data = urlencode(formData).encode('UTF-8')

  # First request object
  req = Request(postURL, data)

  # Submit request and read data
  resp = urlopen(req)
  respRead = resp.read().decode('utf-8')

  # Find the ticket number
  ticket = "<input type=\"hidden\" name=\"lt\" value=\"(.*?)\" />"
  t = re.search(ticket, respRead)

  # Extract jsession ID
  firstRequestInfo = str(resp.info())
  jsession = "Set-Cookie: JSESSIONID=(.*?);"
  j = re.search(jsession, firstRequestInfo)

  # Second request form data with ticket
  formData2 = {
    'username': cwl_user,
    'password': cwl_pass,
    'execution': 'e1s1',
    '_eventId': 'submit',
    'lt': t.group(1),
    'submit': 'Continue >'
    }

  # Form POST URL with JSESSION ID
  postURL2 = "https://cas.id.ubc.ca/ubc-cas/login;jsessionid=" + j.group(1)

  # Encode form data
  data2 = urlencode(formData2).encode('UTF-8')

  # Submit request
  req2 = Request(postURL2, data2)
  resp2 = urlopen(req2)

  loginURL = "https://courses.students.ubc.ca/cs/secure/login"
  # Perform login and registration
  urlopen(loginURL)
  register = urlopen(registerURL)
  respReg = register.read()
  print("Course Registered.")
  webbrowser.open_new('https://ssc.adm.ubc.ca/sscportal/')


# Scan webpage for seats
def checkSeats(varCourse):

  url = varCourse
  ubcResp = urlopen(url);
  ubcPage = ubcResp.read().decode('utf-8');

  # Search for the seat number element
  t = re.search(totalSeats, ubcPage)
  g = re.search(generalSeats, ubcPage)
  r = re.search(restrictedSeats, ubcPage)

  # Find remaining seats
  if t:
    if t.group(1) == '0':
      return 0
  else:
    print ("Error: Can't locate number of seats.")

  if g:
    if g.group(1) != '0':
      return 1
  else:
    print ("Error: Can't locate number of seats.")
    
  if r:
    if r.group(1) != '0':
      return 2
  else:
    print ("Error: Can't locate number of seats.")




# Get GPA scale 
# gpa_scale = input("Enter GPA scale you wish to use (4.0 or 4.33):")

# Get CWL login credentials
cwl_username = input("CWL Username:")
cwl_password = input("CWL Password:")


if login() == True:
  print('Successfully logged in. Calculating GPA...')
  calculate()
else:
  print('Unable to login. Too bad!!!!')
