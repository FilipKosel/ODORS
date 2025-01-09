## IMPORTS

import serial	# Needed to interface with Arduino
from serial import Serial

import time		# Used only if sleep command is needed for delays
import datetime	# Used to track date/time of readings
from datetime import datetime

import csv		# Used to write data; could be replaced with read() and write() commands to reduce needed modules


runAgain = "Y"						# Run code again for next subject
fileCorrect = "N"					# Confirm if file naming is correct
fileName = "OHD_Generic_File.csv"	# Fallback/default output filename

sesType = "NA"			# Session type (habituation or testing session)
sesNum = 0				# Session number (for repeated testing)
subNum = 0				# Subject ID number
subIncrement = "NA"		# Automatically increment subject number by 1 when running code again

runExp = "N"	# Temporarily holds script until recording is initiated

print('\n\n')	# Adds line breaks


while sesType not in ("ses", "hab"):	# Set session type
	try:
		sesType = input("Are you testing or habituating today? ('ses' or ENTER for testing, 'hab' for habituation, CTRL+C to exit) ") or "ses"
		print("You have indicated: " + sesType)
		print()

	except KeyboardInterrupt:
		print("Exiting program.")
		print()
		exit()

	except:
		print("ERROR in sesType - Exiting program")
		print()
		exit()


print("The session number is used for repeated testing.")

while sesNum < 1:	# Set session number
	try:
		sesNum = "% s" % sesNum
		sesNum = input("Which session is this? Enter a number (default is 1) or CTRL+C to exit. ") or "1"
		print("You have indicated: " + sesNum)
		print()

		if sesNum == "TEST":
			break

		sesNum = int(sesNum)

	except ValueError:
		print("Please enter a number for the session ID, or press ENTER to default to 1.")
		sesNum = 0

	except KeyboardInterrupt:
		print("Exiting program.")
		print()
		exit()

	except:
		print("ERROR in sesNum - Exiting program.")
		print()
		exit()
		

print("Subject numbers can be incremented by 1 (e.g., 1, 2, 3...) automatically during testing.")

while subIncrement not in ("Y", "y", "YES", "Yes", "yes", "N", "n", "NO", "No", "no"):	# Increment subject number for subsequent runs after ending script?
	try:
		subIncrement = input("Would you like to automatically increment subject number after each testing session? ('N' or ENTER to manually enter subject numbers, 'Y' to automatically increment, CTRL+C to exit) ") or "N"
		print("You have indicated: " + subIncrement)
		print()

	except KeyboardInterrupt:
		print("Exiting program.")
		print()
		exit()

	except:
		print("ERROR in subIncrement - Exiting program")
		print()
		exit()
		
		
