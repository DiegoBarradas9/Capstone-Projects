from ..paramcheck import basicParamFileCheck, basicParamFormCheck

def requirementsParamCheck():
  missingParams = basicParamFileCheck([
    "medCert",
    "waiver",
  ])

  missingParams += basicParamFormCheck([
    "fullname",
    "email",
    "srcode",
    "age",
    "birthday",
    "sex",
  ])

  if (len(missingParams) > 0):
    return ({
      "fieldError": missingParams,
      "message": "Missing required fields"
    }, 400)
