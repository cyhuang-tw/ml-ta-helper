# Machine Learning TA Helper

A simple toolkit for accessing data from Kaggle and post-process for calculating student grades and finding potential cheatings.


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
`<student list>.csv` is required.
```
python3 collect_score.py \
    --public <public leaderboard>.csv \
    --private <private leaderboard>.html \
    --students <student list>.csv \
    --publ-bl <public baselines (from easy to hard)> \
    --priv-bl <private baselines (from easy to hard)> \
    --output <final output file>.csv
```

### Convert to NTU COOL-compatible Files
```
python3 convert_to_ntucool.py \
    --orig-file <original score file (w/ ID)>.csv \
    --id-col <column index of ID> \
    --score-col <column index of scores> \
    --cool-grade <original NTU COOL grade file>.csv \
    --cool-output <output NTU COOL grade file>.csv \
    --title "<title for the new added HW>"
```

### Find Potential Cheatings
```
python3 find_cheating.py \
    --dir kaggle_output/single_student \
    --id2n kaggle_output/id2name.json \
    --output <output file>.txt
```

