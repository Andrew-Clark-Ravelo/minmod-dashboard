import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import dash_bootstrap_components as dbc
from dash import dcc


# a function to safely load WKT strings to geometry objects
def safe_wkt_load(wkt_str):
    try:
        return loads(wkt_str)
    except Exception as e:
        print(f"Error loading WKT: {e}")
        return None


def get_geo_model(gm):

    # Apply the function to convert WKT strings to geometry objects
    gm.df["geometry"] = gm.df["loc_wkt.value"].apply(safe_wkt_load)
    gdf = gpd.GeoDataFrame(gm.df, geometry="geometry", crs="epsg:4326")
    gdf = gdf.dropna(subset=["geometry"])

    # Ensure all geometries are Points (if not, convert them to Points using centroid)
    gdf["geometry"] = gdf["geometry"].apply(
        lambda geom: geom if geom.geom_type == "Point" else geom.centroid
    )

    # removing any rows where the geometry conversion has failed (i.e., NaN in 'lon' or 'lat')
    gdf = gdf[~gdf["geometry"].isna()]

    # Extracting longitude and latitude
    gdf["lon"] = gdf["geometry"].x
    gdf["lat"] = gdf["geometry"].y

    # invalid_geo_df = gdf[~gdf["lat"].between(-90, 90) | ~gdf["lon"].between(-180, 180)]
    gdf = gdf[(gdf["lat"].between(-90, 90)) & (gdf["lon"].between(-180, 180))]

    gm.set_gdf(gdf)

    geo_model = px.scatter_mapbox(
        gdf,
        lat="lat",
        lon="lon",
        hover_name="name.value",
        zoom=2,
        height=900,
    )

    # Setting Map Style
    geo_model.update_layout(mapbox_style="open-street-map")
    # geo_model.update_layout(
    #     mapbox_style="white-bg",
    #     mapbox_layers=[
    #         {
    #             "below": "traces",
    #             "sourcetype": "raster",
    #             "sourceattribution": "United States Geological Survey",
    #             "source": [
    #                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    #             ],
    #         }
    #     ],
    # )
    geo_model.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 10})

    return geo_model


def geo_model_card(geo_min):
    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="clickable-geo-plot",
                    figure=get_geo_model(geo_min),
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "responsive": True,
                    },
                ),
            ]
        )
    )
