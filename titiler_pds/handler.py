"""AWS Lambda handler."""

import logging

from mangum import Mangum

from titiler_pds.main import app

logging.getLogger("mangum.lifespan").setLevel(logging.ERROR)
logging.getLogger("mangum.http").setLevel(logging.INFO)

handler = Mangum(app, lifespan="auto")
