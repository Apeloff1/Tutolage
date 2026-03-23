// ============================================================================
// CODEDOCK ULTIMATE HUB - Main Application
// Version: 9.0.0 | Ultimate Hub Edition
// Voice • Pipeline • Learning • Collaboration • WASM Compiler • AI Hub
// ============================================================================

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput,
  ActivityIndicator, SafeAreaView, StatusBar, Platform, Dimensions,
  KeyboardAvoidingView, Modal, Alert, Animated, Vibration,
  Pressable,
} from 'react-native';
import { WebView } from 'react-native-webview';
import { Ionicons } from '@expo/vector-icons';

// Custom Hooks
import { useTheme } from '../hooks/useTheme';
import { useStorage } from '../hooks/useStorage';
import { useAPI } from '../hooks/useAPI';

// Features
import { BibleModal } from '../features/Bible/BibleModal';
import { CompilerModal } from '../features/Compiler/CompilerModal';
import { PipelineVisualizer } from '../features/Pipeline/PipelineVisualizer';
import { LearningDashboard } from '../features/Learning/LearningDashboard';
import { CollaborationModal } from '../features/Collaboration/CollaborationModal';
import { HubModal } from '../features/Hub/HubModal';
import { AISuggestionsModal } from '../features/AI/AISuggestionsModal';
import { useVoiceCommands, speak } from '../features/Voice/useVoiceCommands';
import { starlog } from '../features/VersionControl/Starlog';
import { wasmCompiler } from '../features/WasmCompiler/WasmCompiler';

// v11.0 Features
import { AIPipelineModal } from '../features/AIPipeline/AIPipelineModal';
import { CurriculumBrowser } from '../features/Curriculum/CurriculumBrowser';
import { VaultModal } from '../features/Vault/VaultModal';
import { AdvancedFeaturesModal } from '../features/Advanced/AdvancedFeaturesModal';
import { CodeToAppModal } from '../features/CodeToApp/CodeToAppModal';
import { ImagineModal } from '../features/Imagine/ImagineModal';

// v11.1 SOTA 2026 Features
import { DebuggerModal } from '../features/Debugger/DebuggerModal';
import { MusicPipelineModal } from '../features/Music/MusicPipelineModal';
import { EducationModal } from '../features/Education/EducationModal';
import { JeevesModal } from '../features/Jeeves/JeevesModal';

// v11.2 Masterclass, Assets & Game Systems
import { MasterclassModal } from '../features/Masterclass/MasterclassModal';
import { AssetPipelineModal } from '../features/AssetPipeline/AssetPipelineModal';
import { GameGenresModal } from '../features/GameGenres/GameGenresModal';

// v11.3 Command Palette for Clean UI
import { CommandPalette } from '../components/CommandPalette';

// Types
import { Language, Template, AIMode } from '../types';

// Constants
import { VERSION, CODENAME } from '../constants/config';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

