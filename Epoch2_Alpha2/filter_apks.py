#########################################################################################################################################################
# Python 2.7.3
#
# Filters apks based on data flow content by using FlowDroid, an open-source static taint analysis tool for Android apps
# About FlowDroid: http://sseblog.ec-spride.de/tools/flowdroid/
# Installing FlowDroid: https://github.com/secure-software-engineering/soot-infoflow-android/wiki
# 
# Executes FlowDroid command and processes the output files to reduce false positives
#
# Generates the following text files:
#	[1] filter_apks_output.txt ---> list of apks that contain flows with specified sources and sinks
#	[2] filter_apks_output_noDataFlows.txt ---> list of apks that don't contain flows with specified sources and sinks
#                                             or any data flows in general
# 
# Also produces the following additional files:
#	[1] output of FlowDroid command results for each apk (ex. testApk.apk_flowDroidOutput.txt)
#	[2] filter_apks_output_errorLog.txt ---> Error log
#
# All files are saved in the directory = "/tmp/ec700_alpha2/filter_apks_files"
#
# If FlowDroid execution stalls, press Ctrl + C to continue script to analyze the next available apk
#
# Run script in the directory where the the following FlowDroid jars and config files are located:
#   axml-2.0.jar
#   slf4j-api-1.7.5.jar
#   slf4j-simple-1.7.5.jar
#   soot-infoflow.jar
#   soot-infoflow-android.jar
#   soot-trunk.jar
#   AndroidCallbacks.txt
#   EasyTaintWrapperSource.txt
#   SourcesAndSinks.txt (customized)
#
# Usage: python filter_apks.py <path to directory of apks to test> <path to Android SDK platforms>
# Example: python filter_apks.py ~/Desktop/test_apks ~/Desktop/androidSdkPlatforms
#
#########################################################################################################################################################
import os
import sys
import shutil

# List of required jars to run FlowDroid
jars = "soot-trunk.jar:soot-infoflow.jar:soot-infoflow-android.jar:slf4j-api-1.7.5.jar:slf4j-simple-1.7.5.jar:axml-2.0.jar"

# Sources to indicate incoming data flows
sourcesIncoming = ["java.net.URLConnection: java.io.InputStream getInputStream()", 
						"java.io.InputStream: void <init>()", 
						"java.io.InputStream: java.io.InputStream getInputStream()", 
						"org.apache.http.HttpResponse: org.apache.http.HttpEntity getEntity()"]

# Sinks to indicate outgoing data flows
sinksOutgoing = ["java.net.URLConnection: java.io.OutputStream getOutputStream()",
						"java.io.DataOutputStream: void write(byte[], int, int)",
						"java.io.DataOutputStream: void write(byte[])",
						"java.io.DataOutputStream: void	write(int)",
						"java.io.OutputStream: void write(byte[])",
						"java.io.OutputStream: void write(byte[],int,int)",
						"java.io.OutputStream: void write(int)",
						"java.io.FileOutputStream: void write(byte[])",
						"java.io.FileOutputStream: void write(byte[],int,int)",
						"java.io.FileOutputStream: void write(int)",
						"org.apache.http.impl.client.DefaultHttpClient: org.apache.http.HttpResponse execute(org.apache.http.client.methods.HttpUriRequest)",
						"org.apache.http.client.HttpClient: org.apache.http.HttpResponse execute(org.apache.http.client.methods.HttpUriRequest)"]
