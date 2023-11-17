## titiler-pds

[titiler](https://github.com/developmentseed/titiler) application built specifically for AWS Public Data Set.

supported PDS:
- Landsat 8
- Sentinel 2 (COGS)
- NAIP

## Deploy

```bash
# Install AWS CDK requirements
$ pip install -e .["deploy"]

# Create AWS env
$ AWS_DEFAULT_REGION=us-west-2 AWS_REGION=us-west-2 cdk bootstrap

# Deploy app
$ AWS_DEFAULT_REGION=us-west-2 AWS_REGION=us-west-2 cdk deploy
```

## Testing it locally

### Using empty event (catches early errors)

   curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
