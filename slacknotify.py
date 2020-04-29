from __future__ import print_function
import time
from botocore.vendored import requests
from boto3 import session, client
import boto3
import json
import os

#Add Slack Webhook in Env Variable
url = os.environ["SLACK_WEBHOOK_URL"]

def lambda_handler(event, context):
    if "detail-type" not in event:
        raise ValueError("ERROR: event object is not a valid CloudWatch Logs event")
    else:
        if event["detail-type"] == "ECS Task State Change":
            detail = event["detail"]
            if detail["lastStatus"] == "RUNNING":
                if detail["desiredStatus"] == "RUNNING":
                  time.sleep(20)
                  # Send an error status message.
                  Subject="ECS Deployment Done with latest image",
                  Message=json.dumps(detail)
                  messagedata = json.loads(Message)
                  # Break out Cloudwatch payload into variables that we use
                  taskArn = messagedata['taskArn']
                  desiredStatus = messagedata['desiredStatus']
                  lastStatus = messagedata['lastStatus']
                  #stoppedReason = messagedata['stoppedReason']
                  clusterArn = messagedata['clusterArn']
                  
                  taskDefinitionArn = messagedata['taskDefinitionArn']
                  # Get all content from nested containers param:
                  containers = messagedata['containers'][0]['name']
                  # Get specific nested content from containers param:
                  #containersreason = messagedata['containers'][0]['reason']
                  
                  #ALL DATA that was posted from cloudwatch## 
                  #Only post to slack with specific data from cloudwatch ##
                  payload = {'channel': '#cloudwatch-alert', 'username': 'cloudwatch', 'text': '%s \n Container Name:  %s \n Task Defi ARN: %s \n Desired Status: %s \n Last Status: %s ' % (Subject, containers, taskDefinitionArn, desiredStatus, lastStatus,  ), 'icon_emoji': 'ghostwn:'}
                  headers = {"content-type": "application/json" }
                  r = requests.put(url, data=json.dumps(payload), headers=headers)
                  
                  #print json.dumps(messagedata)
                  print(r.status_code)
                  print(r.content)
                  note = "Post of data to slack was attempted"
                  
            #Notify if ECS Task Stopped
            if detail["lastStatus"] == "STOPPED":
                if detail["desiredStatus"] == "STOPPED":
                  if detail["stoppedReason"] == "Essential container in task exited":
                    time.sleep(20)
                    # Send an error status message.
                    Subject="ECS task failure detected for container",
                    Message=json.dumps(detail)
                    messagedata = json.loads(Message)
                    # Break out Cloudwatch payload into variables that we use
                    taskArn = messagedata['taskArn']
                    desiredStatus = messagedata['desiredStatus']
                    lastStatus = messagedata['lastStatus']
                    stoppedReason = messagedata['stoppedReason']
                    clusterArn = messagedata['clusterArn']
                      
                    taskDefinitionArn = messagedata['taskDefinitionArn']
                    # Get all content from nested containers param:
                    containers = messagedata['containers'][0]['name']
                    # Get specific nested content from containers param:
                    #containersreason = messagedata['containers'][0]['reason']
    		  
    		        #ALL DATA that was posted from cloudwatch## 
                    #Only post to slack with specific data from cloudwatch ##
                    payload = {'channel': '#cloudwatch-alert', 'username': 'cloudwatch', 'text': '%s \n Container Name:  %s \n Task Defi ARN: %s \n Stopped Reason: %s \n Desired Status: %s \n Last Status: %s ' % (Subject, containers, taskDefinitionArn, stoppedReason, desiredStatus, lastStatus,  ), 'icon_emoji': 'ghostwn:'}
                    headers = {"content-type": "application/json" }
                    response = requests.put(url, data=json.dumps(payload), headers=headers)
                      
                    #print json.dumps(messagedata)
                    print (response.status_code)
                    print (response.content)
                    note = "Post of data to slack was attempted"