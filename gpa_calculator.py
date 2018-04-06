import re
import getpass
import requests

try:
  input = raw_input
except NameError:
  pass

LOGIN_URL = "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSRVSSCFramework"
SSC_URL = 'https://ssc.adm.ubc.ca/sscportal/servlets/SRVSSCFramework?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSRVSSCFramework'
GRADES_URL = "https://ssc.adm.ubc.ca/sscportal/servlets/SRVSSCFramework?function=SessGradeRpt"
GRADES_TABLE_URL = "https://ssc.adm.ubc.ca/sscportal/servlets/SRVAcademicRecord?context=html"
LOGOUT_URL = 'https://courses.students.ubc.ca/cs/main?submit=Logout'
  
  
def login(cwl_username, cwl_password):
  session_requests = requests.session()
  response = session_requests.get(LOGIN_URL)
  lt = re.findall(r'name="lt" value="(.*?)" />', str(response.content))
  payload = {
      'username' : cwl_username,
      'password' : cwl_password,
      'lt': lt,
      'execution': 'e1s1',
      '_eventId': 'submit',
      'submit': 'Continue >'
  }

  headers = {}
  #headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  
  # Login request
  headers['refer'] = LOGIN_URL
  result = session_requests.post(LOGIN_URL, data=payload, headers = headers)
  
  # Get SSC menu page
  headers['refer'] = SSC_URL
  result = session_requests.get(SSC_URL, headers = headers)

  # Get grades page
  headers['refer'] = GRADES_URL
  result = session_requests.get(GRADES_URL, headers = headers)
  # print('result is ' + result.content)

  # Get grades table
  headers['refer'] = GRADES_TABLE_URL
  result = session_requests.get(GRADES_TABLE_URL, headers = headers)
  #print('result is ' + result.content)

  courses = re.findall(r'class="listRow grade" grade="(.*?)" credits="(.*?)"', str(result.content))
  print('number of actual grades is: ' + str(len(courses)))
  

  # Logout
  # headers['refer'] = LOGOUT_URL
  # result = session_requests.get(LOGOUT_URL, headers = headers)


def calculate():
  return


def main():
    # Get CWL login credentials
    cwl_username = input("CWL Username:")
    cwl_password = getpass.getpass("CWL Password:")

    if login(cwl_username, cwl_password) == True:
      print('Successfully logged in. Calculating GPA...')
      calculate()
    else:
      print('Unable to login. Please try again.')


if __name__ == '__main__':
    main()
