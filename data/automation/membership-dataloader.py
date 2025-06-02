import requests as re
import pandas as pd
import json

loadData = pd.read_excel("../member-app.xlsx")
# print(list(loadData.columns))
# columns = ['Email Address', "I'm applying as", 'Do you have any prior volunteerism experience?',
# 'How much time can you devote for volunteering activities on weekdays?', 
# 'How much time can you devote for volunteering activities on weekends?',
# 'What areas or interests do you want to volunteer in? Check the area(s) that interest you. ',
# '1. What volunteering activities of Sulambi VOSA last Academic Year did you join?',
# '2. What volunteering activities did you join outside Sulambi VOSA and/or the University?',
# '2.1 Upload proof for the volunteering activities you joined outside(e.g. Pictures, Certificate)',
# 'Why do you want to become a member?', 'What can you contribute to the organization?',
# 'Name (Last Name, First Name, Middle Initial)', 'Gsuite Email', 'Sr-Code', 'Age', 'Birthday', 'Sex', 'Campus', 'College/Department',
# 'Year Level & Program', 'Address', 'Contact Number', 'Facebook Link', 'Blood Type', 'Blood Donation',
# 'Do you have any existing medical condition/s? If yes, please specify. If none, type N/A.',
# 'Payment Options', 'What areas or interests do you want to volunteer in? Check the area(s) that interest you.']
# Outreach (Medical mission, Dental mission, Optical mission, Blood donation, Visit to orphanages, Visit to prison camps, Visit to rehabilitation center, Relief operation, Gift-giving activity, Sports and Recreation)
# dataFormat = {
#   "applyyingAs",
#   "volunterismExperience",
#   "weekdaysTimeDevotion",
#   "weekendsTimeDevotion",
#   "fullname",
#   "email",
#   "affiliation",
#   "srcode",
#   "age",
#   "birthday",
#   "sex",
#   "campus",
#   "collegeDept",
#   "yrlevelprogram",
#   "address",
#   "contactNum",
#   "fblink",
#   "bloodType",
#   "bloodDonation",
#   "paymentOption",
#   "username",
#   "areasOfInterest",
#   "password"
# }

API_ENDPOINT = "http://localhost:8000/api/auth/register"

def insertData(data):
  response = re.post(API_ENDPOINT, json=data, headers={'Content-Type': 'application/json'})
  if (response.status_code != 200):
    print("[Response] Status Code: ", response.status_code)
    print("[Response] Raw Response: ", response.text)

for index, data in loadData.iterrows():
  if (index == 0): continue
  areaOfInterest = data["What areas or interests do you want to volunteer in? Check the area(s) that interest you. "]

  dataFormat = {
    "applyingAs": data["I'm applying as"],
    "volunterismExperience": data["Do you have any prior volunteerism experience?"].lower(),
    "weekdaysTimeDevotion": data["How much time can you devote for volunteering activities on weekdays?"],
    "weekendsTimeDevotion": data["How much time can you devote for volunteering activities on weekends?"],
    "fullname": data["Name (Last Name, First Name, Middle Initial)"],
    "email": data["Email Address"],
    "affiliation": "Batangas State University",
    "srcode": data["Sr-Code"],
    "age": data["Age"],
    "birthday": data["Birthday"] if type(data["Birthday"]) is str else data["Birthday"].strftime("%B, %d %Y"),
    "sex": data["Sex"],
    "campus": data["Campus"],
    "collegeDept": data["College/Department"],
    "yrlevelprogram": data["Year Level & Program"],
    "address": data["Address"],
    "contactNum": data["Contact Number"],
    "fblink": data["Facebook Link"],
    "bloodType": data["Blood Type"],
    "bloodDonation": data["Blood Donation"],
    "paymentOption": data["Payment Options"],
    "username": data["Name (Last Name, First Name, Middle Initial)"].split(" ")[0].replace(" ", "").replace(",", "") + str(index),
    "areasOfInterest": json.dumps(areaOfInterest.split(", ") if type(areaOfInterest) is str else []),
    "password": "password"
  }

  # print("[+] Registering: ", dataFormat["username"], ":", dataFormat["password"])
  insertData(dataFormat)