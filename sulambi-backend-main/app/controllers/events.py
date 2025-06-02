from ..models.ExternalEventModel import ExternalEventModel
from ..models.InternalEventModel import InternalEventModel
from ..models.ExternalReportModel import ExternalReportModel
from ..models.InternalReportModel import InternalReportModel
from ..models.SignatoriesModel import SignatoriesModel

from ..models.AccountModel import AccountModel
from ..models.RequirementsModel import RequirementsModel
from ..models.EvaluationModel import EvaluationModel

from ..modules.LSIAlgorithm import LSICosineSimilarityMatch

from flask import request, g
from datetime import datetime

ExternalEventDb = ExternalEventModel()
InternalEventDb = InternalEventModel()
ExternalReportDb = ExternalReportModel()
InternalReportDb = InternalReportModel()
RequirementsDb  = RequirementsModel()
SignatoriesDb = SignatoriesModel()
EvaluationDb = EvaluationModel()
AccountDb = AccountModel()

def getAll():
  # manual mapping of user details
  accountSessionInfo = g.get("accountSessionInfo")
  externalEvents = ExternalEventDb.getAll()
  internalEvents = InternalEventDb.getAll()

  combinedEvents = []

  if (accountSessionInfo["accountType"] == "admin"):
    externalEvents = [event for event in externalEvents if event["status"] != "editing"]
    internalEvents = [event for event in internalEvents if event["status"] != "editing"]

  if (accountSessionInfo["accountType"] == "member"):
    timeNow = int(datetime.now().timestamp() * 1000)
    externalEvents = [event for event in externalEvents if event["status"] == "accepted" and event["durationEnd"] - timeNow > 0]
    internalEvents = [event for event in internalEvents if event["status"] == "accepted" and event["durationEnd"] - timeNow > 0]

  # external events formatting
  for i in range(len(externalEvents)):
    externalEvents[i]["createdBy"] = AccountDb.get(externalEvents[i]["createdBy"])
    externalEvents[i]["hasReport"] = len(ExternalReportDb.getAndSearch(["eventId"], [externalEvents[i]["id"]])) > 0
    externalEvents[i]["eventTypeIndicator"] = "external"
    externalEvents[i]["signatoriesId"] = SignatoriesDb.get(externalEvents[i]["signatoriesId"])

  # internal events formatting
  for i in range(len(internalEvents)):
    internalEvents[i]["createdBy"] = AccountDb.get(internalEvents[i]["createdBy"])
    internalEvents[i]["hasReport"] = len(InternalReportDb.getAndSearch(["eventId"], [internalEvents[i]["id"]])) > 0
    internalEvents[i]["eventTypeIndicator"] = "internal"
    internalEvents[i]["signatoriesId"] = SignatoriesDb.get(internalEvents[i]["signatoriesId"])

  # sort combined events
  combinedEvents: list = externalEvents + internalEvents
  combinedEvents.sort(key=lambda x: x["createdAt"], reverse=True)

  return {
    "events": combinedEvents,
    "external": externalEvents,
    "internal": internalEvents,
    "message": "Successfully retrieved all events"
  }

def getOne(id: int, eventType: str):
  if (eventType == "external"):
    return {
      "data": ExternalEventDb.get(id),
      "message": "Successfully retrieved external event"
    }

  if (eventType == "internal"):
    return {
      "data": InternalEventDb.get(id),
      "message": "Successfully retrieved internal event"
    }

def getPublicEvents():
  accountSessionInfo = g.get("accountSessionInfo")
  externalEvents = ExternalEventDb.getAndSearch(["toPublic"], [1])
  internalEvents = InternalEventDb.getAndSearch(["toPublic"], [1])

  filteredExternalEvents = []
  filteredInternalEvents = []

  for event in externalEvents:
    expirationDate = event["durationEnd"]
    timeNow = int(datetime.now().timestamp() * 1000)
    if expirationDate - timeNow < 0:
      continue
    filteredExternalEvents.append(event)

  for event in internalEvents:
    expirationDate = event["durationEnd"]
    timeNow = int(datetime.now().timestamp() * 1000)
    if expirationDate - timeNow < 0:
      continue
    filteredInternalEvents.append(event)

  return {
    "external": filteredExternalEvents,
    "internal": filteredInternalEvents,
    "message": "Successfully retrieved all events"
  }

