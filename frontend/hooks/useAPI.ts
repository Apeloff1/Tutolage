// ============================================================================
// CODEDOCK QUANTUM NEXUS - API HOOK
// Version: 4.2.0 | Refactored Architecture
// ============================================================================

import { useState, useEffect, useCallback } from 'react';
import ApiService, { parseError, retryWithBackoff } from '../services/api';
import { 
  Language, Template, CodeFile, AIMode, 
  TutorialStep, Tooltip, ConnectionStatus, AppError 
} from '../types';

export const useAPI = () => {
  // State
  const [languages, setLanguages] = useState<Language[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [files, setFiles] = useState<CodeFile[]>([]);
  const [aiModes, setAIModes] = useState<AIMode[]>([]);
  const [tutorialSteps, setTutorialSteps] = useState<TutorialStep[]>([]);
  const [tooltips, setTooltips] = useState<Record<string, Tooltip>>({});
  const [availableDocks, setAvailableDocks] = useState<Language[]>([]);
  
  // Connection state
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('connected');
  const [lastError, setLastError] = useState<AppError | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initial data load
  const loadInitialData = useCallback(async () => {
    setConnectionStatus('reconnecting');
    setIsLoading(true);
    
    try {
      // Load critical data with retry
      const [langData, aiData] = await Promise.all([
        retryWithBackoff(() => ApiService.getLanguages()),
        retryWithBackoff(() => ApiService.getAIModes()),
      ]);
      
      setLanguages(langData.languages || []);
      setAIModes(aiData.modes || []);

      // Load non-critical data (no retry)
      try {
        const [tooltipData, tutorialData, dockData, filesData] = await Promise.all([
          ApiService.getTooltips(),
          ApiService.getTutorialSteps(),
          ApiService.getAvailableDocks(),
          ApiService.getFiles(),
        ]);
        
        setTooltips(tooltipData.tooltips || {});
        setTutorialSteps(tutorialData.steps || []);
        setAvailableDocks(dockData.docks || []);
        setFiles(filesData.files || []);
      } catch (e) {
        // Non-critical, continue
      }

      setConnectionStatus('connected');
      setLastError(null);
    } catch (error: any) {
      console.error('Failed to load initial data:', error);
      setConnectionStatus('disconnected');
      setLastError(parseError(error));
      
      // Set fallback languages
      setLanguages(getFallbackLanguages());
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Load templates for a language
  const loadTemplates = useCallback(async (language: string) => {
    try {
      const data = await ApiService.getTemplates(language);
      setTemplates(data.templates || []);
    } catch (error) {
      console.error('Failed to load templates:', error);
      setTemplates([]);
    }
  }, []);

  // Refresh files
  const refreshFiles = useCallback(async () => {
    try {
      const data = await ApiService.getFiles();
      setFiles(data.files || []);
    } catch (error) {
      console.error('Failed to refresh files:', error);
    }
  }, []);

  // Execute code
  const executeCode = useCallback(async (code: string, language: string) => {
    try {
      const result = await ApiService.executeCode(code, language);
      return result;
    } catch (error: any) {
      throw parseError(error);
    }
  }, []);

  // AI Assist
  const aiAssist = useCallback(async (code: string, language: string, mode: string, context?: string) => {
    try {
      const result = await ApiService.aiAssist(code, language, mode, context);
      return result;
    } catch (error: any) {
      throw parseError(error);
    }
  }, []);

  // Save file
  const saveFile = useCallback(async (file: Partial<CodeFile>) => {
    try {
      const saved = await ApiService.saveFile(file);
      await refreshFiles();
      return saved;
    } catch (error: any) {
      throw parseError(error);
    }
  }, [refreshFiles]);

  // Delete file
  const deleteFile = useCallback(async (fileId: string) => {
    try {
      await ApiService.deleteFile(fileId);
      await refreshFiles();
    } catch (error: any) {
      throw parseError(error);
    }
  }, [refreshFiles]);

  // Analyze code
  const analyzeCode = useCallback(async (code: string, language: string) => {
    try {
      const result = await ApiService.analyzeCode(code, language);
      return result;
    } catch (error: any) {
      throw parseError(error);
    }
  }, []);

  // Add addon
  const addAddon = useCallback(async (addon: { name: string; extension: string; description?: string }) => {
    try {
      await ApiService.addLanguageAddon(addon);
      await loadInitialData(); // Refresh languages
    } catch (error: any) {
      throw parseError(error);
    }
  }, [loadInitialData]);

  return {
    // Data
    languages,
    templates,
    files,
    aiModes,
    tutorialSteps,
    tooltips,
    availableDocks,
    
    // Status
    connectionStatus,
    lastError,
    isLoading,
    
    // Actions
    loadInitialData,
    loadTemplates,
    refreshFiles,
    executeCode,
    aiAssist,
    saveFile,
    deleteFile,
    analyzeCode,
    addAddon,
    
    // Error handling
    clearError: () => setLastError(null),
  };
};

// Fallback languages when offline
function getFallbackLanguages(): Language[] {
  return [
    { key: 'python', name: 'Python', display_name: 'Python 3.12+', extension: '.py', icon: 'logo-python', color: '#3776AB', executable: true, type: 'builtin', tier: 1 },
    { key: 'javascript', name: 'JavaScript', display_name: 'JavaScript ES2026', extension: '.js', icon: 'logo-javascript', color: '#F7DF1E', executable: true, type: 'builtin', tier: 1 },
    { key: 'html', name: 'HTML', display_name: 'HTML 5.3', extension: '.html', icon: 'logo-html5', color: '#E34F26', executable: true, type: 'builtin', tier: 1 },
    { key: 'cpp', name: 'C++', display_name: 'C++23', extension: '.cpp', icon: 'code-slash', color: '#00599C', executable: true, type: 'builtin', tier: 1 },
    { key: 'c', name: 'C', display_name: 'C23', extension: '.c', icon: 'code-slash', color: '#A8B9CC', executable: true, type: 'builtin', tier: 1 },
    { key: 'typescript', name: 'TypeScript', display_name: 'TypeScript 5.6+', extension: '.ts', icon: 'logo-javascript', color: '#3178C6', executable: true, type: 'builtin', tier: 1 },
  ];
}

export default useAPI;
