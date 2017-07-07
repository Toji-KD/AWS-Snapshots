#!/usr/bin/python3
import datetime
import boto3
import datetime
import sys
import requests

###### Retention in days ######
Retention = 4     #Specify retention here
###############################
#This scipt takes SnapShot of all volumes for the current instance where this script is configured. 
#snapshots will be removed accoding to the retention period.
#
##### Server Requirements ####################
# AWS CLI - # pip install awscli , # aws configure
# Python3 -   Default in all servers.
# Pip3     - # apt-get install -y python3-pip
# Boto3   - # pip3 install boto3
#########################################
# Written by Toji K Dominic 
# tojikdominic@gmail.com +91 9747389586
#########################################

ID = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
ID = ID.text

Time_Now = datetime.datetime.now().strftime("%Y-%m-%d/%H-%M-%S")
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
response = client.describe_snapshots(Filters=[{'Name': 'description','Values': ['SnapShot of *']}])

#take SnapShot

for i in client.describe_volumes()['Volumes']:
  if i['Attachments'][0]['InstanceId'] == ID:
    try:
      snap = client.create_snapshot(Description='SnapShot of '+i['VolumeId']+' dated '+Time_Now+' for instance '+i['Attachments'][0]['InstanceId'],VolumeId=i['VolumeId'])
      if isinstance(snap['SnapshotId'],str):
        print('SnapShot successfully taken ('+snap['SnapshotId']+') for the volume',i['VolumeId'],'. Attached instance',i['Attachments'][0]['InstanceId'])
        print('')
      else:
        print('Error in taking SnapShot')
        print('')
    except:
      print('Script couldnt take SnapShot')
      print('')
  else:
    print('Checking volumes for current instance')
     

      
#Check retention and remove Snapshots
print('')
if response['Snapshots'] == []:
  print('No SnapShots available in this region. Exiting..')
  sys.exit()
else:
  print('Script is Checking snapshot details..')
  print('')

for time in response['Snapshots']:
  snap_time = str(time['StartTime']).split(' ')[0]
  snap_time = datetime.datetime.strptime(snap_time, "%Y-%m-%d")
  time_now = datetime.datetime.now()
  D = time_now - snap_time
  Days=int(D.days)
  if Days > Retention:
    try:
      del_snap = client.delete_snapshot(SnapshotId=time['SnapshotId'])
      if del_snap['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Removing SnapShot ',time['SnapshotId'])
        print('')
      else:
        print('Error in removing SnapShot')
        print('')
    except:
      print('Script couldnt remove SnapShot')
      print('')
			
  else:
    print('Not removing SnapShot '+time['SnapshotId']+' as it come under retention period')
    print('')
