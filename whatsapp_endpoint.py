from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import requests
import json
import random
import os
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = "1208269639027754"
RECIPENT_NUMBER=os.getenv("RECIPENT_NUMBER") 

URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

body="Your appointment is confirmed"

class UserDetails(BaseModel):
    Patient_Name: str
    Patient_Age: int
    Gender: str
    Mobile_Number: str
    Appointment_Date: str
    Appointment_Time: str
    Doctor: str
    Department: str
    Branch_Name: str
    Branch_Location: str
    Message_type: int

class lead_summary(BaseModel):
    totalNewLeadsReceived: int
    contactedLeads: int
    convertedToPatients: int
    pendingFollowUps: int
    notInterested: int
    conversionRate: float

class lead_details(BaseModel):
    type: str
    reportDate: str
    hospitalName: str
    branchName: str
    summary: lead_summary

def lead(details: lead_details):
    payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "RECIPENT_NUMBER", 
    "type": "template",
    "template": {
        "name": "lead_generation", 
        "language": {
            "code": "en_US" 
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": f"{details.reportDate}"},  # {{1}} Date
                    {"type": "text", "text": f"{details.summary.totalNewLeadsReceived}"},         # {{2}} Total Leads
                    {"type": "text", "text": f"{details.summary.contactedLeads}"},         # {{3}} Contacted
                    {"type": "text", "text": f"{details.summary.convertedToPatients}"},          # {{4}} Converted
                    {"type": "text", "text": f"{details.summary.pendingFollowUps}"},          # {{5}} Pending
                    {"type": "text", "text": f"{details.summary.notInterested}"},          # {{6}} Not Interested
                    {"type": "text", "text": f"{details.summary.conversionRate}"}        # {{7}} Conversion Rate
                            ]
                        }
                    ]
                }
            }
            
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
        
    if response.status_code == 200:
            print("Message sent successfully!")
            print("Response details:", response.json())
    else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print("Error details:", response.json())
    return response
      

def appointment_confirmed(details: UserDetails):
    confirmation_no=f"{details.Doctor[:3]}{random.randint(100,999)}"
    payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "RECIPENT_NUMBER",
    "type": "template",
    "template": {
        "name": "appointment_confirm", 
        "language": {
            "code": "en_US"
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": details.Patient_Name},              
                    {"type": "text", "text": f"{details.Appointment_Date} at {details.Appointment_Time}"},
                    {"type": "text", "text": f"Appoint with {details.Doctor}"},            
                    {"type": "text", "text": confirmation_no}               
                        ]
                    }
                ]
            }
        }
 
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
        
    if response.status_code == 200:
            print("Message sent successfully!")
            print("Response details:", response.json())
    else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print("Error details:", response.json())
    return response

def appointment_cancelled(details: UserDetails):
    payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "RECIPENT_NUMBER",
    "type": "template",
    "template": {
        "name": "cancel_appointment", 
        "language": {
            "code": "en_US"
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": details.Patient_Name},           
                    {"type": "text", "text": details.Doctor},  
                    {"type": "text", "text": details.Appointment_Date},
                    {"type": "text", "text": details.Appointment_Time} 
                ]
            }
        ]
        }
        }
 
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
        
    if response.status_code == 200:
            print("Message sent successfully!")
            print("Response details:", response.json())
    else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print("Error details:", response.json())
    return response

def appointment_reschedule(details: UserDetails):
    confirmation_no=f"{details.Doctor[:3]}{random.randint(100,999)}"
    payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "RECIPENT_NUMBER",
    "type": "template",
    "template": {
        "name": "reschedule_appointment", 
        "language": {
            "code": "en_US"
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": details.Patient_Name},               
                    {"type": "text", "text": f"{details.Appointment_Date} at {details.Appointment_Time}"},
                    {"type": "text", "text": f"Appoint with {details.Doctor}"},          
                    {"type": "text", "text": confirmation_no}               
                        ]
                    }
                ]
            }
        }
 
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
        
    if response.status_code == 200:
            print("Message sent successfully!")
            print("Response details:", response.json())
    else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print("Error details:", response.json())
    return response


app=FastAPI()

@app.post('/send_message')
def message(details: UserDetails):
    print(details)
    type=details.Message_type
    response={}
    if(type==1):
        response=appointment_confirmed(details)
    elif(type==2):
          response=appointment_cancelled(details)
    elif(type==3):
          response=appointment_reschedule(details)
    
    
    if response.status_code!=200:
        return {"error" : f"Error occured :\n{response}"}
    else:
        return {"success" : "Successfully sent the message"}
    
@app.post('/lead_generate')
def lead_generate(details: lead_details):
    print(details)
    
    response=lead(details)
    
    
    if response.status_code!=200:
        return {"error" : f"Error occured :\n{response}"}
    else:
        return {"success" : "Successfully sent the message"}
    