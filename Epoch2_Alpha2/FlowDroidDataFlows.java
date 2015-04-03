import java.util.*;
import java.io.*;
import java.util.regex.*;

public class FlowDroidDataFlows {
    public static void main(String[] args) {
        // Check args 
        if (args.length <= 0) {
            Usage("Missing arguments!");
            System.exit(1);
        } else {
            try {
                // Create new output file
                PrintWriter outputFile = new PrintWriter(new BufferedWriter(new FileWriter("FlowDroidDataFlows_Output.txt", true)));

                // Create file to contain list of apks with no data flows detected
                PrintWriter outputNoFlowFile = new PrintWriter(new BufferedWriter(new FileWriter("FlowDroidDataFlows_NoFlowsOutput.txt", true)));
            
                // First argument: path to folder containing apks
                // Second argument: path to Android platforms folder
                File apkFolderPath = new File(args[0]);
                File[] fileList = apkFolderPath.listFiles();
                ArrayList<File> apkList = new ArrayList<File>();
                for(File f : fileList){
                    if(f.getName().endsWith(".apk")){
                        System.out.println(f);
                        apkList.add(f);
                    }
                }
                File[] apkArray = new File[apkList.size()];
                apkArray = apkList.toArray(apkArray);

                for(File file : apkArray) {
                    try {
                        String apkPath = args[0] + "/" + file.getName();
                        String androidPlatformsPath = args[1];
                        System.out.println("Running FlowDroid on the following apk: " + apkPath);
                        System.out.println("Using the following Android platforms path: " + androidPlatformsPath); // Ex. /home/minniek/android-sdks/platforms

                        // Run Flowdroid and get list of Flow objects
                        List<Flow> flowList = new ArrayList<Flow>();
                        FlowDroidDataFlows fd = new FlowDroidDataFlows();
                        flowList = fd.getFlows(apkPath, androidPlatformsPath);

                        // Check if flowList is empty
                        if (flowList.isEmpty()) {
                            outputNoFlowFile.append(file.getName() + ", " + "No flows detected" + "\n");
                            System.out.println("FlowDroidDataFlows says: No data flows detected in this apk: " + file.getName() + "\n");
                            outputNoFlowFile.flush();
                        } else {
                            // Print fields
                            for (Flow f : flowList) {
                                System.out.println("Sink API Name: " + f.getSinkApiName());
                                System.out.println("Sink Class Name: " + f.getSinkClassName());
                                System.out.println("Sink Method Name: " + f.getSinkMethodName());
                                System.out.println("Source API Name: " + f.getSourceApiName());
                                System.out.println("Source Class Name: " + f.getSourceClassName());
                                System.out.println("Source Method Name: " + f.getSourceMethodName());
                                System.out.println("Flow isOutgoing?: " + f.getIsOutgoing());
                                System.out.println("");

                                outputFile.append(file.getName() + ", " + f.getIsOutgoing() + "\n");
                                System.out.println(file.getName() + ", " + f.getIsOutgoing() + "\n");
                                outputFile.flush();
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                        System.out.println("Exception caught: " + e);
                        outputNoFlowFile.append(file.getName() + ", " + "No flows detected" + "\n");
                    }
                }
                outputFile.close();
                outputNoFlowFile.close();
            } catch(Exception e){
                e.printStackTrace();
                System.out.println("Exception caught: " + e);
            }
        }
    }

    public List<Flow> getFlows(String apkPath, String androidPlatformsPath) {
        // Generate FlowDroid command
        String flowDroidJars = "soot-trunk.jar:soot-infoflow.jar:soot-infoflow-android.jar:slf4j-api-1.7.5.jar:slf4j-simple-1.7.5.jar:axml-2.0.jar";
        String runFlowDroidCmd = "java -cp " + flowDroidJars + " soot.jimple.infoflow.android.TestApps.Test " + apkPath + " " + androidPlatformsPath;
        System.out.println("runFlowDroidCmd: " + runFlowDroidCmd);

        List<Flow> flowList = new ArrayList<Flow>();
        String foundPathIndicator = "Found a flow to sink";
        String endIndicator = "Analysis has run";

        // Run FlowDroid and create Flow objects from data path result
        try {
            Process p = Runtime.getRuntime().exec(runFlowDroidCmd);
            System.out.println("Executing FlowDroid command...");
            BufferedReader inputReader = new BufferedReader(new InputStreamReader(p.getInputStream()));

            for (String nextLine, currentLine = inputReader.readLine(); currentLine != null; currentLine = nextLine) {
                System.out.println("From inputReader: " + currentLine);

                nextLine = inputReader.readLine(); // Get next line

                if (currentLine.contains(foundPathIndicator)) {
                    System.out.println("Sink: " + currentLine);

                    // Create Flow object
                    Flow f = new Flow();

                    // Parse currentLine to set sinkApiName, sinkClassName, sinkMethodName
                    // Set sinkApiName
                    Pattern p1 = Pattern.compile("<(.*?)>");
                    Matcher m1 = p1.matcher(currentLine);
                    String temp1 = "";
                    if (m1.find()) {
                        temp1 = m1.group(1);
                    }
                    System.out.println("temp1: " + temp1);

                    // Set sinkMethodName
                    String[] temp2Array = temp1.split("\\:");
                    f.setSinkMethodName(temp2Array[1].replaceFirst(" ", ""));
                    System.out.println("f's sink method name: " + f.getSinkMethodName());

                    String s = temp1.replaceAll(":.*$", "");
                    String[] temp3Array = s.split("\\.");
                    System.out.println("temp3Array: " + Arrays.toString(temp3Array));
                    int temp3ArrayLen = temp3Array.length;
                    System.out.println("temp3ArrayLen: " + temp3ArrayLen);
                    String sinkApiStr = "";
                    f.setSinkClassName(temp3Array[temp3ArrayLen-1]);
                    System.out.println("f's sink class name: " + f.getSinkClassName());
                    for (int i = 0; i < temp3Array.length-1; i++){
                        sinkApiStr += temp3Array[i] + ".";
                    }
                    f.setSinkApiName(sinkApiStr);
                    System.out.println("f's sink API/package name: " + f.getSinkApiName());

                    // If the sink is "fromJson", then this is incoming data
                    if (f.getSinkMethodName().contains("fromJson")) {
                        f.setIsOutgoing(false);
                    }
                    //System.out.println("f isOutgoing?: " + f.getIsOutgoing()); // Null pointer exception

                    // Parse nextLine to get the first source information
                    //Pattern p2 = Pattern.compile("<(.*?)>");
                    Matcher m2 = p1.matcher(nextLine);
                    String temp2 = "";
                    if (m2.find()) {
                        temp2 = m2.group(1);
                    }

                    // Set sourceMethodName
                    String[] temp4Array = temp2.split("\\:");
                    f.setSourceMethodName(temp4Array[1].replaceFirst(" ", ""));
                    System.out.println("f's source method name: " + f.getSourceMethodName());

                    String ss = temp2.replaceAll(":.*$", "");
                    String[] temp5Array = ss.split("\\.");
                    System.out.println("temp5Array: " + Arrays.toString(temp5Array));
                    String sourceApiStr = "";
                    f.setSourceClassName(temp5Array[temp5Array.length-1]);
                    System.out.println("f's source class name: " + f.getSourceClassName());
                    for (int i = 0; i < temp5Array.length-1; i++){
                        sourceApiStr += temp5Array[i] + ".";
                    }
                    f.setSourceApiName(sourceApiStr);
                    System.out.println("f's source API/package name: " + f.getSourceApiName());

                    // If the source is "toJson", then this is considered outgoing data
                    if (f.getSourceMethodName().contains("toJson")) {
                        f.setIsOutgoing(true);
                    } 

                    // Add initial Flow object to list
                    flowList.add(f);

                    // If multiple sources exist for the same sink, create new Flow object for each with the same sink information
                    nextLine = inputReader.readLine();
                    while ((!nextLine.contains(foundPathIndicator)) && (!nextLine.contains(endIndicator))) { // Indicates a source
                        System.out.println("Source: " + nextLine);

                        // Create new Flow object and set sink information
                        Flow ff = new Flow();
                        ff.setSinkApiName(f.getSinkApiName());
                        ff.setSinkClassName(f.getSinkClassName());
                        ff.setSinkMethodName(f.getSinkMethodName());

                         // If the sink is "fromJson", then this is incoming data
                        if (ff.getSinkMethodName().contains("fromJson")) {
                            ff.setIsOutgoing(false);
                        }

                        // Parse nextLine to get the first source information
                        //Pattern p2 = Pattern.compile("<(.*?)>");
                        Matcher m3 = p1.matcher(nextLine);
                        String temp3 = "";
                        if (m3.find()) {
                            temp3 = m3.group(1);
                        }

                        // Set sourceMethodName
                        String[] temp6Array = temp3.split("\\:");
                        System.out.println("temp6Array: " + Arrays.toString(temp6Array));
                        ff.setSourceMethodName(temp6Array[1].replaceFirst(" ", ""));
                        System.out.println("ff's source method name: " + ff.getSourceMethodName());

                        String[] temp7Array = temp3.split("\\.");
                        String sourceApiStr2 = "";
                        ff.setSourceClassName(temp7Array[temp7Array.length-1]);
                        System.out.println("ff's source class name: " + ff.getSourceClassName());
                        for (int i = 0; i < temp7Array.length-1; i++){
                            sourceApiStr2 += temp7Array[i] + ".";
                        }
                        ff.setSourceApiName(sourceApiStr2);
                        System.out.println("ff's source API/package name: " + ff.getSourceApiName());

                        // If the source is "toJson", then this is considered outgoing data
                        if (ff.getSourceMethodName().contains("toJson")) {
                            ff.setIsOutgoing(true);
                        }    

                        // If the source is "toJson", then this is considered outgoing data
                        if (ff.getSourceMethodName().contains("toJson")) {
                            ff.setIsOutgoing(true);
                        }

                        flowList.add(ff);

                        nextLine = inputReader.readLine();
                    }
                    int exitVal = p.waitFor();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("IOException caught: " + e);
            return flowList;
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Throwable caught: " + e);
            return flowList;
        }
        System.out.println("Exiting getFlows()...");
        return flowList;
    }

    public static void Usage(String error) {
        System.out.println("Error:\t" + error);
        System.out.println("Usage:\tjava RunFlowDroid <path to folder containing apks> <path to Android platforms directory>");
        System.out.println("\tEx. of <path to apk>: /home/minniek/Desktop/apks");
        System.out.println("\tEx. of <path to Android platforms directory>: /home/minniek/android-sdks/platforms");
    }

    public class Flow {
        Boolean isOutgoing = null; // Set to true if toJson is the source, set to false if fromJson is the sink
        String sourceApiName; // Ex. com.google.gson
        String sourceClassName; // Ex. Gson
        String sourceMethodName; // Ex. java.lang.String toJson(java.lang.Object)
        String sinkApiName; // Ex. java.io
        String sinkClassName; // Ex. DataOutputStream
        String sinkMethodName; // Ex. void write(byte[])

        public boolean getIsOutgoing() {
            return this.isOutgoing;
        }

        public String getSourceApiName() {
            return this.sourceApiName;
        }

        public String getSourceClassName() {
            return this.sourceClassName;
        }

        public String getSourceMethodName() {
            return this.sourceMethodName;
        }

        public String getSinkApiName() {
            return this.sinkApiName;
        }

        public String getSinkClassName() {
            return this.sinkClassName;
        }

        public String getSinkMethodName() {
            return this.sinkMethodName;
        }

        public void setIsOutgoing(boolean isOutgoing) {
            this.isOutgoing = isOutgoing;
        }

        public void setSourceApiName(String sourceApiName) {
            this.sourceApiName = sourceApiName;
        }

        public void setSourceClassName(String sourceClassName) {
            this.sourceClassName = sourceClassName;
        }

        public void setSourceMethodName(String sourceMethodName) {
            this.sourceMethodName = sourceMethodName;
        }

        public void setSinkApiName(String sinkApiName) {
            this.sinkApiName = sinkApiName;
        }

        public void setSinkClassName(String sinkClassName) {
            this.sinkClassName = sinkClassName;
        }

        public void setSinkMethodName(String sinkMethodName) {
            this.sinkMethodName = sinkMethodName;
        }
    }
}
