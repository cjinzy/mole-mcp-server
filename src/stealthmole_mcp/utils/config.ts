import { z } from 'zod';

// Configuration schema
const ConfigSchema = z.object({
  apiUrl: z.string().url().default('https://api.stealthmole.com'),
  accessKey: z.string().optional(),
  secretKey: z.string().optional(),
  defaultSearchLimit: z.number().int().positive().default(10),
  defaultTimeout: z.number().int().positive().default(30000),
});

export type Config = z.infer<typeof ConfigSchema>;

/**
 * Parse configuration from query parameters using dot notation
 * Example: ?apiUrl=https://api.example.com&accessKey=key123
 */
export function parseConfiguration(queryParams: any): Config {
  const config: any = {};
  
  // Convert query parameters to nested object
  for (const [key, value] of Object.entries(queryParams)) {
    if (typeof value === 'string') {
      // Handle dot notation (e.g., "server.host" -> { server: { host: value } })
      const keys = key.split('.');
      let current = config;
      
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) {
          current[keys[i]] = {};
        }
        current = current[keys[i]];
      }
      
      const lastKey = keys[keys.length - 1];
      
      // Convert string values to appropriate types
      if (value === 'true') {
        current[lastKey] = true;
      } else if (value === 'false') {
        current[lastKey] = false;
      } else if (/^\d+$/.test(value)) {
        current[lastKey] = parseInt(value, 10);
      } else if (/^\d+\.\d+$/.test(value)) {
        current[lastKey] = parseFloat(value);
      } else {
        current[lastKey] = value;
      }
    }
  }
  
  // Map common parameter names to our schema
  const mappedConfig = {
    apiUrl: config.apiUrl || config.api_url || config.STEALTHMOLE_API_URL,
    accessKey: config.accessKey || config.access_key || config.STEALTHMOLE_ACCESS_KEY,
    secretKey: config.secretKey || config.secret_key || config.STEALTHMOLE_SECRET_KEY,
    defaultSearchLimit: config.defaultSearchLimit || config.default_search_limit || config.DEFAULT_SEARCH_LIMIT,
    defaultTimeout: config.defaultTimeout || config.default_timeout || config.DEFAULT_TIMEOUT,
  };
  
  // Parse and validate configuration
  return ConfigSchema.parse(mappedConfig);
}

/**
 * Validate that required environment variables are set for local development
 */
export function validateEnvironment(): void {
  const requiredEnvVars = ['STEALTHMOLE_ACCESS_KEY', 'STEALTHMOLE_SECRET_KEY'];
  
  for (const envVar of requiredEnvVars) {
    if (!process.env[envVar]) {
      console.warn(`Warning: ${envVar} environment variable is not set`);
    }
  }
}

/**
 * Create error response helper
 */
export function createErrorResponse(message: string): { error: string; timestamp: string } {
  return {
    error: message,
    timestamp: new Date().toISOString(),
  };
}