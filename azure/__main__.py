"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_docker as docker
from pulumi_azure_native import containerinstance
from pulumi_azure_native import containerregistry
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup('VFTS-RG',
    resource_group_name='VFTS-RG')

# Create an Azure Container Registry
registry = containerregistry.Registry('vftsRegistry',
    admin_user_enabled=True,
    registry_name='vftsRegistry',
    sku=containerregistry.SkuArgs(
        name=containerregistry.SkuName.BASIC
    ),
    resource_group_name=resource_group.name)

credentials = containerregistry.list_registry_credentials_output(registry.name, resource_group.name)

admin_username = credentials.username
admin_password = credentials.passwords[0]["value"]

pulumi.export("login_server", registry.login_server)
pulumi.export("admin_username", admin_username)
pulumi.export("admin_password", admin_password)

custom_image = "vfts"
docker_image = docker.Image(
    custom_image,
    image_name=registry.login_server.apply(
        lambda login_server: f"{login_server}/{custom_image}:v1.0.0"),
    build=docker.DockerBuild(context=f"./../{custom_image}"),
    registry=docker.ImageRegistry(
        server=registry.login_server,
        username=admin_username,
        password=admin_password
    ))

pulumi.export('image_name', docker_image.image_name)

# Create an Azure Container Instance
container_group = containerinstance.ContainerGroup("VFTS-CG",
    container_group_name="VFTS-CG",
    containers=[containerinstance.ContainerArgs(
        command=[],
        environment_variables=[],
        image=docker_image.image_name,
        name="vfts",
        ports=[containerinstance.ContainerPortArgs(
            port=80,
        )],
        resources=containerinstance.ResourceRequirementsArgs(
            requests=containerinstance.ResourceRequestsArgs(
                cpu=1,
                memory_in_gb=1.5,
            ),
        ),
    )],
    image_registry_credentials=[containerinstance.ImageRegistryCredentialArgs(
            server=registry.login_server,
            username=admin_username,
            password=admin_password
    )],
    os_type="Linux",
    resource_group_name=resource_group.name)
