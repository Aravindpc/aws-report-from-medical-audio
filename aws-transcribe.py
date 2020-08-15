import json
import boto3
# lambda function to convert audio input from an s3 bucket to a json file in another bucket(file-aws-comprehend) using aws-medicaltranscribe
transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    if event:
        file_obj = event["Records"][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        s3_uri = "s3://"+bucket_name+"/"+file_name
        job_name = context.aws_request_id
        
        transcribe.start_medical_transcription_job(MedicalTranscriptionJobName=job_name,
            Media = {'MediaFileUri': s3_uri}, MediaFormat = 'wav', LanguageCode = 'en-US',
            OutputBucketName = 'file-aws-comprehend',
            Settings={ 'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 2, 'ChannelIdentification': False},
            Type='DICTATION', Specialty='PRIMARYCARE')
    return {
        'statusCode': 200,
        'body': json.dumps('Transcription job created!')
    }
