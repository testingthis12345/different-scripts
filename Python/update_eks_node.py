"""
This script connects to an AWS EKS cluster and increases/decreases nodes in EKS cluster.
The only mandatory argument is desired node count.

usage: update_eks_node.py [-h] [--cluster CLUSTER] [--nodegroup NODEGROUP] [--min MIN] [--max MAX] --desired DESIRED
"""

import boto3
import argparse

def update_eks_nodegroup_scaling(cluster_name, nodegroup_name, min_size, max_size, desired_size):
    eks = boto3.client('eks')

    try:
        response = eks.update_nodegroup_config(
			clusterName=cluster_name,
            nodegroupName=nodegroup_name,
            scalingConfig={
                'minSize': min_size,
                'maxSize': max_size,
                'desiredSize': desired_size
            }
        )
        update_id = response['update']['id']
        print(f"Scaling config update requested. Update ID: {update_id}")
    except Exception as e:
        print(f"Failed to update node group scaling config: {e}")

def main():
    parser = argparse.ArgumentParser(description='Update EKS managed node group scaling config.')
    parser.add_argument('--cluster', required=False, default='my-cluster', help='EKS cluster name')
    parser.add_argument('--nodegroup', required=False, default='spot-ng', help='EKS node group name')
    parser.add_argument('--min', type=int, required=False, default=0, help='Minimum node count')
    parser.add_argument('--max', type=int, required=False, default=1, help='Maximum node count')
    parser.add_argument('--desired', type=int, required=True, default=0, help='Desired node count')

    args = parser.parse_args()

    update_eks_nodegroup_scaling(
		args.cluster,
        args.nodegroup,
        args.min,
        args.max,
        args.desired,
    )

if __name__ == "__main__":
    main()

