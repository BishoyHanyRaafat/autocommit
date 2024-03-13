import pieces_os_client as pos_client
import platform
from urllib import request
import json

platform_info = platform.platform()
if 'Linux' in platform_info:
    port = 5323
else:
    port = 1000

# Defining the host is optional and defaults to http://localhost:1000
# See configuration.py for a list of all supported configuration parameters.
configuration = pos_client.Configuration(host=f"http://localhost:{port}")

# Initialize the ApiClient globally
api_client = pos_client.ApiClient(configuration)



# Models
# api_instance = pos_client.ModelsApi(api_client)
# api_response = api_instance.models_snapshot()
# print(api_response.json())
# models = {model.name: {"uuid":model.id,"word_limit":model.max_tokens.input} for model in api_response.iterable if model.cloud or model.downloading} 
response = request.urlopen('http://localhost:1000/models').read()
response = json.loads(response)["iterable"]
models = {model["name"]:{"uuid":model["id"] ,"word_limit" :model["maxTokens"]["input"]} for model in response if model["cloud"] or model["downloading"]} # getting the models that are available in the cloud or is downloaded
default_model_name = "GPT-3.5-turbo Chat Model"
model_id = models[default_model_name]["uuid"] # default model id
word_limit = models[default_model_name]["word_limit"]
