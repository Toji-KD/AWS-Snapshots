#!/usr/bin/python3
import datetime
import boto3
import datetime
import sys
##### Volume IDs #############
#Specify voulume ids of instance volume to be backed up. Those should be comma seperated and kept in single quotes.
Volume_list = ['vol-0bf7d84b29e915079','vol-00137057e16ee3954']  
###### Retention in days ######
Retention = 0     #Specify retention here
###############################
#This scipt takes SnapShots of specified volumes for the current region. Volume IDs should be specified above as list.
#snapshots will be removed accoding to the retention period.
#
##### Server Requirements ####################
# AWS CLI - # pip install awscli , # aws configure
# Python3 -   Default in all servers.
# Pip     - # apt-get install -y python3-pip
# Boto3   - # pip install boto3
##############################################
# Written by Toji K Dominic 
# tojikdominic@gmail.com +91 9747389586
##############################################

Time_Now = datetime.datetime.now().strftime("%Y-%m-%d/%H-%M-%S")
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
response = client.describe_snapshots(Filters=[{'Name': 'description','Values': ['SnapShot of *']}])

#take SnapShot

for i in Volume_list:
  try:
      snap = client.create_snapshot(Description='SnapShot of '+i+' dated '+Time_Now,VolumeId=i)
      if isinstance(snap['SnapshotId'],str):
        print('SnapShot successfully taken ('+snap['SnapshotId']+') for the volume',i)
        print('')
      else:
        print('Error in taking SnapShot')
        print('')
  except:
      print('Script couldnt take SnapShot')
      print('')

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
  if Days >= Retention:
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
