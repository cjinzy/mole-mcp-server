import asyncio
import os
import time
import uuid
from typing import Any, Dict, Optional

import httpx
import jwt
from dotenv import load_dotenv

load_dotenv()

# Global configuration
BASE_URL = "https://api.stealthmole.com"
TIMEOUT = 600.0
DOWNLOAD_TIMEOUT = 600.0
MAX_RETRIES = 10
RETRY_DELAY = 1.0


async def _make_request(endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated request to StealthMole API with retry logic."""
    url = f"{BASE_URL}{endpoint}"

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for attempt in range(MAX_RETRIES):
            try:
                headers = _get_headers()
                response = await client.get(url, headers=headers, params=params or {})
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == MAX_RETRIES - 1:
                    raise httpx.TimeoutException(
                        f"Request timed out after {MAX_RETRIES} attempts: {str(e)}"
                    )
                await asyncio.sleep(RETRY_DELAY * (2**attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (2**attempt))
                    continue
                raise

    # This should never be reached due to the raise statements above
    raise RuntimeError("Request failed after all retry attempts")


async def _download_file(service: str, file_hash: str) -> bytes:
    """Download file by hash from dt or tt service with extended timeout."""
    url = f"{BASE_URL}/v2/api/file/{service}/f/{file_hash}"

    async with httpx.AsyncClient(timeout=DOWNLOAD_TIMEOUT) as client:
        for attempt in range(MAX_RETRIES):
            try:
                headers = _get_headers()
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.content
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == MAX_RETRIES - 1:
                    raise httpx.TimeoutException(
                        f"File download timed out after {MAX_RETRIES} attempts: {str(e)}"
                    )
                await asyncio.sleep(RETRY_DELAY * (2**attempt))
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (2**attempt))
                    continue
                raise

    # This should never be reached due to the raise statements above
    raise RuntimeError("File download failed after all retry attempts")


def _generate_jwt_token() -> str:
    """Generate JWT token for authentication."""
    access_key = os.getenv("STEALTHMOLE_ACCESS_KEY", "")
    secret_key = os.getenv("STEALTHMOLE_SECRET_KEY", "")
    
    if not access_key or not secret_key:
        raise ValueError("STEALTHMOLE_ACCESS_KEY and STEALTHMOLE_SECRET_KEY environment variables are required")
    
    payload = {
        "access_key": access_key,
        "nonce": str(uuid.uuid4()),
        "iat": int(time.time()),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def _get_headers() -> Dict[str, str]:
    """Get headers with JWT authentication."""
    token = _generate_jwt_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
