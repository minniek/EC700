Instructions to Run "filter_apks.py"

NOTE: the script executes the FlowDroid command on Unix machine (Ubuntu 14.04). If you want to run it on a Windows machine,
you need to change the directory/file syntax throughout the script and the colons to semicolons on the following on line 43:

jars = "soot-trunk.jar:soot-infoflow.jar:soot-infoflow-android.jar:slf4j-api-1.7.5.jar:slf4j-simple-1.7.5.jar:axml-2.0.jar"

1) Need to run "filter_apks.py" in the same directory that stores the following required FlowDroid jars and configuration files:
    axml-2.0.jar
    slf4j-api-1.7.5.jar
    slf4j-simple-1.7.5.jar
    soot-infoflow.jar
    soot-infoflow-android.jar
    soot-trunk.jar
    AndroidCallbacks.txt
    EasyTaintWrapperSource.txt
    SourcesAndSinks.txt (customized)
  
2) Also need a directory that stores the Android SDK platforms for all API versions of apps that you want 
to test. For our project, we used APIs 2-19, excluding 13 (issues with downloading from SDK mananger from Android Studio 
and Eclipse).

3) To run, execute the following command:
    python filter_apks.py \<path to directory of apks to test\> \<path to Android SDK platforms\>
