from typing import Any, Dict

from src.tools._request import _make_request


async def get_user_quotas() -> Dict[str, Any]:
    """Get API usage quotas by service."""
    endpoint = "/v2/user/quotas"
    return await _make_request(endpoint)