#########################################################################################################################################################
# Execute if optional argument is not entered
if (len(sys.argv) == 3):
	apkDir = sys.argv[1]
	#print("apkDir: ", apkDir) # DEBUGGING
	platformDir = sys.argv[2]
	#print("platformDir: ", platformDir) # DEBUGGING


	# Create directory to save all output files
	directory = "/tmp/ec700_alpha2/filter_apks_files"
	if not os.path.exists(directory):
		os.makedirs(directory, 0755)
		print "Created new directory to store filter_apk.py files, continuing script..."
	else:
		shutil.rmtree(directory)
		os.makedirs(directory, 0755)
		print "Deleted and made directory: " + directory + ", continuing script..."


	# Loop through each apk in apkDir
	for file in os.listdir(sys.argv[1]):
		# For each apk, generate and execute FlowDroid command
		cmd = "java -cp " + jars + " soot.jimple.infoflow.android.TestApps.Test " + apkDir + "/" + file + " " + platformDir + " > outputFile.txt"
		print(cmd)
		#exit() # TEMP
		# Execute FlowDroid command
		os.system(cmd)
		print "Finished executing FlowDroid command.\nAnalyzing output file..."
		

		# Check for outputFile.txt; it exists, rename it and move it to directory; else, create errorLog and move onto next apk
		if os.path.isfile("outputFile.txt"):
			print "Renaming outputFile.txt for " + file + " and moving it to " + directory
			os.rename("outputFile.txt", directory + "/" + file + "_" + "flowdroidOutput.txt")
		else:
			errorMsg = "Error: could not create outputFile.txt for apk: " + file
			with open(directory + "/" + "filter_apks_output_errorLog.txt", "a") as errorFile:
				errorFile.write(errorMsg + "\n")
			# Go on to next apk file
			continue
		

		# Check if outputFile.txt contains any dataflows
		# outputFile.txt will contain the flow paths at the end of file, if they exist
		# Go on to next apk file if no paths found
		if not "Found a flow to sink" in open(directory + "/" + file + "_" + "flowdroidOutput.txt").read():
			print "No dataflows found in: ", file
			with open(directory + "/" + "filter_apks_output_noDataFlows.txt", "a") as nayFile:
				nayFile.write(file + "\n")
			# Go to next apk
			continue

		# If the outputFile for the apk contains data flows, check to see if they are the ones we are interested in, based on the sources and sink
		else:
			with open(directory + "/" + file + "_" + "flowdroidOutput.txt", "r") as outputFile:
				print "IN WITH"
				# Set flag to indicate if a data flow that we wanted is found
				isFound = ""

				for line in outputFile:
					# Indicates possible INCOMING data flow (source: sourcesIncoming, sink: fromJson method)
					if "Found a flow to sink" in line and "fromJson" in line:
						nextLine = outputFile.next()
						while not "Found a flow to sink" in nextLine and not "Analysis has run" in nextLine: # Indicates a source 
							# Check if the sources are the ones we are interested in (listed in sourcesIncoming)
							if any([x in nextLine for x in sourcesIncoming]):
								print "INCOMING data flow detected..."
								isFound = 1
								with open(directory + "/" + "filter_apks_output.txt", "a") as finalOutputFile:
									finalOutputFile.write(file + ",false\n")
								break
							nextLine = outputFile.next()
					# Indicates possible OUTGOING data flow (source: toJson method, sink: sinksOutgoing)
					# Check if any of the sinks are the ones we interested in (listed in sinksOutgoing)
					elif "Found a flow to sink" in line and any([y in line for y in sinksOutgoing]):
						nextLine = outputFile.next()
						while not "Found a flow to sink" in nextLine and not "Analysis has run" in nextLine: # Indicates a source
							if "toJson" in nextLine:
								print "OUTGOING data flow detected..."
								isFound = 1
								with open(directory + "/" + "filter_apks_output.txt", "a") as finalOutputFile:
									finalOutputFile.write(file + ",true\n")
								break
							nextLine = outputFile.next()
					else:
						continue

				# Check isFound value after iteration of outputFile.txt is finished
				else:
					if isFound != 1:
						print "Specified data flows not found in " + file + ", moving on..."
						with open(directory + "/" + "filter_apks_output_noDataFlows.txt", "a") as nayFile:
							nayFile.write(file + "\n")
					outputFile.close()
					print "Finished analyzing output file."
					print "\nNext apk..."
					continue
	else:
		print "Finished processing apks.\nExiting."
		exit();


#########################################################################################################################################################
# Execute if required command-line args are not entered
else:
	print "Error!\tNeeds at two arguments."
	print "Usage (Python 2.7.3):\tpython filter_apks.py <path to directory of apks to test> <path to Android SDK platforms>"
	print "Ex:\tpython filter_apks.py ~/Desktop/test_apks ~/Desktop/androidSdkPlatforms"
	exit()
