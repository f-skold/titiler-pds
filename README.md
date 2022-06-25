## titiler-pds

[titiler](https://github.com/developmentseed/titiler) application built specifically for AWS Public Data Set.

supported PDS:
- Landsat 8
- Sentinel 2 (COGS)
- NAIP

## Run locally

```
    uvicorn titiler_pds.main:app
```

## Deploy

```bash
sudo npm -g install aws-cdk@1.160.0
# Install AWS CDK requirements
$ pip install -e .["deploy"]

# Create AWS env
$ AWS_DEFAULT_REGION=us-west-2 AWS_REGION=us-west-2 cdk bootstrap

# Deploy app
$ AWS_DEFAULT_REGION=us-west-2 AWS_REGION=us-west-2 cdk deploy
```
