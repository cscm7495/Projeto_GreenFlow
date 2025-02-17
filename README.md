

# Data Analysis for a fictional company called GreenFlow

This project is composed of:

- a script called `data_analysis_cleanup_greenflow.py` which works for cleaning the original data, removing duplicates and filling null values. It also provides a summary/overview of the dataset. You can run this script to look at the summary which contains information such as nr. of rows, correlation, mean, std, etc.

## Requirements

- Python 3.x
- pip

## Instructions for running the data_analysis_cleanup_greenflow.py script

### 1. Install dependencies

Execute the command below to install dependencies listed on `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Run the Script Locally

Run the script through a code editor (VSCODE RECOMENDED) or run the following command

```bash
python src/data_analysis_cleanup_greenflow.py
```

## Instructions for running the streamlit app

### Locally
Execute the command below to install dependencies listed on `requirements.txt`, if you haven't already:

```bash
pip install -r requirements.txt
```

### Using Docker
```bash
docker compose up -d
```