# aws-report-from-medical-audio
The lambda functions for converting a medical audio into a text report using aws medicaltranscribe and medicalcomprehend.</br>

Lambda functions:</br>
   1.aws-transcribe.py</br>
   2.aws-comprehend.py</br>
   
S3 buckets:</br>
   1.audio-aws-transcribe : to store audio file(wav files) which triggers aws-transcribe function</br> 
   2.file-aws-comprehend  : this bucket stores the output of aws-transcribe function which triggers aws-comprehend</br>
   3.our-output           : this bucket stores the text output from aws-comprehend</br>
   
 DynamoDB table:</br>
   Medical-record : to store the report from medicalcomprehend.
   
 # NOTE:</br>
 
 Triggers are needed to be created while creating the lambda functions.</br>
     1.Audiofile(.wav) input to audio-aws-transcribe bucket triggers aws-transcribe.</br >
     2.Json input to file-aws-comprehend bucket triggers aws-comprehend</br >
     
 IAM roles for the lambda functions include:</br>
     1.S3fullaccess</br >
     2.Transcribefullaccess</br >
     3.Dynamodbfullaccess</br >
     4.Comprehendmedicalfullaccess</br >
     5.Cloudwatchlogs</br >
