from . import connection
from dotenv import load_dotenv
import os

load_dotenv()
DEBUG = os.getenv("DEBUG") == "True"
conn, cursor = connection.cursorInstance()

"""
NOTE: I will not add any relations to tables, but I will be doing these stuffs
on logic-level of the application for faster implementation
"""


####################
#  ACCOUNTS TABLE  #
####################
DEBUG and print("[*] Initializing accounts table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username STRING NOT NULL,
    password STRING NOT NULL,
    accountType STRING NOT NULL,
    membershipId INTEGER,
    active BOOLEAN DEFAULT TRUE
  )
""")

DEBUG and print("Done")

####################
#  SESSIONS TABLE  #
####################
DEBUG and print("[*] Initializing sessions table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token STRING UNIQUE,
    userid INTEGER NOT NULL,
    accountType STRING NOT NULL
  )
""")

DEBUG and print("Done")

######################
#  MEMBERSHIP TABLE  #
######################
DEBUG and print("[*] Initializing membership table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS membership(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applyingAs VARCHAR NOT NULL,
    volunterismExperience BOOLEAN NOT NULL,
    weekdaysTimeDevotion VARCHAR NOT NULL,
    weekendsTimeDevotion VARCHAR NOT NULL,
    areasOfInterest TEXT NOT NULL,

    fullname STRING NOT NULL,
    email STRING NOT NULL,
    affiliation STRING DEFAULT 'N/A',
    srcode STRING NOT NULL,
    age INTEGER NOT NULL,
    birthday STRING NOT NULL,
    sex STRING NOT NULL,
    campus STRING NOT NULL,
    collegeDept STRING NOT NULL,
    yrlevelprogram STRING NOT NULL,
    address TEXT NOT NULL,
    contactNum STRING NOT NULL,
    fblink STRING NOT NULL,
    bloodType VARCHAR NOT NULL,
    bloodDonation STRING NOT NULL,

    medicalCondition TEXT NOT NULL,
    paymentOption TEXT NOT NULL,

    username STRING NOT NULL,
    password STRING NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    accepted BOOLEAN,

    volunteerExpQ1 TEXT,
    volunteerExpQ2 TEXT,
    volunteerExpProof STRING,

    reasonQ1 TEXT,
    reasonQ2 TEXT
  )
""")

DEBUG and print("Done")

########################
#  REQUIREMENTS TABLE  #
########################
# for passing requirements for helpdesk/events
DEBUG and print("[*] Initializing requirements table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS requirements(
    id STRING UNIQUE,
    medCert STRING NOT NULL,
    waiver STRING NOT NULL,
    type STRING NOT NULL,

    eventId INTEGER NOT NULL,
    affiliation STRING DEFAULT 'N/A',
    curriculum STRING,
    destination STRING,
    firstAid STRING,
    fees STRING,
    personnelInCharge STRING,
    personnelRole STRING,

    fullname STRING,
    email STRING,
    srcode STRING,
    age INTEGER,
    birthday STRING,
    sex STRING,
    campus STRING,
    collegeDept STRING,
    yrlevelprogram STRING,
    address TEXT,
    contactNum STRING,
    fblink STRING,

    accepted BOOLEAN
  )
""")

DEBUG and print("Done")

###########################
#  INTERNAL EVENTS TABLE  #
###########################
# for events proposal
DEBUG and print("[*] Initializing internalEvents table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS internalEvents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING NOT NULL,
    durationStart INTEGER NOT NULL,
    durationEnd INTEGER NOT NULL,
    venue STRING NOT NULL,
    modeOfDelivery STRING NOT NULL,
    projectTeam TEXT NOT NULL,
    partner STRING NOT NULL,
    participant STRING NOT NULL,
    maleTotal INTEGER NOT NULL,
    femaleTotal INTEGER NOT NULL,
    rationale TEXT NOT NULL,
    objectives TEXT NOT NULL,
    description TEXT NOT NULL,
    workPlan TEXT NOT NULL,
    financialRequirement TEXT NOT NULL,
    evaluationMechanicsPlan TEXT NOT NULL,
    sustainabilityPlan TEXT NOT NULL,
    createdBy INTEGER NOT NULL,
    status STRING NOT NULL,
    toPublic BOOLEAN NOT NULL,
    evaluationSendTime INTEGER NOT NULL,

    feedback_id INTEGER,
    eventProposalType STRING,
    signatoriesId INTEGER,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
  )
