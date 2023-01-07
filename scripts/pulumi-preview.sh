#!/bin/bash

# exit if a command returns a non-zero exit code and also print the commands and their args as they are executed
set -e -x

# Add the pulumi CLI to the PATH
export PATH=$PATH:$HOME/.pulumi/bin

# Preview AWS resources
cd ./aws
pulumi stack select -s Tanishy/vocabs-for-TOEFL-server_aws/dev
# The following is just a sample config setting that the hypothetical pulumi
# program needs.
# Learn more about pulumi configuration at: https://www.pulumi.com/docs/intro/concepts/config/
pulumi config set aws:region ap-northeast-1
pulumi config set vocabs-for-TOEFL-server_aws:siteDomainName "vocabs-for-toefl.com"
pulumi preview

# # Preview Azure resources
# cd ./azure
# pulumi stack select -s Tanishy/vocabs-for-TOEFL-server_azure/dev
# # The following is just a sample config setting that the hypothetical pulumi
# # program needs.
# # Learn more about pulumi configuration at: https://www.pulumi.com/docs/intro/concepts/config/
# pulumi config set azure-native:location japaneast
# pulumi config set azure-native:clientId $AZURE_CLIENT_ID
# pulumi config set azure-native:clientSecret $AZURE_CLIENT_SECRET --secret
# pulumi config set azure-native:tenantId $AZURE_TENANT_ID
# pulumi config set azure-native:subscriptionId $AZURE_SUBSCRIPTION_ID
# pulumi config set docker:host tcp://127.0.0.1:2376/
# pulumi preview