def getAnalysis(id: int, eventType: str):
  eventDetails = None
  if (eventType == "external"):
    eventDetails = ExternalEventDb.get(id)

  if (eventType == "internal"):
    eventDetails = InternalEventDb.get(id)

  if (eventDetails == None):
    return ({ "message": "Cannot find event specified" }, 404)

  matchedRequirements = RequirementsDb.getAndSearch(["eventId", "type"], [id, eventType])
  if (len(matchedRequirements) == 0):
    return ({ "message": "No Requirements for the specified event found" }, 406)

  textToAnalyze = []
  for requirement in matchedRequirements:
    matchedEvaluation = EvaluationDb.getAndSearch(["requirementId"], [requirement["id"]])
    if (len(matchedEvaluation) == 0):
      continue

    matchedEvaluation = matchedEvaluation[0]
    textToAnalyze.append(matchedEvaluation["recommendations"])

  analysis = LSICosineSimilarityMatch(textToAnalyze)
  normalized = averageAnalysis(analysis)

  return {
    "analysis": normalized,
    "message": "Successfully returned analysis"
  }

def createExternalEvent():
  accountSessionInfo = g.get("accountSessionInfo")
  createdSignatories = SignatoriesDb.create(
    approvedBy="NAME",
    preparedBy="NAME",
    recommendingApproval1="NAME",
    recommendingApproval2="NAME",
    reviewedBy="NAME"
  )

  createdExternalEvent = ExternalEventDb.create(
    request.json["extensionServiceType"],
    request.json["title"],
    request.json["location"],
    request.json["durationStart"],
    request.json["durationEnd"],
    request.json["sdg"],
    request.json["orgInvolved"],
    request.json["programInvolved"],
    request.json["projectLeader"],
    request.json["partners"],
    request.json["beneficiaries"],
    request.json["totalCost"],
    request.json["sourceOfFund"],
    request.json["rationale"],
    request.json["objectives"],
    request.json["expectedOutput"],
    request.json["description"],
    request.json["financialPlan"],
    request.json["dutiesOfPartner"],
    request.json["evaluationMechanicsPlan"],
    request.json["sustainabilityPlan"],
    accountSessionInfo["id"],
    "editing",
    request.json["evaluationSendTime"],
    signatoriesId=createdSignatories["id"],
    externalServiceType=request.json["externalServiceType"] or "[]",
    eventProposalType=request.json["eventProposalType"] or "[]"
  )

  return {
    "data": createdExternalEvent,
    "message": "Successfully created a new external event!"
  }

def createInternalEvent():
  accountSessionInfo = g.get("accountSessionInfo")

  createdSignatories = SignatoriesDb.create(
    approvedBy="NAME",
    preparedBy="NAME",
    recommendingApproval1="NAME",
    recommendingApproval2="NAME",
    reviewedBy="NAME"
  )

  createdInternalEvent = InternalEventDb.create(
    request.json["title"],
    request.json["durationStart"],
    request.json["durationEnd"],
    request.json["venue"],
    request.json["modeOfDelivery"],
    request.json["projectTeam"],
    request.json["partner"],
    request.json["participant"],
    request.json["maleTotal"],
    request.json["femaleTotal"],
    request.json["rationale"],
    request.json["objectives"],
    request.json["description"],
    request.json["workPlan"],
    request.json["financialRequirement"],
    request.json["evaluationMechanicsPlan"],
    request.json["sustainabilityPlan"],
    accountSessionInfo["id"],
    "editing",
    False,
    request.json["evaluationSendTime"],
    createdSignatories["id"],
    eventProposalType=request.json.get("eventProposalType") or "[]"
  )

  return {
    "data": createdInternalEvent,
    "message": "Successfully created a new external event!"
  }

def editExternalEventStatus(id, status: str):
  accountSessionInfo = g.get("accountSessionInfo")
  externalEvent = ExternalEventDb.get(id)

  if (externalEvent == None):
    return ({ "message": "The specified event does not exist" }, 404)

  if (externalEvent["createdBy"] != accountSessionInfo["id"] and status == "submitted"):
    return ({ "message": "You have no permission to submit this event" }, 403)

  ExternalEventDb.updateSpecific(id, ["status"], (status,))
  updatedData = ExternalEventDb.get(id)
  return {
    "data": updatedData,
    "message": "Event successfully submitted"
  }

