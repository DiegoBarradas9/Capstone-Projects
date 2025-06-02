from flask import request
from ..models.ExternalEventModel import ExternalEventModel
from ..models.InternalEventModel import InternalEventModel
from ..models.MembershipModel import MembershipModel
from ..models.AccountModel import AccountModel
from ..models.RequirementsModel import RequirementsModel
from ..models.EvaluationModel import EvaluationModel

from datetime import datetime

'''
Data needed:
 - total approved events
 - pending events
 - rejected events
 - done events
 - total accounts
 - total pending membership
 - total members
 - total active members
'''

def getSummary():
  externalEvents = ExternalEventModel().getAll()
  internalEvents = InternalEventModel().getAll()
  allMembers = MembershipModel().getAll()
  allAccounts = AccountModel().getAll()

  # event information
  totalApprovedEvents = 0
  pendingEvents = 0
  rejectedEvents = 0
  implementedEvent = 0

  # members information
  totalMembers = 0
  totalPendingMembers = 0
  totalActiveMembers = 0

  # already summarized
  totalAccounts = len(allAccounts)

  # convert current time to milliseconds format
  currentTime = int(datetime.now().timestamp()) * 1000

  # external event data extraction
  for external in externalEvents:
    if (external["status"] == "editing"):
      continue

    if (external["status"] == "accepted"):
      totalApprovedEvents += 1
    elif (external["status"] == "submitted"):
      pendingEvents += 1
    else:
      rejectedEvents += 1

    if (external["status"] == "accepted" and (external["durationEnd"] - currentTime) < 0):
      implementedEvent += 1

  # internal event data extraction
  for internal in internalEvents:
    if (internal["status"] == "editing"):
      continue

    if (internal["status"] == "accepted"):
      totalApprovedEvents += 1
    elif (internal["status"] == "submitted"):
      pendingEvents += 1
    else:
      rejectedEvents += 1

    if (internal["status"] == "accepted" and (internal["durationEnd"] - currentTime) < 0):
      implementedEvent += 1

  # membership data extraction
  for member in allMembers:
    if (member["accepted"] == 1):
      totalMembers += 1
    elif (member["accepted"] == None):
      totalPendingMembers += 1

    if (member["accepted"] == 1 and member["active"] == 1):
      totalActiveMembers += 1

  return {
    "data": {
      "totalApprovedEvents": totalApprovedEvents,
      "pendingEvents": pendingEvents,
      "rejectedEvents": rejectedEvents,
      "implementedEvent": implementedEvent,
      "totalMembers": totalMembers,
      "totalPendingMembers": totalPendingMembers,
      "totalActiveMembers": totalActiveMembers,
      "totalAccounts": totalAccounts
    },
    "message": "Successfully retrieved system summary"
  }

def getAnalytics():
  allRequirements = RequirementsModel().getAll()
  ageGroup = {}
  sexGroup = {}

  for requirement in allRequirements:
    if (requirement["accepted"] != 1):
      continue

    # calculate age and sex group
    if (ageGroup.get(requirement["age"]) == None):
      ageGroup[requirement["age"]] = 1
    else:
      ageGroup[requirement["age"]] += 1

    if (sexGroup.get(requirement["sex"]) == None):
      sexGroup[requirement["sex"]] = 1
    else:
      sexGroup[requirement["sex"]] += 1

  return {
    "message": "Successfully retrieved analytics",
    "data": {
      "ageGroup": ageGroup,
      "sexGroup": sexGroup
    },
  }

def getEventInformation(eventId: int, eventType: str):
  if (eventType == "external"):
    event = ExternalEventModel().get(eventId)
  else:
    event = InternalEventModel().get(eventId)

  allrequirements = RequirementsModel().getAndSearch(["eventId", "type", "accepted"], [eventId, eventType, 1])
  answered = 0

  for requirement in allrequirements:
    evaluation = EvaluationModel().getAndSearch(["requirementId"], [requirement["id"]])
    if (len(evaluation) > 0): evaluation = evaluation[0]
    if (evaluation["finalized"] and evaluation["recommendations"] != ""):
      answered += 1

  return {
    "data": {
      "event": event,
      "registered": len(allrequirements),
      "attended": answered
    },

    "message": "Successfully retrieved event details"
  }

def getActiveMemberData():
  responseData = {}

  activeMembers = MembershipModel().getAndSearch(["active", "accepted"], [True, True])
  for activeMember in activeMembers:
    userEmailIndicator = activeMember["email"]
    userFullname = activeMember["fullname"]
    matchedRequirements = RequirementsModel().getAndSearch(["email"], [userEmailIndicator])

    responseData[userFullname] = 0

    # for counting the evaluation done by the user
    for requirement in matchedRequirements:
      matchedEvaluation = EvaluationModel().getAndSearch(["requirementId", "finalized"], [requirement["id"], 1])
      if (len(matchedEvaluation) == 0):
        continue

      matchedEvaluation = matchedEvaluation[0]
      if (matchedEvaluation["recommendations"] != ""):
        responseData[userFullname] += 1

  return {
    "data": responseData,
    "message": "Successfully retrieved member details for event participation"
  }