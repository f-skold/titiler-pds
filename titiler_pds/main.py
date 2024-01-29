"""titiler-pds app."""

import logging

from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from tilebench.middleware import VSIStatsMiddleware

from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.core.middleware import CacheControlMiddleware, TotalTimeMiddleware

from .routes import landsat_collection2, naip, sentinel, skridskonet
from .settings import api_config

logs = [
    "asyncio",
    "boto3.resources",
    "boto3",
    "botocore.auth",
    "botocore.awsrequest",
    "botocore.endpoint_provider",
    "botocore.endpoint",
    "botocore.handlers",
    "botocore.loaders",
    "botocore.regions",
    "botocore.response",
    "botocore.retries.adaptive",
    "botocore.retries.special",
    "botocore.retries.standard",
    "botocore.retries",
    "botocore.retryhandler" "botocore.session",
    "botocore.tokens",
    "botocore.utils",
    "botocore",
    "fastapi",
    "rasterio.io",
    "rasterio",
    "rasterio._base",
    "rasterio._env",
    "rasterio._err",
    "rio-tiler",
]

if False:
    # turn off or quiet logs
    logging.getLogger("botocore.credentials").disabled = True
    logging.getLogger("botocore.utils").disabled = True
    # logging.getLogger("rio-tiler").setLevel(logging.ERROR)
    logging.getLogger("rio-tiler").setLevel(logging.DEBUG)
else:
    logging.getLogger("botocore.credentials").disabled = False
    logging.getLogger("botocore.credentials").setLevel(logging.DEBUG)
    logging.getLogger("botocore.utils").disabled = False
    logging.getLogger("botocore.utils").setLevel(logging.DEBUG)
    # logging.getLogger("rio-tiler").setLevel(logging.ERROR)
    logging.getLogger("rio-tiler").setLevel(logging.DEBUG)
    for name in logs:
        logger = logging.getLogger(name)
        # logger.disabled = False
        logger.setLevel(logging.DEBUG)
    if False:
        print(f"Enabled logs for: {logs}")

app = FastAPI(title="titiler-pds", version="0.1.0")


print("LOGGING")
logger_names = [
    "gunicorn.access",
    "gunicorn.error",
    "rio-tiler",
    "uvicorn.access",
    "uvicorn.error",
]
if False:
    logger_names += list(logging.root.manager.loggerDict.keys())
print(logger_names)

some_exceptions = {
    key: value
    for key, value in DEFAULT_STATUS_CODES.items()
    if value != status.HTTP_500_INTERNAL_SERVER_ERROR
}
add_exception_handlers(app, some_exceptions)
if api_config.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

app.add_middleware(BrotliMiddleware, minimum_size=0, gzip_fallback=True)
app.add_middleware(CacheControlMiddleware, cachecontrol=api_config.cachecontrol)

if api_config.debug:
    app.add_middleware(TotalTimeMiddleware)

if api_config.vsi_stats:
    app.add_middleware(VSIStatsMiddleware)

app.include_router(
    landsat_collection2.scenes.router, prefix="/scenes/landsat", tags=["Landsat"]
)
app.include_router(
    landsat_collection2.mosaicjson.router,
    prefix="/mosaicjson/landsat",
    tags=["Landsat"],
)

app.include_router(
    sentinel.scenes.router, prefix="/scenes/sentinel", tags=["Sentinel 2 COG"]
)
app.include_router(
    sentinel.mosaicjson.router, prefix="/mosaicjson/sentinel", tags=["Sentinel 2 COG"]
)

# NAIP tiler is a regular tiler with requester-pays set
app.include_router(naip.mosaicjson.router, prefix="/mosaicjson/naip", tags=["NAIP"])

if True:
    app.include_router(
        skridskonet.sn_scenes.router, prefix="/sn/sentinel", tags=["Sentinel 2 SN-COG"]
    )
    # app.include_router(skridskonet.mosaicjson.router, prefix="/mosaicjson/sentinel", tags=["Sentinel 2 COG"])


@app.get("/healtz", description="Health Check", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}
