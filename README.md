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

   # Done once
   # docker buildx build   --progress plain   -f Dockerfile -t titilerpds .
   docker build -f Dockerfile  -t titilerpds .
   docker run -p 9000:8080 titilerpds

### uvicorn

   docker run -p 9000:8080 -it  -v ~/.aws-lambda-rie:/aws-lambda -v ~/.aws:/root/.aws  --entrypoint bash   titilerpds -c \
   "python3 -m uvicorn titiler_pds.main:app  --host 0.0.0.0 --port 8080"

   date ; curl "http://localhost:9000/sn/sentinel/info?sceneid=S2A_33VXE_20230605_0_L2A"
   date ; curl "http://localhost:9000/sn/sentinel/tiles/9/281/154?sceneid=S2A_33VXE_20230605_0_L2A&bands=B04&bands=B08&bands=B03&rescale=118,666&rescale=97,3015&rescale=188,718"

## aws lambaric

   docker run -d -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 \
    -v "$PWD/mepsdata:/mepsdata" \
    --entrypoint /aws-lambda/aws-lambda-rie \
    titilerpds /usr/local/bin/python -m awslambdaric lambda_function.handler

### Using empty event (catches early errors)

   curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
