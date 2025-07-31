"""StealthMole MCP Server implementation."""

import asyncio
import os
import sys
from typing import Any, Optional, Sequence

from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)
from pydantic import AnyUrl

from .tools import *

load_dotenv()

prompts_path = os.path.join(os.path.dirname(__file__), "prompt")

server: Server = Server(
    "stealthmole-mcp",
    "250715",
)


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return []


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a specific resource."""
    raise ValueError(f"Unknown resource: {uri}")


@server.list_prompts()
async def handle_list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="stealthmole_default_prompt",
            description="Default behavior guidelines for StealthMole MCP",
            arguments=[
                PromptArgument(
                    name="context",
                    description="Current search context",
                    required=False,
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    """Get a specific prompt."""
    if name == "stealthmole_default_prompt":
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="assistant",
                    content=TextContent(
                        type="text",
                        text=open(f"{prompts_path}/default_prompt.md").read(),
                    ),
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available StealthMole tools."""
    try:
        print("Returning StealthMole tools list", file=sys.stderr)
        return [
            Tool(
                name="search_darkweb",
                description="Search dark web content for indicators like domains, IPs, emails, etc.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "The indicator type to search for",
                            "enum": [
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
                                "iol",
                            ],
                        },
                        "text": {
                            "type": "string",
                            "description": "Search keyword or data to find. Supports AND, OR, NOT operators (max 3 OR, 5 total operators)",
                        },
                        "target": {
                            "type": "string",
                            "description": "Target type to search (default: 'all'). Use comma-separated values for multiple targets",
                            "default": "all",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                        "orderType": {
                            "type": "string",
                            "description": "Ordering type",
                            "enum": ["createDate", "value"],
                            "default": "createDate",
                        },
                        "order": {
                            "type": "string",
                            "description": "Sort order",
                            "enum": ["asc", "desc"],
                            "default": "desc",
                        },
                    },
                    "required": ["indicator", "text"],
                },
            ),
            Tool(
                name="search_telegram",
                description="Search Telegram content for indicators",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "The indicator type to search for",
                            "enum": [
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
                            ],
                        },
                        "text": {
                            "type": "string",
                            "description": "Search keyword or data to find. Supports AND, OR, NOT operators (max 3 OR, 5 total operators)",
                        },
                        "target": {
                            "type": "string",
                            "description": "Target type to search (default: 'all'). Use comma-separated values for multiple targets",
                            "default": "all",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                        "orderType": {
                            "type": "string",
                            "description": "Ordering type",
                            "enum": ["createDate", "value"],
                            "default": "createDate",
                        },
                        "order": {
                            "type": "string",
                            "description": "Sort order",
                            "enum": ["asc", "desc"],
                            "default": "desc",
                        },
                    },
                    "required": ["indicator", "text"],
                },
            ),
            Tool(
                name="search_credentials",
                description="Search for leaked credentials using keywords or specific indicators (domain:, email:, id:, password:, after:, before:)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "Search query - can use indicators like 'domain:example.com', 'email:user@domain.com', 'id:username', 'password:pass123', 'after:2023-01', 'before:2024-01' or plain keywords",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                        "cursor": {
                            "type": "integer",
                            "description": "Pagination cursor (default: 0)",
                            "default": 0,
                            "minimum": 0,
                        },
                        "orderType": {
                            "type": "string",
                            "description": "Order type",
                            "enum": [
                                "LeakedDate",
                                "domain",
                                "email",
                                "password",
                                "LeakedFrom",
                            ],
                            "default": "LeakedDate",
                        },
                        "order": {
                            "type": "string",
                            "description": "Sort order",
                            "enum": ["asc", "desc"],
                            "default": "desc",
                        },
                        "start": {
                            "type": "integer",
                            "description": "Filter data added to the system after start time (UTC timestamp)",
                        },
                        "end": {
                            "type": "integer",
                            "description": "Filter data added to the system before end time (UTC timestamp)",
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="search_ransomware",
                description="Search ransomware monitoring data using torurl: or domain: indicators",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "Search query - use 'torurl:site.onion' to search ransomware sites or 'domain:victim.com' to search victim websites. Leave empty for recent list.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                        "cursor": {
                            "type": "integer",
                            "description": "Pagination cursor (default: 0)",
                            "default": 0,
                            "minimum": 0,
                        },
                        "orderType": {
                            "type": "string",
                            "description": "Order type",
                            "enum": ["detectionTime", "victim", "attackGroup"],
                            "default": "detectionTime",
                        },
                        "order": {
                            "type": "string",
                            "description": "Sort order",
                            "enum": ["asc", "desc"],
                            "default": "desc",
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="get_node_details",
                description="Get detailed information about a specific node",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service type (dt, tt, cl, rm, etc.)",
                        },
                        "node_id": {
                            "type": "string",
                            "description": "Node ID to get details for",
                        },
                        "pid": {
                            "type": "string",
                            "description": "Parent node ID (optional)",
                        },
                        "data_from": {
                            "type": "boolean",
                            "description": "Import data source list (default: False)",
                            "default": False,
                        },
                        "include_url": {
                            "type": "boolean",
                            "description": "Import included URL list (default: False)",
                            "default": False,
                        },
                        "include_contents": {
                            "type": "boolean",
                            "description": "Include HTML source contents for torurl, i2purl, url (default: True)",
                            "default": True,
                        },
                    },
                    "required": ["service", "node_id"],
                },
            ),
            Tool(
                name="get_targets",
                description="Get available search targets for a service and indicator",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service type (dt, tt, cl, rm, etc.)",
                        },
                        "indicator": {
                            "type": "string",
                            "description": "The indicator type",
                        },
                    },
                    "required": ["service", "indicator"],
                },
            ),
            Tool(
                name="export_data",
                description="Export search results in specified format",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service type (dt, tt, cl, rm, etc.)",
                        },
                        "indicator": {
                            "type": "string",
                            "description": "The indicator to export data for",
                        },
                        "format": {
                            "type": "string",
                            "description": "Export format (json or csv)",
                            "enum": ["json", "csv"],
                            "default": "json",
                        },
                    },
                    "required": ["service", "indicator"],
                },
            ),
            Tool(
                name="search_compromised_dataset",
                description="Search compromised data set information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "The indicator to search for",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="get_compromised_dataset_node",
                description="Get detailed compromised data set node information (Cyber Security Edition required)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "node_id": {
                            "type": "string",
                            "description": "Node ID to get details for",
                        }
                    },
                    "required": ["node_id"],
                },
            ),
            Tool(
                name="search_combo_binder",
                description="Search leaked ID/Password combo information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "The indicator to search for",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="search_ulp_binder",
                description="Search URL-Login-Password combination information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "The indicator to search for",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="search_government_monitoring",
                description="Search government sector threat monitoring data using url: or id: indicators",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "Search query - use 'url:hackersite.com' to search threat event URLs or 'id:hacker123' to search actor IDs. Leave empty for recent list.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                        "cursor": {
                            "type": "integer",
                            "description": "Pagination cursor (default: 0)",
                            "default": 0,
                            "minimum": 0,
                        },
                        "orderType": {
                            "type": "string",
                            "description": "Order type",
                            "enum": ["detectionTime", "title", "author"],
                            "default": "detectionTime",
                        },
                        "order": {
                            "type": "string",
                            "description": "Sort order",
                            "enum": ["asc", "desc"],
                            "default": "desc",
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="search_leaked_monitoring",
                description="Search enterprise sector threat monitoring data using url: or id: indicators",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "Search query - use 'url:hackersite.com' to search threat event URLs or 'id:hacker123' to search actor IDs. Leave empty for recent list.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                        "cursor": {
                            "type": "integer",
                            "description": "Pagination cursor (default: 0)",
                            "default": 0,
                            "minimum": 0,
                        },
                        "orderType": {
                            "type": "string",
                            "description": "Order type",
                            "enum": ["detectionTime", "title", "author"],
                            "default": "detectionTime",
                        },
                        "order": {
                            "type": "string",
                            "description": "Sort order",
                            "enum": ["asc", "desc"],
                            "default": "desc",
                        },
                    },
                    "required": ["indicator"],
                },
            ),
            Tool(
                name="download_file",
                description="Download file by hash from dt or tt service",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service type (dt or tt)",
                            "enum": ["dt", "tt"],
                        },
                        "file_hash": {
                            "type": "string",
                            "description": "File hash to download",
                        },
                    },
                    "required": ["service", "file_hash"],
                },
            ),
            Tool(
                name="search_pagination",
                description="Pagination search using search ID for dt or tt service",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service type (dt or tt)",
                            "enum": ["dt", "tt"],
                        },
                        "search_id": {
                            "type": "string",
                            "description": "Search ID from previous search",
                        },
                        "cursor": {
                            "type": "integer",
                            "description": "Pagination cursor (default: 0)",
                            "default": 0,
                            "minimum": 0,
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 50)",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 50,
                        },
                    },
                    "required": ["service", "search_id"],
                },
            ),
            Tool(
                name="get_user_quotas",
                description="Get API usage quotas by service",
                inputSchema={"type": "object", "properties": {}, "required": []},
            ),
        ]
    except Exception as e:
        print(f"Error in handle_list_tools: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        return []


def apply_default_behavior(
    name: str, arguments: dict[str, Any], prompt: Optional[str] = None
) -> dict[str, Any]:
    """Apply default behavior rules to tool arguments based on tool name and optional prompt context.

    Args:
        name: The tool name being called
        arguments: The original arguments dictionary
        prompt: Optional prompt context to influence behavior

    Returns:
        Modified arguments dictionary with defaults applied
    """
    # Create a copy to avoid mutating the original
    modified_args = arguments.copy()

    # Apply limit defaults based on tool type
    if "limit" in modified_args:
        if name in ["search_darkweb", "search_telegram"]:
            # For general searches, use smaller limit unless prompt suggests otherwise
            if prompt and (
                "detailed" in prompt.lower() or "comprehensive" in prompt.lower()
            ):
                modified_args["limit"] = 20
            else:
                modified_args["limit"] = 10
        elif name in [
            "search_credentials",
            "search_ransomware",
            "search_compromised_dataset",
            "search_combo_binder",
            "search_ulp_binder",
            "search_government_monitoring",
            "search_leaked_monitoring",
        ]:
            # For sensitive data searches, use larger limit by default
            if prompt and "quick" in prompt.lower():
                modified_args["limit"] = 20
            else:
                modified_args["limit"] = 50

    # Handle indicator defaults for search tools
    if name in ["search_darkweb", "search_telegram"]:
        if "indicator" not in modified_args or not modified_args["indicator"]:
            # Default to keyword search unless prompt suggests otherwise
            if prompt:
                if "domain" in prompt.lower():
                    modified_args["indicator"] = "domain"
                elif "ip" in prompt.lower() or "address" in prompt.lower():
                    modified_args["indicator"] = "ip"
                elif "email" in prompt.lower():
                    modified_args["indicator"] = "email"
                else:
                    modified_args["indicator"] = "keyword"
            else:
                modified_args["indicator"] = "keyword"

    return modified_args


def removal_empty(result: dict[str, Any]) -> dict[str, Any]:
    """Remove empty keys from result."""
    keys_to_remove = [
        key for key in result.keys() if result[key].get("totalCount") == 0
    ]
    for key in keys_to_remove:
        del result[key]
    return result


def removal_highlight(result: dict[str, Any]) -> dict[str, Any]:
    """Remove highlight from result."""
    for key in list(result.keys()):
        if len(result[key]["data"]) > 0:
            for contents in result[key]["data"]:
                if "highlight" in contents:
                    del contents["highlight"]
    return result


def removal_empty_metadata(result: dict[str, Any]) -> dict[str, Any]:
    """Remove metadata from result."""
    for key in list(result.keys()):
        if len(result[key]["data"]) > 0:
            for contents in result[key]["data"]:
                if bool(contents.get("metadata")) == False:
                    del contents["metadata"]
    return result


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls with default behavior applied."""

    # Extract prompt from arguments if provided (for context-aware defaults)
    prompt = arguments.pop("_prompt", None) if "_prompt" in arguments else None

    # Apply default behavior rules with prompt context
    arguments = apply_default_behavior(name, arguments, prompt)

    try:
        if name == "search_darkweb":
            result = await search_darkweb(
                indicator=arguments["indicator"],
                text=arguments["text"],
                target=arguments.get("target", "all"),
                limit=arguments.get("limit", 10),
                orderType=arguments.get("orderType", "createDate"),
                order=arguments.get("order", "desc"),
            )

            if type(result) == dict:
                result = removal_empty(result)
                result = removal_highlight(result)
                result = removal_empty_metadata(result)

        elif name == "search_telegram":
            result = await search_telegram(
                indicator=arguments["indicator"],
                text=arguments["text"],
                target=arguments.get("target", "all"),
                limit=arguments.get("limit", 10),
                orderType=arguments.get("orderType", "createDate"),
                order=arguments.get("order", "desc"),
            )

            if type(result) == dict:
                result = removal_empty(result)
                result = removal_highlight(result)
                result = removal_empty_metadata(result)

        elif name == "search_credentials":
            result = await search_credentials(
                indicator=arguments["indicator"],
                limit=arguments.get("limit", 50),
                cursor=arguments.get("cursor", 0),
                orderType=arguments.get("orderType", "LeakedDate"),
                order=arguments.get("order", "desc"),
                start=arguments.get("start"),
                end=arguments.get("end"),
            )
        elif name == "search_ransomware":
            result = await search_ransomware(
                indicator=arguments["indicator"],
                limit=arguments.get("limit", 50),
                cursor=arguments.get("cursor", 0),
                orderType=arguments.get("orderType", "detectionTime"),
                order=arguments.get("order", "desc"),
            )
        elif name == "get_node_details":
            result = await get_node_details(
                service=arguments["service"],
                node_id=arguments["node_id"],
                pid=arguments.get("pid"),
                data_from=arguments.get("data_from", False),
                include_url=arguments.get("include_url", False),
                include_contents=arguments.get("include_contents", True),
            )
        elif name == "get_targets":
            result = await get_targets(
                service=arguments["service"], indicator=arguments["indicator"]
            )
        elif name == "export_data":
            result = await export_data(
                service=arguments["service"],
                indicator=arguments["indicator"],
                format=arguments.get("format", "json"),
            )
        elif name == "search_compromised_dataset":
            result = await search_compromised_dataset(
                indicator=arguments["indicator"], limit=arguments.get("limit", 50)
            )
        elif name == "get_compromised_dataset_node":
            result = await get_compromised_dataset_node(node_id=arguments["node_id"])
        elif name == "search_combo_binder":
            result = await search_combo_binder(
                indicator=arguments["indicator"], limit=arguments.get("limit", 50)
            )
        elif name == "search_ulp_binder":
            result = await search_ulp_binder(
                indicator=arguments["indicator"], limit=arguments.get("limit", 50)
            )
        elif name == "search_government_monitoring":
            result = await search_government_monitoring(
                indicator=arguments["indicator"],
                limit=arguments.get("limit", 50),
                cursor=arguments.get("cursor", 0),
                orderType=arguments.get("orderType", "detectionTime"),
                order=arguments.get("order", "desc"),
            )
        elif name == "search_leaked_monitoring":
            result = await search_leaked_monitoring(
                indicator=arguments["indicator"],
                limit=arguments.get("limit", 50),
                cursor=arguments.get("cursor", 0),
                orderType=arguments.get("orderType", "detectionTime"),
                order=arguments.get("order", "desc"),
            )
        elif name == "download_file":
            file_content = await download_file(
                service=arguments["service"], file_hash=arguments["file_hash"]
            )
            return [
                TextContent(
                    type="text",
                    text=f"Downloaded file {arguments['file_hash']} from {arguments['service']} service. File size: {len(file_content)} bytes",
                )
            ]
        elif name == "search_pagination":
            result = await search_pagination(
                service=arguments["service"],
                search_id=arguments["search_id"],
                cursor=arguments.get("cursor", 0),
                limit=arguments.get("limit", 50),
            )
        elif name == "get_user_quotas":
            result = await get_user_quotas()
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        # Format response
        # result remove whitespace
        response_text = f"{result}"
        return [
            TextContent(
                type="text",
                text=response_text,
            )
        ]

    except asyncio.TimeoutError:
        return [
            TextContent(
                type="text",
                text="Request timed out. The API request took too long to complete.",
            )
        ]
    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            return [
                TextContent(
                    type="text",
                    text=f"Timeout error: {error_msg}. Try reducing the result limit or check your network connection.",
                )
            ]
        return [
            TextContent(
                type="text",
                text=f"Error calling StealthMole API: {error_msg}",
            )
        ]


async def run_server():
    """Run the MCP server."""
    try:
        print("Starting StealthMole MCP server...", file=sys.stderr)

        # Check environment variables
        access_key = os.getenv("STEALTHMOLE_ACCESS_KEY")
        secret_key = os.getenv("STEALTHMOLE_SECRET_KEY")

        print(f"Access key: {'SET' if access_key else 'NOT SET'}", file=sys.stderr)
        print(f"Secret key: {'SET' if secret_key else 'NOT SET'}", file=sys.stderr)

        if not access_key or not secret_key:
            print(
                "Warning: STEALTHMOLE_ACCESS_KEY and STEALTHMOLE_SECRET_KEY environment variables not set",
                file=sys.stderr,
            )
            print("MCP server will start but tools will not function", file=sys.stderr)
        else:
            try:
                # API 연결 테스트 (타임아웃 없이 간단히)
                try:
                    quotas = await get_user_quotas()
                    print(
                        f"✓ API connection successful. Available quotas: {quotas}",
                        file=sys.stderr,
                    )
                except Exception as api_error:
                    print(f"Warning: API test failed: {api_error}", file=sys.stderr)
                    print("Continuing with server startup...", file=sys.stderr)

            except Exception as e:
                print(f"Warning: Error testing API connection: {e}", file=sys.stderr)
                print(
                    "MCP server will start but tools may not function properly",
                    file=sys.stderr,
                )
                import traceback

                traceback.print_exc(file=sys.stderr)

        print("Creating stdio server...", file=sys.stderr)
        async with stdio_server() as (read_stream, write_stream):
            print("Starting MCP server...", file=sys.stderr)
            try:
                await server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="stealthmole-mcp",
                        server_version="1.0.0",
                        capabilities=server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ),
                )
                print("MCP server completed normally", file=sys.stderr)
            except Exception as e:
                print(f"Error in MCP server.run: {e}", file=sys.stderr)
                import traceback

                traceback.print_exc(file=sys.stderr)
                raise
    except Exception as e:
        print(f"Error in run_server: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)


def main():
    """Main entry point for the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
