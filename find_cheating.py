'''
    Author: Heng-Jui Chang
'''

import os
import argparse
import json
from pathlib import Path
from collect_score import get_student_id


def get_student_submissions(path):
    with open(path, 'r') as fp:
        subm_list = json.load(fp)
        scores = []
        for subm in subm_list:
            if subm['publicScore'] is None or subm['publicScore'] is None:
                continue
            publ_score = subm['publicScore'].ljust(8, '0')
            priv_score = subm['privateScore'].ljust(8, '0')
            scores.append('{}-{}'.format(publ_score, priv_score))
        scores = list(set(scores))
        return scores


def get_all_scores(args):
    all_json_files = list(Path(args.dir).rglob("*.json"))
    score_dict = {}
    for json_file in all_json_files:
        team_id = str(json_file).split('/')[-1].split('.')[0]
        scores = get_student_submissions(json_file)
        for s in scores:
            if score_dict.get(s, None):
                score_dict[s].append(team_id)
            else:
                score_dict[s] = [team_id]
    return score_dict


def find_same(args, score_dict):
    with open(args.id2n, 'r') as fp:
        teamid2name = json.load(fp)

    cheat_list = []
    for key in score_dict:
        if len(score_dict[key]) > 1:
            team_names = [teamid2name[idx] for idx in score_dict[key]]
            contain_student = len(''.join([get_student_id(n) for n in team_names])) > 0
            if contain_student:
                cheat_list.append('{} : {}\n'.format(key, ', '.join(team_names)))
    cheat_list = sorted(cheat_list, reverse=args.descending)
    with open(args.output, 'w') as fp:
        fp.writelines(cheat_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find potential cheatings.')
    parser.add_argument(
        '--dir', type=str, help='Directory of all .json files.')
    parser.add_argument(
        '--id2n', type=str, help='Team ID to name conversion .json file.')
    parser.add_argument(
        '--output', type=str, help='Output file.')
    parser.add_argument(
        '--descending', action='store_true', help='List scores in ascending order.')
    args = parser.parse_args()

    score_dict = get_all_scores(args)
    find_same(args, score_dict)
