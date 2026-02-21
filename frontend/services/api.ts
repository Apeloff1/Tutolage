// ============================================================================
// CODEDOCK QUANTUM NEXUS - API SERVICE
// Version: 4.2.0 | Refactored Architecture
// ============================================================================

import axios, { AxiosError } from 'axios';
import { API_URL, CONFIG } from '../constants/config';
import { 
  Language, Template, CodeFile, ExecutionResult, 
  AIMode, AIResponse, TutorialStep, Tooltip, AppError, ErrorType 
} from '../types';

// Create axios instance with defaults
const api = axios.create({
  baseURL: API_URL,
  timeout: CONFIG.API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Retry with exponential backoff
export const retryWithBackoff = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = CONFIG.MAX_RETRIES,
  delay: number = CONFIG.RETRY_DELAY
): Promise<T> => {
  let lastError: any;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
      }
    }
  }
  throw lastError;
};

// Parse errors for better UX
export const parseError = (error: any): AppError => {
  if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
    return { type: 'timeout', message: 'Request timed out. Check your connection.', retry: true };
  }
  if (error.response?.status === 500) {
    return { type: 'server', message: 'Server error. Please try again.', code: 500, retry: true };
  }
  if (error.response?.status === 404) {
    return { type: 'validation', message: 'Resource not found.', code: 404, retry: false };
  }
  if (!error.response && error.message?.includes('Network')) {
    return { type: 'network', message: 'Network error. Check your internet connection.', retry: true };
  }
  return { type: 'unknown', message: error.message || 'An unexpected error occurred.', retry: true };
};

// API Methods
export const ApiService = {
  // Health & Info
  async getStatus() {
    const response = await api.get('/api/');
    return response.data;
  },

  async getHealth() {
    const response = await api.get('/api/health');
    return response.data;
  },

  // Languages
  async getLanguages(): Promise<{ languages: Language[] }> {
    const response = await retryWithBackoff(() => api.get('/api/languages'));
    return response.data;
  },

  // Templates
  async getTemplates(language: string): Promise<{ templates: Template[] }> {
    const response = await api.get(`/api/templates/${language}`);
    return response.data;
  },

  // Code Execution
  async executeCode(code: string, language: string): Promise<ExecutionResult> {
    const response = await api.post('/api/execute', { code, language });
    return response.data;
  },

  // Files
  async getFiles(): Promise<{ files: CodeFile[] }> {
    const response = await api.get('/api/files');
    return response.data;
  },

  async saveFile(file: Partial<CodeFile>): Promise<CodeFile> {
    const response = await api.post('/api/files', file);
    return response.data;
  },

  async deleteFile(fileId: string): Promise<void> {
    await api.delete(`/api/files/${fileId}`);
  },

  // AI Assistant
  async getAIModes(): Promise<{ modes: AIMode[] }> {
    const response = await retryWithBackoff(() => api.get('/api/ai/modes'));
    return response.data;
  },

  async aiAssist(code: string, language: string, mode: string, context?: string): Promise<AIResponse> {
    const response = await api.post('/api/ai/assist', {
      code,
      language,
      mode,
      context,
    });
    return response.data;
  },

  // Analysis
  async analyzeCode(code: string, language: string) {
    const response = await api.post('/api/analyze', { code, language });
    return response.data;
  },

  // Tutorial
  async getTutorialSteps(): Promise<{ steps: TutorialStep[] }> {
    const response = await api.get('/api/tutorial/steps');
    return response.data;
  },

  // Tooltips
  async getTooltips(): Promise<{ tooltips: Record<string, Tooltip> }> {
    const response = await api.get('/api/tooltips');
    return response.data;
  },

  // Dock
  async getAvailableDocks(): Promise<{ docks: Language[] }> {
    const response = await api.get('/api/dock/available');
    return response.data;
  },

  // Addons
  async addLanguageAddon(addon: { name: string; extension: string; description?: string }) {
    const response = await api.post('/api/addons', addon);
    return response.data;
  },
};

export default ApiService;