// ============================================================================
// MAIN APP COMPONENT
// ============================================================================
export default function CodeDockApp() {
  // Core Hooks
  const { theme, colors, toggleTheme, isLoading: themeLoading } = useTheme();
  const { 
    tutorialCompleted, setTutorialCompleted,
    bibleProgress, markChapterComplete, toggleBookmark, 
    isLoading: storageLoading 
  } = useStorage();
  const {
    languages, templates, files, aiModes, tutorialSteps,
    connectionStatus, lastError, isLoading: apiLoading,
    loadInitialData, loadTemplates, refreshFiles,
    executeCode: apiExecuteCode, aiAssist, saveFile: apiSaveFile,
    clearError,
  } = useAPI();

  // Core State
  const [selectedLanguage, setSelectedLanguage] = useState<Language | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [currentFileName, setCurrentFileName] = useState('untitled');
  const [executionTime, setExecutionTime] = useState<number | null>(null);

  // Modal State
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [showFilesModal, setShowFilesModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showAIModal, setShowAIModal] = useState(false);
  const [showBibleModal, setShowBibleModal] = useState(false);
  const [showCompilerModal, setShowCompilerModal] = useState(false);
  const [showPipelineModal, setShowPipelineModal] = useState(false);
  const [showLearningModal, setShowLearningModal] = useState(false);
  const [showCollaborationModal, setShowCollaborationModal] = useState(false);
  const [showHubModal, setShowHubModal] = useState(false);
  const [showAISuggestionsModal, setShowAISuggestionsModal] = useState(false);
  const [showTutorial, setShowTutorial] = useState(false);
  const [showOutput, setShowOutput] = useState(false);
  const [showWebPreview, setShowWebPreview] = useState(false);
  const [htmlPreview, setHtmlPreview] = useState('');
  
  // v11.0 Modal State
  const [showAIPipelineModal, setShowAIPipelineModal] = useState(false);
  const [showCurriculumModal, setShowCurriculumModal] = useState(false);
  const [showVaultModal, setShowVaultModal] = useState(false);
  const [showAdvancedModal, setShowAdvancedModal] = useState(false);
  const [showCodeToAppModal, setShowCodeToAppModal] = useState(false);
  const [showImagineModal, setShowImagineModal] = useState(false);
  
  // v11.1 SOTA 2026 Modal State
  const [showDebuggerModal, setShowDebuggerModal] = useState(false);
  const [showMusicPipelineModal, setShowMusicPipelineModal] = useState(false);
  const [showEducationModal, setShowEducationModal] = useState(false);
  const [showJeevesModal, setShowJeevesModal] = useState(false);
  
  // v11.2 Masterclass & Asset Pipeline Modal State
  const [showMasterclassModal, setShowMasterclassModal] = useState(false);
  const [showAssetPipelineModal, setShowAssetPipelineModal] = useState(false);
  const [showGameGenresModal, setShowGameGenresModal] = useState(false);
  
  // v11.3 Command Palette State
  const [showCommandPalette, setShowCommandPalette] = useState(false);
  
  // Voice Command Handler
  const handleVoiceCommand = useCallback((action: string, params?: any) => {
    switch (action) {
      case 'RUN_CODE':
        executeCode();
        break;
      case 'CLEAR_CODE':
        clearCode();
        break;
      case 'SAVE_FILE':
        saveFile();
        break;
      case 'OPEN_MODAL':
        if (params?.modal === 'compiler') setShowCompilerModal(true);
        else if (params?.modal === 'bible') setShowBibleModal(true);
        else if (params?.modal === 'settings') setShowSettingsModal(true);
        break;
      case 'RUN_ANALYSIS':
        setShowCompilerModal(true);
        break;
      case 'HELP':
        speak('Available commands: Run code, Clear code, Save file, Open compiler, Open bible, Engage LTO, Engage PGO, Set optimization level O3');
        break;
      default:
        console.log('Voice command:', action, params);
    }
  }, []);

  // Voice Commands Hook
  const voice = useVoiceCommands(handleVoiceCommand);
  
  // AI State
  const [selectedAIMode, setSelectedAIMode] = useState<AIMode | null>(null);
  const [aiResponse, setAIResponse] = useState('');
  const [isAILoading, setIsAILoading] = useState(false);

  // Tutorial State
  const [currentTutorialStep, setCurrentTutorialStep] = useState(0);

  // Animation
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  // Derived
  const isLoading = themeLoading || storageLoading || apiLoading;

  // ============================================================================
  // EFFECTS
  // ============================================================================
  useEffect(() => {
    loadInitialData();
    
    // Start entrance animation
    Animated.timing(fadeAnim, { toValue: 1, duration: 500, useNativeDriver: true }).start();
    
    // Pulse animation for AI button
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.05, duration: 1500, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1500, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  // Set default language when languages load
  useEffect(() => {
    if (languages.length > 0 && !selectedLanguage) {
      const defaultLang = languages.find(l => l.key === 'python') || languages[0];
      setSelectedLanguage(defaultLang);
      loadTemplates(defaultLang.key);
    }
  }, [languages]);

  // Show tutorial for first-time users
  useEffect(() => {
    if (!tutorialCompleted && !isLoading && tutorialSteps.length > 0) {
      setTimeout(() => setShowTutorial(true), 1000);
    }
  }, [tutorialCompleted, isLoading, tutorialSteps]);

  // ============================================================================
  // HANDLERS
  // ============================================================================
  const selectLanguage = useCallback((lang: Language) => {
    setSelectedLanguage(lang);
    setShowLanguageModal(false);
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    setExecutionTime(null);
    loadTemplates(lang.key);
    if (Platform.OS !== 'web') Vibration.vibrate(10);
  }, [loadTemplates]);

  const executeCode = useCallback(async () => {
    if (!code.trim() || !selectedLanguage) return;

    setIsExecuting(true);
    setOutput('');
    setShowOutput(true);
    setShowWebPreview(false);
    setExecutionTime(null);

    try {
      // Handle HTML preview
      if (selectedLanguage.key === 'html') {
        setHtmlPreview(code);
        setShowWebPreview(true);
        setShowOutput(false);
        return;
      }

      // Handle JS/TS preview in WebView
      if (selectedLanguage.key === 'javascript' || selectedLanguage.key === 'typescript') {
        const result = await apiExecuteCode(code, selectedLanguage.key);
        const wrappedCode = result.result?.stdout || (result as any).output;
        setHtmlPreview(`
          <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
          <style>body{font-family:monospace;padding:16px;background:${colors.codeBackground};color:${colors.text};font-size:14px;margin:0;}</style></head>
          <body><pre id="o">${wrappedCode || 'No output'}</pre></body></html>
        `);
        setShowWebPreview(true);
        setShowOutput(false);
        setExecutionTime(result.result?.execution_time || 0);
        return;
      }

      // Standard execution
      const result = await apiExecuteCode(code, selectedLanguage.key);
      setExecutionTime(result.result?.execution_time || 0);
      
      const stdout = result.result?.stdout || (result as any).output;
      const stderr = result.result?.stderr;
      
      if (stderr) {
        setOutput(`❌ Error:\n${stderr}`);
      } else if (stdout) {
        setOutput(stdout);
      } else {
        setOutput('✓ Program executed successfully (no output)');
      }
    } catch (error: any) {
      setOutput(`❌ Execution failed: ${error.message || 'Unknown error'}`);
    } finally {
      setIsExecuting(false);
    }
  }, [code, selectedLanguage, apiExecuteCode, colors]);

  const applyTemplate = useCallback((template: Template) => {
    setCode(template.code);
    setShowTemplateModal(false);
    setShowOutput(false);
    setExecutionTime(null);
  }, []);

  const saveFile = useCallback(async () => {
    if (!code.trim() || !selectedLanguage) return;
    try {
      await apiSaveFile({
        name: currentFileName + selectedLanguage.extension,
        language: selectedLanguage.key,
        code,
      });
      Alert.alert('✓ Saved', `${currentFileName}${selectedLanguage.extension} saved successfully`);
      refreshFiles();
    } catch (error: any) {
      Alert.alert('Error', `Failed to save: ${error.message}`);
    }
  }, [code, selectedLanguage, currentFileName, apiSaveFile, refreshFiles]);

  const loadFile = useCallback((file: any) => {
    const lang = languages.find(l => l.key === file.language);
    if (lang) {
      setSelectedLanguage(lang);
      setCode(file.code);
      setCurrentFileName(file.name.replace(/\.[^/.]+$/, ''));
      setShowFilesModal(false);
      setShowOutput(false);
      loadTemplates(lang.key);
    }
  }, [languages, loadTemplates]);

  const clearCode = useCallback(() => {
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    setExecutionTime(null);
  }, []);

  const askAI = useCallback(async (mode: AIMode) => {
    if (!code.trim()) {
      Alert.alert('No Code', 'Please write some code first');
      return;
    }
    setSelectedAIMode(mode);
    setIsAILoading(true);
    setAIResponse('');
    try {
      const result = await aiAssist(code, selectedLanguage?.key || 'python', mode.key);
      setAIResponse(result.suggestion || 'No suggestion available');
    } catch (error: any) {
      setAIResponse(`AI Error: ${error.message}`);
    } finally {
      setIsAILoading(false);
    }
  }, [code, selectedLanguage, aiAssist]);

  // Tutorial handlers
  const nextTutorialStep = useCallback(() => {
    if (currentTutorialStep < tutorialSteps.length - 1) {
      setCurrentTutorialStep(prev => prev + 1);
    } else {
      setShowTutorial(false);
      setTutorialCompleted(true);
      Alert.alert('🎉 Welcome!', 'You\'re ready to start coding. Have fun!');
    }
  }, [currentTutorialStep, tutorialSteps.length, setTutorialCompleted]);

  const skipTutorial = useCallback(() => {
    setShowTutorial(false);
    setTutorialCompleted(true);
  }, [setTutorialCompleted]);

  // Bible handlers
  const handleBibleLoadCode = useCallback((bibleCode: string, language: string) => {
    const lang = languages.find(l => l.key === language || l.name.toLowerCase() === language);
    if (lang) {
      setSelectedLanguage(lang);
      setCode(bibleCode);
      loadTemplates(lang.key);
    }
  }, [languages, loadTemplates]);

  // Command Palette Action Handler
  const handleCommandPaletteAction = useCallback((actionId: string) => {
    setShowCommandPalette(false);
    switch (actionId) {
      // Code actions
      case 'run': executeCode(); break;
      case 'compile': setShowCompilerModal(true); break;
      case 'format': setShowCompilerModal(true); break;
      case 'hub': setShowHubModal(true); break;
      // AI actions
      case 'ai_pipeline': setShowAIPipelineModal(true); break;
      case 'debugger': setShowDebuggerModal(true); break;
      case 'code_to_app': setShowCodeToAppModal(true); break;
      case 'imagine': setShowImagineModal(true); break;
      case 'multi_agent': setShowAdvancedModal(true); break;
      // Learn actions
      case 'masterclass': setShowMasterclassModal(true); break;
      case 'education': setShowEducationModal(true); break;
      case 'curriculum': setShowCurriculumModal(true); break;
      case 'jeeves': setShowJeevesModal(true); break;
      // Create actions
      case 'assets': setShowAssetPipelineModal(true); break;
      case 'games': setShowGameGenresModal(true); break;
      case 'music': setShowMusicPipelineModal(true); break;
      // Pro tools
      case 'advanced': setShowAdvancedModal(true); break;
      case 'vault': setShowVaultModal(true); break;
      case 'collab': setShowCollaborationModal(true); break;
      case 'intelligence': setShowAdvancedModal(true); break;
      default: console.log('Unknown action:', actionId);
    }
  }, [executeCode]);

  // Icon helper
  const getIconName = (icon: string): keyof typeof Ionicons.glyphMap => {
    const iconMap: Record<string, keyof typeof Ionicons.glyphMap> = {
      'logo-python': 'logo-python', 'logo-html5': 'logo-html5', 'logo-javascript': 'logo-javascript',
      'logo-css3': 'logo-css3', 'code-slash': 'code-slash', 'document-text': 'document-text',
    };
    return iconMap[icon] || 'code-slash';
  };

  // ============================================================================
  // LOADING STATE
  // ============================================================================
  if (isLoading) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: colors.background }]}>
        <Animated.View style={{ opacity: fadeAnim }}>
          <View style={styles.loadingLogo}>
            <Ionicons name="code-slash" size={48} color={colors.primary} />
          </View>
          <Text style={[styles.loadingTitle, { color: colors.text }]}>CodeDock</Text>
          <Text style={[styles.loadingSubtitle, { color: colors.textMuted }]}>{CODENAME}</Text>
          <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 24 }} />
        </Animated.View>
      </View>
    );
  }

  const currentStep = tutorialSteps[currentTutorialStep];

  // ============================================================================
  // RENDER
  // ============================================================================
  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <StatusBar barStyle={theme === 'dark' ? 'light-content' : 'dark-content'} />
      
      {/* ============ HEADER ============ */}
      <View style={[styles.header, { backgroundColor: colors.surface, borderBottomColor: colors.border }]}>
        <Pressable style={styles.languageSelector} onPress={() => setShowLanguageModal(true)}>
          {selectedLanguage && (
            <>
              <View style={[styles.langIconBg, { backgroundColor: selectedLanguage.color + '20' }]}>
                <Ionicons name={getIconName(selectedLanguage.icon)} size={18} color={selectedLanguage.color} />
              </View>
              <View style={styles.langInfo}>
                <Text style={[styles.languageName, { color: colors.text }]}>{selectedLanguage.name}</Text>
                <Text style={[styles.languageVersion, { color: colors.textMuted }]}>
                  {selectedLanguage.display_name || selectedLanguage.extension}
                </Text>
              </View>
              <Ionicons name="chevron-down" size={16} color={colors.textMuted} />
            </>
          )}
        </Pressable>
        
        <View style={styles.headerActions}>
          {/* Connection Status */}
          {connectionStatus !== 'connected' && (
            <TouchableOpacity 
              style={[styles.headerButton, { backgroundColor: colors.error + '20' }]} 
              onPress={loadInitialData}
            >
              <Ionicons name="cloud-offline" size={18} color={colors.error} />
            </TouchableOpacity>
          )}
          <TouchableOpacity style={styles.headerButton} onPress={toggleTheme}>
            <Ionicons name={theme === 'dark' ? 'sunny' : 'moon'} size={20} color={colors.textSecondary} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.headerButton} onPress={() => setShowSettingsModal(true)}>
            <Ionicons name="settings-outline" size={20} color={colors.textSecondary} />
          </TouchableOpacity>
        </View>
      </View>

      {/* ============ ERROR BANNER ============ */}
      {lastError && (
        <View style={[styles.errorBanner, { backgroundColor: colors.error + '15', borderColor: colors.error }]}>
          <View style={styles.errorContent}>
            <Ionicons name="alert-circle" size={18} color={colors.error} />
            <Text style={[styles.errorText, { color: colors.error }]}>{lastError.message}</Text>
          </View>
          {lastError.retry && (
            <TouchableOpacity style={[styles.retryButton, { backgroundColor: colors.error }]} onPress={loadInitialData}>
              <Ionicons name="refresh" size={14} color="#FFF" />
              <Text style={styles.retryText}>Retry</Text>
            </TouchableOpacity>
          )}
        </View>
      )}

      {/* ============ TOOLBAR ============ */}
      <View style={[styles.toolbar, { backgroundColor: colors.surfaceAlt }]}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.toolbarContent}>
          <TouchableOpacity style={[styles.toolButton, { backgroundColor: colors.surface }]} onPress={() => setShowTemplateModal(true)}>
            <Ionicons name="flash" size={15} color={colors.warning} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Templates</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={[styles.toolButton, { backgroundColor: colors.surface }]} onPress={() => setShowFilesModal(true)}>
            <Ionicons name="folder" size={15} color={colors.accent} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Files</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={[styles.toolButton, { backgroundColor: colors.surface }]} onPress={saveFile}>
            <Ionicons name="save" size={15} color={colors.success} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Save</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={[styles.toolButton, { backgroundColor: colors.surface }]} onPress={clearCode}>
            <Ionicons name="trash-outline" size={15} color={colors.error} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Clear</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* ============ AI BAR (CLEANED UP v11.3) ============ */}
      <View style={[styles.aiBar, { backgroundColor: colors.surface }]}>
        <View style={styles.aiBarClean}>
          {/* AI Button - Primary Action */}
          <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
            <Pressable 
              style={[styles.aiButton, { backgroundColor: colors.primary + '15', borderColor: colors.primary + '40' }]}
              onPress={() => setShowAIModal(true)}
            >
              <Ionicons name="sparkles" size={18} color={colors.primary} />
              <Text style={[styles.aiButtonText, { color: colors.primary }]}>AI</Text>
              <View style={[styles.aiBadge, { backgroundColor: colors.primary }]}>
                <Text style={styles.aiBadgeText}>GPT-4o</Text>
              </View>
            </Pressable>
          </Animated.View>
          
          {/* Command Palette Button - Access All Features */}
          <TouchableOpacity 
            style={[styles.commandPaletteButton, { backgroundColor: colors.secondary + '15', borderColor: colors.secondary + '40' }]}
            onPress={() => setShowCommandPalette(true)}
          >
            <Ionicons name="apps" size={18} color={colors.secondary} />
            <Text style={[styles.commandPaletteText, { color: colors.secondary }]}>All Features</Text>
            <View style={[styles.featureCountBadge, { backgroundColor: colors.secondary }]}>
              <Text style={styles.featureCountText}>20+</Text>
            </View>
          </TouchableOpacity>
          
          {/* Quick Access: Jeeves AI Tutor */}
          <TouchableOpacity 
            style={[styles.quickAccessChip, { backgroundColor: '#6366F120' }]} 
            onPress={() => setShowJeevesModal(true)}
          >
            <Ionicons name="chatbubbles" size={16} color="#6366F1" />
          </TouchableOpacity>
          
          {/* Quick Access: Vault */}
          <TouchableOpacity 
            style={[styles.quickAccessChip, { backgroundColor: '#14B8A620' }]} 
            onPress={() => setShowVaultModal(true)}
          >
            <Ionicons name="file-tray-full" size={16} color="#14B8A6" />
          </TouchableOpacity>
          
          {/* Voice Button (if supported) */}
          {voice.isSupported && (
            <TouchableOpacity 
              style={[styles.quickAccessChip, { backgroundColor: voice.isListening ? '#EF444440' : '#EF444420' }]} 
              onPress={voice.toggleListening}
            >
              <Ionicons name={voice.isListening ? 'mic' : 'mic-outline'} size={16} color="#EF4444" />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* ============ EDITOR ============ */}
      <KeyboardAvoidingView style={styles.mainContent} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
        <View style={[styles.editorContainer, { backgroundColor: colors.codeBackground }]}>
          {/* Editor Header */}
          <View style={[styles.editorHeader, { borderBottomColor: colors.borderSubtle }]}>
            <View style={[styles.editorTab, { backgroundColor: colors.primary + '20', borderBottomColor: colors.primary }]}>
              <TextInput 
                style={[styles.fileNameInput, { color: colors.text }]} 
                value={currentFileName}
                onChangeText={setCurrentFileName} 
                placeholder="filename" 
                placeholderTextColor={colors.textMuted} 
              />
              <Text style={[styles.extensionText, { color: colors.textMuted }]}>{selectedLanguage?.extension || ''}</Text>
            </View>
            {executionTime !== null && (
              <Text style={[styles.execTime, { color: colors.success }]}>{executionTime.toFixed(1)}ms</Text>
            )}
          </View>
          
          {/* Code Editor */}
          <ScrollView style={styles.editorScroll} keyboardShouldPersistTaps="handled">
            <View style={styles.editorContent}>
              {/* Line Numbers */}
              <View style={[styles.lineNumbers, { backgroundColor: colors.surface + '50' }]}>
                {(code || ' ').split('\n').map((_, i) => (
                  <Text key={i} style={[styles.lineNumber, { color: colors.textMuted }]}>{i + 1}</Text>
                ))}
              </View>
              {/* Code Input */}
              <TextInput 
                style={[styles.codeInput, { color: colors.text }]} 
                value={code} 
                onChangeText={setCode}
                multiline 
                autoCapitalize="none" 
                autoCorrect={false} 
                spellCheck={false}
                placeholder="// Start coding here..." 
                placeholderTextColor={colors.textMuted} 
                textAlignVertical="top" 
              />
            </View>
          </ScrollView>
        </View>

        {/* ============ OUTPUT ============ */}
        {(showOutput || showWebPreview) && (
          <View style={[styles.outputContainer, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
            <View style={[styles.outputHeader, { borderBottomColor: colors.borderSubtle }]}>
              <View style={styles.outputTitleRow}>
                <Ionicons name={showWebPreview ? "globe" : "terminal"} size={16} color={colors.accent} />
                <Text style={[styles.outputTitle, { color: colors.text }]}>{showWebPreview ? 'Preview' : 'Output'}</Text>
              </View>
              <TouchableOpacity onPress={() => { setShowOutput(false); setShowWebPreview(false); }}>
                <Ionicons name="close" size={20} color={colors.textSecondary} />
              </TouchableOpacity>
            </View>
            {showWebPreview ? (
              <WebView style={styles.webPreview} source={{ html: htmlPreview }} originWhitelist={['*']} javaScriptEnabled />
            ) : (
              <ScrollView style={styles.outputScroll}>
                <Text style={[styles.outputText, { color: colors.text }]}>{output || 'No output'}</Text>
              </ScrollView>
            )}
          </View>
        )}
      </KeyboardAvoidingView>

      {/* ============ RUN BUTTON ============ */}
      <View style={[styles.bottomBar, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
        <Pressable 
          style={[styles.runButton, { backgroundColor: selectedLanguage?.executable ? colors.success : colors.surfaceAlt }]}
          onPress={executeCode} 
          disabled={isExecuting || !selectedLanguage?.executable}
        >
          {isExecuting ? (
            <ActivityIndicator size="small" color="#FFF" />
          ) : (
            <>
              <Ionicons name={selectedLanguage?.key === 'html' ? 'eye' : 'play'} size={22} color="#FFF" />
              <Text style={styles.runButtonText}>{selectedLanguage?.key === 'html' ? 'Preview' : 'Run'}</Text>
            </>
          )}
        </Pressable>
      </View>

      {/* ============ MODALS ============ */}

      {/* Language Modal */}
      <Modal visible={showLanguageModal} transparent animationType="slide" onRequestClose={() => setShowLanguageModal(false)}>
        <Pressable style={styles.modalOverlay} onPress={() => setShowLanguageModal(false)}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Select Language</Text>
              <TouchableOpacity onPress={() => setShowLanguageModal(false)}>
                <Ionicons name="close" size={24} color={colors.textSecondary} />
              </TouchableOpacity>
            </View>
            <ScrollView style={styles.modalScroll}>
              {languages.map((lang) => (
                <TouchableOpacity 
                  key={lang.key} 
                  style={[styles.langItem, { backgroundColor: colors.surfaceAlt, borderColor: selectedLanguage?.key === lang.key ? lang.color : colors.border }]}
                  onPress={() => selectLanguage(lang)}
                >
                  <View style={[styles.langItemIcon, { backgroundColor: lang.color + '20' }]}>
                    <Ionicons name={getIconName(lang.icon)} size={24} color={lang.color} />
                  </View>
                  <View style={styles.langItemInfo}>
                    <Text style={[styles.langItemName, { color: colors.text }]}>{lang.name}</Text>
                    <Text style={[styles.langItemDesc, { color: colors.textMuted }]}>{lang.display_name}</Text>
                  </View>
                  {lang.executable && (
                    <View style={[styles.execBadge, { backgroundColor: colors.success + '20' }]}>
                      <Text style={[styles.execBadgeText, { color: colors.success }]}>Run</Text>
                    </View>
                  )}
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        </Pressable>
      </Modal>

      {/* Templates Modal */}
      <Modal visible={showTemplateModal} transparent animationType="slide" onRequestClose={() => setShowTemplateModal(false)}>
        <Pressable style={styles.modalOverlay} onPress={() => setShowTemplateModal(false)}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Templates</Text>
              <TouchableOpacity onPress={() => setShowTemplateModal(false)}>
                <Ionicons name="close" size={24} color={colors.textSecondary} />
              </TouchableOpacity>
            </View>
            <ScrollView style={styles.modalScroll}>
              {templates.length === 0 ? (
                <Text style={[styles.emptyText, { color: colors.textMuted }]}>No templates available for {selectedLanguage?.name}</Text>
              ) : (
                templates.map((template, index) => (
                  <TouchableOpacity 
                    key={template.key || index} 
                    style={[styles.templateItem, { backgroundColor: colors.surfaceAlt }]}
                    onPress={() => applyTemplate(template)}
                  >
                    <Ionicons name="code-slash" size={20} color={colors.primary} />
                    <View style={styles.templateInfo}>
                      <Text style={[styles.templateName, { color: colors.text }]}>{template.name}</Text>
                      {template.description && (
                        <Text style={[styles.templateDesc, { color: colors.textMuted }]}>{template.description}</Text>
                      )}
                    </View>
                    <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
                  </TouchableOpacity>
                ))
              )}
            </ScrollView>
          </View>
        </Pressable>
      </Modal>

      {/* Files Modal */}
      <Modal visible={showFilesModal} transparent animationType="slide" onRequestClose={() => setShowFilesModal(false)}>
        <Pressable style={styles.modalOverlay} onPress={() => setShowFilesModal(false)}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Your Files</Text>
              <TouchableOpacity onPress={() => setShowFilesModal(false)}>
                <Ionicons name="close" size={24} color={colors.textSecondary} />
              </TouchableOpacity>
            </View>
            <ScrollView style={styles.modalScroll}>
              {files.length === 0 ? (
                <View style={styles.emptyState}>
                  <Ionicons name="folder-open-outline" size={48} color={colors.textMuted} />
                  <Text style={[styles.emptyText, { color: colors.textMuted }]}>No saved files yet</Text>
                  <Text style={[styles.emptyHint, { color: colors.textMuted }]}>Save your code to see it here</Text>
                </View>
              ) : (
                files.map((file, index) => (
                  <TouchableOpacity 
                    key={file.id || index} 
                    style={[styles.fileItem, { backgroundColor: colors.surfaceAlt }]}
                    onPress={() => loadFile(file)}
                  >
                    <Ionicons name="document-text" size={20} color={colors.accent} />
                    <View style={styles.fileInfo}>
                      <Text style={[styles.fileName, { color: colors.text }]}>{file.name}</Text>
                      <Text style={[styles.fileMeta, { color: colors.textMuted }]}>{file.language}</Text>
                    </View>
                    <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
                  </TouchableOpacity>
                ))
              )}
            </ScrollView>
          </View>
        </Pressable>
      </Modal>

      {/* AI Modal */}
      <Modal visible={showAIModal} transparent animationType="slide" onRequestClose={() => setShowAIModal(false)}>
        <Pressable style={styles.modalOverlay} onPress={() => setShowAIModal(false)}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface, maxHeight: '85%' }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.aiModalTitle}>
                <Ionicons name="sparkles" size={22} color={colors.primary} />
                <Text style={[styles.modalTitle, { color: colors.text }]}>AI Assistant</Text>
              </View>
              <TouchableOpacity onPress={() => setShowAIModal(false)}>
                <Ionicons name="close" size={24} color={colors.textSecondary} />
              </TouchableOpacity>
            </View>
            
            {!selectedAIMode ? (
              <ScrollView style={styles.modalScroll}>
                <Text style={[styles.aiSectionTitle, { color: colors.textMuted }]}>Choose an action</Text>
                {aiModes.map((mode) => (
                  <TouchableOpacity 
                    key={mode.key} 
                    style={[styles.aiModeItem, { backgroundColor: colors.surfaceAlt }]}
                    onPress={() => askAI(mode)}
                  >
                    <View style={[styles.aiModeIcon, { backgroundColor: colors.primary + '20' }]}>
                      <Ionicons name={mode.icon as any || 'bulb'} size={22} color={colors.primary} />
                    </View>
                    <View style={styles.aiModeInfo}>
                      <Text style={[styles.aiModeName, { color: colors.text }]}>{mode.name}</Text>
                      <Text style={[styles.aiModeDesc, { color: colors.textMuted }]}>{mode.description}</Text>
                    </View>
                    <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
                  </TouchableOpacity>
                ))}
              </ScrollView>
            ) : (
              <View style={styles.aiResponseContainer}>
                <View style={styles.aiResponseHeader}>
                  <TouchableOpacity style={styles.aiBackButton} onPress={() => setSelectedAIMode(null)}>
                    <Ionicons name="arrow-back" size={20} color={colors.primary} />
                    <Text style={[styles.aiBackText, { color: colors.primary }]}>Back</Text>
                  </TouchableOpacity>
                  <Text style={[styles.aiModeLabel, { color: colors.text }]}>{selectedAIMode.name}</Text>
                </View>
                {isAILoading ? (
                  <View style={styles.aiLoading}>
                    <ActivityIndicator size="large" color={colors.primary} />
                    <Text style={[styles.aiLoadingText, { color: colors.textMuted }]}>Thinking...</Text>
                  </View>
                ) : (
                  <ScrollView style={styles.aiResponseScroll}>
                    <Text style={[styles.aiResponseText, { color: colors.text }]}>{aiResponse}</Text>
                  </ScrollView>
                )}
              </View>
            )}
          </View>
        </Pressable>
      </Modal>

      {/* Settings Modal */}
      <Modal visible={showSettingsModal} transparent animationType="slide" onRequestClose={() => setShowSettingsModal(false)}>
        <Pressable style={styles.modalOverlay} onPress={() => setShowSettingsModal(false)}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Settings</Text>
              <TouchableOpacity onPress={() => setShowSettingsModal(false)}>
                <Ionicons name="close" size={24} color={colors.textSecondary} />
              </TouchableOpacity>
            </View>
            <ScrollView style={styles.modalScroll}>
              {/* Theme */}
              <TouchableOpacity style={[styles.settingItem, { backgroundColor: colors.surfaceAlt }]} onPress={toggleTheme}>
                <Ionicons name={theme === 'dark' ? 'moon' : 'sunny'} size={22} color={colors.primary} />
                <View style={styles.settingInfo}>
                  <Text style={[styles.settingName, { color: colors.text }]}>Theme</Text>
                  <Text style={[styles.settingValue, { color: colors.textMuted }]}>{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
              </TouchableOpacity>
              
              {/* Tutorial */}
              <TouchableOpacity 
                style={[styles.settingItem, { backgroundColor: colors.surfaceAlt }]} 
                onPress={() => { setShowSettingsModal(false); setCurrentTutorialStep(0); setShowTutorial(true); }}
              >
                <Ionicons name="school" size={22} color={colors.secondary} />
                <View style={styles.settingInfo}>
                  <Text style={[styles.settingName, { color: colors.text }]}>Tutorial</Text>
                  <Text style={[styles.settingValue, { color: colors.textMuted }]}>Restart the onboarding</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
              </TouchableOpacity>
              
              {/* About */}
              <View style={[styles.aboutSection, { backgroundColor: colors.surfaceAlt }]}>
                <Text style={[styles.aboutTitle, { color: colors.text }]}>CodeDock</Text>
                <Text style={[styles.aboutVersion, { color: colors.textMuted }]}>v{VERSION} • {CODENAME}</Text>
                <Text style={[styles.aboutDesc, { color: colors.textMuted }]}>A mobile-first code compiler and learning platform.</Text>
              </View>
            </ScrollView>
          </View>
        </Pressable>
      </Modal>

      {/* Tutorial Modal */}
      <Modal visible={showTutorial && tutorialSteps.length > 0} transparent animationType="fade" onRequestClose={skipTutorial}>
        <View style={styles.tutorialOverlay}>
          <View style={[styles.tutorialCard, { backgroundColor: colors.surface }]}>
            <View style={[styles.tutorialHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.tutorialProgress}>
                <Text style={[styles.tutorialStep, { color: colors.secondary }]}>
                  Step {currentTutorialStep + 1} of {tutorialSteps.length}
                </Text>
                <View style={[styles.progressBar, { backgroundColor: colors.surfaceAlt }]}>
                  <View style={[styles.progressFill, { 
                    backgroundColor: colors.secondary, 
                    width: `${((currentTutorialStep + 1) / tutorialSteps.length) * 100}%` 
                  }]} />
                </View>
              </View>
              <TouchableOpacity onPress={skipTutorial}>
                <Text style={[styles.skipText, { color: colors.textMuted }]}>Skip</Text>
              </TouchableOpacity>
            </View>
            
            {currentStep && (
              <ScrollView style={styles.tutorialContent}>
                <View style={[styles.tutorialIcon, { backgroundColor: colors.secondary + '20' }]}>
                  <Ionicons name={
                    currentStep.key === 'welcome' ? 'rocket' :
                    currentStep.key === 'select_language' ? 'code-slash' :
                    currentStep.key === 'use_templates' ? 'flash' :
                    currentStep.key === 'write_code' ? 'create' :
                    currentStep.key === 'run_code' ? 'play' :
                    currentStep.key === 'use_ai' ? 'sparkles' : 'bulb'
                  } size={40} color={colors.secondary} />
                </View>
                <Text style={[styles.tutorialTitle, { color: colors.text }]}>{currentStep.title}</Text>
                <Text style={[styles.tutorialDesc, { color: colors.textSecondary }]}>{currentStep.description}</Text>
                <Text style={[styles.tutorialContentText, { color: colors.text }]}>{currentStep.content}</Text>
                
                {currentStep.tips && currentStep.tips.length > 0 && (
                  <View style={[styles.tutorialTips, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.tipsTitle, { color: colors.secondary }]}>💡 Tips</Text>
                    {currentStep.tips.map((tip, i) => (
                      <Text key={i} style={[styles.tipText, { color: colors.textSecondary }]}>• {tip}</Text>
                    ))}
                  </View>
                )}
              </ScrollView>
            )}
            
            <View style={[styles.tutorialNav, { borderTopColor: colors.border }]}>
              {currentTutorialStep > 0 ? (
                <TouchableOpacity 
                  style={[styles.tutorialNavBtn, { backgroundColor: colors.surfaceAlt }]} 
                  onPress={() => setCurrentTutorialStep(prev => prev - 1)}
                >
                  <Ionicons name="arrow-back" size={18} color={colors.text} />
                  <Text style={[styles.tutorialNavText, { color: colors.text }]}>Back</Text>
                </TouchableOpacity>
              ) : <View style={styles.tutorialNavBtn} />}
              
              <TouchableOpacity 
                style={[styles.tutorialNavBtn, styles.tutorialNavPrimary, { backgroundColor: colors.secondary }]} 
                onPress={nextTutorialStep}
              >
                <Text style={styles.tutorialNavTextPrimary}>
                  {currentTutorialStep === tutorialSteps.length - 1 ? 'Get Started' : 'Next'}
                </Text>
                <Ionicons name={currentTutorialStep === tutorialSteps.length - 1 ? 'checkmark' : 'arrow-forward'} size={18} color="#FFF" />
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* Bible Modal */}
      <BibleModal
        visible={showBibleModal}
        onClose={() => setShowBibleModal(false)}
        colors={colors}
        progress={bibleProgress}
        onMarkComplete={markChapterComplete}
        onToggleBookmark={toggleBookmark}
        onLoadCode={handleBibleLoadCode}
      />

      {/* Compiler Suite Modal */}
      <CompilerModal
        visible={showCompilerModal}
        onClose={() => setShowCompilerModal(false)}
        colors={colors}
        code={code}
        language={selectedLanguage?.key || 'python'}
        onApplyFix={(fixedCode) => setCode(fixedCode)}
      />

      {/* Pipeline Visualizer Modal */}
      <PipelineVisualizer
        visible={showPipelineModal}
        onClose={() => setShowPipelineModal(false)}
        colors={colors}
      />

      {/* Learning Dashboard Modal */}
      <LearningDashboard
        visible={showLearningModal}
        onClose={() => setShowLearningModal(false)}
        colors={colors}
      />

      {/* Collaboration Modal */}
      <CollaborationModal
        visible={showCollaborationModal}
        onClose={() => setShowCollaborationModal(false)}
        colors={colors}
        code={code}
        language={selectedLanguage?.key || 'python'}
        onCodeChange={setCode}
      />

      {/* Ultimate Hub Modal */}
      <HubModal
        visible={showHubModal}
        onClose={() => setShowHubModal(false)}
        colors={colors}
      />

      {/* AI Feature Suggestions Modal */}
      <AISuggestionsModal
        visible={showAISuggestionsModal}
        onClose={() => setShowAISuggestionsModal(false)}
        colors={colors}
        context={{
          languages: [selectedLanguage?.key || 'python'],
          skill_level: 'intermediate',
        }}
      />

      {/* v11.0 AI Pipeline Modal */}
      <AIPipelineModal
        visible={showAIPipelineModal}
        onClose={() => setShowAIPipelineModal(false)}
        colors={colors}
        onCodeGenerated={(generatedCode, lang) => {
          setCode(generatedCode);
          const language = languages.find(l => l.key === lang);
          if (language) {
            setSelectedLanguage(language);
          }
          setShowAIPipelineModal(false);
        }}
      />

      {/* v11.0 Curriculum Browser Modal */}
      <CurriculumBrowser
        visible={showCurriculumModal}
        onClose={() => setShowCurriculumModal(false)}
        colors={colors}
        onCodeExample={(exampleCode, lang) => {
          setCode(exampleCode);
          const language = languages.find(l => l.key === lang);
          if (language) {
            setSelectedLanguage(language);
          }
          setShowCurriculumModal(false);
        }}
      />

      {/* v11.0 Vault Modal */}
      <VaultModal
        visible={showVaultModal}
        onClose={() => setShowVaultModal(false)}
        colors={colors}
        currentCode={code}
        currentLanguage={selectedLanguage?.key}
        onLoadCode={(loadedCode, lang) => {
          setCode(loadedCode);
          const language = languages.find(l => l.key === lang);
          if (language) {
            setSelectedLanguage(language);
          }
          setShowVaultModal(false);
        }}
      />

      {/* v11.0 Advanced Features Modal */}
      <AdvancedFeaturesModal
        visible={showAdvancedModal}
        onClose={() => setShowAdvancedModal(false)}
        colors={colors}
        currentCode={code}
        currentLanguage={selectedLanguage?.key}
      />

      {/* v11.0 Code-to-App Modal */}
      <CodeToAppModal
        visible={showCodeToAppModal}
        onClose={() => setShowCodeToAppModal(false)}
        colors={colors}
        currentCode={code}
        currentLanguage={selectedLanguage?.key}
      />

      {/* v11.0 Imagine (Image Generation) Modal */}
      <ImagineModal
        visible={showImagineModal}
        onClose={() => setShowImagineModal(false)}
        colors={colors}
      />

      {/* v11.1 SOTA 2026 Feature Modals */}
      {/* AI Debugger Modal */}
      <DebuggerModal
        visible={showDebuggerModal}
        onClose={() => setShowDebuggerModal(false)}
        colors={colors}
        currentCode={code}
        currentLanguage={selectedLanguage?.key}
        onApplyFix={(fixedCode) => setCode(fixedCode)}
      />

      {/* Music Pipeline Modal */}
      <MusicPipelineModal
        visible={showMusicPipelineModal}
        onClose={() => setShowMusicPipelineModal(false)}
        colors={colors}
      />

      {/* Interactive Education Modal */}
      <EducationModal
        visible={showEducationModal}
        onClose={() => setShowEducationModal(false)}
        colors={colors}
        onCodeLoad={(loadedCode, lang) => {
          setCode(loadedCode);
          const language = languages.find(l => l.key === lang);
          if (language) {
            setSelectedLanguage(language);
          }
          setShowEducationModal(false);
        }}
      />

      {/* Jeeves AI Tutor Modal */}
      <JeevesModal
        visible={showJeevesModal}
        onClose={() => setShowJeevesModal(false)}
        colors={colors}
        currentCode={code}
        currentLanguage={selectedLanguage?.key}
      />

      {/* v11.2 Masterclass Modal */}
      <MasterclassModal
        visible={showMasterclassModal}
        onClose={() => setShowMasterclassModal(false)}
        colors={colors}
      />

      {/* Asset Pipeline Modal */}
      <AssetPipelineModal
        visible={showAssetPipelineModal}
        onClose={() => setShowAssetPipelineModal(false)}
        colors={colors}
      />

      {/* Game Genres Modal */}
      <GameGenresModal
        visible={showGameGenresModal}
        onClose={() => setShowGameGenresModal(false)}
        colors={colors}
      />

      {/* v11.3 Command Palette */}
      <CommandPalette
        visible={showCommandPalette}
        onClose={() => setShowCommandPalette(false)}
        onSelectAction={handleCommandPaletteAction}
        colors={colors}
      />
    </SafeAreaView>
  );
}

// ============================================================================
// STYLES
// ============================================================================
const styles = StyleSheet.create({
  // Loading
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingLogo: {
    width: 80,
    height: 80,
    borderRadius: 20,
    backgroundColor: 'rgba(99, 102, 241, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    alignSelf: 'center',
  },
  loadingTitle: {
    fontSize: 28,
    fontWeight: '800',
    textAlign: 'center',
  },
  loadingSubtitle: {
    fontSize: 14,
    marginTop: 4,
    textAlign: 'center',
  },

  // Main Container
  container: {
    flex: 1,
  },

  // Header
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  languageSelector: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingVertical: 4,
  },
  langIconBg: {
    width: 36,
    height: 36,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  langInfo: {
    marginRight: 4,
  },
  languageName: {
    fontSize: 16,
    fontWeight: '700',
  },
  languageVersion: {
    fontSize: 11,
    marginTop: 1,
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  headerButton: {
    padding: 8,
    borderRadius: 8,
  },

  // Error Banner
  errorBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderBottomWidth: 1,
  },
  errorContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    flex: 1,
  },
  errorText: {
    fontSize: 13,
    fontWeight: '500',
    flex: 1,
  },
  retryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
    gap: 4,
  },
  retryText: {
    color: '#FFF',
    fontSize: 12,
    fontWeight: '600',
  },

  // Toolbar
  toolbar: {
    paddingVertical: 8,
    paddingHorizontal: 8,
  },
  toolbarContent: {
    paddingHorizontal: 8,
    gap: 8,
  },
  toolButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    gap: 6,
  },
  toolButtonText: {
    fontSize: 13,
    fontWeight: '600',
  },

  // AI Bar
  aiBar: {
    paddingVertical: 10,
  },
  aiBarContent: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    gap: 10,
  },
  aiBarClean: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    gap: 10,
  },
  aiButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 10,
    borderWidth: 1,
    gap: 8,
  },
  aiButtonText: {
    fontSize: 14,
    fontWeight: '700',
  },
  aiBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  aiBadgeText: {
    color: '#FFF',
    fontSize: 10,
    fontWeight: '700',
  },
  commandPaletteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 10,
    borderWidth: 1,
    gap: 8,
    flex: 1,
  },
  commandPaletteText: {
    fontSize: 14,
    fontWeight: '600',
  },
  featureCountBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    marginLeft: 'auto',
  },
  featureCountText: {
    color: '#FFF',
    fontSize: 10,
    fontWeight: '700',
  },
  quickAccessChip: {
    width: 40,
    height: 40,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureChip: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    gap: 6,
  },
  featureChipText: {
    fontSize: 13,
    fontWeight: '600',
  },

  // Editor
  mainContent: {
    flex: 1,
  },
  editorContainer: {
    flex: 1,
  },
  editorHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderBottomWidth: 1,
  },
  editorTab: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
    borderBottomWidth: 2,
  },
  fileNameInput: {
    fontSize: 14,
    fontWeight: '600',
    minWidth: 80,
  },
  extensionText: {
    fontSize: 12,
  },
  execTime: {
    fontSize: 12,
    fontWeight: '600',
  },
  editorScroll: {
    flex: 1,
  },
  editorContent: {
    flexDirection: 'row',
    minHeight: 300,
  },
  lineNumbers: {
    paddingVertical: 12,
    paddingHorizontal: 12,
    alignItems: 'flex-end',
  },
  lineNumber: {
    fontSize: 13,
    lineHeight: 22,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  codeInput: {
    flex: 1,
    fontSize: 14,
    lineHeight: 22,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    paddingVertical: 12,
    paddingHorizontal: 12,
    textAlignVertical: 'top',
  },

  // Output
  outputContainer: {
    height: 180,
    borderTopWidth: 1,
  },
  outputHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderBottomWidth: 1,
  },
  outputTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  outputTitle: {
    fontSize: 14,
    fontWeight: '700',
  },
  outputScroll: {
    flex: 1,
    padding: 12,
  },
  outputText: {
    fontSize: 13,
    lineHeight: 20,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  webPreview: {
    flex: 1,
  },

  // Bottom Bar
  bottomBar: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
  },
  runButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 12,
    gap: 10,
  },
  runButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '700',
  },

  // Modal Base
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    maxHeight: '80%',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
  },
  modalScroll: {
    padding: 16,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 15,
    marginTop: 12,
    textAlign: 'center',
  },
  emptyHint: {
    fontSize: 13,
    marginTop: 4,
    textAlign: 'center',
  },

  // Language Modal Items
  langItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderRadius: 12,
    marginBottom: 10,
    borderWidth: 1.5,
  },
  langItemIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  langItemInfo: {
    flex: 1,
    marginLeft: 12,
  },
  langItemName: {
    fontSize: 16,
    fontWeight: '700',
  },
  langItemDesc: {
    fontSize: 12,
    marginTop: 2,
  },
  execBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
  },
  execBadgeText: {
    fontSize: 11,
    fontWeight: '700',
  },

  // Template Items
  templateItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderRadius: 12,
    marginBottom: 10,
    gap: 12,
  },
  templateInfo: {
    flex: 1,
  },
  templateName: {
    fontSize: 15,
    fontWeight: '600',
  },
  templateDesc: {
    fontSize: 12,
    marginTop: 2,
  },

  // File Items
  fileItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderRadius: 12,
    marginBottom: 10,
    gap: 12,
  },
  fileInfo: {
    flex: 1,
  },
  fileName: {
    fontSize: 15,
    fontWeight: '600',
  },
  fileMeta: {
    fontSize: 12,
    marginTop: 2,
  },

  // AI Modal
  aiModalTitle: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  aiSectionTitle: {
    fontSize: 13,
    fontWeight: '600',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  aiModeItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderRadius: 12,
    marginBottom: 10,
    gap: 12,
  },
  aiModeIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  aiModeInfo: {
    flex: 1,
  },
  aiModeName: {
    fontSize: 15,
    fontWeight: '700',
  },
  aiModeDesc: {
    fontSize: 12,
    marginTop: 2,
  },
  aiResponseContainer: {
    flex: 1,
  },
  aiResponseHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 12,
  },
  aiBackButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  aiBackText: {
    fontSize: 14,
    fontWeight: '600',
  },
  aiModeLabel: {
    fontSize: 15,
    fontWeight: '600',
  },
  aiLoading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  aiLoadingText: {
    marginTop: 16,
    fontSize: 14,
  },
  aiResponseScroll: {
    flex: 1,
    padding: 16,
  },
  aiResponseText: {
    fontSize: 14,
    lineHeight: 22,
  },

  // Settings Modal
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderRadius: 12,
    marginBottom: 10,
    gap: 12,
  },
  settingInfo: {
    flex: 1,
  },
  settingName: {
    fontSize: 15,
    fontWeight: '600',
  },
  settingValue: {
    fontSize: 12,
    marginTop: 2,
  },
  aboutSection: {
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 20,
  },
  aboutTitle: {
    fontSize: 20,
    fontWeight: '800',
  },
  aboutVersion: {
    fontSize: 13,
    marginTop: 4,
  },
  aboutDesc: {
    fontSize: 12,
    marginTop: 8,
    textAlign: 'center',
  },

  // Tutorial Modal
  tutorialOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'center',
    padding: 20,
  },
  tutorialCard: {
    borderRadius: 20,
    maxHeight: '80%',
    overflow: 'hidden',
  },
  tutorialHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  tutorialProgress: {
    flex: 1,
    marginRight: 16,
  },
  tutorialStep: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 6,
  },
  progressBar: {
    height: 4,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 2,
  },
  skipText: {
    fontSize: 14,
    fontWeight: '600',
  },
  tutorialContent: {
    padding: 20,
  },
  tutorialIcon: {
    width: 80,
    height: 80,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginBottom: 16,
  },
  tutorialTitle: {
    fontSize: 24,
    fontWeight: '800',
    textAlign: 'center',
    marginBottom: 8,
  },
  tutorialDesc: {
    fontSize: 15,
    textAlign: 'center',
    marginBottom: 16,
  },
  tutorialContentText: {
    fontSize: 14,
    lineHeight: 22,
  },
  tutorialTips: {
    padding: 14,
    borderRadius: 12,
    marginTop: 16,
  },
  tipsTitle: {
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 8,
  },
  tipText: {
    fontSize: 13,
    lineHeight: 22,
  },
  tutorialNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderTopWidth: 1,
  },
  tutorialNavBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 10,
    gap: 6,
  },
  tutorialNavPrimary: {
    paddingHorizontal: 24,
  },
  tutorialNavText: {
    fontSize: 14,
    fontWeight: '600',
  },
  tutorialNavTextPrimary: {
    color: '#FFF',
    fontSize: 14,
    fontWeight: '700',
  },
});
