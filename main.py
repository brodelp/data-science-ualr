from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

from src.map_gen import state_tornado_path_map
from src.data_filtering import create_df
from src.helpers import get_tornado_data_path, get_usa_geojson_path

app = FastAPI()

data=create_df(data_path='data/1950-2019_all_tornadoes.csv')
geojson_path = 'data/us_states.json'

capital_dict = {}
with open('data/us_state_capitals.json') as f:
    cap: dict = json.load(f)
    for key, value in cap.items():
        capital_dict[key] = (float(value['lat']), float(value['long']))

@app.get("/")
async def fullscreen():
    """Simple example of a fullscreen map."""
    m = state_tornado_path_map(state='AR', year=2001, data=data, geojson_path=geojson_path, capital_locations=capital_dict)
    return HTMLResponse(m.get_root().render())

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