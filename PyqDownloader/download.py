import os
import ssl
import argparse
import requests
import urllib.request
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
                    prog='PYQ Downloaer',
                    description='Downloads PYQs from the BSW Website for a particular course',)
parser.add_argument('-c', '--course', type=str, required=True, dest="course", default=None)
parser.add_argument("-p", '--path', type=str, required=False, dest="path", default="./")
args = parser.parse_args() 
course = args.course
print(course)
path = args.path

url = f"https://bsw.iitd.ac.in/coursepage.php?course={course}"


def get_all_courses():
    soup = BeautifulSoup(requests.get("https://bsw.iitd.ac.in/question_papers.php", verify=False).text, "html.parser")
    courses = [link.get_text() for link in soup.find_all("a", class_="list-group-item")]
    return courses

def check_valid_course(course):
    return course in get_all_courses()


if not check_valid_course(course):
    print("Invalid Course")
    exit()
    

soup = BeautifulSoup(requests.get(url, verify=False).text, "html.parser")

resources = soup.find_all("a", class_="list-group-item")

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
https_handler = urllib.request.HTTPSHandler(context=ssl_context)
opener = urllib.request.build_opener(https_handler)
urllib.request.install_opener(opener)


try:
    os.makedirs(os.path.join(path, course))
except OSError as e:
    print(f"Error creating folder: {e}")
    exit()

for resource in resources:
    resource_url = f"https://bsw.iitd.ac.in/{resource.get('href')}"
    semester = resource.get_text()
    exam_type = resource_url.split("/")[-2]
    os.makedirs(os.path.join(path, course, semester), exist_ok=True)
    local_file_path = os.path.join(path, course, semester, resource_url.split("/")[-1])
    urllib.request.urlretrieve(resource_url, local_file_path)