from ..models.AccountModel import AccountModel
from ..models.MembershipModel import MembershipModel
from ..models.SessionModel import SessionModel
from flask import request

AccountDb = AccountModel()
MembershipDb = MembershipModel()
SessionDb = SessionModel()

def login():
  username = request.json['username']
  password = request.json['password']

  sessionDetails = AccountDb.authenticate(username, password)
  if (sessionDetails == None):
    return ({ "message": "Invalid Credentials" }, 403)

  membershipData = None
  if (sessionDetails["accountType"] == "member"):
    accountData = AccountDb.get(sessionDetails["userid"])
    membershipData = MembershipDb.get(accountData["membershipId"])

  return {
    "message": "Successfully logged in",
    "session": sessionDetails,
    "memberData": membershipData
  }

def logout(usertoken):
  matchedToken = SessionDb.get(usertoken)
  if (matchedToken == None):
    return { "message": "Token does not exist (cannot logout)" }

  result = SessionDb.delete(matchedToken["id"])
  return { "message": "Successfully logged out token" }

def register():
  applyingAs = request.json["applyingAs"]
  volunterismExperience = request.json["volunterismExperience"]
  weekdaysTimeDevotion = request.json["weekdaysTimeDevotion"]
  weekendsTimeDevotion = request.json["weekendsTimeDevotion"]
  fullname = request.json["fullname"]
  email = request.json["email"]
  affiliation = request.json["affiliation"]
  srcode = request.json["srcode"]
  age = request.json["age"]
  birthday = request.json["birthday"]
  sex = request.json["sex"]
  campus = request.json["campus"]
  collegeDept = request.json["collegeDept"]
  yrlevelprogram = request.json["yrlevelprogram"]
  address = request.json["address"]
  contactNum = request.json["contactNum"]
  fblink = request.json["fblink"]
  bloodType = request.json["bloodType"]
  bloodDonation = request.json["bloodDonation"]
  paymentOption = request.json["paymentOption"]
  username = request.json["username"]
  password = request.json["password"]

  # optional fields
  medicalCondition = request.json.get("medicalCondition") or ""
  areasOfInterest = request.json.get("areasOfInterest") or ""
  volunteerExpQ1 = request.json.get("volunteerExpQ1") or ""
  volunteerExpQ2 = request.json.get("volunteerExpQ2") or ""
  volunteerExpProof = request.json.get("volunteerExpProof") or ""
  reasonQ1 = request.json.get("reasonQ1") or ""
  reasonQ2 = request.json.get("reasonQ2") or ""

  # check for existence of member
  memberMatch = MembershipDb.getOrSearch(["username", "email", "srcode"], [username, email, srcode])
  if (len(memberMatch) > 0):
    fieldError = []
    for member in memberMatch:
      if (member["username"] == username and fieldError.count("username") == 0):
        fieldError.append("username")
      if (member["email"] == email and fieldError.count("email") == 0):
        fieldError.append("email")
      if (member["srcode"] == srcode and fieldError.count("email") == 0):
        fieldError.append("srcode")

    return ({
      "message": "Membership for your account already exists",
      "fieldError": fieldError
    }, 400)

  # register membership for approval
  createdMember = MembershipDb.create(
    address=address,
    age=age,
    applyingAs=applyingAs,
    areasOfInterest=areasOfInterest,
    birthday=birthday,
    bloodDonation=bloodDonation,
    bloodType=bloodType,
    campus=campus,
    collegeDept=collegeDept,
    contactNum=contactNum,
    email=email,
    affiliation=affiliation,
    fblink=fblink,
    fullname=fullname,
    medicalCondition=medicalCondition,
    password=password,
    paymentOption=paymentOption,
    reasonQ1=reasonQ1,
    reasonQ2=reasonQ2,
    sex=sex,
    srcode=srcode,
    username=username,
    volunterismExperience=volunterismExperience,
    volunteerExpQ1=volunteerExpQ1,
    volunteerExpQ2=volunteerExpQ2,
    weekdaysTimeDevotion=weekdaysTimeDevotion,
    weekendsTimeDevotion=weekendsTimeDevotion,
    yrlevelprogram=yrlevelprogram,
    volunteerExpProof=volunteerExpProof,
  )

  return {
    "member": createdMember,
    "message": "Member successfully created"
  }