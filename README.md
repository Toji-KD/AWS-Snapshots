# Python scripts to take Instance volume snapshots

These scripts can be used to take AWS instance snapshots and old snapshots can be removed with retention period.
snapshots will be removed accoding to the retention period. More details of each script are given below.

# snapshot-all-volumes.py
This script takes snapshot of all volumes available in the region configured in aws cli. Retention works as region wide according to snapshot Description. No need to specify voulume ids with this script.

# snapshot-single-instance.py
This script takes snapshot of volumes attached to the current instance. Retention works as region wide according to snapshot Description. No need to specify voulume id for this script.

# snapshot-from-specific-list.py
This script takes snapshot of volumes specified as list in the script Volume ids of the instance drive should be specified. Retention works as region wide according to snapshot Description.

# Server Requirements

AWS CLI - # pip install awscli , # aws configure

Python3 -   Default in all servers.

Pip3     - # apt-get install -y python3-pip

Boto3   - # pip3 install boto3

# Written by Toji K Dominic 
tojikdominic@gmail.com +91 9747389586

