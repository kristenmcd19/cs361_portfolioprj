#cite sources: https://thepythoncode.com/code/extracting-and-submitting-web-page-forms-in-python

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser
import sys


# initialize an HTTP session
session = HTMLSession()


def get_form(url):
    """Returns form tags from URL"""
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    form = soup.find("form")
    return form


def get_form_details(form):
    '''Returns action, method and input controls of form'''
    # create dictionary for details
    details = {}
    
    # get the form action
    action = form.attrs.get("action").lower()

    # get the form method. get is default if attribute does not exist
    method = form.attrs.get("method", "get").lower()
    
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get ID attribute
        input_id = input_tag.attrs.get("id")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "id": input_id, "value": input_value})

        
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def form_submission(details):
    # compose what to submit to the home page form
    data = {}
    data['pred_type'] = 'substrate'
    data['input_sdf_file'] = 'partner_microservice\input_substrate.sdf'


    # join the url with the action (form request URL)
    new_url = urljoin(url, details["action"])
    if details["method"] == "post":
        res = session.post(url, data=data)
    elif details["method"] == "get":
        res = session.get(url, params=data)
    
    return data, new_url


if __name__ == "__main__":
    import sys
    # get URL from the command line
    url = 'https://pgprules.cmdm.tw/'
    # get all form tags
    forms = get_form(url)
    # iteratte over forms
    details = get_form_details(forms)
    sub = form_submission(details)
    #pprint(sub)

