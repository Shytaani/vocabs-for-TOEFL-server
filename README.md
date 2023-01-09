# vocabs-for-TOEFL-server
## TODO
- Azure or AWSでバックエンドリソース作成
- IaCを実践する
- https://www.pulumi.com/

## Get Started
### <u>**AWS**</u>
1. Create a new stack
    ```bash
    pulumi stack init dev
    ```

2. Configure Credentials for Pulumi AWS provider

    See following pages:  
    - https://www.pulumi.com/registry/packages/aws/installation-configuration/#credentials  
    - https://www.pulumi.com/registry/packages/aws/installation-configuration/#configuration

3. Preview and deploy changes
    ```bash
    pulumi up
    ```
    If this error occured, follow the message and run the command in it, then rerun `pulumi up`.
    ```bash
    error: no resource plugin 'pulumi-resource-aws' found in the workspace at version v5.4.0 or on your $PATH, install the plugin using `pulumi plugin install resource aws v5.4.0`
    ```
### <u>**Azure**</u>
1. Create a new stack
    ```bash
    pulumi stack init dev
    ```

2. Configure Credentials for Pulumi Azure Native provider

    See: https://www.pulumi.com/registry/packages/azure-native/installation-configuration/#credentials

3. Configure Credentials for Pulumi Docker provider
    ```bash
    pulumi config set docker:host tcp://127.0.0.1:2376/
    ```

4. Preview and deploy changes
    ```bash
    pulumi up
    ```

**Appendix:** Destroy deployed resources
```bash
pulumi destroy -s dev
```
