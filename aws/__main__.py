import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

config = pulumi.Config()
site_domain_name = config.get("siteDomainName")
container_port = config.get_int("containerPort", 80)
cpu = config.get_int("cpu", 512)
memory = config.get_int("memory", 128)

# A custom VPC contains resources
vpc = awsx.ec2.Vpc("vftsVPC",
    availability_zone_names=[
        "ap-northeast-1a",
        "ap-northeast-1c"])
pulumi.export("vpcId", vpc.vpc_id)
pulumi.export("publicSubnetIds", vpc.public_subnet_ids)
pulumi.export("privateSubnetIds", vpc.private_subnet_ids)

# An ECS cluster to deploy into
cluster = aws.ecs.Cluster("vftsCluster", name="vftsCluster")

# An ACM Certificate for the domain
certificate = aws.acm.Certificate("vftsCert",
    domain_name=site_domain_name,
    validation_method="DNS",
    opts=pulumi.ResourceOptions(
        delete_before_replace=True))

# An ALB to serve the container endpoint to the internet
loadbalancer = awsx.lb.ApplicationLoadBalancer("vftsLB",
    name="vftsLB",
    subnet_ids=vpc.public_subnet_ids)

# A Route53 public host zone
zone = aws.route53.Zone("vftsZone", name=certificate.domain_name)

# A DNS record to route traffic from the domain to a load balancer
loadbalancer_alias_record = aws.route53.Record("vftsLBAliasRecord",
    zone_id=zone.zone_id,
    name=certificate.domain_name,
    type="A",
    aliases=[aws.route53.RecordAliasArgs(
        name=loadbalancer.load_balancer.dns_name,
        zone_id=loadbalancer.load_balancer.zone_id,
        evaluate_target_health=True)])
pulumi.export("vftsLBAliasRecordFqdn", loadbalancer_alias_record.fqdn)

# A DNS record of a certificate's CNAME record
certificate_record = aws.route53.Record("vftsCertRecord",
    name=certificate.domain_validation_options[0].resource_record_name,
    records=[certificate.domain_validation_options[0].resource_record_value],
    ttl=60,
    type=certificate.domain_validation_options[0].resource_record_type,
    zone_id=zone.zone_id)

# A resource to run certificate validation
certificate_validation = aws.acm.CertificateValidation("vftsCertValidation",
    certificate_arn=certificate.arn,
    validation_record_fqdns=[
        loadbalancer_alias_record.fqdn,
        certificate.domain_validation_options[0].resource_record_name])

# A Listener for a load balancer to listen HTTPS requests from the Internet
listener = aws.lb.Listener("vftsLB-Listener",
        load_balancer_arn=loadbalancer.load_balancer.arn,
        port=443,
        protocol="HTTPS",
        ssl_policy="ELBSecurityPolicy-2016-08",
        certificate_arn=certificate.arn,
        default_actions=[aws.lb.ListenerDefaultActionArgs(
            type="forward",
            target_group_arn=loadbalancer.default_target_group.arn)],
        opts=pulumi.ResourceOptions(depends_on=certificate_validation))

# A certificate for a listener listening HTTPS requests from the Internet
listener_certificate = aws.lb.ListenerCertificate("vftsListenerCert",
    certificate_arn=certificate.arn,
    listener_arn=listener.arn)

pulumi.export("lb_vpcId", loadbalancer.vpc_id)
pulumi.export("load_balancer", loadbalancer.load_balancer)

# A Security Group to be attached to an ECS Service
security_group = aws.ec2.SecurityGroup("vftsSG",
    name="vftsSG",
    vpc_id=vpc.vpc_id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        description="Allow HTTP inbound traffic from LB",
        from_port=80,
        to_port=80,
        protocol="tcp",
        cidr_blocks=[vpc.vpc.cidr_block],
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

# The URL at which the container's HTTPS endpoint will be available
pulumi.export("url", pulumi.Output.concat("https://", site_domain_name))
