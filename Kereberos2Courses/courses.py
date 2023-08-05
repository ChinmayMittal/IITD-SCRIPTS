import json
import argparse

parser = argparse.ArgumentParser(
                    prog='Course Finder',
                    description='Finds the Courses enrolled in given the kereberos',)

parser.add_argument('-k', '--kereberos', type=str, required=True, dest="kereberos")
args = parser.parse_args() 
kereberos = args.kereberos
file_path = "course_lists.json"
with open(file_path, "r") as f:
    course_dict = json.load(f)


for course, students in course_dict.items():
    if kereberos in students:
        print (course)