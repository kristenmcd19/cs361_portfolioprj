# cite sources: https://thepythoncode.com/code/extracting-and-submitting-web-page-forms-in-python
# https://stackoverflow.com/questions/19577484/radio-button-value-being-sent-as-on-upon-form-submission

from requests_html import HTMLSession
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json


# initialize an HTTP session
session = HTMLSession()

# url of site where form lives
url = 'https://pgprules.cmdm.tw/'


def submit_form(url):
    # GET request to the URL with the submission form
    url_add = ''
    response = session.get(url)

    # find the radio button and file inputs
    file_input = response.html.find('input[type="file"]', first=True)
    radio_input = response.html.find('input[type="radio"][name="pred_type"]', first=True)

    # new url is what we will post against
    file_name = file_input.attrs['name']
    file_action = 'ajaxsubmit.php'
    new_url = urljoin(url, file_action)

    # create dictionary for the file and radio button values to include in post submission
    data = {"pred_type": "substrate"}
    files = {file_name: open('input_substrate.sdf', 'rb')}

    # submit the form. form_response is an HTMLresponse
    form_response = session.post(new_url, data=data, files=files)

    json_string = "[" + form_response.text.replace("\n", ",") + "]"
    json_string_mod = json_string[:-2] + "]"

    updated_response = json.loads(json_string_mod)
    for item in updated_response:
        if item["status"] == "done":
            url_add = item["rurl"]

    report_link = urljoin(url[:-1], url_add)
    return report_link


def scrape_results(report_link):
    # Get the HTML content from the report URL
    report_response = session.get(report_link)

    # parse with bs
    soup = BeautifulSoup(report_response.content, "html.parser")

    # Find all the elements with the specified class name
    elements = soup.find_all("h5", class_= "card-header")

    #clear out json file
    with open("results_pgp.json", "w") as results:
        json.dump({}, results)

    # create list of dictionaries, add that dictionary to results json
    molc_list = []
    for i in range (0, len(elements), 2):
        molc_dict = {}
        molc_dict["id"] = elements[i].text.replace('\n', '')
        molc_dict["substrate_stat"] = elements[i+1].text
        molc_list.append(molc_dict)
    with open("results_pgp.json", "w") as results:
        json.dump(molc_list, results, indent=4)
    results.close()


# monitor SDF file to trigger workflow
while True:
    with open('input_substrate.sdf', "r") as sdf_file:
        if sdf_file.readline() != "":
            report_link = submit_form(url)
            scrape_results(report_link)
            sdf_file.close()
            with open('input_substrate.sdf', "w") as f_sdf_file:
                f_sdf_file.truncate(0)


