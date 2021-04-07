import json, boto3, datetime

def lambda_handler(event, context):
    # TODO implement
    print('toji')
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')
    #snaps = ec2.snapshots.filter(OwnerIds='494457599025')
    response = client.describe_snapshots(Filters=[{'Name': 'owner-id','Values': ['494457599025']}])
    for time in response['Snapshots']:

            print(time['SnapshotId'])
            try:
                  del_snap = client.delete_snapshot(SnapshotId=time['SnapshotId'])
                  if del_snap['ResponseMetadata']['HTTPStatusCode'] == 200:
                     print('Removing SnapShot ',time['SnapshotId'])
                  else:
                     print('Error in removing SnapShot')
                     print('')
            except:
                  print('Script couldnt remove SnapShot')
                  print('')            

