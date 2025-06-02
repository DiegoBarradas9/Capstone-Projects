from ..models.SignatoriesModel import SignatoriesModel
from flask import request

def updateSignatories(id: int):
  currentSignatory = SignatoriesModel().get(id)\

  preparedBy = request.json.get("preparedBy")
  reviewedBy = request.json.get("reviewedBy")
  recommendingApproval1 = request.json.get("recommendingApproval1")
  recommendingApproval2 = request.json.get("recommendingApproval2")
  approvedBy = request.json.get("approvedBy")
  preparedTitle = request.json.get("preparedTitle")
  reviewedTitle = request.json.get("reviewedTitle")
  approvedTitle = request.json.get("approvedTitle")
  recommendingSignatory1 = request.json.get("recommendingSignatory1")
  recommendingSignatory2 = request.json.get("recommendingSignatory2")

  SignatoriesModel().updateSpecific(id,
    [
      "preparedBy",
      "reviewedBy",
      "recommendingApproval1",
      "recommendingApproval2",
      "approvedBy",
      "preparedTitle",
      "reviewedTitle",
      "approvedTitle",
      "recommendingSignatory1",
      "recommendingSignatory2",
    ],
    (
      "" if preparedBy is None else preparedBy,
      "" if reviewedBy is None else reviewedBy,
      "" if recommendingApproval1 is None else recommendingApproval1,
      "" if recommendingApproval2 is None else recommendingApproval2,
      "" if approvedBy is None else approvedBy,

      "" if preparedTitle is None else preparedTitle,
      "" if reviewedTitle is None else reviewedTitle,
      "" if approvedTitle is None else approvedTitle,
      "" if recommendingSignatory1 is None else recommendingSignatory1,
      "" if recommendingSignatory2 is None else recommendingSignatory2,
    )
  )

  return {
    "data": SignatoriesModel().get(id),
    "message": "Successfully updated signatories data"
  }

def getSignatoriesData(id: int):
  matchedSignatory = SignatoriesModel().get(id)
  return matchedSignatory

