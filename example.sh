#!/bin/bash

score=hw1_kaggle_score.csv
cheat=hw1_cheat.txt

python3 collect_score.py \
    --public hw1_public.csv \
    --private hw1_private.txt \
    --students ../ML2021_students.csv \
    --publ-bl 2.03004 1.28359 0.88017 \
    --priv-bl 2.04826 1.36937 0.89266 \
    --output ${score}

python3 get_kaggle.py \
    --competition_id ml2021spring-hw1

python3 find_cheating.py \
    --dir kaggle_output/single_student \
    --id2n kaggle_output/id2name.json \
    --output ${cheat}

# python3 convert_to_ntucool.py \
#     --orig-file ML2021_hw1_score_original.csv \
#     --id-col 11 \
#     --score-col 14 \
#     --cool-grade ntucool_20210407.csv \
#     --cool-output ntucool_20210407_hw1.csv \
#     --title "HW01 total score"