# Script runs from here down
while runAgain in ("Y", "y", "YES", "Yes", "yes"):
	try:
		#print(runAgain)
		
		if subNum != "TEST":	# Check for subject number or "TEST" (for debugging)
			while subNum < 1:
				try:
					subNum = "% s" % subNum
					subNum = input("What is the ID number of the subject you are testing? Enter a number (default is 1) or CTRL+C to exit. ") or "1"
					print("You have indicated: " + subNum)
					print()

					if subNum == "TEST":
						break

					subNum = int(subNum)

				except ValueError:
					print("Please enter the numerical subject ID of the subject being tested, or press ENTER to default to 1.")
					subNum = 0

				except KeyboardInterrupt:
					print("Exiting program.")
					print()
					exit()

				except:
					print("ERROR in subNum - Exiting program.")
					print()
					exit()
		
		
		# Set filename based on subject and session numbers
		fileSub = "% s" % subNum
		fileSes = "% s" % sesNum

		if sesType == "ses":	# Testing or habituation session?
			#print(sesType)
			print("You are currently running subject " + fileSub + ", session " + fileSes + ".")

			if subNum == "TEST":
				fileName = "OHD_subTESTses" + fileSes + ".csv"
			if subNum < 10:
				fileName = "OHD_sub0" + fileSub + "ses" + fileSes + ".csv"
			else:
				fileName = "OHD_sub" + fileSub + "ses" + fileSes + ".csv"

		else:
			print("You are currently running subject " + fileSub + ", habituation " + fileSes + ".")

			if subNum == "TEST":
				fileName = "OHD_subTESThab" + fileSes + ".csv"
			if subNum < 10:
				fileName = "OHD_sub0" + fileSub + "hab" + fileSes + ".csv"
			else:
				fileName = "OHD_sub" + fileSub + "hab" + fileSes + ".csv"

		print("This recording will be saved as " + fileName) # Confirm filename
		fileCorrect = input("Is this correct? 'Y' or ENTER for yes, 'N' for no, CTRL+C to exit. ") or "Y"
		print()


		if fileCorrect not in ("Y", "y", "YES", "Yes", "yes"):
			print("You have indicated that the above is not correct.")
			print("What would you like to change?")

		while fileCorrect not in ("Y", "y", "YES", "Yes", "yes"):	# Change values if filename not correct
			try:
				print("1 - Subject ID number")
				print("2 - Session type (ses or hab)")
				print("3 - Session number")
				print("Y - All correct; continue")
				fileCorrect = input("Please enter a number, 'Y' or ENTER to continue, or CTRL+C to exit. ") or "Y"

				if fileCorrect == "1":
					subNum = 0
					while subNum < 1:
						try:
							subNum = "% s" % subNum
							subNum = input("What is the ID number of the next subject? ") or "1"

							if subNum == "TEST":
								break

							subNum = int(subNum)

						except ValueError:
							print("Please enter the numerical subject ID of the first subject being tested, or press ENTER to default to 1.")
							subNum = 0

						except KeyboardInterrupt:
							print("Exiting program.")
							print()
							exit()

						except:
							print("ERROR in fileCorrect == 1 - Exiting program.")
							print()
							exit()

				elif fileCorrect == "2":
					sesType = "NA"
					while sesType not in ("ses", "hab"):
						try:
							sesType = input("Is this a testing (ses)sion or (hab)ituation session? Please enter 'ses' or ENTER for testing, 'hab' for habituation, or CTRL+C to exit. ") or "ses"

						except KeyboardInterrupt:
							print("Exiting program.")
							print()
							exit()

						except:
							print("ERROR in fileCorrect == 2 - Exiting program.")
							print()
							exit()

				elif fileCorrect == "3":
					sesNum = 0
					while sesNum < 1:
						try:
							sesNum = "% s" % sesNum
							sesNum = input("Which session is this? ") or "1"

							if sesNum == "TEST":
								break

							sesNum = int(sesNum)

						except ValueError:
							print("Please enter the session number, or press ENTER to default to 1.")
							subNum = 0

						except KeyboardInterrupt:
							print("Exiting program.")
							print()
							exit()

						except:
							print("ERROR in fileCorrect == 3 - Exiting program.")
							print()
							exit()

				elif fileCorrect in ("Y", "y", "YES", "Yes", "yes"):
					break

				else:
					print("You have entered an invalid option.")
					print()


				if sesType == "ses":
					print("You are currently running subject " + "% s" % subNum + ", session " + "% s" % sesNum + ".")

					if subNum == "TEST":
						fileName = "OHD_subTESTses" + "% s" % sesNum + ".csv"
					if subNum < 10:
						fileName = "OHD_sub0" + "% s" % subNum + "ses" + "% s" % sesNum + ".csv"
					else:
						fileName = "OHD_sub" + "% s" % subNum + "ses" + "% s" % sesNum + ".csv"

				else:
					print("You are currently running subject " + "% s" % subNum + ", habituation" + "% s" % sesNum + ".")

					if subNum == "TEST":
						fileName = "OHD_subTESTses" + "% s" % habNum + ".csv"
					if subNum < 10:
						fileName = "OHD_sub0" + "% s" % subNum + "hab" + "% s" % sesNum + ".csv"
					else:
						fileName = "OHD_sub" + "% s" % subNum + "hab" + "% s" % sesNum + ".csv"

				print()
				print("This file will be saved as: " + fileName)
				fileCorrect = input("Is this correct? ('Y' or ENTER to continue, 'N' to re-enter information, or CTRL+C to exit) ") or "Y"
				print()

			except KeyboardInterrupt:
				print("Exiting program.")
				print()
				exit()

			except:
				print("ERROR in fileCorrect - Exiting program.")
				print()
				exit()


		runExp = "N"

		print()

		while runExp not in ("Y", "y", "YES", "Yes", "yes"):	# Temporarily hold script until initiated
			try:
				print()
				runExp = input("Start recording? 'Y' or ENTER to continue, CTRL+C to exit. ") or "Y"

			except KeyboardInterrupt:
				print("Exiting program.")
				print()
				exit()

			except:
				print("ERROR in runExp - Exiting program.")
				print()
				exit()

		print("Data will be saved in " + fileName)
		print("Data recording will commence momentarily.")
		print()
			
		data_out = open(fileName, "a")

		writer = csv.writer(data_out, delimiter = ",")	# Create file or append to existing file
        writer.writerow(["DateTime", "A_Baseline", "A_tVOC", "B_Baseline", "B_tVOC", "Valve", "Runtime1", "Runtime2", "Runtime3") # Column names for csv file
		#writer.writerow(["START", "START", "START", "START", "START", "START", "START", "START", "START"]) # Alternative code to indicate start of session instead of column names if appending to existing file



		#time.sleep(1)

		arduinoInput = "0"
		#runExp = "0"
		expStart = 0

		ser_A_base = "NA"	# Serial input: VOC Sensor A baseline
		ser_A_tVOC = "NA"	# Serial input: VOC Sensor A relative total VOC
		ser_B_base = "NA"	# Serial input: VOC Sensor B baseline (if attached)
		ser_B_tVOC = "NA"	# Serial input: VOC Sensor B relative total VOC (if attached)
		ser_stim = "NA"		# Serial input: Stimulus
		ser_msec1 = "NA"	# Serial input: First runtime reading (start of Arduino cycle)
		ser_msec2 = "NA"	# Serial input: Second runtime reading (after sensor readings)
		ser_msec3 = "NA"	# Serial input: Third runtime reading (after valve trigger readings)


		ser = serial.Serial('COM8', 115200)	# Set serial port for Arduino

		# Flush Arduino inputs/outputs and initiate connection
		ser.flush()
		ser.flushInput()
		ser.flushOutput()

		while arduinoInput not in ("1", "2"):	# Wait for Arduino to initialize
			try:
				arduinoInput = ser.readline().decode("utf-8").rstrip()
				#print(arduinoInput)
				print("Initializing...")
				print()

			except KeyboardInterrupt:
				print("Exiting program.")
				print()
				writer.writerow(["END", "END", "END", "END", "END", "END", "END", "END", "END"])
				data_out.close()
				ser.flush()
				ser.flushInput()
				ser.flushOutput()
				ser.close()
				exit()

			except:
				print("ERROR - Failed before sensor ready. Exiting program.")
				print()
				writer.writerow(["ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"])
				data_out.close()
				ser.flush()
				ser.flushInput()
				ser.flushOutput()
				ser.close()
				exit()

		while arduinoInput != "2":
			try:
				arduinoInput = ser.readline().decode("utf-8").rstrip()
				#print(arduinoInput)
				print("Waiting to start...")
				print()

			except KeyboardInterrupt:
				print("Exiting program.")
				print()
				writer.writerow(["END", "END", "END", "END", "END", "END", "END", "END", "END"])
				data_out.close()
				ser.flush()
				ser.flushInput()
				ser.flushOutput()
				ser.close()
				exit()

			except:
				print("ERROR - Failed before experiment started. Exiting program.")
				print()
				writer.writerow(["ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"])
				data_out.close()
				ser.flush()
				ser.flushInput()
				ser.flushOutput()
				ser.close()
				exit()

		# Flush Arduino inputs/outputs to start collecting data only at start
		ser.flush()
		ser.flushInput()
		ser.flushOutput()
		
		print("Experiment started.")
		print()

		while True:	# Repeat until KeyboardInterrupt or Exception thrown
			try:
				
				# Serial inputs
				ser_A_base = ser.readline()
				ser_A_tVOC = ser.readline()
				ser_B_base = ser.readline()
				ser_B_tVOC = ser.readline()
				ser_stim = ser.readline()
				ser_msec1 = ser.readline()
				ser_msec2 = ser.readline()
				ser_msec3 = ser.readline()
				
				# Converted output to print/write to CSV
				out_A_base = ser_A_base.decode("utf-8").rstrip()
				out_A_tVOC = ser_A_tVOC.decode("utf-8").rstrip()
				out_B_base = ser_B_base.decode("utf-8").rstrip()
				out_B_tVOC = ser_B_tVOC.decode("utf-8").rstrip()
				out_stim = ser_stim.decode("utf-8").rstrip()
				out_msec1 = ser_msec1.decode("utf-8").rstrip()
				out_msec2 = ser_msec2.decode("utf-8").rstrip()
				out_msec3 = ser_msec3.decode("utf-8").rstrip()
		

				print()
				print(datetime.now())
				print(out_A_base)
				print(out_A_tVOC)
				print(out_B_base)
				print(out_B_tVOC)
				print(out_stim)
				print(out_msec1)
				print(out_msec3)
				print(out_msec2)


				#with open(fileName, "a") as data_out:

				#writer = csv.writer(data_out, delimiter = ",")
				
				# Append output to CSV file
				writer.writerow([datetime.now(), out_A_base, out_A_tVOC, out_B_base, out_B_tVOC, out_stim, out_msec1, out_msec2, out_msec3])
	

			except KeyboardInterrupt:
				print("Keyboard interrupt - Data collection stopped")
				#with open(fileName, "a") as data_out:
		
				#writer = csv.writer(data_out, delimiter = ",")
				writer.writerow(["END", "END", "END", "END", "END", "END", "END", "END", "END"])
				data_out.close()
				ser.flush()
				ser.flushInput()
				ser.flushOutput()
				ser.close()
				break

			except:
				print("ERROR - Data collection stopped. Exiting program.")
				#with open(fileName, "a") as data_out:

				#writer = csv.writer(data_out, delimiter = ",")
				writer.writerow(["ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"])
				data_out.close()
				ser.flush()
				ser.flushInput()
				ser.flushOutput()
				ser.close()
				exit()

		print()
		
		# Should the script run again?
		runAgain = input("Would you like to run another trial? (Y or ENTER to continue; any other key to exit) ") or "Y"
		print()
		
		if subNum != "TEST":
			if subIncrement in ("Y", "y", "YES", "Yes", "yes"):
				subNum += 1
			else:
				subNum = 0

	except KeyboardInterrupt:
		print("Keyboard interrupt - Exiting program.")
		exit()

	except:
		print("ERROR - Exiting program.")
		exit()


exit()
