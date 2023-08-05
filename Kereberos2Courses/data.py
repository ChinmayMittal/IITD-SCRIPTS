import json
import argparse
import requests
import argparse
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(
                    prog='Course Loader',
                    description='Loads the courses and students given the semester',)
parser.add_argument('-s', '--semester', type=str, required=False, dest="semester", default="")
args = parser.parse_args() 
semester = args.semester

url = "http://ldapweb.iitd.ac.in/LDAP/courses/gpaliases.html"
file_path = "course_lists.json"

soup = BeautifulSoup(requests.get(url).text, "html.parser")
links = []
for link in soup.find_all("a"):
    links.append((link.get("href")))

if semester == "":
    currentYear = datetime.today().year
    currentMonth = datetime.today().month
    semester = f"{str(currentYear)[2:]}{'02' if currentMonth <= 6 else '01'}"

course_dict = {}
for link in tqdm(links):
    if semester not in link:
        continue
    r = requests.get(f"http://ldapweb.iitd.ac.in/LDAP/courses/{link}")
    soup = BeautifulSoup(r.text, "html.parser")
    course = link.split("-")[1].split(".")[0]
    course_dict[course] = []
    for student in (soup.find_all("td", attrs={"align": "LEFT"})):
            course_dict[course].append(student.text)

with open(file_path, 'w') as json_file:
    json.dump(course_dict, json_file, indent=4)


