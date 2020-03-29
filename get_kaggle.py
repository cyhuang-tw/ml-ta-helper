import os
import re
import argparse
import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.5f')


parameters = r"""PARAMETERS"""

def get_pages(args):
    os.makedirs(args.page_path, exist_ok=True)
    for i in range(5):
        command = "curl \'{}{}\' {} > {}".format(args.page_prefix, i + 1, parameters, os.path.join(args.page_path, '{}.json'.format(i + 1)))
        os.system(command)

def get_student_data(args):
    os.makedirs(args.single_path, exist_ok=True)
    page_list = os.listdir(args.page_path)
    leaderboard = {}
    pattern = re.compile("^([a-z])\d{2}(\d{1}|[a-z])\d{2}(\d{1}|[a-z])\d{2}$")
    for page_file in page_list:
        with open(os.path.join(args.page_path, page_file), 'r') as f:
            page = json.load(f)
        for team in page['teamsList']:
            team_id = team['id']
            student_id = team['name'].split('_')[0]
            if bool(pattern.match(student_id)):
                leaderboard[student_id] = {'public': float(team['publicScore']), 'private': float(team['privateScore'])}
                command = "curl \'{}{}\' {} > {}".format(args.single_prefix, team_id, parameters, os.path.join(args.single_path, '{}.json'.format(student_id)))
                print(student_id)
                os.system(command)
    with open(os.path.join(args.output_path, 'leaderboard.json'), 'w') as f:
        json.dump(leaderboard, f)

def get_selected_scores(args):
    student_list = os.listdir(args.single_path)
    student_dict = {}
    for student_file in student_list:
        student_id = os.path.splitext(student_file)[0]
        final_submission = []
        with open(os.path.join(args.single_path, student_file), 'r') as f:
            student_data = json.load(f)
        for submission in student_data:
            if submission['isSelected']:
                final_submission.append({'public': float(submission['publicScore']), 'private': float(submission['privateScore'])})

        if len(final_submission) < 2:
            ns_sub = [x for x in student_data if (not x['isSelected']) and (x['status'] != 'error')]
            ns_sub = sorted(ns_sub, key=lambda k: float(k['publicScore']))
            for i in range(min(len(ns_sub), 2 - len(final_submission))):
                final_submission.append({'public': float(ns_sub[i]['publicScore']), 'private': float(ns_sub[i]['privateScore'])})

        assert len(final_submission) <= 2
        student_dict[student_id] = final_submission
    with open(os.path.join(args.output_path, 'submissions.json'), 'w') as f:
        json.dump(student_dict, f)

def main(args):
    get_pages(args)
    get_student_data(args)
    get_selected_scores(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--competition_id', '-c', type=int, default=18455)
    parser.add_argument('--output_path', '-o', type=str, default='kaggle_output')

    args = parser.parse_args()
    args.page_path = os.path.join(args.output_path, 'pages')
    args.single_path = os.path.join(args.output_path, 'single_student')
    args.page_prefix = 'https://www.kaggle.com/c/{}/teams.json?sortBy=rank&filter=_&hideUnrankedTeams=true&page='.format(args.competition_id)
    args.single_prefix = 'https://www.kaggle.com/c/{}/team-submissions.json?teamId='.format(args.competition_id)
    main(args)