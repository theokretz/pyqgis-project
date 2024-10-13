# Bachelor's Thesis Project

This PyQGIS project was developed as part of my bachelor's thesis.

## Current Features

- Returns a True Color Image of Vienna for a specific time frame using Sentinel Hub.
- Downloads the True Color Image in preferred file format.

## Installation

1. Open QGIS
2. Install [Sentinel Hub Python package](https://pypi.org/project/sentinelhub/) via OsGeo4W Shell:
```bash
pip install sentinelhub
```
3. Create a [Sentinel Hub Account](https://www.sentinel-hub.com/)
4. Add credentials to C:\Users\User\.config\sentinelhub\config.toml

```toml
[default-profile]
instance_id = "instance_id"
sh_client_id = "sh_client_id"
sh_client_secret = "sh_client_secret"
```
5. Run main.py inside QGIS

## Acknowledgements
This project uses code from the [Sentinel Hub Python package documentation](https://sentinelhub-py.readthedocs.io/en/latest/examples/process_request.html).
