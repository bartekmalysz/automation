import pandas as pd
import boto3
pd.options.display.max_columns = 20
pd.options.display.max_colwidth = 255

client = boto3.client('ec2')
resources = boto3.resource('ec2')


def get_instances():
    instances = resources.instances.all()
    instance_holder = pd.DataFrame()

    for instance in instances:
        temp = pd.DataFrame(data={
            'ID': [instance.id],
            'State': [instance.state['Name']],
            'KeyName': [instance.key_name],
            'Type': [instance.instance_type],
            'AvailabilityZone': [instance.placement['AvailabilityZone']],
            'Tenancy': [instance.placement['Tenancy']],
            'VPCID': [instance.vpc_id],
            'SubnetID': [instance.subnet_id],
            'PrivateIP': [instance.private_ip_address],
            'Platform': [instance.platform],
            'RootDeviceName': [instance.root_device_name],
            'RootDeviceType': [instance.root_device_type],
        })

        instance_holder = instance_holder.append(temp, ignore_index=True, sort=False)
    return(instance_holder)
       # instance_holder.to_csv('./all_instances.csv', sep=',', index=False)


def get_running_instances():
    temp = get_instances()
    running = temp[temp['State'] == 'running']['ID'].unique().tolist()
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
    stopped = temp[temp['State'] == 'stopped']['ID'].unique().tolist()
    return stopped


def start_stopped_instances():
    temp = get_stopped_instances()
    if len(temp) < 1:
        print('All instances running)')
    else:
        client.start_instances(InstanceIds=temp)
        print('Started below instances: ')
        print('\n'.join(x for x in temp))


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

# subnet_id – The VPC Subnet ID, if running in VPC.
# vpc_id – The VPC ID, if running in VPC.
# private_ip_address – The private IP address of the instance.
# ip_address – The public IP address of the instance.
# platform – Platform of the instance (e.g. Windows)
# root_device_name – The name of the root device.
# root_device_type – The root device type (ebs|instance-store).
# block_device_mapping – The Block Device Mapping for the instance.
# state_reason – The reason for the most recent state transition.


#
# Variables:
# id – The unique ID of the Instance.
# groups – A list of Group objects representing the security groups associated with the instance.
# public_dns_name – The public dns name of the instance.
# private_dns_name – The private dns name of the instance.
# state – The string representation of the instance’s current state.
# state_code – An integer representation of the instance’s current state.
# previous_state – The string representation of the instance’s previous state.
# previous_state_code – An integer representation of the instance’s current state.
# key_name – The name of the SSH key associated with the instance.
# instance_type – The type of instance (e.g. m1.small).
# launch_time – The time the instance was launched.
# image_id – The ID of the AMI used to launch this instance.
# placement – The availability zone in which the instance is running.
# placement_group – The name of the placement group the instance is in (for cluster compute instances).
# placement_tenancy – The tenancy of the instance, if the instance is running within a VPC. An instance with a tenancy of dedicated runs on a single-tenant hardware.
# kernel – The kernel associated with the instance.
# ramdisk – The ramdisk associated with the instance.
# architecture – The architecture of the image (i386|x86_64).
# hypervisor – The hypervisor used.
# virtualization_type – The type of virtualization used.
# product_codes – A list of product codes associated with this instance.
# ami_launch_index – This instances position within it’s launch group.
# monitored – A boolean indicating whether monitoring is enabled or not.
# monitoring_state – A string value that contains the actual value of the monitoring element returned by EC2.
# spot_instance_request_id – The ID of the spot instance request if this is a spot instance.
# subnet_id – The VPC Subnet ID, if running in VPC.
# vpc_id – The VPC ID, if running in VPC.
# private_ip_address – The private IP address of the instance.
# ip_address – The public IP address of the instance.
# platform – Platform of the instance (e.g. Windows)
# root_device_name – The name of the root device.
# root_device_type – The root device type (ebs|instance-store).
# block_device_mapping – The Block Device Mapping for the instance.
# state_reason – The reason for the most recent state transition.
# interfaces – List of Elastic Network Interfaces associated with this instance.
# ebs_optimized – Whether instance is using optimized EBS volumes or not.
# instance_profile – A Python dict containing the instance profile id and arn associated with this instance.
