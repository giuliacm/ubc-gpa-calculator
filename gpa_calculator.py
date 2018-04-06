import re
import getpass
import requests
from bs4 import BeautifulSoup

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
  
  # Login request
  headers['refer'] = LOGIN_URL
  result = session_requests.post(LOGIN_URL, data=payload, headers = headers)
  
  # Get SSC menu page
  headers['refer'] = SSC_URL
  result = session_requests.get(SSC_URL, headers = headers)

  # Get grades page
  headers['refer'] = GRADES_URL
  result = session_requests.get(GRADES_URL, headers = headers)

  # Get grades table
  headers['refer'] = GRADES_TABLE_URL
  result = session_requests.get(GRADES_TABLE_URL, headers = headers)


  grades = []
  valid_row_count = 0
  total_credits = 0.0

  soup = BeautifulSoup(result.content, 'html.parser')
  table = soup.find('table', {'id': 'allSessionsGrades'})
  rows = table.find_all('tr', {'class': 'listRow'})
  
  for row in rows:
      cells = row.find_all('td')
      if cells[2].text.strip():
          percent_grade = cells[2].text.strip()
          letter_grade = cells[3].text.strip()
          credits = cells[2]['credits']
          valid_row_count = valid_row_count + 1
          total_credits = total_credits + float(credits)
  print('final valid row count is: ' + str(valid_row_count))
  print('total credits is: ' + str(total_credits))

  

  # Logout
  # headers['refer'] = LOGOUT_URL
  # result = session_requests.get(LOGOUT_URL, headers = headers)


def calculate():
  return

def getScale():
    scale = input("Enter GPA scale (4.0 or 4.33):")
    if scale == "4.0" or scale == "4.33":
        return scale
    else:
        print("Please enter a valid scale.")
        return getScale()


def main():
    # Get CWL login credentials
    ##    scale = getScale()
    cwl_username = input("CWL Username:")
    cwl_password = getpass.getpass("CWL Password:")

    if login(cwl_username, cwl_password) == True:
      print('Successfully logged in. Calculating GPA...')
      calculate()
    else:
      print('Unable to login. Please try again.')


if __name__ == '__main__':
    main()
