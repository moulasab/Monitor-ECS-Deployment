# Monitor-ECS-Deployment
Implement monitor service for ECS Deployment, as part of monitor service implemented slack notification whenever Service deployed with latest image in ECS 

Implementaion:
1) Create CloudWatch Event Rule for ECS service All Events 
2) Select Lambda Function in Add Target while creating CloudWatch event Rule in the above step
3) Create Lambda fucntion to Notify Slack channel and mentioned code in the python script
