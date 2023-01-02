#!/bin/bash

# exit if a command returns a non-zero exit code and also print the commands and their args as they are executed
set -e -x

# Add the pulumi CLI to the PATH
export PATH=$PATH:$HOME/.pulumi/bin

cd ./aws

pulumi stack select -s Tanishy/vocabs-for-TOEFL-server_aws/dev
# The following is just a sample config setting that the hypothetical pulumi
# program needs.
# Learn more about pulumi configuration at: https://www.pulumi.com/docs/intro/concepts/config/
pulumi config set aws:region ap-northeast-1
pulumi config set vocabs-for-TOEFL-server_aws:siteDomainName "vocabs-for-toefl.com"
# pulumi config set azure-native:location japaneast
pulumi up --yes