import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { Config } from './config.js';

export interface StealthMoleClient {
  get(endpoint: string, params?: any): Promise<any>;
  post(endpoint: string, data?: any): Promise<any>;
  downloadFile(url: string): Promise<Buffer>;
}

export class StealthMoleApiClient implements StealthMoleClient {
  private client: AxiosInstance;
  private config: Config;

  constructor(config: Config) {
    this.config = config;
    
    this.client = axios.create({
      baseURL: config.apiUrl,
      timeout: config.defaultTimeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'StealthMole-MCP-Server/1.0.0',
      },
    });

    // Add request interceptor for authentication
    this.client.interceptors.request.use((config) => {
      if (this.config.accessKey && this.config.secretKey) {
        config.headers['X-Access-Key'] = this.config.accessKey;
        config.headers['X-Secret-Key'] = this.config.secretKey;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // Server responded with error status
          const message = error.response.data?.message || error.response.statusText;
          throw new Error(`API Error (${error.response.status}): ${message}`);
        } else if (error.request) {
          // Request was made but no response received
          throw new Error('Network Error: No response from API server');
        } else {
          // Something else happened
          throw new Error(`Request Error: ${error.message}`);
        }
      }
    );
  }

  async get(endpoint: string, params?: any): Promise<any> {
    const response = await this.client.get(endpoint, { params });
    return response.data;
  }

  async post(endpoint: string, data?: any): Promise<any> {
    const response = await this.client.post(endpoint, data);
    return response.data;
  }

  async downloadFile(url: string): Promise<Buffer> {
    const response = await this.client.get(url, {
      responseType: 'arraybuffer',
    });
    return Buffer.from(response.data);
  }

  // Helper method to check API connectivity
  async checkConnection(): Promise<boolean> {
    try {
      await this.get('/health');
      return true;
    } catch (error) {
      console.warn('API connection check failed:', error);
      return false;
    }
  }
}

/**
 * Factory function to create StealthMole API client
 */
export function createStealthMoleClient(config: Config): StealthMoleClient {
  return new StealthMoleApiClient(config);
}