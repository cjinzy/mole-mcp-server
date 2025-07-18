import { StealthMoleClient } from '../utils/client.js';

export type ToolHandler = (args: any) => Promise<any>;

export function getToolHandlers(apiClient: StealthMoleClient): Record<string, ToolHandler> {
  return {
    search_darkweb: async (args: { query: string; limit?: number }) => {
      try {
        const result = await apiClient.get('/api/v1/search/darkweb', {
          q: args.query,
          limit: args.limit || 10,
        });
        return result;
      } catch (error) {
        throw new Error(`Dark web search failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    },

    search_telegram: async (args: { query: string; limit?: number }) => {
      try {
        const result = await apiClient.get('/api/v1/search/telegram', {
          q: args.query,
          limit: args.limit || 10,
        });
        return result;
      } catch (error) {
        throw new Error(`Telegram search failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    },

    search_credentials: async (args: { query: string; limit?: number }) => {
      try {
        const result = await apiClient.get('/api/v1/search/credentials', {
          q: args.query,
          limit: args.limit || 10,
        });
        return result;
      } catch (error) {
        throw new Error(`Credential search failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    },

    search_ransomware: async (args: { query: string; limit?: number }) => {
      try {
        const result = await apiClient.get('/api/v1/search/ransomware', {
          q: args.query,
          limit: args.limit || 10,
        });
        return result;
      } catch (error) {
        throw new Error(`Ransomware search failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    },

    get_user_quota: async () => {
      try {
        const result = await apiClient.get('/api/v1/user/quota');
        return result;
      } catch (error) {
        throw new Error(`Failed to get user quota: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    },

    download_file: async (args: { url: string }) => {
      try {
        const buffer = await apiClient.downloadFile(args.url);
        return {
          success: true,
          size: buffer.length,
          message: 'File downloaded successfully',
          // Note: In a real implementation, you would handle the buffer appropriately
          // For MCP, we typically return metadata rather than binary data
        };
      } catch (error) {
        throw new Error(`File download failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    },
  };
}