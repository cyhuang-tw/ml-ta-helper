'''
    Author: Heng-Jui Chang
'''

import argparse
import csv


def normalize_team_name(team_name):
    ''' Processing team name (trimming long names) '''
    team_name = team_name.strip().strip('\"')
    return team_name[:min(len(team_name), 20)]


def get_student_id(name):
    ''' Parse student ID (you may modify this part to meet your need) '''
    student_id = normalize_team_name(name).split('_')[0].lower()
    if len(student_id) != 9:
        return ''
    alphas = sum([c.isalpha() for c in student_id])
    number = sum([c.isdigit() for c in student_id])
    if alphas + number != 9 or alphas > 2:
        return ''
    return student_id


def single_score_dict(team_name, score, lb='public'):
    return {
        'team_name': normalize_team_name(team_name),
        f'{lb}_score': score
    }


def read_public(path):
    ''' Parse public leaderboard's .csv file '''
    with open(path, 'r') as fp:
        rows = csv.reader(fp)
        data = {}
        students, repeat, invalid, ascending, prev_score = 0, 0, 0, -1, -1
        repeat_id = []
        for i, row in enumerate(rows):
            if i == 0:
                continue
            name = get_student_id(row[1])
            if name == '':
                invalid += 1
                continue
            score = float(row[3])
            if data.get(name, None):
                # For the repeated case, we only get the one with better public score
                repeat += 1
                repeat_id.append(name)
            else:
                data[name] = single_score_dict(row[1], score, 'public')
                students += 1

            if type(ascending) is int:
                if prev_score != -1 and score != prev_score:
                    ascending = score > prev_score
                else:
                    prev_score = score

        print(f'Repeated students: {repeat_id}')
        print(
            f'Public set: {students} students, {repeat} repeated IDs, {invalid} invalid IDs')
        print(f'Ascending = {ascending}')

        return data, students + repeat + invalid, ascending


def read_private(path, data, contestants):
    ''' Parse public leaderboard's .txt/.html file '''
    with open(path, 'r') as fp:
        start = False
        prev_name = ''
        cnt = 0
        for line in fp:
            if cnt == contestants:
                break
            line = line.strip()
            if line[:6] == '#\t△pub':
                start = True
                continue
            elif not start or line == '':
                continue

            if line[0].isdigit():
                cnt += 1
                team_name = normalize_team_name(line.split('\t')[2])
                name = get_student_id(team_name)
                prev_name = name
                if name == '' or data[name]['team_name'] != team_name:
                    prev_name = ''
                    if name != '' and data[name]['team_name'] != team_name:
                        print(data[name]['team_name'] + '\n' + team_name)
                    continue
                data[name]['private_score'] = 0.0
            elif line[0] == '<' and prev_name != '':
                data[name]['private_score'] = float(line.split('\t')[1])
        return data


def read_student_list(path):
    ''' Parse student list from a .csv file 
        format should be <index>,<student ID>,<original ID>
    '''
    with open(path, 'r') as fp:
        rows = csv.reader(fp)
        student_list = []
        for i, row in enumerate(rows):
            if i == 0:
                continue
            student_list.append({
                'index': int(row[0]),
                'ID': row[1],
                'orig_ID': row[2]})
        print(f'Found {len(student_list)} students')
        return student_list


def score(data, student_list, publ_bl, priv_bl, rev=1):
    ''' Calculate students' score '''
    results = []
    for student in student_list:
        sid = student['ID']
        res = [student['index'], student['orig_ID']]
        if data.get(sid, None):
            total_score = 0
            res.append(data[sid]['public_score'])
            for b in publ_bl:
                total_score += int(data[sid]['public_score'] * rev >= b * rev)
            res.append(data[sid]['private_score'])
            for b in priv_bl:
                total_score += int(data[sid]['private_score'] * rev >= b * rev)
            res.append(total_score)
        else:
            res += ['nan', 'nan', 0]
        results.append(res)

    return results


def output_csv(data, path):
    ''' Write Kaggle scores to specified path. '''
    with open(path, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['index', 'ID', 'public_score',
                         'private_score', 'total_score'])
        writer.writerows(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Collect score from Kaggle leaderboards.')
    parser.add_argument(
        '--public', type=str, help='Path to public leaderboard\'s raw file.')
    parser.add_argument(
        '--private', type=str, help='Path to private leaderboard\'s raw file.')
    parser.add_argument(
        '--students', type=str, help='Path to student list.')
    parser.add_argument(
        '--publ-bl', type=float, nargs='+', help='Public baselines (from simple to strong).')
    parser.add_argument(
        '--priv-bl', type=float, nargs='+', help='Private baselines (from simple to strong).')
    parser.add_argument(
        '--output', type=str, default='score.csv', help='Path to save scores.')

    args = parser.parse_args()

    assert len(args.publ_bl) == len(args.priv_bl), \
        (len(args.publ_bl), len(args.priv_bl))

    # Read public/private leaderboards
    data, contestants, ascending = read_public(args.public)
    contestants -= len(args.publ_bl)
    data = read_private(args.private, data, contestants)

    # Read student list
    student_list = read_student_list(args.students)

    # Calculate scores
    results = score(
        data, student_list, args.publ_bl, args.priv_bl, -1 if ascending else 1)

    # Write results to args.output
    output_csv(results, args.output)
