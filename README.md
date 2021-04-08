# Machine Learning TA Helper
[![Python version](https://img.shields.io/badge/python-%3E=_3.6-green.svg?style=flat-square)](_blank)

A simple toolkit for accessing data from Kaggle and post-process for calculating student grades and finding potential cheatings 📝🎓.


## Requirements
```
Python 3
```
No extra packages needed.

## Installation
```
git clone https://github.com/cyhuang-tw/ml-ta-helper.git
```

## Usage

### Download Kaggle Leaderboards
* **Public Leaderboard**:  
  Directly dowload the `.csv` file from Kaggle.
* **Private Leaderboard**:  
  Download the whole webpage as a plain text file.


###  Calculate Kaggle Scores
`<student list>.csv` is required, and the columns should be in the order of `index`, `student ID`, `orginal student ID`.
```
python3 collect_score.py \
    --public <public leaderboard>.csv \
    --private <private leaderboard>.html \
    --students <student list>.csv \
    --publ-bl <public baselines (from easy to hard)> \
    --priv-bl <private baselines (from easy to hard)> \
    --output <final output file>.csv
```

### Download Kaggle Submission Records
```
python3 get_kaggle.py \
    --competition_id <competition ID>
```
This step might take some time if there are thousands of teams in the competition.  
The downloaded `.json` files recording the submission of the students are in the directory `kaggle_output/single_student/` while the team ID to team name mapping will be saved in `kaggle_output/id2name.json`.

### Find Potential Cheatings
```
python3 find_cheating.py \
    --dir kaggle_output/single_student \
    --id2n kaggle_output/id2name.json \
    --output <output file>.txt \
    [--descending]
```
The potential cheatings will be stored in a `.txt` file.

### Convert to NTU COOL-compatible Files
Download a fresh copy of the score file from NTU COOL.  
Download a `.csv` file containing the NTU COOL ID and score of each student.
```
python3 convert_to_ntucool.py \
    --orig-file <original score file (w/ ID)>.csv \
    --id-col <column index of ID> \
    --score-col <column index of scores> \
    --cool-grade <original NTU COOL grade file>.csv \
    --cool-output <output NTU COOL grade file>.csv \
    --title "<title for the new added HW>"
```
