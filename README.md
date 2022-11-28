# vocabs-for-TOEFL-server
## TODO
- Azure or AWSでバックエンドリソース作成
- IaCを実践する
- https://www.pulumi.com/

## Get Started
### <u>**Azure**</u>
1. Create a new stack
    ```bash
    pulumi stack init dev
    ```

2. Configure Credentials for Pulumi Azure Native provider

    See: https://www.pulumi.com/registry/packages/azure-native/installation-configuration/#credentials

3. Preview and deploy changes
    ```bash
    pulumi up
    ```

**Appendix:** Destroy deployed resources
```bash
pulumi destroy -s dev
```
