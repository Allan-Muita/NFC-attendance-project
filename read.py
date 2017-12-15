#!/usr/bin/python
import sys
import time 
import json
import rfidiot
import MySQLdb
import os

try:
        card= rfidiot.card
except:
	print "Couldn't open reader!"
        os._exit(True)

args= rfidiot.args

card.info('cardselect v0.1m')
# force card type if specified
if len(args) == 1:
	card.settagtype(args[0])
else:
	card.settagtype(card.ALL)

if card.select():
	print '    Card ID: ' + card.uid
	if card.readertype == card.READER_PCSC:
		print '    ATR: ' + card.pcsc_atr

# Open database connection
db = MySQLdb.connect("localhost","allan","muriuki1992","nfc" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sqlstmt = "SELECT * FROM students WHERE card_id = %(card_id)s"

try:
   # Execute the SQL command
 cursor.execute(sqlstmt, {'card_id': card.uid})
   # Fetch all the rows in a list of lists.
 results = cursor.fetchall()
 for row in results:
     stud_reg = row[0]
     fname = row[2]
     lname = row[3]
      # Now print fetched result
 #print "fname=%s" % \
       #(fname)
 sqlstmt1 = "SELECT course_reg.unit_code,course_reg.student_reg,units.unit_code,units.description,units.lec_id,units.lec_name FROM course_reg LEFT JOIN units ON course_reg.unit_code=units.unit_code WHERE course_reg.student_reg = %(student_reg)s"
 cursor.execute(sqlstmt1, {'student_reg': stud_reg})                                       
 results1 = cursor.fetchall()
 print "MY COURSES : \n ............."
 for row in results1:
     courses = row[0]
     student_reg = row[2]
     description = row[3]
     
     print (courses), '  ', (stud_reg), '  ', (fname + ' ' + lname),'  ', (description)
except:
 print "Error: unable to fecth data"

# disconnect from server
 db.close()