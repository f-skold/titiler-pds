"""Landsat endpoint."""

from rio_tiler_pds.landsat.aws.landsat_collection2 import LandsatC2Reader

from titiler.core.dependencies import BandsExprParams
from titiler.core.factory import MultiBandTilerFactory
from titiler.core.routing import apiroute_factory
from titiler.mosaic.factory import MosaicTilerFactory

from ..dependencies import CustomPathParams, MosaicParams

from fastapi import APIRouter

route_class = apiroute_factory(
    {
        # IMPORTANT Landsat collection 2 is stored in a REQUESTER-PAYS bucket
        "AWS_REQUEST_PAYER": "requester",
    }
)

scenes = MultiBandTilerFactory(  # type: ignore
    reader=LandsatC2Reader,
    path_dependency=CustomPathParams,
    router_prefix="scenes/landsat",
    router=APIRouter(route_class=route_class),
)

mosaicjson = MosaicTilerFactory(  # type: ignore
    path_dependency=MosaicParams,
    dataset_reader=LandsatC2Reader,
    layer_dependency=BandsExprParams,
    router_prefix="mosaicjson/landsat",
    router=APIRouter(route_class=route_class),
)
