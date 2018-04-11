import re
import getpass
import requests
from bs4 import BeautifulSoup
try:
  input = raw_input
except NameError:
  pass


LOGIN_URL = "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSRVSSCFramework"
GRADES_URL = "https://ssc.adm.ubc.ca/sscportal/servlets/SRVSSCFramework?function=SessGradeRpt"
GRADES_TABLE_URL = "https://ssc.adm.ubc.ca/sscportal/servlets/SRVAcademicRecord?context=html"
  

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
    if re.findall(r'Login Failed. You have entered an invalid login name/password combination.', str(result.content)):
        return False

    # Get grades page
    headers['refer'] = GRADES_URL
    result = session_requests.get(GRADES_URL, headers = headers)

    # Get grades table
    headers['refer'] = GRADES_TABLE_URL
    result = session_requests.get(GRADES_TABLE_URL, headers = headers)
    
    return result
    

def calculate(scale, result):
      valid_row_count = 0
      total_credits = 0.0
      gpa_count = 0.0

      soup = BeautifulSoup(result.content, 'html.parser')
      table = soup.find('table', {'id': 'allSessionsGrades'})
      rows = table.find_all('tr', {'class': 'listRow'})
      
      for row in rows:
          cells = row.find_all('td')
          if cells[2].text.strip():
              letter_grade = cells[3].text.strip()
              if letter_grade in scale:
                  points = scale[letter_grade]
                  credits = cells[2]['credits']
                  gpa_count += (float(credits) * points)
                  valid_row_count += 1
                  total_credits += float(credits)
                  
      if valid_row_count == 0:
          print('Unable to retrieve grades.')
      else:
          gpa = gpa_count/total_credits
          print('GPA based on ' + str(valid_row_count) + ' courses and ' + str(total_credits) + ' credits is ' + str(round(gpa,2)))


def getScale():
    scale = input("Enter GPA scale (4.0 or 4.33): ")
    if scale == "4.0":
        return {
            'A+': 4.0,
            'A' : 4.0,
            'A-': 3.7,
            'B+': 3.3,
            'B' : 3.0,
            'B-': 2.7,
            'C+': 2.3,
            'C' : 2.0,
            'C-': 1.7,
            'D+': 1.3,
            'D' : 1.0,
            'F' : 0.0,
            }
    elif scale == "4.33":
        return {
            'A+': 4.33,
            'A' : 4.0,
            'A-': 3.67,
            'B+': 3.33,
            'B' : 3.0,
            'B-': 2.67,
            'C+': 2.33,
            'C' : 2.0,
            'C-': 1.67,
            'D+': 1.33,
            'D' : 1.0,
            'F' : 0.0,
            }
    else:
        print("Invalid scale. Please try again.")
        return getScale()


def main():
    scale = getScale()
    cwl_username = input("CWL Username: ")
    cwl_password = getpass.getpass("CWL Password: ")
    result = login(cwl_username, cwl_password)

    if result:
      print('Login successful.')
      calculate(scale, result)
    else:
      print('Invalid login credentials. Please try again.')


if __name__ == '__main__':
    main()
