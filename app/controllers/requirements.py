from flask import g, request
from ..models.RequirementsModel import RequirementsModel
from ..models.ExternalEventModel import ExternalEventModel
from ..models.InternalEventModel import InternalEventModel
from ..models.EvaluationModel import EvaluationModel
from ..utils.multipartFileWriter import basicFileWriter
from ..modules.CallbackTimer import executeDelayedAction
from ..modules.Mailer import threadedHtmlMailer, htmlMailer

from dotenv import load_dotenv
import os

load_dotenv()

FRONTEND_APP_URL = os.getenv("FRONTEND_APP_URL")

RequirementsDb = RequirementsModel()
ExternalEventDb = ExternalEventModel()
InternalEventDb = InternalEventModel()
EvaluationDb = EvaluationModel()

def getAllRequirements():
  requirements = RequirementsDb.getAll()

  # manual joining of data (this implementation is just restarted, my bad...)
  for index, requirement in enumerate(requirements):
    if (requirements[index]["type"] == "external"):
      requirements[index]["eventId"] = ExternalEventDb.get(requirements[index]["eventId"])
      continue

    if (requirements[index]["type"] == "internal"):
      requirements[index]["eventId"] = InternalEventDb.get(requirements[index]["eventId"])
      continue

  return {
    "message": "Successfully retrieved all requirements",
    "data": requirements
  }

def acceptRequirements(id: int):
  existence = RequirementsDb.get(id)
  if (existence == None):
    return ({"message": "Requirement ID entered does not exist"}, 404)

  # get evaluation send time details to automate mailing
  if (existence["type"] == "external"):
    eventDetails = ExternalEventDb.get(existence["eventId"])
  else:
    eventDetails = InternalEventDb.get(existence["eventId"])

  if (eventDetails == None):
    return ({"message": "An error occured in automating mailing"}, 500)

  # create an evaluation template for user to answer
  createdEval = EvaluationDb.create(id, "", "", "", "", "", False)

  # automated mailing executed
  executeDelayedAction(int(eventDetails["evaluationSendTime"]), lambda: sendRenderedEvaluationMail(
    eventDetails=eventDetails,
    requirementDetails=existence
  ), execAnyway=True)

  RequirementsDb.updateSpecific(id, ["accepted"], (True,))
  updatedData = RequirementsDb.get(id)
  sendAcceptedRequirementsMail(existence, eventDetails)

  return {
    "message": "Successfully accepted requirement",
    "data": updatedData
  }

def rejectRequirements(id: int):
  existence = RequirementsDb.get(id)
  if (existence == None):
    return ({"message": "Requirement ID entered does not exist"}, 404)

  RequirementsDb.updateSpecific(id, ["accepted"], (False,))
  updatedData = RequirementsDb.get(id)

  if (existence["type"] == "external"):
    eventDetails = ExternalEventDb.get(existence["eventId"])
  else:
    eventDetails = InternalEventDb.get(existence["eventId"])

  if (eventDetails == None):
    return ({"message": "An error occured in automating mailing"}, 500)

  sendRejectedRequirementsMail(existence, eventDetails)

  return {
    "message": "Successfully rejected requirement",
    "data": updatedData
  }

def createNewRequirement(eventId: int):
  resultingPaths = basicFileWriter(["medCert", "waiver"])
  matchedUserRequirement = RequirementsDb.getAndSearch(
    ["eventId", "type", "email"],
    [eventId, request.form.get("type") or "external", request.form.get("email")]
  )

  if (len(matchedUserRequirement) > 0):
    return ({ "message": "Your email has already been registered to this event" }, 403)

  createdRequirement = RequirementsDb.create(
    resultingPaths.get("medCert") or "",
    resultingPaths.get("waiver") or "",
    eventId,
    request.form.get("type") or "external",
    request.form.get("curriculum") or "",
    request.form.get("destination") or "",
    request.form.get("firstAid") or "",
    request.form.get("fees") or "",
    request.form.get("personnelInCharge") or "",
    request.form.get("personnelRole") or "",
    request.form.get("fullname") or "",
    request.form.get("email") or "",
    request.form.get("srcode") or "",
    request.form.get("age") or "",
    request.form.get("birthday") or "",
    request.form.get("sex") or "",
    request.form.get("campus") or "",
    request.form.get("collegeDept") or "",
    request.form.get("yrlevelprogram") or "",
    request.form.get("address") or "",
    request.form.get("contactNum") or "",
    request.form.get("fblink") or "",
    None,
    request.form.get("affiliation") or "N/A"
  )

  return {
    "message": "Successfully uploaded requirements",
    "data": createdRequirement
  }

######################
#  Helper Functions  #
######################
def sendRenderedEvaluationMail(requirementDetails: dict, eventDetails: dict):
  templateHtml = open("templates/evaluation-mail-template.html", "r").read()
  templateHtml = templateHtml.replace("[name]", requirementDetails.get("fullname"))
  templateHtml = templateHtml.replace("[token]", requirementDetails.get("id"))
  templateHtml = templateHtml.replace("[event-title]", eventDetails.get("title"))
  templateHtml = templateHtml.replace("[link]", FRONTEND_APP_URL + "/evaluation/" + requirementDetails.get("id"))

  htmlMailer(
    mailTo=requirementDetails.get("email"),
    htmlRendered=templateHtml,
    subject="Evaluation Attendance"
  )

def sendRejectedRequirementsMail(requirementDetails: dict, eventDetails: dict):
  templateHtml = open("templates/we-reject-to-inform-requirements.html", "r").read()
  templateHtml = templateHtml.replace("[name]", requirementDetails.get("fullname"))
  templateHtml = templateHtml.replace("[event]", eventDetails.get("title"))

  threadedHtmlMailer(
    mailTo=requirementDetails.get("email"),
    htmlRendered=templateHtml,
    subject="Requirement Evaluation: Sulambi - VOSA"
  )

def sendAcceptedRequirementsMail(requirementDetails: dict, eventDetails: dict):
  templateHtml = open("templates/we-are-pleased-to-inform-requirements.html", "r").read()
  templateHtml = templateHtml.replace("[name]", requirementDetails.get("fullname"))
  templateHtml = templateHtml.replace("[event]", eventDetails.get("title"))

  threadedHtmlMailer(
    mailTo=requirementDetails.get("email"),
    htmlRendered=templateHtml,
    subject="Requirement Evaluation: Sulambi - VOSA"
  )
