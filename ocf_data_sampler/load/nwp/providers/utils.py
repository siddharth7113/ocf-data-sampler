"""Utility functions for the NWP data processing."""

import xarray as xr
import fsspec

def open_zarr_paths(zarr_path: str | list[str], time_dim: str = "init_time") -> xr.Dataset:
    """Opens the NWP data with forced anonymous S3 access."""

    if isinstance(zarr_path, (list, tuple)) or "*" in str(zarr_path):  # Multi-file dataset
        ds = xr.open_mfdataset(
            [fsspec.get_mapper(path, anon=True) for path in zarr_path],  # Force anonymous access
            engine="zarr",
            concat_dim=time_dim,
            combine="nested",
            chunks="auto",
        ).sortby(time_dim)
    else:
        ds = xr.open_dataset(
            fsspec.get_mapper(zarr_path, anon=True),  # Force anonymous access
            engine="zarr",
            consolidated=True,
            mode="r",
            chunks="auto",
        )
    return ds