""")

DEBUG and print("Done")

###########################
#  EXTERNAL EVENTS TABLE  #
###########################
# internal events
DEBUG and print("[*] Initializing externalEvents table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS externalEvents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    extensionServiceType STRING NOT NULL,
    title STRING NOT NULL,
    location STRING NOT NULL,
    durationStart INTEGER NOT NULL,
    durationEnd INTEGER NOT NULL,
    sdg STRING NOT NULL,
    orgInvolved STRING NOT NULL,
    programInvolved STRING NOT NULL,
    projectLeader STRING NOT NULL,
    partners STRING NOT NULL,
    beneficiaries STRING NOT NULL,
    totalCost REAL NOT NULL,
    sourceOfFund STRING NOT NULL,
    rationale TEXT NOT NULL,
    objectives TEXT NOT NULL,
    expectedOutput TEXT NOT NULL,
    description TEXT NOT NULL,
    financialPlan TEXT NOT NULL,
    dutiesOfPartner TEXT NOT NULL,
    evaluationMechanicsPlan TEXT NOT NULL,
    sustainabilityPlan TEXT NOT NULL,
    createdBy INTEGER NOT NULL,
    status STRING NOT NULL,
    evaluationSendTime INTEGER NOT NULL,
    toPublic BOOLEAN DEFAULT FALSE,

    feedback_id INTEGER,
    externalServiceType STRING,
    eventProposalType STRING,

    signatoriesId INTEGER,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
  )
""")

DEBUG and print("Done")

###########################
#  EXTERNAL REPORT TABLE  #
###########################
# for external event proposal
DEBUG and print("[*] Initializing externalReport table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS externalReport(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventId INTEGER NOT NULL,
    narrative TEXT NOT NULL,
    photos TEXT NOT NULL,
    signatoriesId INTEGER
  )
""")
DEBUG and print("Done")

###########################
#  INTERNAL REPORT TABLE  #
###########################
# internal events report
DEBUG and print("[*] Initializing internalReport table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS internalReport(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventId INTEGER NOT NULL,
    narrative TEXT NOT NULL,
    budgetUtilized INTEGER NOT NULL,
    budgetUtilizedSrc STRING NOT NULL,
    psAttribution INTEGER NOT NULL,
    psAttributionSrc STRING NOT NULL,
    photos TEXT NOT NULL,
    signatoriesId INTEGER
  )
""")

DEBUG and print("Done")

####################
#  HELPDESK TABLE  #
####################
DEBUG and print("[*] Initializing helpdesk table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS helpdesk(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email STRING NOT NULL,
    nameOfRequestee STRING NOT NULL,
    addressOfRequestee STRING NOT NULL,
    contactOfRequestee STRING NOT NULL,
    fblinkOfRequestee STRING NOT NULL,
    donationType INTEGER NOT NULL,

    nameOfMoneyRecipient STRING NOT NULL,
    addressOfRecipient STRING NOT NULL,
    contactOfRecipient STRING NOT NULL,
    gcashOrBankOfRecipient STRING,
    reason STRING NOT NULL,
    bloodTypeOfRecipient STRING,
    necessaryFiles TEXT NOT NULL,

    donationNeeded TEXT NOT NULL
  )
""")

DEBUG and print("Done")


###########################
#  EVENT EVALUATION FORM  #
###########################
DEBUG and print("[*] Initializing evaluation table...", end="")
conn.execute("""
  CREATE TABLE IF NOT EXISTS evaluation(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criteria TEXT NOT NULL,
    q13 TEXT NOT NULL,
    q14 TEXT NOT NULL,
    comment TEXT NOT NULL,
    recommendations TEXT NOT NULL,
    requirementId TEXT NOT NULL,
    finalized BOOLEAN DEFAULT FALSE
  )
""")

DEBUG and print("Done")

#######################
#  SIGNATORIES TABLE  #
#######################
DEBUG and print("[*] Initializing eventSignatories table...")
conn.execute("""
  CREATE TABLE IF NOT EXISTS eventSignatories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preparedBy STRING DEFAULT "NAME",
    reviewedBy STRING DEFAULT "NAME",
    recommendingApproval1 STRING DEFAULT "NAME",
    recommendingApproval2 STRING DEFAULT "NAME",
    approvedBy STRING DEFAULT "NAME",

    preparedTitle STRING DEFAULT "Asst. Director, GAD Advocacies/GAD Head Secretariat/Coordinator",
    reviewedTitle STRING DEFAULT "Director, Extension Services/Head, Extension Services",
    approvedTitle STRING DEFAILT "Vice President/Vice Chancellor for Research, Development and Extension Services",
    recommendingSignatory1 STRING DEFAULT "Vice President/Vice Chancellor for Research, Development and Extension Services",
    recommendingSignatory2 STRING DEFAULT "Vice President/Vice Chancellor for Administration and Finance"
  )
""")

####################
#  FEEDBACK TABLE  #
####################
DEBUG and print("[*] Initializing feedback table...")
conn.execute("""
  CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    state STRING
  )
""")


# Insert the initial account values here
initialAccounts = [
  ("Admin", "sulambi@2024", "admin"),
  ("Sulambi-Officer", "password@2024", "officer"),
]

# DEBUG and print("[*] Inserting accounts...")
for account in initialAccounts:
  DEBUG and print("[+] Account:", account[0])
  conn.execute("INSERT INTO accounts (username, password, accountType) VALUES (?, ?, ?)", account)

# DEBUG and print("[+] Done")
conn.commit()
conn.close()
