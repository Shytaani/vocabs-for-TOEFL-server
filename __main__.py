"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_docker as docker
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi_azure_native import containerregistry
from pulumi_azure_native import containerinstance

# Create an Azure Resource Group
resource_group = resources.ResourceGroup('VFTS-RG',
    resource_group_name='VFTS-RG')

# Create an Azure resource (Storage Account)
account = storage.StorageAccount('vftssa',
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2)

# Export the primary key of the Storage Account
primary_key = pulumi.Output.all(resource_group.name, account.name) \
    .apply(lambda args: storage.list_storage_account_keys(
        resource_group_name=args[0],
        account_name=args[1]
    )).apply(lambda accountKeys: accountKeys.keys[0].value)

pulumi.export("primary_storage_key", primary_key)

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
admin_password = credentials.passwards[0]["value"]

custom_image = "vfts"
docker_image = docker.Image(
    custom_image,
    image_name=registry.login_server.apply(
        lambda login_server: f"{login_server}/{custom_image}:v1.0.0"),
    build=docker.DockerBuild(context=f"./{custom_image}"),
    registry=docker.ImageRegistry(
        server=registry.login_server,
        username=admin_username,
        password=admin_password
    ))

# Create an Azure Container Instance
container_group = containerinstance.ContainerGroup("VFTS-CG",
    container_group_name="VFTS-CG",
    containers=[containerinstance.ContainerArgs(
        command=[],
        environment_variables=[],
        image=f"{custom_image}",
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
    os_type="Linux",
    resource_group_name=resource_group.name)
