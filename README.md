# Assignment-1: TOPSIS 

## 📌 Overview

Decision making often involves evaluating multiple alternatives across several conflicting criteria.  
**TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** is a popular Multi-Criteria Decision Making (MCDM) method that ranks alternatives based on their distance from an ideal best and an ideal worst solution.

This assignment demonstrates the implementation of TOPSIS in Python and delivers the solution through three components:

- **Part-I:** Command-line TOPSIS program  
- **Part-II:** Python package published on PyPI with CLI support  
- **Part-III:** Web-based TOPSIS service with email result delivery  

---

## 🔍 TOPSIS Methodology (High-Level)

The TOPSIS method follows these major steps:

1. Construct the decision matrix  
2. Normalize the decision matrix  
3. Apply user-defined weights  
4. Determine ideal best and ideal worst solutions  
5. Calculate separation measures  
6. Compute TOPSIS score  
7. Rank alternatives  

The alternative with the **highest TOPSIS score** is considered the best choice.

---

# 🧩 Part-I: Command Line TOPSIS Tool

## Description

Part-I implements the TOPSIS algorithm as a Python script that can be executed from the command line.  
It accepts an input dataset, weights, and impacts, and generates a ranked output file.

---

## Command Line Usage

```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputFile>
```

## Parameters

| Parameter     | Format                  | Description                                  |
|---------------|-------------------------|----------------------------------------------|
| InputDataFile | String (file path)      | Path to input CSV file                       |
| Weights       | Comma-separated string  | Weights for each criterion                   |
| Impacts       | Comma-separated string  | `+` for benefit, `-` for cost                |
| OutputFile    | String (file path)      | Path where output CSV will be saved          |

---

## Input File Requirements

- Minimum **3 columns**
- First column must contain alternative names or IDs
- Remaining columns must contain **numeric values only**

---
## Output File

The output CSV contains:

- Original dataset
- **Topsis Score**
- **Rank**

Higher score indicates a better alternative.

---

## Validations Implemented

- Input file existence check
- Minimum column requirement
- Numeric validation of criteria
- Matching count of weights and impacts
- Impact validation (`+` or `-`)

--- 

# 📦 Part-II: Python Package (PyPI)
## Description

In Part-II, the TOPSIS logic is packaged as a reusable Python module and uploaded to PyPI.
Users can install the package using pip and execute TOPSIS directly via CLI.

## Package Details
- Package Name: Topsis-Ishita-102317254
- Version: 1.0.1
- License: MIT

## Installation
```
pip install Topsis-Ishita-102317254
```

## CLI Usage After Installation
```
topsis <InputDataFile> <Weights> <Impacts> <OutputFile>
```


## Example:
```
topsis data.csv "1,1,1,2" "+,+,-,+" result.csv
```
---

# 🌐 Part-III: Web-Based TOPSIS Service
## Description

Part-III provides a Flask-based web application that allows users to perform TOPSIS through a browser interface.
Users upload a dataset, specify weights and impacts, and receive the ranked result via email.

## Web Application Features

- File upload (.csv)
- Input for weights and impacts
- Email address validation
- Automatic TOPSIS computation
- Result delivery via email attachment

## User Interface
<img width="1914" height="977" alt="image" src="https://github.com/user-attachments/assets/0ec4d6f0-92de-4fca-ad28-f110c7bb17df" />

## Output
<img width="1898" height="964" alt="image" src="https://github.com/user-attachments/assets/8a79e982-00ac-4fcd-ad90-fd40a04e5538" />

# ▶ Procedure to Run the Project
## 1️⃣ Clone Repository
```
git clone <repository-url>
cd Assi1_Topsis
```

## 2️⃣ Create Virtual Environment And activate
```
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

## 6️⃣ Setup Environment Variables (Part-III)

 Create a .env file inside web/:
```
MAIL_USER=your_email@gmail.com
MAIL_PASS=your_gmail_app_password
```
## 7️⃣ Run Web Application
```
cd web
python app.py
```





