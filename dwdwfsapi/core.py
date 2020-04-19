# -*- coding: utf-8 -*-

"""
Collection of the core functions needed to communicate with the geoserver
operated by the Deutscher Wetterdienst (DWD)

https://maps.dwd.de
"""

import urllib.parse
import requests

DEFAULT_WFS_VERSION = "2.0.0"
DEFAULT_WFS_REQUEST = "GetFeature"
DEFAULT_WFS_OUTPUTFORMAT = "application/json"


def query_dwd(**kwargs):
    """
    Retrive data from DWD server.
    """
    # Make all keys lowercase and escape all values
    kwargs = {k.lower(): urllib.parse.quote(v) for k, v in kwargs.items()}

    # Build the query
    query = "https://maps.dwd.de/geoserver/dwd/ows?service=WFS"
    if "version" in kwargs:
        query += f"&version={kwargs['version']}"
    else:
        query += f"&version={DEFAULT_WFS_VERSION}"
    if "request" in kwargs:
        query += f"&request={kwargs['request']}"
    else:
        query += f"&request={DEFAULT_WFS_REQUEST}"
    if "typename" in kwargs:
        query += f"&typeName={kwargs['typename']}"
    else:
        # Query doesn't make sense without typeName
        return None
    if "cql_filter" in kwargs:
        query += f"&CQL_FILTER={kwargs['cql_filter']}"
    if "outputformat" in kwargs:
        query += f"&OutputFormat={kwargs['outputformat']}"
    else:
        query += f"&OutputFormat={DEFAULT_WFS_OUTPUTFORMAT}"

    # Finally query the dwd geoserver
    try:
        resp = requests.get(query)
        if resp.status_code != 200:
            return None
        return resp.json()
    except: # pylint: disable=bare-except
        return None
