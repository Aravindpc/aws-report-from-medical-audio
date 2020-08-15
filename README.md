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
   
 NOTE:</br>
 1.Triggers are needed to be created while creating the lambda functions.</br>
     Audiofile(.wav) input to audio-aws-transcribe bucket triggers aws-transcribe.</br >
     Json input to file-aws-comprehend bucket triggers aws-comprehend</br >
 2.IAM roles for the lambda functions will include </br>
     S3fullaccess</br >
     Transcribefullaccess</br >
     Dynamodbfullaccess</br >
     Comprehendmedicalfullaccess</br >
     Cloudwatchlogs</br >
