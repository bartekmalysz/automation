import pandas as pd
import boto3

client = boto3.client('ec2')
response = client.describe_instances()
number_of_instances = len(response['Reservations'])
resources = boto3.resource('ec2')


def get_instances():

    instance_summary = pd.DataFrame()

    for instance in range(0, number_of_instances):
        instance_id = response['Reservations'][instance]['Instances'][0]['InstanceId'] if \
            len(response['Reservations'][instance]['Instances'][0]['InstanceId']) > 0 else 'none'

        instance_type = response['Reservations'][instance]['Instances'][0]['InstanceType'] if \
            len(response['Reservations'][instance]['Instances'][0]['InstanceType']) > 0 else 'none'

        instance_state = response['Reservations'][instance]['Instances'][0]['State']['Name'] if \
            len(response['Reservations'][instance]['Instances'][0]['State']['Name']) > 0 else 'none'

        volume_id = response['Reservations'][instance]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'] if \
            len(response['Reservations'][instance]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']) > 0 \
            else 'none'

        device_name = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['DeviceName'] if \
            len(response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['DeviceName']) > 0 else 'none'

        delete_on_termination = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs'][
            'DeleteOnTermination'] if \
            len(response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['DeleteOnTermination']) > \
            0 else 'none'

        device_status = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['Status'] if \
            len(response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['Status']) > 0 else 'none'

        instance_holder = pd.DataFrame(data={'instanceId': [instance_id],
                                             'instanceType': [instance_type],
                                             'instanceState': [instance_state],
                                             'volumeId': [volume_id],
                                             'deviceName': [device_name],
                                             'delete': [delete_on_termination],
                                             'deviceStatus': [device_status]
                                             })

        instance_summary = instance_summary.append(instance_holder, sort=False)

    print('Below instances were found on this AWS account:\n')
    print(instance_summary)
    return instance_summary


def get_running_instances():
    temp = get_instances()
    running = temp[temp['instanceState'] == 'running']['instanceId'].unique().tolist()
    return running


def stop_running_instances():
    temp = get_running_instances()
    if len(temp) < 1:
        print('No running instances')
    else:
        client.stop_instances(InstanceIds=temp)
        print('Stopped below instances: ')
        print('\n'.join(x for x in temp))


def get_stopped_instances():
    temp = get_instances()
    stopped = temp[temp['instanceState'] == 'stopped']['instanceId'].unique().tolist()
    return stopped


def start_stopped_instances():
    temp = get_stopped_instances()
    if len(temp) < 1:
        print('All instances running)')
    else:
        client.start_instances(InstanceIds=temp)
        print('Started below instances: ')
        print('\n'.join(x for x in temp))


def detach_all_drives():
    temp = get_instances()
    attached = temp[temp['deviceStatus'] == 'attached']['volumeId'].unique().tolist()
    if len(attached) < 1:
        print('All volumes are dettacched')
    else:
        ec2 = boto3.resource('ec2')
        for vol in attached:
            volume = ec2.Volume(vol)

            volume.detach_from_instance(Device=temp.loc[temp['volumeId'] == vol, 'deviceName'][0],
                                        Force=True,
                                        InstanceId=temp.loc[temp['volumeId'] == vol, 'instanceId'][0],
                                        DryRun=False)
    print('Detached all drives')


def get_detached_drives():
    temp = resources.volumes.all()
    volumes = list()
    for vol in temp:
        volumes.append(vol.id)
    print(volumes)
    return volumes


def delete_detached_drives():
    detached = get_detached_drives()
    if len(detached) < 1:
        print('All volumes are detached')
    else:
        print('Below volumes are deleted\n')
        print(detached)
        ec2 = boto3.resource('ec2')
        for vol in detached:
            volume = ec2.Volume(vol)
            volume.delete(DryRun=False)
    print('Deleted all drives')
