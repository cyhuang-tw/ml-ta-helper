import os
import argparse
import json

parameters = r"""PARAMETERS"""

def get_page(args):
    os.makedirs(args.page_path, exist_ok=True)
    for i in range(10):
        command = "curl \'{}{}\' {} > {}".format(args.page_prefix, i + 1, parameters, os.path.join(args.page_path, '{}.txt'.format(i + 1)))
        os.system(command)

def get_student_data(args):
    os.makedirs(args.single_path, exist_ok=True)
    student_list = os.listdir(args.page_path)
    for list_file in student_list:
        with open(os.path.join(args.page_path, list_file), 'r') as f:
            for line in f:
                index = line.find(args.student_prefix)
                if index != -1:
                    link = 'https://classroom.github.com{}'.format(line[index:index + len(args.student_prefix) + 6])
                    print(link)
                    command = "curl \'{}\' {} > {}".format(link, parameters, os.path.join(args.single_path, '{}.txt'.format(link[-6:])))
                    os.system(command)

def get_commit(args):
    commit_dict = {}
    student_files = os.listdir(args.single_path)
    for student in student_files:
        with open(os.path.join(args.single_path, student), 'r') as f:
            for line in f:
                index = line.find('View Submission')
                if index != -1:
                    tokens = line.split()
                    github_id = '-'.join(tokens[6].split('/')[-3].split('-')[1:])
                    commit = tokens[6].split('/')[-1].replace('\"', '')
                    commit_dict[github_id] = commit
                    print(github_id, commit)
    with open(os.path.join(args.output_path, 'commit.json'), 'w') as f:
        json.dump(commit_dict, f)

def main(args):
    os.makedirs(args.output_path, exist_ok=True)
    get_page(args)
    get_student_data(args)
    get_commit(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hw', type=int, default=1)
    parser.add_argument('--output_path', type=str, default='output')

    args = parser.parse_args()
    args.page_path = os.path.join(args.output_path, 'student_pages')
    args.single_path = os.path.join(args.output_path, 'single_student')
    args.page_prefix = "https://classroom.github.com/classrooms/61244606-ntu-machine-learning-spring-2020/assignments/hw{}?students_page=".format(args.hw)
    args.student_prefix = "/classrooms/61244606-ntu-machine-learning-spring-2020/assignments/hw{}/roster_entries/".format(args.hw)
    main(args)