import platform
from .config import api_client,pos_client
from . import __version__

application = None

def categorize_os():
    # Get detailed platform information
    platform_info = platform.platform()

    # Categorize the platform information into one of the four categories
    if 'Windows' in platform_info:
        os_info = 'WINDOWS'
    elif 'Linux' in platform_info:
        os_info = 'LINUX'
    elif 'Darwin' in platform_info:  # Darwin is the base of macOS
        os_info = 'MACOS'
    else:
        os_info = 'WEB'  # Default to WEB if the OS doesn't match others

    return os_info
def connect_api() -> pos_client.Application:
    global application
    # Decide if it's Windows, Mac, Linux or Web
    local_os = categorize_os()


    api_instance = pos_client.ConnectorApi(api_client)
    seeded_connector_connection = pos_client.SeededConnectorConnection(
        application=pos_client.SeededTrackedApplication(
            name = pos_client.ApplicationNameEnum.OPEN_SOURCE,
            platform = local_os,
            version = __version__))
    api_response = api_instance.connect(seeded_connector_connection=seeded_connector_connection)
    application =  api_response.application