def editInternalEventStatus(id, status: str):
  accountSessionInfo = g.get("accountSessionInfo")
  internalEvent = InternalEventDb.get(id)

  if (internalEvent == None):
    return ({ "message": "The specified event does not exist" }, 404)

  if (internalEvent["createdBy"] != accountSessionInfo["id"] and status == "submitted"):
    return ({ "message": "You have no permission to submit this event" }, 403)

  InternalEventDb.updateSpecific(id, ["status"], (status,))
  updatedData = InternalEventDb.get(id)
  return {
    "data": updatedData,
    "message": "Event successfully submitted"
  }

def makeEventPublic(id, eventType: str):
  accountSessionInfo = g.get("accountSessionInfo")

  # make external event public
  if (eventType == "external"):
    if (ExternalEventDb.get(id) != None):
      ExternalEventDb.updateSpecific(id, ["toPublic"], (True,))
      return { "message": "Successfully made to public" }
    else:
      return ({ "message": "Specified event ID does not exist" }, 404)

  # make internal event public
  if (eventType == "internal"):
    if (InternalEventDb.get(id) != None):
      InternalEventDb.updateSpecific(id, ["toPublic"], (True,))
      return { "message": "Successfully made to public" }
    else:
      return ({ "message": "Specified event ID does not exist" }, 404)

def updateEvent(id, eventType: str):
  accountSessionInfo = g.get("accountSessionInfo")

  if (eventType == "internal"):
      matchedEvent = InternalEventDb.get(id)
      if (matchedEvent == None): return ({
        "message": "Internal Event provided does not exist"
      }, 404)

      updatedEvent = InternalEventDb.update(id, (
        request.json["title"],
        request.json["durationStart"],
        request.json["durationEnd"],
        request.json["venue"],
        request.json["modeOfDelivery"],
        request.json["projectTeam"],
        request.json["partner"],
        request.json["participant"],
        request.json["maleTotal"],
        request.json["femaleTotal"],
        request.json["rationale"],
        request.json["objectives"],
        request.json["description"],
        request.json["workPlan"],
        request.json["financialRequirement"],
        request.json["evaluationMechanicsPlan"],
        request.json["sustainabilityPlan"],
        accountSessionInfo["id"],
        "editing",
        False,
        request.json["evaluationSendTime"],
        matchedEvent.get("signatoriesId"),
        matchedEvent.get("createdAt"),
        matchedEvent.get("feedback_id"),
        request.json.get("eventProposalType") or "[]"
      ))

  if (eventType == "external"):
    matchedEvent = ExternalEventDb.get(id)
    if (matchedEvent == None): return ({
      "message": "External Event provided does not exist"
    }, 404)

    print("created at", matchedEvent.get("createdAt"))

    updatedEvent = ExternalEventDb.update( id, (
      request.json["extensionServiceType"],
      request.json["title"],
      request.json["location"],
      request.json["durationStart"],
      request.json["durationEnd"],
      request.json["sdg"],
      request.json["orgInvolved"],
      request.json["programInvolved"],
      request.json["projectLeader"],
      request.json["partners"],
      request.json["beneficiaries"],
      request.json["totalCost"],
      request.json["sourceOfFund"],
      request.json["rationale"],
      request.json["objectives"],
      request.json["expectedOutput"],
      request.json["description"],
      request.json["financialPlan"],
      request.json["dutiesOfPartner"],
      request.json["evaluationMechanicsPlan"],
      request.json["sustainabilityPlan"],
      accountSessionInfo["id"],
      "editing",
      request.json["evaluationSendTime"],
      False,
      matchedEvent.get("signatoriesId"),
      matchedEvent.get("createdAt"),
      matchedEvent.get("feedback_id"),
      request.json.get("externalServiceType") or "[]",
      request.json.get("eventProposalType") or "[]"
    ))

  return {
    "message": "Successfully updated event",
    "data": updatedEvent
  }

def averageAnalysis(data):
  avg_data = {}
  for key in data:
      for sub_key, value in data[key].items():
          if sub_key not in avg_data:
              avg_data[sub_key] = {"sum": 0, "count": 0}
          avg_data[sub_key]["sum"] += value
          avg_data[sub_key]["count"] += 1

  for sub_key, stats in avg_data.items():
      avg_data[sub_key] = stats["sum"] / stats["count"]

  return avg_data

def normalizeOutput(data):
  total = 0
  data = averageAnalysis(data)
  normalizedValue = {}

  for keys in data:
    total += data[keys]
  for keys in data:
    normalizedValue[keys] = data[keys] / total

  return normalizedValue