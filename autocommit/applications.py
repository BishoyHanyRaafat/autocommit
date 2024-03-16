import platform
from .config import api_client,pos_client
import json
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
def get_application() -> pos_client.Application:
    well_known_instance = pos_client.WellKnownApi(api_client)

    # Make Sure Server is Running and Get Version
    version = well_known_instance.get_well_known_version()

    # Decide if it's Windows, Mac, Linux or Web
    local_os = categorize_os()

    # Check the database for an existing application
    application_id = "DEFAULT"  # Replace with a default application ID

    application = pos_client.Application(id=application_id, name="OPEN_SOURCE", version=version, platform=local_os, onboarded=False, privacy="OPEN")
    
    return application

def is_registered():
    applications_api = pos_client.ApplicationsApi(api_client)

    apps_raw = applications_api.applications_snapshot()
    apps_json = json.loads(apps_raw.json())["iterable"]
    for app in apps_json:
        if app["name"] == "OPEN_SOURCE":
            return True
    return False

def register_application():
    """Register an application if it is not registered"""
    applications_api = pos_client.ApplicationsApi(api_client)

    if not is_registered():
        application = get_application()
        api_response = applications_api.applications_register(application=application)
        return api_response


