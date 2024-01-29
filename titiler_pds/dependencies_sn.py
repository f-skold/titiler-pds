"""custom skridskonet app dependencies."""

from dataclasses import dataclass  # field
from typing import Dict, Optional  # Sequence

from fastapi import Query  # HTTPException

from titiler.core.dependencies import DefaultDependency

#         "aws_region": "eu-north-1",
reader_params = {
    "bucket": "requester-pays-sn-sat",
    "reader_options": {
        "request_pays": True,
    },
}


def get_reader_params() -> Dict:
    """Function returning reader params"""
    return reader_params


@dataclass
class MyReaderParams2(DefaultDependency):
    """Contains s3 bucket and prefix_pattern"""

    bucket: Optional[str] = Query(
        default="requester-pays-sn-sat",
        title="bucket name",
        description="S3 bucket name.",
        include_in_schema=False,
    )

    # prefix_pattern: Optional[str] = "sentinel-s2-l2a-cogs/"
    def __post_init__(self):
        """post init, trying to set bucket name"""
        name = "requester-pays-sn-sat"
        if self.bucket is not None:
            name = self.bucket  # noqa: F841
        # self.kwargs["bucket"] = name
