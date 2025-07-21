from typing import Any, Dict

from ._request import _make_request


async def export_data(
    service: str, indicator: str, format: str = "json"
) -> Dict[str, Any]:
    """Export data in specified format.

    Args:
        service (str): service name
        indicator (str): search query
        format (str, optional): export format, default is json

    Returns:
        Dict[str, Any]: export data
    """
    endpoint = f"/v2/{service}/export"
    params = {"query": indicator, "exportType": format}
    return await _make_request(endpoint, params)
