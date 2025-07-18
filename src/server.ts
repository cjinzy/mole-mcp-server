#!/usr/bin/env node

import express from 'express';
import cors from 'cors';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { parseConfiguration } from './utils/config.js';
import { createStealthMoleClient } from './utils/client.js';
import { getTools } from './tools/index.js';
import { getToolHandlers } from './handlers/index.js';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// MCP endpoint for Smithery Custom Deploy
app.all('/mcp', async (req, res) => {
  try {
    // Parse configuration from query parameters
    const config = parseConfiguration(req.query);
    
    // Create StealthMole API client with configuration
    const apiClient = createStealthMoleClient(config);
    
    // Create MCP server instance
    const server = new Server(
      {
        name: 'stealthmole-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // Get tools and handlers
    const tools = getTools();
    const toolHandlers = getToolHandlers(apiClient);

    // Set up tool listing handler
    server.setRequestHandler(ListToolsRequestSchema, async () => {
      return { tools };
    });

    // Set up tool execution handler
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      const handler = toolHandlers[name];
      if (!handler) {
        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
      }

      try {
        const result = await handler(args || {});
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [{ type: 'text', text: `Error: ${errorMessage}` }],
          isError: true,
        };
      }
    });

    // Handle different HTTP methods
    if (req.method === 'GET') {
      // Return server info and available tools
      const toolsList = await server.request({ method: 'tools/list' }, ListToolsRequestSchema);
      res.json({
        server: {
          name: 'stealthmole-mcp-server',
          version: '1.0.0',
          description: 'StealthMole MCP Server for dark web and cybersecurity threat intelligence'
        },
        tools: toolsList.tools,
        configuration: config
      });
    } else if (req.method === 'POST') {
      // Handle tool execution
      const { method, params } = req.body;
      
      if (method === 'tools/list') {
        const result = await server.request(req.body, ListToolsRequestSchema);
        res.json(result);
      } else if (method === 'tools/call') {
        const result = await server.request(req.body, CallToolRequestSchema);
        res.json(result);
      } else {
        res.status(400).json({ error: 'Unsupported method' });
      }
    } else if (req.method === 'DELETE') {
      // Handle cleanup/shutdown
      res.json({ message: 'Server cleanup completed' });
    } else {
      res.status(405).json({ error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('MCP endpoint error:', error);
    res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Internal server error' 
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`StealthMole MCP Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`MCP endpoint: http://localhost:${PORT}/mcp`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down gracefully...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\nShutting down gracefully...');
  process.exit(0);
});