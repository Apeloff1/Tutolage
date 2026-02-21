// ============================================================================
// CODEDOCK QUANTUM NEXUS - CONFIGURATION
// Version: 4.2.0 | Refactored Architecture
// ============================================================================

import { AppConfig } from '../types';

export const VERSION = '4.2.0';
export const CODENAME = 'Nexus Refactored';
export const BUILD = '2026.02.21-REFACTOR';

export const CONFIG: AppConfig = {
  API_TIMEOUT: 15000,
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
  CACHE_TTL: 5 * 60 * 1000, // 5 minutes
  ANIMATION_DURATION: 300,
  TOAST_DURATION: 3000,
};

export const FEATURES = [
  'teaching_mode',
  'coding_bible',
  'tooltips_engine',
  'hidden_advanced_panel',
  'language_dock_system',
  'expansion_ready',
  'hotfix_system',
  'plugin_architecture',
  'custom_language_support',
  'retry_with_backoff',
  'connection_status_indicator',
  'enhanced_error_handling',
  'grok_enhanced_prompts',
  'offline_bible',
  'progress_tracking',
  'achievements_system',
];

export const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';

export const STORAGE_KEYS = {
  THEME: 'codedock_theme',
  TUTORIAL_COMPLETED: 'tutorial_completed',
  ADVANCED_UNLOCKED: 'advanced_unlocked',
  BIBLE_PROGRESS: 'bible_progress',
  BIBLE_BOOKMARKS: 'bible_bookmarks',
  USER_PREFERENCES: 'user_preferences',
  RECENT_FILES: 'recent_files',
  ACHIEVEMENTS: 'achievements',
};

export const TIER_COLORS: Record<string, string> = {
  beginner: '#22C55E',
  foundation: '#3B82F6',
  intermediate: '#8B5CF6',
  advanced: '#F59E0B',
  expert: '#EC4899',
  godtier: '#FFD700',
};

export const COMPLEXITY_COLORS: Record<string, string> = {
  trivial: '#22C55E',
  simple: '#3B82F6',
  moderate: '#F59E0B',
  complex: '#EF4444',
  advanced: '#8B5CF6',
};
