"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_docker as docker
# from pulumi_azure_native import containerinstance
from pulumi_azure_native import web
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
    build=docker.DockerBuild(
        context=f"./../{custom_image}",
        extra_options=["--platform", "linux/amd64"]),
    registry=docker.ImageRegistry(
        server=registry.login_server,
        username=admin_username,
        password=admin_password
    ))

pulumi.export('image_name', docker_image.image_name)

# Create App Service Plan
plan = web.AppServicePlan(
    "vftsPlan",
    name="vftsPlan",
    resource_group_name=resource_group.name,
    kind="Linux",
    reserved=True,
    sku=web.SkuDescriptionArgs(
        name="B1",
        tier="Basic",
    )
)
# Run a container on App Service
app = web.WebApp(
    "vfts-app",
    name="vocabs-for-TOEFL",
    resource_group_name=resource_group.name,
    server_farm_id=plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(name="WEBSITES_ENABLE_APP_SERVICE_STORAGE", value="false"),
            web.NameValuePairArgs(name="DOCKER_REGISTRY_SERVER_URL",
                                  value=registry.login_server.apply(
                                      lambda login_server: f"https://{login_server}")),
            web.NameValuePairArgs(name="DOCKER_REGISTRY_SERVER_USERNAME",
                                  value=admin_username),
            web.NameValuePairArgs(name="DOCKER_REGISTRY_SERVER_PASSWORD",
                                  value=admin_password),
            web.NameValuePairArgs(name="WEBSITES_PORT", value="8080"),
        ],
        always_on=True,
        linux_fx_version=docker_image.image_name.apply(lambda image_name: f"DOCKER|{image_name}"),
    ),
    https_only=True)

pulumi.export(
    "appEndpoint",
    app.default_host_name.apply(lambda default_host_name: f"https://{default_host_name}"))

# Create an Azure Container Instance
# container_group = containerinstance.ContainerGroup("VFTS-CG",
#     container_group_name="VFTS-CG",
#     containers=[containerinstance.ContainerArgs(
#         command=[],
#         environment_variables=[],
#         image=docker_image.image_name,
#         name="vfts",
#         ports=[containerinstance.ContainerPortArgs(
#             port=80,
#         )],
#         resources=containerinstance.ResourceRequirementsArgs(
#             requests=containerinstance.ResourceRequestsArgs(
#                 cpu=1,
#                 memory_in_gb=1.5,
#             ),
#         ),
#     )],
#     image_registry_credentials=[containerinstance.ImageRegistryCredentialArgs(
#             server=registry.login_server,
#             username=admin_username,
#             password=admin_password
#     )],
#     os_type="Linux",
#     resource_group_name=resource_group.name)
