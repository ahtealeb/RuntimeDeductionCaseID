Source code associate the paper

#Runtime Deduction of Case ID for Unlabeled Business Process Execution Events
By: Iman Helal, Ahmed Awad, Ali ElBastawissi

Application is applied on:
- Python 2.7
- WatchDog 0.83 "https://github.com/gorakhargosh/watchdog#example-api-usage"
- Eclipse Modeling Tools (Luna)
- Visual Studio 2013 C#

To run our code first:
- Run Behavioral profile
  Get jbpt library from "https://code.google.com/p/jbpt"
  See "https://code.google.com/p/jbpt/source/browse/trunk/jbpt-test/src/test/java/org/jbpt/test/tree/BCTreeTest.java" to add a process model.
  Add process model in "main" of our modified behavioral profile project
- Run _int.main in RDCI using python 2.7 , with arguments
    - Unlabeled event log in (.txt or .csv) formats --> it is simulated using SimulatingEvents C# application
    - Heuristic data in (.csv) format
    - Ranking score threshold (default = 0)

The input exists in pre-specified folder in Debug folder of Simulating events application S.csv, and output in a local file dashboard.csv


This research work is copy righted to: Iman Helal, Ahmed Awad, Ali ElBastawissi @2015
