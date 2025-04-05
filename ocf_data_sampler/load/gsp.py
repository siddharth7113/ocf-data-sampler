"""Functions for loading GSP data."""

from importlib.resources import files

import pandas as pd
import xarray as xr
import numpy as np

def open_gsp(zarr_path: str) -> xr.DataArray:
    """Open the GSP data.

    Args:
        zarr_path: Path to the GSP zarr data

    Returns:
        xr.DataArray: The opened GSP data
    """
    ds = xr.open_dataset(zarr_path,engine="h5netcdf",storage_options={"anon": True})
    ds = xr.Dataset(
    {
        "generation_mw": (("datetime_gmt", "gsp_id"), np.expand_dims(ds["generation_mw"].values, axis=1)),  # Variable 1
        "capacity_mwp": (("datetime_gmt", "gsp_id"), np.expand_dims(ds["capacity_mwp"].values, axis=1))   # Variable 2
    },
    coords={
        "datetime_gmt": ds["datetime_gmt"].values,  # Assign coordinate values for dim1
        "gsp_id": [0]   # Assign coordinate values for dim2
    }
)

    ds = ds.rename({"datetime_gmt": "time_utc"})
    ds = ds.sortby("time_utc")

    # Load UK GSP locations
    df_gsp_loc = pd.read_csv(
        files("ocf_data_sampler.data").joinpath("uk_gsp_locations.csv"),
        index_col="gsp_id",
    )
    # slice to just the 0 gsp_id 
    df_gsp_loc = df_gsp_loc[:1]
    # Add locations and capacities as coordinates for each GSP and datetime
    ds = ds.assign_coords(
        x_osgb=(df_gsp_loc.x_osgb.to_xarray()),
        y_osgb=(df_gsp_loc.y_osgb.to_xarray()),
        # nominal_capacity_mwp=ds.installedcapacity_mwp,
        nominal_capacity_mwp=ds.capacity_mwp,
        effective_capacity_mwp=ds.capacity_mwp,
    )
    # print(ds.generation_mw)
    # print(ds.generation_mw["gsp_id"].values)
    return ds.generation_mw
