import os
import json
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src import configData
    
doctorDF = pd.read_csv("data/doctorData.csv")
patientDF = pd.read_csv("data/patientData.csv")

def retriveDocument(query):
    scope = "scope_patient"
    function_description = "The purpose of this function is to retrieve the document based on the user query. it willl cover any queries realted to hospital or policies also for any general questions."
    query_description = "User Query to retrieve document"
    try:
        embeddings =  HuggingFaceEmbeddings(
            model_name=configData['modelName'],
            model_kwargs=configData['modelArgs'],
            encode_kwargs=configData['encodekwargs']
        )
        db = Chroma(persist_directory=configData['vectorDBPath'], embedding_function=embeddings)
        results = db.similarity_search_with_score(query, k=5)
        return str(results)
    except Exception as e:
        return json.dumps({"error": str(e)})
    

def isExistingUser(mobileNumber):
    try:
        scope = "scope_patient"
        function_description = "The purpose of this function is to check is the user is existing patient or not."
        mobileNumber_description = "user mobile number for verification"
        patient_data = patientDF[patientDF["mobilenumber"] == int(mobileNumber)]
        if not patient_data.empty:
            return "existing user"
        else : 
            return "Not an existing user"
    except Exception as e:
        return str(e)

def getDoctor(symptoms):
    try:
        scope = "scope_patient"
        function_description = "The purpose of this function is to get the appropriate doctor based on the user symptoms or medical problem."
        symptoms_description = "User symptoms or medical problem to get the appropriate doctor"
        doctorList  = doctorDF[['doctorName', 'availableDate','availableSlots']]
        return str(doctorList)
    except Exception as e:
        return str(e)

def getPatientDetails(mobileNumber):
    try:
        scope = "scope_patient"
        function_description = "The purpose of this function is to get the patient details like his history of appoinment etc."
        mobileNumber_description = "Patient mobile number to get the patient details"
        patient_data = patientDF[patientDF["mobilenumber"] == int(mobileNumber)]
        return str(patient_data)
    except Exception as e:
        return str(e)
    
def patientmailnotification(mobileNumber, subject, bodyContent):
    try:
        scope = "scope_patient"
        function_description = "The purpose of this function is to send the mail notification to the patient on confirmation on appointment."
        subject_description = "Mail subject to send to the patient"
        bodyContent_description = "Mail body content to send to the patient on confirmation on appointment"
        patient_data = patientDF[patientDF["mobilenumber"] == int(mobileNumber)]
        patientEmail = patient_data["patientEmailID"].values[0]
        msg = MIMEMultipart()
        msg["From"] = os.getenv("sender_email_ID")
        msg["To"] = patientEmail
        msg["Subject"] = subject
        msg.attach(MIMEText(bodyContent, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Use Outlook SMTP if needed
        server.starttls()  # Secure the connection
        server.login(os.getenv("sender_email_ID"), os.getenv("sender_email_password"))
        server.sendmail(os.getenv("sender_email_ID"), patientEmail, msg.as_string())
        server.quit()
        return "Mail sent successfully"
    except Exception as e:
        return str(e)