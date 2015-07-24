/*
This code is copyrighted to Iman Helal @2015 Research work
Information System Department, Faculty of computers and Information System
Cairo University, Egypt
*/
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading; //for sleep
using System.Diagnostics;
using System.IO;
using System.Globalization;
//using System.Linq.Enumerable;

namespace SimulatingEvents
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            /*
            CultureInfo culture = (CultureInfo)CultureInfo.CurrentCulture.Clone();
            culture.DateTimeFormat.ShortDatePattern = "dd/MM/yyyy HH:mm";
            //culture.DateTimeFormat.LongTimePattern = "dd/MM/yyyy HH:mm";
            Thread.CurrentThread.CurrentCulture = culture;
            Console.WriteLine("Modified time format = "+DateTime.Now);
            */
            String filePath = @"C:\Iman\My Docs\BPM - PhD\Publications\2015-AICCSA\Code\Test data\XOR\unLabeledEventLog100.csv";
            //String filePath = @"C:\Iman\My Docs\VS2013-Projects\SimulatingEvents\SimulatingEvents\bin\Debug\S-XORpaper.csv";
            //String filePath = @"C:\Iman\My Docs\VS2013-Projects\SimulatingEvents\SimulatingEvents\bin\Debug\unLabeledLog-100.csv";
            //String filePath = @"C:\Iman\My Docs\VS2013-Projects\SimulatingEvents\SimulatingEvents\bin\Debug\S2.csv";
            //var events = LoadEvents(filePath);
            //Console.WriteLine("Number of events in txt file = " + events.Count);
            //CreatingCsvFiles();
            if (System.IO.Path.GetExtension(filePath).Equals(".csv") == true)
            {
                LoadEventsCSV(filePath);
            }
            if (System.IO.Path.GetExtension(filePath).Equals(".txt") == true)
            {
                LoadEvents(filePath);
            }
            Console.WriteLine("Press enter to exit...");
            Console.ReadLine();
        }

        private static void LoadEventsCSV(String filePath)
        { 
            StreamReader sr = new StreamReader(filePath);
            List<DateTime> keyList = new List<DateTime>();
            List<String> valueList = new List<String>();

            var lines = new List<string[]>();
            int Row = 0;
            DateTime dt = new DateTime();
            while (!sr.EndOfStream)
            {
                string[] Line = sr.ReadLine().Split(',');
                if (Row > 0)
                {
                    dt = DateTime.Parse(Line[0]);
                    //String.Format("0:M/d/yyyy  H:m", dt); // has no effect :(
                    Console.WriteLine(dt);
                    keyList.Add(dt);
                    valueList.Add(Line[1]);
                }
                lines.Add(Line);
                
                Row++;
                Console.WriteLine(Row);
            }

            var data = lines.ToArray();
            DateTime[] arrayOfAllKeys = keyList.ToArray();
            String[] arrayOfAllValues = valueList.ToArray();
            int v = 0;
            foreach (DateTime key in keyList)
            {
                Console.WriteLine("Timestamp per line " + key + " Activity = " + arrayOfAllValues[v]);
                v++;
            }


            string outputFilePath = @"C:\Iman\My Docs\VS2013-Projects\SimulatingEvents\SimulatingEvents\bin\Debug\S.csv";
            if (File.Exists(outputFilePath))
            {
                File.Delete(outputFilePath);
            }
            //if (!File.Exists(outputFilePath))
            //{
            File.Create(outputFilePath).Close();
            //}
            File.AppendAllText(@"S.csv", "timestamp,activity" + Environment.NewLine);//S3.txt
            int i = 0;
            int sleeptime = 0;
            DateTime prevKey = DateTime.Now;
            Console.WriteLine("Start " + DateTime.Now.ToLongTimeString());

            //System.IO.StreamWriter fileW = new System.IO.StreamWriter("S2.txt");
            //StreamWriter w = File.AppendText("S3.txt");
            foreach (DateTime key in keyList)
            {
                if (i == 0)
                {
                    sleeptime = 0;
                    Console.WriteLine("at i = " + i + " Sleep time = " + sleeptime);
                    Thread.Sleep(sleeptime);
                }
                else
                {
                    sleeptime = Convert.ToInt32((key - prevKey).TotalSeconds);//TotalMinutes
                    if (sleeptime == 0)
                    {
                        sleeptime = 1;//just to be detected
                    } 
                    Console.WriteLine("at i = " + i + " Sleep time = " + sleeptime);
                    Thread.Sleep(sleeptime);
                }
                
                File.AppendAllText(@"S.csv", key + "," + valueList[i] + Environment.NewLine);//S3.txt
                //w.WriteLine(key + ";" + valueList[i]);//events.GetValue(i)//fileW
                i++;
                prevKey = key;


            }

            var stopwatch = Stopwatch.StartNew();
            stopwatch.Stop();
            //w.Close();
            //fileW.Close();
            Console.WriteLine("Elapsed milliseconds " + stopwatch.ElapsedMilliseconds);
            Console.WriteLine("Current time " + DateTime.Now.ToLongTimeString());
            /**/
        }

        private static Dictionary<DateTime, String> LoadEvents(String filePath)
        {
            List<String> activities = new List<String>();
            List<DateTime> timestamps = new List<DateTime>();

            Dictionary<DateTime, String> events = new Dictionary<DateTime, String>();

            int k = 0;
            foreach (String line in File.ReadAllLines(filePath))
            {
                string[] tokens = line.Split(new char[] { ';' });
                Console.WriteLine("Line " + k);
                timestamps.Add(DateTime.Parse(tokens[0]));
                activities.Add(tokens[1]);
                events.Add(DateTime.Parse(tokens[0]), tokens[1]);
                Console.WriteLine("Timestamp per line " + DateTime.Parse(tokens[0]) + " Activity = " + tokens[1]);
                k++;

            }
            var tsArray = timestamps.ToArray();
            var actArray = activities.ToArray();
            Console.WriteLine("tsArray length " + tsArray.Length + ", actArray length " + actArray.Length);
            for (int j = 0; j < tsArray.Length; j++)
            {
                Console.WriteLine("tsArray[" + j + "] = " + tsArray[j].ToString() + " -- actArray[" + j + "] = " + actArray[j].ToString());
            }

            SimulateReadingFile(events);

            return events;
        }

        private static void SimulateReadingFile(Dictionary<DateTime, String> inputEvents)
        {
            /*
            CultureInfo culture = (CultureInfo)CultureInfo.CurrentCulture.Clone();
            culture.DateTimeFormat.ShortDatePattern = "yyyy-MM-dd HH:mm:ss";
            culture.DateTimeFormat.LongTimePattern = "yyyy-MM-dd HH:mm:ss";
            Thread.CurrentThread.CurrentCulture = culture;
            Console.WriteLine(DateTime.Now);
            */
            

            List<DateTime> keyList = new List<DateTime>(inputEvents.Keys);
            List<String> valueList = new List<String>(inputEvents.Values);
            DateTime[] arrayOfAllKeys = keyList.ToArray();
            String[] arrayOfAllValues = valueList.ToArray();
            int counter = inputEvents.Count;//events.Length;
            int i = 0;
            Console.WriteLine("Count of events = " + counter);
            int sleeptime = 0;
            DateTime prevKey = DateTime.Now;
            Console.WriteLine("Start " + DateTime.Now.ToLongTimeString());

            string outputFilePath = @"C:\Iman\My Docs\VS2013-Projects\SimulatingEvents\SimulatingEvents\bin\Debug\S.csv";
            if (!File.Exists(outputFilePath))
            {
                File.Create(outputFilePath).Close();
            }

            System.IO.StreamWriter fileW = new System.IO.StreamWriter(outputFilePath);

            foreach (DateTime key in inputEvents.Keys)
            {
                if (i == 0)
                {
                    sleeptime = 0;
                    //sleeptime = Convert.ToInt32(times.GetValue(i));
                    Console.WriteLine("at i = " + i + " Sleep time = " + sleeptime);
                    Thread.Sleep(sleeptime);
                }
                else
                {
                    sleeptime = Convert.ToInt32((key - prevKey).TotalSeconds);//TotalMinutes
                    if (sleeptime == 0)
                    {
                        sleeptime = 1;//just to be detected
                    }
                    
                    Console.WriteLine("at i = " + i + " Sleep time = " + sleeptime);
                    Thread.Sleep(sleeptime);
                }
                File.AppendAllText(@"S.csv", key + "," + valueList[i] + Environment.NewLine);
                //fileW.WriteLine(key+";"+inputEvents[key]);//events.GetValue(i)
                i++;
                prevKey = key;


            }

            var stopwatch = Stopwatch.StartNew();
            stopwatch.Stop();
            fileW.Close();
            Console.WriteLine("Elapsed milliseconds " + stopwatch.ElapsedMilliseconds);
            Console.WriteLine("Current time " + DateTime.Now.ToLongTimeString());

        }
        /*
        private static void CreatingCsvFiles()
        {
            string filePath = @"C:\Iman\My Docs\VS2013-Projects\SimulatingEvents\SimulatingEvents\bin\Debug\S.csv";
            if (!File.Exists(filePath))
            {
                File.Create(filePath).Close();
            }
            string delimiter = ",";
            string[][] output = new string[][]{
            new string[]{"Value1","Value2","Value3","Value4"} //add the values that you want inside a csv file. Mostly this function can be used in a foreach loop.
            };
            int length = output.GetLength(0);
            StringBuilder sb = new StringBuilder();
            for (int index = 0; index < length; index++)
                sb.AppendLine(string.Join(delimiter, output[index]));
            File.AppendAllText(filePath, sb.ToString());
        }
        */
        /* 
                 //Different time formats:
                 String k = String.Format("{0:t}", key);  // "4:05 PM"                         ShortTime
                 String k = String.Format("{0:d}", key);  // "3/9/2008"                        ShortDate
                 String k = String.Format("{0:T}", key);  // "4:05:07 PM"                      LongTime
                 String k = String.Format("{0:D}", key);  // "Sunday, March 09, 2008"          LongDate
                 String k = String.Format("{0:f}", key);  // "Sunday, March 09, 2008 4:05 PM"  LongDate+ShortTime
                 String k = String.Format("{0:F}", key);  // "Sunday, March 09, 2008 4:05:07 PM" FullDateTime
                 String k = String.Format("{0:g}", key);  // "3/9/2008 4:05 PM"                ShortDate+ShortTime
                 String k = String.Format("{0:G}", key);  // "3/9/2008 4:05:07 PM"             ShortDate+LongTime
                 String k = String.Format("{0:m}", key);  // "March 09"                        MonthDay
                 String k = String.Format("{0:y}", key);  // "March, 2008"                     YearMonth
                 String k = String.Format("{0:r}", key);  // "Sun, 09 Mar 2008 16:05:07 GMT"   RFC1123
                 String k = String.Format("{0:s}", key);  // "2008-03-09T16:05:07"             SortableDateTime
                 String k = String.Format("{0:u}", key);  // "2008-03-09 16:05:07Z"            UniversalSortableDateTime
                 // create date time 2008-03-09 16:05:07.123
                 DateTime dt = new DateTime(2008, 3, 9, 16, 5, 7, 123);
                 String.Format("{0:y yy yyy yyyy}", dt);  // "8 08 008 2008"   year
                 String.Format("{0:M MM MMM MMMM}", dt);  // "3 03 Mar March"  month
                 String.Format("{0:d dd ddd dddd}", dt);  // "9 09 Sun Sunday" day
                 String.Format("{0:h hh H HH}",     dt);  // "4 04 16 16"      hour 12/24
                 String.Format("{0:m mm}",          dt);  // "5 05"            minute
                 String.Format("{0:s ss}",          dt);  // "7 07"            second
                 String.Format("{0:f ff fff ffff}", dt);  // "1 12 123 1230"   sec.fraction
                 String.Format("{0:F FF FFF FFFF}", dt);  // "1 12 123 123"    without zeroes
                 String.Format("{0:t tt}",          dt);  // "P PM"            A.M. or P.M.
                 String.Format("{0:z zz zzz}",      dt);  // "-6 -06 -06:00"   time zone
                    
                String.Format("0:M/d/yyyy  H:m",dt);
                 */
    }

}
