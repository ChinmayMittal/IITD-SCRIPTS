import json
import argparse
import requests
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

def get_course_links(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    return [link.get("href") for link in soup.find_all("a")]

def get_course_students(course_url, session):
    try:
        response = session.get(course_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing {course_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    return [student.text for student in soup.find_all("td", attrs={"align": "LEFT"})]

def main():
    parser = argparse.ArgumentParser(
        prog='Course Loader',
        description='Loads the courses and students given the semester')
    parser.add_argument('-s', '--semester', type=str, required=False, dest="semester", default="")
    args = parser.parse_args() 
    semester = args.semester

    if semester == "":
        currentYear = datetime.today().year
        currentMonth = datetime.today().month
        semester = f"{str(currentYear)[2:]}{'02' if currentMonth <= 6 else '01'}"

    base_url = "http://ldapweb.iitd.ac.in/LDAP/courses/"
    file_path = "course_lists.json"
    course_dict = {}

    with requests.Session() as session:
        # Bypass SSL verification - Warning
        session.verify = False

        links = get_course_links(base_url + "gpaliases.html", session)
        for link in tqdm(links):
            if semester not in link:
                continue
            course = link.split("-")[1].split(".")[0]
            course_dict[course] = get_course_students(base_url + link, session)

    with open(file_path, 'w') as json_file:
        json.dump(course_dict, json_file, indent=4)

if __name__ == "__main__":
    main()
