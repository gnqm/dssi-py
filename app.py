import streamlit as st
from src.inference import get_prediction

#Initialise session state variable
if 'input_features' not in st.session_state:
    st.session_state['input_features'] = {}

def app_sidebar():
    st.sidebar.header('Loan Details')
    emp_length_options = ['< 1 year','1 year','2 years','3 years','4 years','5 years',
                          '6 years','7 years','8 years','9 years','10+ years']
    emp_length = st.sidebar.selectbox("Employment Length", emp_length_options)
    int_rate = st.sidebar.slider('Loan Interest Rate', 5, 40, 10, 1)
    annual_inc = st.sidebar.text_input("Annual Income '000s", placeholder="in '000s")
    fico_range_high = st.sidebar.slider('FICO Upper Boundary', 600, 800, 700, 50)
    loan_amnt = st.sidebar.text_input('Loan Amount')
    def get_input_features():
        input_features = {'emp_length': emp_length,
                          'int_rate': int_rate,
                          'annual_inc': int(annual_inc)*1000,
                          'fico_range_high': fico_range_high,
                          'loan_amnt': int(loan_amnt)
                         }
        return input_features
    sdb_col1, sdb_col2 = st.sidebar.columns(2)
    with sdb_col1:
        predict_button = st.sidebar.button("Assess", key="predict")
    with sdb_col2:
        reset_button = st.sidebar.button("Reset", key="clear")
    if predict_button:
        st.session_state['input_features'] = get_input_features()
    if reset_button:
        st.session_state['input_features'] = {}
    return None

def app_body():
    title = '<p style="font-family:arial, sans-serif; color:Black; font-size: 40px;"><b> Welcome to DSSI Loan Assessment</b></p>'
    st.markdown(title, unsafe_allow_html=True)
    default_msg = '**System assessment says:** {}'
    if st.session_state['input_features']:
        assessment = get_prediction(emp_length=st.session_state['input_features']['emp_length'],
                                    int_rate=st.session_state['input_features']['int_rate'],
                                    annual_inc=st.session_state['input_features']['annual_inc'],
                                    fico_range_high=st.session_state['input_features']['fico_range_high'],
                                    loan_amnt=st.session_state['input_features']['loan_amnt'])
        if assessment.lower() == 'yes':
            st.success(default_msg.format('Approved'))
        else:
            st.warning(default_msg.format('Rejected'))
    return None

def main():
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()