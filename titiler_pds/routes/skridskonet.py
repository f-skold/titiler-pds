"""Skridskonet Sentinel endpoint."""

from fastapi import APIRouter
from rio_tiler_pds.sentinel.aws import S2COGReader

from titiler.core.dependencies import BandsExprParams
from titiler.core.factory import MultiBandTilerFactory
from titiler.core.routing import apiroute_factory
from titiler.mosaic.factory import MosaicTilerFactory

from ..dependencies import CustomPathParams, MosaicParams
from ..dependencies_sn import get_reader_params

route_class = apiroute_factory({"AWS_NO_SIGN_REQUEST": "YES"})


sn_scenes = MultiBandTilerFactory(
    reader=S2COGReader,
    path_dependency=CustomPathParams,
    reader_dependency=get_reader_params,
    router_prefix="sn/sentinel",
    router=APIRouter(route_class=route_class),
)

if False:
    mosaicjson = MosaicTilerFactory(
        path_dependency=MosaicParams,
        dataset_reader=S2COGReader,
        layer_dependency=BandsExprParams,
        router_prefix="mosaicjson/sentinel",
        # router=APIRouter(route_class=route_class),
    )
