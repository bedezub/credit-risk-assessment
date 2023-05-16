import streamlit as st
import pandas as pd
import joblib
import json

def home():
    data={}
    ## Details Tab:
    st.header("Credit Risk Assessment System")

    #Full Name:
    first,last=st.columns(2)
    first=first.text_input("Enter your First Name:")
    last=last.text_input("Enter your Last Name:")
    data["First Name"]=first
    data["Last Name"]=last

    name=first+" "+last
    data["Full Name"]=name

    ##Age:
    age=st.slider("Enter your Age:",20,60)
    data["Age"]=age

    ##Annual Income:
    ai=st.number_input("Enter your Annual Income:",1000,100000)
    data["Annual Income"]=ai

    ##Home Ownership:
    ho=st.selectbox("What is the type of House Ownership:", ["RENT", "OWN", "MORTGAGE","OTHER"])
    data["Home Ownership"]=ho

    ##Employment Length:
    el=st.number_input("Enter your Work Experience in years:",2,50)
    data["Employment Length"]=el

    ##Loan Intent:
    li=st.selectbox("Why do you want a loan?", ['EDUCATION', 'MEDICAL', 'VENTURE', 'PERSONAL', 'DEBTCONSOLIDATION',
                                                'HOMEIMPROVEMENT'])
    data["Loan Intent"]=li
    ##Loan Grade:
    lg=st.selectbox("Grade of Loan expected?", ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    data["Loan Grade"]=lg

    ## Loan Amount:
    la=st.number_input("Enter your requested amount of loan",5000,1000000)
    data["Loan Amount"]=la

    ## loan_percent_income:
    lpi=st.number_input("Enter your % Income to be used for repaying:",0,100)
    data["Loan Percent Income"]=lpi

    ## cb_person_default_on_file:
    def_his=st.selectbox("Have your ever defaulted?",["Yes","No"]) 
    data["Previous Defaults"]= "Y" if def_his == "Yes" else "N"

    if def_his == "Yes":
    ## cb_person_cred_hist_length:
        n_def=st.slider("Total Number of Defaults:",0,50)
        data["Number of Defaults"]=n_def
    else:
        data["Number of Defaults"] = 0

    ## Make a submit button:
    data_display=json.dumps(data)
    temp=pd.DataFrame(data,index=[0])  ## making a record

    ## Display the input data as a json:
    # if st.button("Display Data",key = 8)==1:
    #     st.write("The data in JSON Format:")
    #     st.write(data_display)        
    #     st.write("\nThe data in Tabular Format:")
    #     st.write(temp)   
 
    ## Display the prediction:
    if st.button("Submit",key = 9)==1:
        ## Order of passing the data into the pipeline:
        cols=[
            'person_age', 'person_income', 'person_emp_length', 'loan_amnt',
            'loan_percent_income', 'cb_person_cred_hist_length',
            'person_home_ownership', 'loan_intent', 'loan_grade',
            'cb_person_default_on_file'
       ]  ## List of columns of the original dataframe
                
        input_data=[
            [
                data["Age"],data["Annual Income"],data["Employment Length"],data["Loan Amount"],
                round(data["Loan Percent Income"]/100,2),data["Number of Defaults"],
                data["Home Ownership"],data["Loan Intent"],data["Loan Grade"],data["Previous Defaults"]
            ]
        ]
        
        pipe=joblib.load('best_pipeline.pkl')  ## Loading the pipeline
        
        input_data=pd.DataFrame(input_data,columns=cols)  ## Converting input into a dataframe with respective columns

        res=pipe.predict(input_data)[0]  ## Predicting the class
        out={1:"The customer is capable of defaulting. \nHence it is risky to provide loan!", 0:"The customer is not defaulting. \nHence it is possible to provide loan!"}
        st.write(f"Based on the details: {out[res]}")

home()
