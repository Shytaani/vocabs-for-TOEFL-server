import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

config = pulumi.Config()
container_port = config.get_int("containerPort", 80)
cpu = config.get_int("cpu", 512)
memory = config.get_int("memory", 128)

# A custom VPC contains resources
vpc = awsx.ec2.Vpc("vftsVPC")
pulumi.export("vpcId", vpc.vpc_id)
pulumi.export("publicSubnetIds", vpc.public_subnet_ids)
pulumi.export("privateSubnetIds", vpc.private_subnet_ids)

# An ECS cluster to deploy into
cluster = aws.ecs.Cluster("vftsCluster",
    name="vftsCluster")

# An ALB to serve the container endpoint to the internet
loadbalancer = awsx.lb.ApplicationLoadBalancer("vftsLB",
    awsx.lb.ApplicationLoadBalancerArgs(
        name="vftsLB",
        subnet_ids=vpc.public_subnet_ids))
pulumi.export("lb_vpcId", loadbalancer.vpc_id)
pulumi.export("load_balancer", loadbalancer.load_balancer)

# A Security Group to be attached to an ECS Service
security_group = aws.ec2.SecurityGroup("vftsSG",
    name="vftsSG",
    vpc_id=vpc.vpc_id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        description="Allow inbound traffic from LB",
        from_port=80,
        to_port=80,
        protocol="tcp",
        cidr_blocks=["10.0.0.0/16"],
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        description="Allow all outbound traffic",
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"],
    )])

# An ECR repository to store our application's container image
repo = awsx.ecr.Repository("vftsRepo",
    name="vftsrepo",
    force_delete=True)

# Build and publish our application's container image from ./app to the ECR repository
image = awsx.ecr.Image(
    "vftsImage",
    repository_url=repo.url,
    path="./../vfts",
    extra_options=["--platform", "linux/amd64"])

# Deploy an ECS Service on Fargate to host the application container
service = awsx.ecs.FargateService("vftsService",
    name="vftsService",
    cluster=cluster.arn,
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
        subnets=vpc.private_subnet_ids,
        security_groups=[security_group.id],
    ),
    task_definition_args=awsx.ecs.FargateServiceTaskDefinitionArgs(
        container=awsx.ecs.TaskDefinitionContainerDefinitionArgs(
            image=image.image_uri,
            cpu=cpu,
            memory=memory,
            essential=True,
            port_mappings=[awsx.ecs.TaskDefinitionPortMappingArgs(
                container_port=container_port,
                target_group=loadbalancer.default_target_group,
            )],
        ),
    ))
pulumi.export("taskDefinition", service.task_definition)

# The URL at which the container's HTTP endpoint will be available
pulumi.export("url", pulumi.Output.concat("http://", loadbalancer.load_balancer.dns_name))
