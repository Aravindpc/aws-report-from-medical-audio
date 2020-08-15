import json
import boto3
import datetime
from decimal import Decimal
from pprint import pprint
# function to create text file for displaying the output
def file_creation(response):
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    client = boto3.client('s3')
    res = client.list_objects(Bucket='audio-aws-transcribe')['Contents']
    name = str([obj['Key'] for obj in sorted(res, key=get_last_modified, reverse=True)][0])
    pprint(name)
    file_name = name.split('.')[0]+'.txt'
    txt_file = "/tmp/"+file_name
    s31=boto3.resource("s3")
    with open(txt_file,'w') as txt:
        txt.write("     "+name+"\n\n")
        s=" "
        if response["PHI"]=={} and response["Medical_condition"]=={} and response["Anatomy"]=={} and response["Test_treatment"]=={} and response["Medication"]=={}:
            txt.write("Audio has no medical data")
        else:
            if "NAME" in response["PHI"]:
                txt.write("NAME :  "+s.join(response["PHI"]["NAME"])+"\n")
            for key,value in response["PHI"].items():
                if key!="NAME":
                    txt.write(key+" :  "+s.join(value)+"\n")
            txt.write("\nMEDICAL CONDITION\n")
            for key,value in response["Medical_condition"].items():
                s1=""
                for key1,value1 in value.items():
                    txt.write("\t"+key1+" :  "+s1.join(value1)+"\n")
            txt.write("\nANATOMY\n")
            for key,value in response["Anatomy"].items():
                txt.write("\t"+key+" :  "+s.join(value)+"\n")
            txt.write("\nTEST AND TREATMENT\n")
            for key,value in response["Test_treatment"].items():
                # for key1,value1 in value.items():
                txt.write("\t"+key+" :  "+s.join(value)+"\n")            
            txt.write("\nMEDICATION\n")
            for key,value in response["Medication"].items():
                txt.write("\t"+key+" :  "+s.join(value)+"\n")
    s31.meta.client.upload_file(txt_file,'our-output',file_name) 
# function to call comprehendmedical which takes the input json from file-aws-comprehend(this json file is stored by aws-transcribe function)     
def lambda_handler(event, context):
    if event:
        s3=boto3.client("s3")
        file_obj=event['Records'][0]
        bucket_name=str(file_obj['s3']['bucket']['name'])
        file_name=str(file_obj['s3']['object']['key'])
        file=s3.get_object(Bucket=bucket_name,Key=file_name) 
        result=json.loads(file['Body'].read())
        pprint(type(result))
        pprint(result)
        p=result['results']
        pprint(type(p))
        p1=p['transcripts']
        paragraph=p1[0]['transcript']
        comprehend_medical=boto3.client("comprehendmedical")
        entities=comprehend_medical.detect_entities(Text=paragraph)
    
        obj=entities
        phi={}
        anatomy={}
        test_treatment={}
        medical_condition={}
        medication={}
        for entity in obj['Entities']:
            if entity["Category"]=="PROTECTED_HEALTH_INFORMATION":
                if entity["Score"]>0.6:
                    if entity["Type"] in phi and entity["Text"] not in phi[entity["Type"]]:
                        phi[entity["Type"]].append(entity["Text"])
                    else:
                        phi[entity["Type"]]=[entity["Text"]]
            elif entity["Category"]=="ANATOMY":
                if entity["Score"]>0.6:
                    if entity["Type"] in anatomy and entity["Text"] not in anatomy[entity["Type"]]:
                        anatomy[entity["Type"]].append(entity["Text"])
                    else:
                        anatomy[entity["Type"]]=[entity["Text"]]
            elif entity["Category"]=="TEST_TREATMENT_PROCEDURE":
                if entity["Score"]>0.6:
                    if entity["Type"] in test_treatment and entity["Text"] not in test_treatment[entity["Type"]]:
                        test_treatment[entity["Type"]].append(entity["Text"])
                    else:
                        test_treatment[entity["Type"]]=[entity["Text"]]
            elif entity["Category"]=="MEDICAL_CONDITION":
                if entity["Type"]=="DX_NAME":
                    if entity["Score"]>0.6:
                        for i in entity["Traits"]:
                            if i["Score"]>0.6:
                                if "DX_NAME" in medical_condition:
                                    medical_condition["DX_NAME"].update({i["Name"]:entity["Text"]}) 
                                else:
                                    medical_condition["DX_NAME"]={i["Name"]:entity["Text"]}
                else:
                    if entity["Score"]>0.6:
                        if entity["Type"] in medical_condition and entity["Text"] not in medical_condition[entity["Type"]]:
                            medical_condition[entity["Type"]].append(entity["Text"])
                        else:
                            medical_condition[entity["Type"]]=[entity["Text"]]
            elif entity["Category"]=="MEDICATION":
                if entity["Score"]>0.6:
                    medication[entity["Type"]]= entity["Text"]
                    for attribute in entity["Attributes"]:
                        if attribute["Score"]>0.6:
                            medication[attribute["Type"]]=attribute["Text"]
        
        now = datetime.datetime.now()
        entity={"datetime":str(now),"PHI":phi,"Anatomy":anatomy,"Test_treatment":test_treatment,"Medical_condition":medical_condition,"Medication":medication}
        pprint(entity)
        file_creation(entity)#passing the entity to create a text file
        dynamo = boto3.resource('dynamodb')
        table = dynamo.Table('Medical_Record')
        response = table.put_item(Item=entity) #storing the entity in a dyamodb table(Medical_Record)
            
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }