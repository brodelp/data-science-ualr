from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from src.map_gen import state_tornado_path_map, tornado_choropleth_map
from src.data_filtering import create_df, create_geo_df, create_tornado_count, create_merged_data
from src.helpers import get_tornado_data_path, get_usa_geojson_path

app = FastAPI()

templates = Jinja2Templates(directory="templates")

data=create_df(data_path='data/1950-2019_all_tornadoes.csv')
geo_data = create_geo_df('data/us_states.json')
geojson_path = 'data/us_states.json'

capital_dict = {}
with open('data/us_state_capitals.json') as f:
    cap: dict = json.load(f)
    for key, value in cap.items():
        capital_dict[key] = (float(value['lat']), float(value['long']))

@app.get("/api/fullscreen")
async def fullscreen():
    """Simple example of a fullscreen map."""
    m = state_tornado_path_map(state='AR', year=2001, data=data, geojson_path=geojson_path, capital_locations=capital_dict)
    return HTMLResponse(m.get_root().render())

@app.get("/api/iframe", response_class=HTMLResponse)
async def iframe(request: Request, state: str = 'TX', year: int = 2001):
    """Simple example of a fullscreen map."""
    m = state_tornado_path_map(state=state, year=year, data=data, geojson_path=geojson_path, capital_locations=capital_dict)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return templates.TemplateResponse(
        request=request, name='iframe.html', context={"iframe": iframe}
    )

@app.get("/api/map/country/fullscreen")
async def fullscreen():
    tornado_df = create_tornado_count(data=data, year=2001)
    merged_df = create_merged_data(tornado_count_df=tornado_df, geo_df=geo_data)
    m = tornado_choropleth_map(geojson_path=geojson_path, geo_df=merged_df, year=2001)

    return HTMLResponse(m.get_root().render())

@app.get("/api/map/country/iframe")
async def country_map(request: Request, year: int):
    tornado_df = create_tornado_count(data=data, year=year)
    merged_df = create_merged_data(tornado_count_df=tornado_df, geo_df=geo_data)
    m = tornado_choropleth_map(geojson_path=geojson_path, geo_df=merged_df)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return templates.TemplateResponse(
        request=request, name='iframe.html', context={"iframe": iframe}
    )

@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)