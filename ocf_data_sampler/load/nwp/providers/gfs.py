"""Open GFS Forecast data."""

import logging

import xarray as xr

from ocf_data_sampler.load.nwp.providers.utils import open_zarr_paths
from ocf_data_sampler.load.utils import check_time_unique_increasing, make_spatial_coords_increasing

_log = logging.getLogger(__name__)


def open_gfs(zarr_path: str | list[str]) -> xr.DataArray:
    """Opens the GFS data.

    Args:
        zarr_path: Path to the zarr to open

    Returns:
        Xarray DataArray of the NWP data
    """
    _log.info("Loading NWP GFS data")

    # Open data
    gfs: xr.Dataset = open_zarr_paths(zarr_path, time_dim="init_time_utc")
    # nwp: xr.DataArray = gfs.to_array()
    nwp: xr.DataArray = gfs.to_array(dim="channel")



    # Remap 0–360 longitude back to -180 to 180 to match POI inputs
    # This must be done before slicing! temp fix
    if (nwp.longitude > 180).any():
        print("Converting longitude from 0-360 to -180-180")
        nwp = nwp.assign_coords(longitude=(((nwp.longitude + 180) % 360) - 180))
        # nwp = nwp.sortby("longitude")
    del gfs

    # # nwp = nwp.rename({"variable": "channel","init_time": "init_time_utc"})
    # rename_dict = {"variable": "channel"}
    # if "init_time" in nwp.coords:
    #     rename_dict["init_time"] = "init_time_utc"  # If 'init_time' exists, rename it
    # nwp = nwp.rename(rename_dict)

    check_time_unique_increasing(nwp.init_time_utc)
    # Ensure longitude is in increasing order
    if not (nwp.longitude.values[0] < nwp.longitude.values[-1]):
        nwp = nwp.sortby("longitude")

    # Ensure latitude is in increasing order
    if not (nwp.latitude.values[0] < nwp.latitude.values[-1]):
        nwp = nwp.sortby("latitude")

    nwp = nwp.transpose("init_time_utc", "step", "channel", "latitude", "longitude")

    return nwp
