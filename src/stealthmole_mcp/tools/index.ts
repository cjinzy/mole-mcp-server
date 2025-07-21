import { Tool } from '@modelcontextprotocol/sdk/types.js';

export function getTools(): Tool[] {
  return [
    {
      name: 'search_darkweb',
      description: 'Search for dark web content and threats',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query for dark web content',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results to return',
            default: 10,
          },
        },
        required: ['query'],
      },
    },
    {
      name: 'search_telegram',
      description: 'Search Telegram channels for threat intelligence',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query for Telegram content',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results to return',
            default: 10,
          },
        },
        required: ['query'],
      },
    },
    {
      name: 'search_credentials',
      description: 'Search for leaked credentials and data breaches',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query for credential leaks',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results to return',
            default: 10,
          },
        },
        required: ['query'],
      },
    },
    {
      name: 'search_ransomware',
      description: 'Search for ransomware group activities and victims',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query for ransomware activities',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results to return',
            default: 10,
          },
        },
        required: ['query'],
      },
    },
    {
      name: 'get_user_quota',
      description: 'Get current user API quota and usage statistics',
      inputSchema: {
        type: 'object',
        properties: {},
      },
    },
    {
      name: 'download_file',
      description: 'Download a file from StealthMole API',
      inputSchema: {
        type: 'object',
        properties: {
          url: {
            type: 'string',
            description: 'URL of the file to download',
          },
        },
        required: ['url'],
      },
    },
  ];
}