## Data Product Development and Deployment with Streamlit
### Requirements
1. Setup Github account
2. Create virtual environment
```
python -m venv venv
```
3. Activate virtual environment
* Windows
```
venv\Scripts\activate
```
* Linux/MacOS
```
source venv/bin/activate
```
4. Install required packages:
```
pip install -r requirements.txt
```
### Prelude: Try Streamlit
1. Create toy application with Streamlit.
2. Push repository to GitHub.
3. Deploy on Streamlit community cloud.  

Sample application code: [toy-app.py](https://github.com/NUS-ISS-DS/dssi-streamlit/blob/main/toy-app.py)
### Step 1: Train and Save Model
1. Perform EDA and model development on Jupyter notebook.
2. Develop training and model registry scripts to automate model training and persistance respectively.
3. Run the training script to train a loan approval model:
```
python src/training.py --data_path data/loan_dataset.csv --model_path models/ --f1_criteria 0.6
```
Sample model training notebook: [DSSI_LoanModel.ipynb](https://github.com/NUS-ISS-DS/dssi-streamlit/blob/main/notebooks/DSSl_LoanModel.ipynb)  
Sample training script: [training.py](https://github.com/NUS-ISS-DS/dssi-streamlit/blob/main/src/training.py)  
Sample model registry script: [model_registry.py](https://github.com/NUS-ISS-DS/dssi-streamlit/blob/main/src/model_registry.py)
### Step 2: Create App and Load Model
1. Develop an inference script to serve predictions.
2. Create a loan approval application with Streamlit that automates decisions with user inputs and trained model.  

Sample inference script: [inference.py](https://github.com/NUS-ISS-DS/dssi-streamlit/blob/main/src/inference.py)  
Sample application code: [app.py](https://github.com/NUS-ISS-DS/dssi-streamlit/blob/main/app.py)
### Step 3: Test App Locally
Run and test the application locally:
```
streamlit run app.py
```
### Step 4: Deploy App Online
1. Commit repository to GitHub.
2. Deploy on Streamlit community cloud.