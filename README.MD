# MARCH 2, 2025
## COMPLETED
1. Created this project to automate writing to the Google spreadsheet for news
1. Using docker to eliminate various conflicts including feedparser, message update OpenSSL from OpenSSL 1.0.2k-fips to 1.1.1+, error in feedparser setup command: use_2to3 is invalid etc.
1. Using ASK SAM CLI since the AWS Serverless Application Model (SAM) CLI is useful for deploying Lambda functions  (The AWS CLI is a unified tool to manage your AWS services from the command line. It allows you to interact with various AWS services, including EC2, S3, Lambda etc)
1. Created lambda.py and requirements.txt
1. Wrote to the Sheets successfully by topic.

## TO DO
1. Figure out automated writing (chron) and test it
2. Myfunction - what is it?

```
Mounting /Users/tanyagupta/googlesheetswriter/.aws-sam/build/MyFunction as /var/task:ro,delegated, inside runtime container START RequestId: 84f4ce51-9b90-4767-ae6a-c83ee291d792 Version: $LATEST
Function 'MyFunction' timed out after 3 seconds 02 Mar 2025 21:57:00,997 [ERROR] (rapid) Invoke failed InvokeID=e40fa3f6-01fd-4d28-b51a-c63f95671205 error=errResetReceived
  END RequestId: e40fa3f6-01fd-4d28-b51a-c63f95671205
  REPORT RequestId: e40fa3f6-01fd-4d28-b51a-c63f95671205	Init Duration: 0.03 ms	Duration: 3000.00 ms	Billed Duration: 3000 ms	Memory Size: 128 MB	Max Memory Used: 128 MB
  No response from invoke container for MyFunction     
```
[Mother document readme](../news_collection/UPDATES.MD)
