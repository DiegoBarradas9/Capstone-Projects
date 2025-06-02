from flask import request
import json

def basicParamCheck(params: list[str], paramStringify: bool=False):
  requestJson: dict = request.json
  requestParams = list(requestJson.keys())
  missingParams = []

  for requiredParams in params:
    if (requiredParams not in requestParams):
      missingParams.append(requiredParams)
      continue

    if (paramStringify and (
        type(requestJson[requiredParams]) is dict or
        type(requestJson[requiredParams]) is list)):
      requestJson[requiredParams] = json.dumps(requestJson[requiredParams])

  return missingParams

def basicParamFileCheck(params: list[str], paramStringify: bool=False):
  requestJson: dict = request.files
  requestParams = list(requestJson.keys())
  missingParams = []

  for requiredParams in params:
    if (requiredParams not in requestParams):
      missingParams.append(requiredParams)
      continue

    if (paramStringify and (type(requestJson[requiredParams]) is dict or type(requestJson[requiredParams]) is list)):
      requestJson[requiredParams] = json.dumps(requestJson[requiredParams])

  return missingParams

def basicParamFormCheck(params: list[str], paramStringify: bool=False):
  requestJson: dict = request.form
  requestParams = list(requestJson.keys())
  missingParams = []

  for requiredParams in params:
    if (requiredParams not in requestParams):
      missingParams.append(requiredParams)
      continue

    if (requestJson.get(requiredParams) == None or requestJson.get(requiredParams) == ""):
      missingParams.append(requiredParams)
      continue


    if (paramStringify and (type(requestJson[requiredParams]) is dict or type(requestJson[requiredParams]) is list)):
      requestJson[requiredParams] = json.dumps(requestJson[requiredParams])

  return missingParams