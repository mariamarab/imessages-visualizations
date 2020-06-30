import os
import sys
import sqlite3
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt

SOLIMANS_PHONE_NUMBER = 28196

def macTimeToLocalTime(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000000000 + 978307200))

def localTimeToMacTime(date):
    return ((time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')) - 978307200) * 1000000000)

class Connection:
    def __init__(self, phoneNumber=None):
        username = os.popen('whoami').read().strip()
        self.db = "/Users/{username}/Library/Messages/chat.db".format(
            username=username)
        self.connection = sqlite3.connect(self.db, check_same_thread=False)
        self.phoneNumber = phoneNumber
        # self.handle_id = self.getHandleID()
    
    def validateNumber(self):
        if self.phoneNumber is None:
            raise ValueError("Phone number not provided")
        
    def getHandleID(self):
        self.validateNumber()            
        query = '''
        SELECT ROWID
        FROM handle
        WHERE id LIKE '%{phoneNumber}%
        '''.format(phoneNumber=self.phoneNumber)
        return pd.read_sql_query(query, self.connection)

    def getChats(self):
        self.validateNumber()            
        query = '''
        SELECT * 
        FROM chat 
        WHERE guid LIKE '%{phoneNumber}%'
        '''.format(phoneNumber=self.phoneNumber)
        return pd.read_sql_query(query, self.connection)

    def getMessagesCountOnDate(self, startDate, endDate):
        self.validateNumber()            
        query = '''
        SELECT count(*), messageT.date
        FROM message messageT
        INNER JOIN chat_message_join chatMessageT 
        ON (chatMessageT.chat_id=148 OR chatMessageT.chat_id=377) 
        AND messageT.ROWID=chatMessageT.message_id 
        AND (messageT.date > {startDate} and messageT.date < {endDate}) 
        ORDER BY messageT.date
        '''.format(startDate=startDate, endDate=endDate)
        return pd.read_sql_query(query, self.connection)

c = Connection(SOLIMANS_PHONE_NUMBER)