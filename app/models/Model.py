from ..database import connection
from datetime import datetime

class Model:
  def __init__(self):
    self.table = ""
    self.primaryKey = ""
    self.columns = []
    self.filteredColumns = []
    self.createdAtCol = ""

  def parseResponse(self, response: tuple | None, overwriteColumns=[]):
    if (response == None): return None
    if (len(overwriteColumns) == 0):
      completeColumns = [self.primaryKey] + self.columns
    else:
      completeColumns = overwriteColumns

    if (len(response) != len(completeColumns)):
      raise Exception("Response not equal to specified column(s)")

    singleParsed = {}
    for index, coldata in enumerate(response):
      if (completeColumns[index] in self.filteredColumns):
        singleParsed[completeColumns[index]] = "**redacted**"
        continue

      if (self.createdAtCol != "" and completeColumns[index] == self.createdAtCol):
        if (coldata != None):
          if (isinstance(coldata, int)):
            coldata: datetime = datetime.fromtimestamp(coldata / 10000)
          else:
            coldata: datetime = datetime.strptime(coldata, "%Y-%m-%d %H:%M:%S")
        singleParsed[completeColumns[index]] = int(coldata.timestamp()) * 1000 if coldata else 0
      else:
        singleParsed[completeColumns[index]] = coldata
    return singleParsed

  def parseManyResponse(self, response: list[tuple], overwriteColumns=[]):
    if (len(response) == 0): return []
    manyParsed = []
    for coldata in response:
      manyParsed.append(self.parseResponse(coldata, overwriteColumns))
    return manyParsed

  # gets a single data through the use of the primary key
  def get(self, key):
    conn, cursor = connection.cursorInstance()
    columnQuery = ", ".join([self.primaryKey] + self.columns)
    query = f"SELECT {columnQuery} FROM {self.table} WHERE {self.primaryKey}=?"

    cursor.execute(query, (key, ))
    dbResponse = cursor.fetchone()

    response = self.parseResponse(dbResponse)
    conn.close()
    return response

  # returns all the data in the table
  def getAll(self):
    conn, cursor = connection.cursorInstance()
    columnQuery = ", ".join([self.primaryKey] + self.columns)

    query = f"SELECT {columnQuery} FROM {self.table}"

    cursor.execute(query)
    dbResponse = cursor.fetchall()

    response = self.parseManyResponse(dbResponse)
    conn.close()
    return response

  # gets a specific value by matching its column values
  def getOrSearch(self, columns: list, values: list):
    conn, cursor = connection.cursorInstance()
    columnQuery = ", ".join([self.primaryKey] + self.columns)

    queryFormatter = [f"{col}=?" for col in columns]
    queryFormatter = " OR ".join(queryFormatter)
    query = f"SELECT {columnQuery} FROM {self.table} WHERE {queryFormatter}"

    cursor.execute(query, values)
    dbResponse = cursor.fetchall()

    response = self.parseManyResponse(dbResponse, [self.primaryKey] + self.columns)
    conn.close()
    return response

  # gets a specific value by matching its column values
  def getAndSearch(self, columns: list, values: list):
    conn, cursor = connection.cursorInstance()
    columnQuery = ", ".join([self.primaryKey] + self.columns)

    queryFormatter = [f"{col}=?" for col in columns]
    queryFormatter = " AND ".join(queryFormatter)
    query = f"SELECT {columnQuery} FROM {self.table} WHERE {queryFormatter}"

    cursor.execute(query, values)
    dbResponse = cursor.fetchall()

    response = self.parseManyResponse(dbResponse, [self.primaryKey] + self.columns)
    conn.close()
    return response

  # creates a new data with the provided columns and data value
  def create(self, data: tuple, includePrimaryKey=False):
    conn, cursor = connection.cursorInstance()

    if (includePrimaryKey):
      columnFormatter = ", ".join([self.primaryKey] + self.columns)
      queryFormatter = ", ".join('?' * (len(self.columns) + 1))
    else:
      columnFormatter = ", ".join(self.columns)
      queryFormatter = ", ".join('?' * len(self.columns))

    query = f"INSERT INTO {self.table} ({columnFormatter}) VALUES ({queryFormatter})"
    print(query)
    cursor.execute(query, data)
    conn.commit()

    lastRowId = self.getLastPrimaryKey()
    insertedData = self.get(lastRowId)

    conn.close()
    return insertedData

  # updates the data with the given primary key
  def update(self, key, data: tuple):
    conn, cursor = connection.cursorInstance()
    queryFormatter = [f"{col}=?" for col in self.columns]
    queryFormatter = ", ".join(queryFormatter)

    query = f"UPDATE {self.table} SET {queryFormatter} WHERE {self.primaryKey}=?"
    print("update query: ", query)
    cursor.execute(query, data + (key,))
    conn.commit()

    return self.get(key)

  # updates specific fields only
  def updateSpecific(self, key, fields: list[str], data: tuple):
    conn, cursor = connection.cursorInstance()
    queryFormatter = [f"{col}=?" for col in fields]
    queryFormatter = ", ".join(queryFormatter)

    cursor.execute(f"UPDATE {self.table} SET {queryFormatter} WHERE {self.primaryKey}=?", data + (key,))
    conn.commit()

  # deletes one data
  def delete(self, key):
    conn, cursor = connection.cursorInstance()
    tmpDeleted = self.get(key)

    cursor.execute(f"DELETE FROM {self.table} WHERE {self.primaryKey}=?", (key,))
    conn.commit()
    return tmpDeleted

  # last row primary key
  def getLastPrimaryKey(self, overwritingKey=""):
    if (overwritingKey == ""):
      overwritingKey = self.primaryKey

    conn, cursor = connection.cursorInstance()
    query = f"SELECT {overwritingKey} FROM {self.table} ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    lastPrimary = cursor.fetchone()

    conn.close()
    if (lastPrimary == None): return None
    return lastPrimary[0]
