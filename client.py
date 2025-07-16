"""StealthMole API client implementation."""

import asyncio
import time
import uuid
from typing import Any, Dict, List, Optional

import httpx
import jwt
from pydantic import BaseModel


class StealthMoleConfig(BaseModel):
    """Configuration for StealthMole API."""

    access_key: str
    secret_key: str
    base_url: str = "https://api.stealthmole.com"
    timeout: float = 600.0
    download_timeout: float = 600.0
    max_retries: int = 3
    retry_delay: float = 1.0


class StealthMoleClient:
    """Client for interacting with StealthMole API."""

    def __init__(self, config: StealthMoleConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=self.config.timeout)
        self.download_client = httpx.AsyncClient(timeout=self.config.download_timeout)

    def _generate_jwt_token(self) -> str:
        """Generate JWT token for authentication."""
        payload = {
            "access_key": self.config.access_key,
            "nonce": str(uuid.uuid4()),
            "iat": int(time.time()),
        }
        return jwt.encode(payload, self.config.secret_key, algorithm="HS256")

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with JWT authentication."""
        token = self._generate_jwt_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make authenticated request to StealthMole API with retry logic."""
        url = f"{self.config.base_url}{endpoint}"

        for attempt in range(self.config.max_retries):
            try:
                headers = self._get_headers()
                response = await self.client.get(
                    url, headers=headers, params=params or {}
                )
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == self.config.max_retries - 1:
                    raise httpx.TimeoutException(
                        f"Request timed out after {self.config.max_retries} attempts: {str(e)}"
                    )
                await asyncio.sleep(self.config.retry_delay * (2**attempt))
            except httpx.HTTPStatusError as e:
                if (
                    e.response.status_code >= 500
                    and attempt < self.config.max_retries - 1
                ):
                    await asyncio.sleep(self.config.retry_delay * (2**attempt))
                    continue
                raise

    async def search_darkweb(
        self,
        indicator: str,
        text: str,
        target: str = "all",
        limit: int = 50,
        orderType: str = "createDate",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search dark web content."""
        valid_indicators = {
            "adsense",
            "analyticsid",
            "band",
            "bitcoin",
            "blueprint",
            "creditcard",
            "cve",
            "discord",
            "document",
            "domain",
            "email",
            "ethereum",
            "exefile",
            "facebook",
            "filehosting",
            "googledrive",
            "gps",
            "hash",
            "hashstring",
            "i2p",
            "i2purl",
            "id",
            "image",
            "instagram",
            "ioc",
            "ip",
            "kakaotalk",
            "keyword",
            "kssn",
            "leakedaudio",
            "leakedemailfile",
            "leakedvideo",
            "line",
            "linkedin",
            "malware",
            "monero",
            "otherfile",
            "pastebin",
            "pgp",
            "serverstatus",
            "session",
            "shorten",
            "sshkey",
            "sslkey",
            "tel",
            "telegram",
            "tor",
            "torurl",
            "twitter",
            "url",
        }

        if indicator not in valid_indicators:
            raise ValueError(
                f"Invalid indicator type: {indicator}. Valid types: {', '.join(sorted(valid_indicators))}"
            )

        if target == "all":
            endpoint = f"/v2/dt/search/{indicator}/target/all"
        else:
            endpoint = f"/v2/dt/search/{indicator}/target"
            params = {
                "targets": target,
                "text": text,
                "limit": limit,
                "orderType": orderType,
                "order": order,
            }
            return await self._make_request(endpoint, params)
        params = {"text": text, "limit": limit, "orderType": orderType, "order": order}
        return await self._make_request(endpoint, params)

    async def search_telegram(
        self,
        indicator: str,
        text: str,
        target: str = "all",
        limit: int = 50,
        orderType: str = "createDate",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search Telegram content."""
        valid_indicators = {
            "band",
            "bitcoin",
            "creditcard",
            "cve",
            "discord",
            "document",
            "domain",
            "email",
            "ethereum",
            "exefile",
            "facebook",
            "filehosting",
            "googledrive",
            "gps",
            "hash",
            "hashstring",
            "i2p",
            "i2purl",
            "id",
            "image",
            "instagram",
            "ip",
            "kakaotalk",
            "keyword",
            "kssn",
            "line",
            "monero",
            "otherfile",
            "pastebin",
            "pgp",
            "tel",
            "session",
            "shorten",
            "telegram",
            "telegram.channel",
            "telegram.message",
            "telegram.user",
            "tor",
            "torurl",
            "tox",
            "twitter",
            "url",
        }

        if indicator not in valid_indicators:
            raise ValueError(
                f"Invalid indicator type: {indicator}. Valid types: {', '.join(sorted(valid_indicators))}"
            )

        if target == "all":
            endpoint = f"/v2/tt/search/{indicator}/target/all"
        else:
            endpoint = f"/v2/tt/search/{indicator}/target"
            params = {
                "targets": target,
                "text": text,
                "limit": limit,
                "orderType": orderType,
                "order": order,
            }
            return await self._make_request(endpoint, params)
        params = {"text": text, "limit": limit, "orderType": orderType, "order": order}
        return await self._make_request(endpoint, params)

    async def search_credentials(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "leakedDate",
        order: str = "desc",
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Search for leaked credentials."""
        endpoint = "/v2/cl/search"
        params = {
            "query": indicator,
            "limit": limit,
            "cursor": cursor,
            "orderType": orderType,
            "order": order,
        }
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return await self._make_request(endpoint, params)

    async def search_ransomware(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "detectionTime",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search ransomware monitoring data."""
        endpoint = "/v2/rm/search"
        params = {
            "query": indicator,
            "limit": limit,
            "cursor": cursor,
            "orderType": orderType,
            "order": order,
        }
        return await self._make_request(endpoint, params)

    async def get_node_details(
        self,
        service: str,
        node_id: str,
        pid: Optional[str] = None,
        data_from: bool = False,
        include_url: bool = False,
        include_contents: bool = True,
    ) -> Dict[str, Any]:
        """Get detailed information about a specific node."""
        endpoint = f"/v2/{service}/node"
        params = {
            "id": node_id,
            "data_from": data_from,
            "include_url": include_url,
            "include_contents": include_contents,
        }
        if pid is not None:
            params["pid"] = pid
        return await self._make_request(endpoint, params)

    async def export_data(
        self, service: str, indicator: str, format: str = "json"
    ) -> Dict[str, Any]:
        """Export data in specified format."""
        endpoint = f"/v2/{service}/export"
        params = {"query": indicator, "exportType": format}
        return await self._make_request(endpoint, params)

    async def get_targets(self, service: str, indicator: str) -> Dict[str, Any]:
        """Get available targets for a service and indicator."""
        endpoint = f"/v2/{service}/search/{indicator}/targets"
        return await self._make_request(endpoint)

    async def search_compromised_dataset(
        self, indicator: str, limit: int = 50
    ) -> Dict[str, Any]:
        """Search compromised data set information."""
        endpoint = "/v2/cds/search"
        params = {"query": indicator, "limit": limit}
        return await self._make_request(endpoint, params)

    async def export_compromised_dataset(
        self, indicator: str, format: str = "json"
    ) -> Dict[str, Any]:
        """Export compromised data set as CSV/JSON."""
        endpoint = "/v2/cds/export"
        params = {"query": indicator, "exportType": format}
        return await self._make_request(endpoint, params)

    async def get_compromised_dataset_node(self, node_id: str) -> Dict[str, Any]:
        """Get detailed compromised data set node information (Cyber Security Edition required)."""
        endpoint = "/v2/cds/node"
        params = {"id": node_id}
        return await self._make_request(endpoint, params)

    async def search_combo_binder(
        self, indicator: str, limit: int = 50
    ) -> Dict[str, Any]:
        """Search leaked ID/Password combo information."""
        endpoint = "/v2/cb/search"
        params = {"query": indicator, "limit": limit}
        return await self._make_request(endpoint, params)

    async def export_combo_binder(
        self, indicator: str, format: str = "json"
    ) -> Dict[str, Any]:
        """Export combo binder data as CSV/JSON."""
        endpoint = "/v2/cb/export"
        params = {"query": indicator, "exportType": format}
        return await self._make_request(endpoint, params)

    async def search_ulp_binder(
        self, indicator: str, limit: int = 50
    ) -> Dict[str, Any]:
        """Search URL-Login-Password combination information."""
        endpoint = "/v2/ub/search"
        params = {"query": indicator, "limit": limit}
        return await self._make_request(endpoint, params)

    async def export_ulp_binder(
        self, indicator: str, format: str = "json"
    ) -> Dict[str, Any]:
        """Export ULP binder data as CSV/JSON."""
        endpoint = "/v2/ub/export"
        params = {"query": indicator, "exportType": format}
        return await self._make_request(endpoint, params)

    async def search_government_monitoring(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "detectionTime",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search government sector threat monitoring data."""
        endpoint = "/v2/gm/search"
        params = {
            "query": indicator,
            "limit": limit,
            "cursor": cursor,
            "orderType": orderType,
            "order": order,
        }
        return await self._make_request(endpoint, params)

    async def search_leaked_monitoring(
        self,
        indicator: str,
        limit: int = 50,
        cursor: int = 0,
        orderType: str = "detectionTime",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """Search enterprise sector threat monitoring data."""
        endpoint = "/v2/lm/search"
        params = {
            "query": indicator,
            "limit": limit,
            "cursor": cursor,
            "orderType": orderType,
            "order": order,
        }
        return await self._make_request(endpoint, params)

    async def download_file(self, service: str, file_hash: str) -> bytes:
        """Download file by hash from dt or tt service with extended timeout."""
        url = f"{self.config.base_url}/v2/api/file/{service}/f/{file_hash}"

        for attempt in range(self.config.max_retries):
            try:
                headers = self._get_headers()
                response = await self.download_client.get(url, headers=headers)
                response.raise_for_status()
                return response.content
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt == self.config.max_retries - 1:
                    raise httpx.TimeoutException(
                        f"File download timed out after {self.config.max_retries} attempts: {str(e)}"
                    )
                await asyncio.sleep(self.config.retry_delay * (2**attempt))
            except httpx.HTTPStatusError as e:
                if (
                    e.response.status_code >= 500
                    and attempt < self.config.max_retries - 1
                ):
                    await asyncio.sleep(self.config.retry_delay * (2**attempt))
                    continue
                raise

    async def search_pagination(
        self, service: str, search_id: str, cursor: int = 0, limit: int = 50
    ) -> Dict[str, Any]:
        """Pagination search using search ID for dt or tt service."""
        endpoint = f"/v2/{service}/search/{search_id}"
        params = {"cursor": cursor, "limit": limit}
        return await self._make_request(endpoint, params)

    async def get_user_quotas(self) -> Dict[str, Any]:
        """Get API usage quotas by service."""
        endpoint = "/v2/user/quotas"
        return await self._make_request(endpoint)

    async def close(self):
        """Close the HTTP clients."""
        await self.client.aclose()
        await self.download_client.aclose()
