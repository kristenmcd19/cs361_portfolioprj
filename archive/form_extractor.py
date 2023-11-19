# cite sources: https://thepythoncode.com/code/extracting-and-submitting-web-page-forms-in-python
# https://stackoverflow.com/questions/19577484/radio-button-value-being-sent-as-on-upon-form-submission

from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin


# initialize an HTTP session
session = HTMLSession()

# url of site where form lives
url = 'https://pgprules.cmdm.tw/'

# GET request to the URL with the submission form
response = session.get(url)

# find the radio button and file inputs
file_input = response.html.find('input[type="file"]', first=True)
radio_input = response.html.find('input[type="radio"][name="pred_type"]', first=True)

# action pulled by submitting post response in live window
# new url is what we will post against
file_action = 'ajaxsubmit.php'
new_url = urljoin(url, file_action)

# create dictionary for the file and radio button values to include in post submission
data = {"pred_type": "substrate"}
files = {file_name: open('../input_substrate.sdf', 'rb')}

# submit the form
response = session.post(new_url, data=data, files=files)

print(response.text)





