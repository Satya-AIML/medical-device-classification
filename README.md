# MEDICAL-DEVICE-CLASSIFICATION

## Overview
This project aims to classify medical devices into four categories using a Fine-tuned BioBERT model. In addition to classification, the project also recommends similar medical devices based on the classification results.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Model](#model)
- [Results](#results)
- [License](#license)

## Installation
To set up the project, follow these steps:

1. Create a Python Environment
   Choose one of the following methods to create a Python environment compatible with the project. 
   If using venv or virtualenv ensure that the Python version is 3.12.7 installed.

   Using Conda
   ```bash
   conda create -n env_name python=3.12.7
   conda activate env_name
   ```

   Using Python's venv

   ```bash
   python3 -m venv env_name
   source env_name/bin/activate  # On Linux/MacOS
   env_name\Scripts\activate     # On Windows
   ```
   
   Using virtualenv
   First, install virtualenv if it’s not already installed:

   ```bash
   pip install virtualenv
   ```
   Then, create and activate the environment:

   ```bash
   virtualenv env_name
   source env_name/bin/activate  # On Linux/MacOS
   env_name\Scripts\activate     # On Windows
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/Satya-AIML/medical-device-classification.git
   cd medical-device-classification

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt

