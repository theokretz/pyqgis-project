# sentinel_hub.py
from qgis._core import QgsProject, QgsApplication, QgsMessageLog, Qgis
import matplotlib.pyplot as plt
import numpy as np
from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
    bbox_to_dimensions,
)
from qgis.core import QgsRasterLayer

config = SHConfig()

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

vienna_coords_wgs84 = (16.22, 48.15, 16.47, 48.32)
resolution = 60
vienna_bbox = BBox(bbox=vienna_coords_wgs84, crs=CRS.WGS84)
vienna_size = bbox_to_dimensions(vienna_bbox, resolution=resolution)

def plot_image(image, factor=1.0, clip_range=None):
    if clip_range:
        image = np.clip(image, clip_range[0], clip_range[1])
    plt.imshow(image * factor)
    plt.axis('off')
    plt.show()

def true_color_with_clouds(start_date, end_date):
    evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=(start_date, end_date),
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=vienna_bbox,
        size=vienna_size,
        config=config,
    )
    true_color_imgs = request_true_color.get_data()
    image = true_color_imgs[0]

    image_normalized = (image - image.min()) / (image.max() - image.min())
    image_brightened = image_normalized * 1.5
    image_brightened = np.clip(image_brightened, 0, 1)
    plot_image(image_brightened, factor=1.0)


def true_color_with_cloud_mask(start_date, end_date):
    evalscript_clm = """
    //VERSION=3
    function setup() {
      return {
        input: ["B02", "B03", "B04", "CLM"],
        output: { bands: 3 }
      }
    }

    function evaluatePixel(sample) {
      if (sample.CLM == 1) {
        return [0.75 + sample.B04, sample.B03, sample.B02]
      }
      return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
    }
    """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_clm,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=(start_date, end_date),
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=vienna_bbox,
        size=vienna_size,
        config=config,
    )
    data_with_cloud_mask_request = request_true_color.get_data(save_data=True)
    data_with_cloud_mask = data_with_cloud_mask_request[0]

    image_cloud_mask_normalized =(data_with_cloud_mask - data_with_cloud_mask.min()) / (data_with_cloud_mask.max() - data_with_cloud_mask.min())
    plot_image(image_cloud_mask_normalized)


def true_color_without_clouds(start_date, end_date):
    evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """
    request_true_color = SentinelHubRequest(
        data_folder="test_dir",
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=(start_date, end_date),
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=vienna_bbox,
        size=vienna_size,
        config=config,
    )

    image = request_true_color.get_data(save_data=True)[0]
    image_normalized = (image - image.min()) / (image.max() - image.min())
    image_brightened = image_normalized * 1.5
    image_brightened = np.clip(image_brightened, 0, 1)
    plot_image(image_brightened)


def import_into_qgis():
    # path to image, right now just a test path
    image_path = 'test_dir/c8088537648609eb3c59904559fcf26c/response.tiff'

    # load the raster layer into QGIS
    raster_layer = QgsRasterLayer(image_path, "Vienna Sentinel Image")
    if not raster_layer.isValid():
        QgsMessageLog.logMessage("Layer failed to load!", level=Qgis.Critical)
        print("File path:", image_path)
    else:
        QgsProject.instance().addMapLayer(raster_layer)