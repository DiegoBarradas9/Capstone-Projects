from flask import Blueprint, request
from ..middlewares import tokenCheck
from ..controllers import requirements
from ..middlewares.requiredParams import requirementsParams

RequirementsBlueprint = Blueprint('requirements', __name__, url_prefix="/requirements")

@RequirementsBlueprint.get("/")
def getAllRequirementsRoute():
  return requirements.getAllRequirements()

@RequirementsBlueprint.post("/<eventId>")
def uploadRequirementsRoute(eventId):
  return requirements.createNewRequirement(eventId)

@RequirementsBlueprint.patch("/accept/<requirementId>")
def acceptRequirementsRoute(requirementId):
  return requirements.acceptRequirements(requirementId)

@RequirementsBlueprint.patch("/reject/<requirementId>")
def rejectRequirementsRoute(requirementId):
  return requirements.rejectRequirements(requirementId)

@RequirementsBlueprint.before_request
def requirementsMiddleware():
  if (request.method != "OPTIONS"):
    if (request.method not in ["GET", "DELETE", "PATCH"]):
      missingParams = None

      # create request
      if (request.method == "POST" and request.view_args.get("eventId") != None):
        missingParams = requirementsParams.requirementsParamCheck()

      if (missingParams != None):
        return missingParams