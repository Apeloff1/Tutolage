import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  TextInput,
  ActivityIndicator,
  SafeAreaView,
  StatusBar,
  Platform,
  Dimensions,
  KeyboardAvoidingView,
  Modal,
  FlatList,
  Alert,
  Animated,
  Vibration,
} from 'react-native';
import { WebView } from 'react-native-webview';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';
const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

// Types
interface Language {
  key: string;
  name: string;
  extension: string;
  icon: string;
  color: string;
  executable: boolean;
  description?: string;
  version?: string;
  type: 'builtin' | 'addon';
  templates_available?: boolean;
}

interface ExecutionResult {
  status: 'success' | 'error' | 'timeout' | 'pending' | 'security_violation';
  output: string;
  error: string;
  metrics?: {
    execution_time_ms: number;
  };
  analysis?: CodeAnalysis;
}

interface CodeAnalysis {
  complexity: string;
  cyclomatic_complexity: number;
  lines_of_code: number;
  functions_count: number;
  classes_count: number;
}

interface Template {
  key: string;
  name: string;
  code: string;
  description?: string;
  complexity?: string;
}

interface SavedFile {
  id: string;
  name: string;
  language: string;
  code: string;
  updated_at: string;
  is_favorite?: boolean;
  execution_count?: number;
}

interface AIMode {
  key: string;
  name: string;
  description: string;
}

// Theme configuration - 2026 Design System
const themes = {
  dark: {
    background: '#09090B',
    surface: '#18181B',
    surfaceAlt: '#27272A',
    surfaceHover: '#3F3F46',
    primary: '#6366F1',
    primaryGlow: 'rgba(99, 102, 241, 0.3)',
    secondary: '#A1A1AA',
    accent: '#22D3EE',
    text: '#FAFAFA',
    textSecondary: '#A1A1AA',
    textMuted: '#71717A',
    border: '#3F3F46',
    borderSubtle: '#27272A',
    success: '#22C55E',
    successGlow: 'rgba(34, 197, 94, 0.2)',
    error: '#EF4444',
    errorGlow: 'rgba(239, 68, 68, 0.2)',
    warning: '#F59E0B',
    warningGlow: 'rgba(245, 158, 11, 0.2)',
    codeBackground: '#0A0A0B',
    codeLine: '#18181B',
    aiGlow: 'rgba(139, 92, 246, 0.3)',
  },
  light: {
    background: '#FAFAFA',
    surface: '#FFFFFF',
    surfaceAlt: '#F4F4F5',
    surfaceHover: '#E4E4E7',
    primary: '#4F46E5',
    primaryGlow: 'rgba(79, 70, 229, 0.15)',
    secondary: '#71717A',
    accent: '#0891B2',
    text: '#18181B',
    textSecondary: '#52525B',
    textMuted: '#A1A1AA',
    border: '#E4E4E7',
    borderSubtle: '#F4F4F5',
    success: '#16A34A',
    successGlow: 'rgba(22, 163, 74, 0.1)',
    error: '#DC2626',
    errorGlow: 'rgba(220, 38, 38, 0.1)',
    warning: '#D97706',
    warningGlow: 'rgba(217, 119, 6, 0.1)',
    codeBackground: '#FAFAFA',
    codeLine: '#F4F4F5',
    aiGlow: 'rgba(124, 58, 237, 0.15)',
  },
};

export default function CodeDockQuantum() {
  // Core State
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [languages, setLanguages] = useState<Language[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<Language | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [currentFileName, setCurrentFileName] = useState('untitled');
  
  // Modal State
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [showFilesModal, setShowFilesModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showAddonModal, setShowAddonModal] = useState(false);
  const [showAIModal, setShowAIModal] = useState(false);
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);
  
  // Data State
  const [templates, setTemplates] = useState<Template[]>([]);
  const [savedFiles, setSavedFiles] = useState<SavedFile[]>([]);
  const [aiModes, setAIModes] = useState<AIMode[]>([]);
  const [selectedAIMode, setSelectedAIMode] = useState<AIMode | null>(null);
  const [aiResponse, setAIResponse] = useState('');
  const [isAILoading, setIsAILoading] = useState(false);
  const [codeAnalysis, setCodeAnalysis] = useState<CodeAnalysis | null>(null);
  
  // UI State
  const [showOutput, setShowOutput] = useState(false);
  const [showWebPreview, setShowWebPreview] = useState(false);
  const [htmlPreview, setHtmlPreview] = useState('');
  const [loading, setLoading] = useState(true);
  const [executionTime, setExecutionTime] = useState<number | null>(null);

  // Animation refs
  const pulseAnim = useRef(new Animated.Value(1)).current;

  const colors = themes[theme];

  // Pulse animation for AI button
  useEffect(() => {
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 1500,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1500,
          useNativeDriver: true,
        }),
      ])
    );
    pulse.start();
    return () => pulse.stop();
  }, []);

  // Load initial data
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // Load theme
      const savedTheme = await AsyncStorage.getItem('codedock_theme');
      if (savedTheme) setTheme(savedTheme as 'dark' | 'light');

      // Load languages
      const langResponse = await axios.get(`${API_URL}/api/languages`);
      const langs = langResponse.data.languages || [];
      setLanguages(langs);

      // Set default language
      const defaultLang = langs.find((l: Language) => l.key === 'python');
      if (defaultLang) {
        setSelectedLanguage(defaultLang);
        loadTemplates('python');
      }

      // Load AI modes
      const aiResponse = await axios.get(`${API_URL}/api/ai/modes`);
      setAIModes(aiResponse.data.modes || []);

      // Load files
      loadFiles();
    } catch (error) {
      console.error('Failed to load data:', error);
      // Fallback languages
      setLanguages([
        { key: 'python', name: 'Python', extension: '.py', icon: 'logo-python', color: '#3776AB', executable: true, type: 'builtin', version: '3.12+' },
        { key: 'html', name: 'HTML', extension: '.html', icon: 'logo-html5', color: '#E34F26', executable: true, type: 'builtin', version: '5.3' },
        { key: 'javascript', name: 'JavaScript', extension: '.js', icon: 'logo-javascript', color: '#F7DF1E', executable: true, type: 'builtin', version: 'ES2026' },
        { key: 'typescript', name: 'TypeScript', extension: '.ts', icon: 'logo-javascript', color: '#3178C6', executable: true, type: 'builtin', version: '5.6+' },
        { key: 'cpp', name: 'C++', extension: '.cpp', icon: 'code-slash', color: '#00599C', executable: true, type: 'builtin', version: 'C++23' },
        { key: 'c', name: 'C', extension: '.c', icon: 'code-slash', color: '#A8B9CC', executable: true, type: 'builtin', version: 'C23' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const loadTemplates = async (language: string) => {
    try {
      const response = await axios.get(`${API_URL}/api/templates/${language}`);
      setTemplates(response.data.templates || []);
    } catch (error) {
      setTemplates([]);
    }
  };

  const loadFiles = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/files`);
      setSavedFiles(response.data.files || []);
    } catch (error) {
      console.error('Failed to load files:', error);
    }
  };

  const toggleTheme = async () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    await AsyncStorage.setItem('codedock_theme', newTheme);
    if (Platform.OS !== 'web') Vibration.vibrate(10);
  };

  const selectLanguage = (lang: Language) => {
    setSelectedLanguage(lang);
    setShowLanguageModal(false);
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    setCodeAnalysis(null);
    loadTemplates(lang.key);
  };

  const executeCode = async () => {
    if (!code.trim() || !selectedLanguage) return;

    setIsExecuting(true);
    setOutput('');
    setShowOutput(true);
    setShowWebPreview(false);
    setExecutionTime(null);

    try {
      // For HTML, show preview directly
      if (selectedLanguage.key === 'html') {
        setHtmlPreview(code);
        setShowWebPreview(true);
        setShowOutput(false);
        setOutput('HTML rendered in preview');
        return;
      }

      // For JavaScript/TypeScript, execute in WebView
      if (selectedLanguage.key === 'javascript' || selectedLanguage.key === 'typescript') {
        const response = await axios.post(`${API_URL}/api/execute`, {
          code,
          language: selectedLanguage.key,
        });
        
        const wrappedCode = response.data.result.output;
        setHtmlPreview(`
          <html>
          <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              body { 
                font-family: 'SF Mono', Menlo, monospace; 
                padding: 16px; 
                background: ${colors.codeBackground}; 
                color: ${colors.text};
                font-size: 14px;
                line-height: 1.6;
              }
              pre { white-space: pre-wrap; word-wrap: break-word; margin: 0; }
              .success { color: ${colors.success}; }
              .error { color: ${colors.error}; }
            </style>
          </head>
          <body>
          <pre id="output"></pre>
          <script>
            try {
              var result = ${wrappedCode};
              document.getElementById('output').innerHTML = 
                '<span class="' + result.status + '">' + 
                (result.status === 'success' ? result.output : 'Error: ' + result.error) + 
                '</span>';
            } catch(e) {
              document.getElementById('output').innerHTML = '<span class="error">Error: ' + e.message + '</span>';
            }
          </script>
          </body>
          </html>
        `);
        setShowWebPreview(true);
        setExecutionTime(response.data.result.metrics?.execution_time_ms || 0);
        return;
      }

      // For other languages, execute on server
      const response = await axios.post(`${API_URL}/api/execute`, {
        code,
        language: selectedLanguage.key,
        timeout_seconds: 15,
        include_analysis: true,
      });

      const result: ExecutionResult = response.data.result;
      setExecutionTime(result.metrics?.execution_time_ms || 0);
      
      if (result.analysis) {
        setCodeAnalysis(result.analysis);
      }
      
      if (result.status === 'success') {
        setOutput(result.output || 'Program executed successfully (no output)');
      } else if (result.status === 'timeout') {
        setOutput(`⏱ Timeout: ${result.error}`);
      } else if (result.status === 'security_violation') {
        setOutput(`🛡 Security: ${result.error}`);
      } else {
        setOutput(`❌ Error: ${result.error || 'Unknown error'}`);
      }
    } catch (error: any) {
      setOutput(`Execution failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsExecuting(false);
    }
  };

  const analyzeCode = async () => {
    if (!code.trim() || !selectedLanguage) return;
    
    try {
      const response = await axios.post(`${API_URL}/api/analyze`, {
        code,
        language: selectedLanguage.key,
      });
      setCodeAnalysis(response.data.analysis);
      setShowAnalysisModal(true);
    } catch (error) {
      Alert.alert('Error', 'Failed to analyze code');
    }
  };

  const askAI = async (mode: AIMode) => {
    if (!code.trim() || !selectedLanguage) {
      Alert.alert('No Code', 'Please write some code first');
      return;
    }

    setSelectedAIMode(mode);
    setIsAILoading(true);
    setAIResponse('');

    try {
      const response = await axios.post(`${API_URL}/api/ai/assist`, {
        code,
        language: selectedLanguage.key,
        mode: mode.key,
      });
      
      setAIResponse(response.data.suggestion);
    } catch (error: any) {
      setAIResponse(`AI Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsAILoading(false);
    }
  };

  const saveFile = async () => {
    if (!code.trim() || !selectedLanguage) return;

    try {
      await axios.post(`${API_URL}/api/files`, {
        name: currentFileName + selectedLanguage.extension,
        language: selectedLanguage.key,
        code,
      });
      Alert.alert('Saved', 'File saved successfully');
      loadFiles();
    } catch (error) {
      Alert.alert('Error', 'Failed to save file');
    }
  };

  const loadFile = (file: SavedFile) => {
    const lang = languages.find(l => l.key === file.language);
    if (lang) {
      setSelectedLanguage(lang);
      setCode(file.code);
      setCurrentFileName(file.name.replace(/\.[^/.]+$/, ''));
      setShowFilesModal(false);
      setShowOutput(false);
      loadTemplates(lang.key);
    }
  };

  const deleteFile = async (fileId: string) => {
    try {
      await axios.delete(`${API_URL}/api/files/${fileId}`);
      loadFiles();
    } catch (error) {
      Alert.alert('Error', 'Failed to delete file');
    }
  };

  const applyTemplate = (template: Template) => {
    setCode(template.code);
    setShowTemplateModal(false);
    setShowOutput(false);
    setCodeAnalysis(null);
  };

  const clearCode = () => {
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    setCodeAnalysis(null);
    setExecutionTime(null);
  };

  const getIconName = (icon: string): keyof typeof Ionicons.glyphMap => {
    const iconMap: { [key: string]: keyof typeof Ionicons.glyphMap } = {
      'logo-python': 'logo-python',
      'logo-html5': 'logo-html5',
      'logo-javascript': 'logo-javascript',
      'logo-css3': 'logo-css3',
      'code-slash': 'code-slash',
      'code-working': 'code-working',
      'document-text': 'document-text',
      'server': 'server',
      'hardware-chip': 'hardware-chip',
      'terminal': 'terminal',
    };
    return iconMap[icon] || 'code-slash';
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'trivial': return colors.success;
      case 'simple': return colors.accent;
      case 'moderate': return colors.warning;
      case 'complex': return colors.error;
      case 'very_complex': return '#DC2626';
      default: return colors.secondary;
    }
  };

  if (loading) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: colors.background }]}>
        <View style={styles.loadingContent}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={[styles.loadingTitle, { color: colors.text }]}>CodeDock Quantum</Text>
          <Text style={[styles.loadingSubtitle, { color: colors.textSecondary }]}>2026+ Edition</Text>
        </View>
      </View>
    );
  }

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <StatusBar barStyle={theme === 'dark' ? 'light-content' : 'dark-content'} />
      
      {/* Header */}
      <View style={[styles.header, { backgroundColor: colors.surface, borderBottomColor: colors.border }]}>
        <TouchableOpacity
          style={styles.languageSelector}
          onPress={() => setShowLanguageModal(true)}
        >
          {selectedLanguage && (
            <>
              <View style={[styles.langIconBg, { backgroundColor: selectedLanguage.color + '20' }]}>
                <Ionicons
                  name={getIconName(selectedLanguage.icon)}
                  size={18}
                  color={selectedLanguage.color}
                />
              </View>
              <View>
                <Text style={[styles.languageName, { color: colors.text }]}>
                  {selectedLanguage.name}
                </Text>
                <Text style={[styles.languageVersion, { color: colors.textMuted }]}>
                  {selectedLanguage.version || selectedLanguage.extension}
                </Text>
              </View>
              <Ionicons name="chevron-down" size={16} color={colors.secondary} />
            </>
          )}
        </TouchableOpacity>
        
        <View style={styles.headerActions}>
          <TouchableOpacity style={styles.headerButton} onPress={toggleTheme}>
            <Ionicons
              name={theme === 'dark' ? 'sunny' : 'moon'}
              size={20}
              color={colors.secondary}
            />
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.headerButton} onPress={() => setShowSettingsModal(true)}>
            <Ionicons name="settings-outline" size={20} color={colors.secondary} />
          </TouchableOpacity>
        </View>
      </View>

      {/* Toolbar */}
      <View style={[styles.toolbar, { backgroundColor: colors.surfaceAlt }]}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.toolbarContent}>
          <TouchableOpacity
            style={[styles.toolButton, { backgroundColor: colors.surface }]}
            onPress={() => setShowTemplateModal(true)}
          >
            <Ionicons name="flash" size={15} color={colors.warning} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Templates</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.toolButton, { backgroundColor: colors.surface }]}
            onPress={() => setShowFilesModal(true)}
          >
            <Ionicons name="folder" size={15} color={colors.accent} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Files</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.toolButton, { backgroundColor: colors.surface }]}
            onPress={saveFile}
          >
            <Ionicons name="save" size={15} color={colors.success} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Save</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.toolButton, { backgroundColor: colors.surface }]}
            onPress={analyzeCode}
          >
            <Ionicons name="analytics" size={15} color={colors.primary} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Analyze</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.toolButton, { backgroundColor: colors.surface }]}
            onPress={clearCode}
          >
            <Ionicons name="trash" size={15} color={colors.error} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Clear</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* AI Assistant Bar */}
      <Animated.View style={[
        styles.aiBar, 
        { backgroundColor: colors.surface, borderBottomColor: colors.border, transform: [{ scale: pulseAnim }] }
      ]}>
        <TouchableOpacity
          style={[styles.aiButton, { backgroundColor: colors.primary + '15', borderColor: colors.primary + '40' }]}
          onPress={() => setShowAIModal(true)}
        >
          <Ionicons name="sparkles" size={18} color={colors.primary} />
          <Text style={[styles.aiButtonText, { color: colors.primary }]}>AI Assist</Text>
          <View style={[styles.aiBadge, { backgroundColor: colors.primary }]}>
            <Text style={styles.aiBadgeText}>GPT-4o</Text>
          </View>
        </TouchableOpacity>
        
        {codeAnalysis && (
          <View style={[styles.analysisChip, { backgroundColor: getComplexityColor(codeAnalysis.complexity) + '20' }]}>
            <Text style={[styles.analysisChipText, { color: getComplexityColor(codeAnalysis.complexity) }]}>
              {codeAnalysis.complexity.toUpperCase()}
            </Text>
          </View>
        )}
      </Animated.View>

      {/* Main Content */}
      <KeyboardAvoidingView
        style={styles.mainContent}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
      >
        {/* Code Editor */}
        <View style={[styles.editorContainer, { backgroundColor: colors.codeBackground }]}>
          <View style={[styles.editorHeader, { borderBottomColor: colors.borderSubtle }]}>
            <View style={styles.editorTabs}>
              <View style={[styles.editorTab, { backgroundColor: colors.primary + '20', borderBottomColor: colors.primary }]}>
                <TextInput
                  style={[styles.fileNameInput, { color: colors.text }]}
                  value={currentFileName}
                  onChangeText={setCurrentFileName}
                  placeholder="filename"
                  placeholderTextColor={colors.textMuted}
                />
                <Text style={[styles.extensionText, { color: colors.textMuted }]}>
                  {selectedLanguage?.extension || ''}
                </Text>
              </View>
            </View>
            {executionTime !== null && (
              <Text style={[styles.execTimeText, { color: colors.success }]}>
                {executionTime.toFixed(1)}ms
              </Text>
            )}
          </View>
          
          <ScrollView style={styles.editorScroll} keyboardShouldPersistTaps="handled">
            <View style={styles.editorContent}>
              <View style={[styles.lineNumbers, { backgroundColor: colors.codeLine }]}>
                {code.split('\n').map((_, index) => (
                  <Text key={index} style={[styles.lineNumber, { color: colors.textMuted }]}>
                    {index + 1}
                  </Text>
                ))}
                {code === '' && <Text style={[styles.lineNumber, { color: colors.textMuted }]}>1</Text>}
              </View>
              
              <TextInput
                style={[styles.codeInput, { color: colors.text }]}
                value={code}
                onChangeText={(text) => {
                  setCode(text);
                  setCodeAnalysis(null);
                }}
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

        {/* Output/Preview Section */}
        {(showOutput || showWebPreview) && (
          <View style={[styles.outputContainer, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
            <View style={[styles.outputHeader, { borderBottomColor: colors.borderSubtle }]}>
              <View style={styles.outputTitleRow}>
                <Ionicons 
                  name={showWebPreview ? "globe" : "terminal"} 
                  size={16} 
                  color={colors.accent} 
                />
                <Text style={[styles.outputTitle, { color: colors.text }]}>
                  {showWebPreview ? 'Preview' : 'Output'}
                </Text>
              </View>
              <TouchableOpacity
                onPress={() => {
                  setShowOutput(false);
                  setShowWebPreview(false);
                }}
                style={styles.closeButton}
              >
                <Ionicons name="close" size={20} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            {showWebPreview ? (
              <WebView
                style={styles.webPreview}
                source={{ html: htmlPreview }}
                originWhitelist={['*']}
                javaScriptEnabled={true}
              />
            ) : (
              <ScrollView style={styles.outputScroll}>
                <Text style={[styles.outputText, { color: colors.text }]}>
                  {output || 'No output'}
                </Text>
              </ScrollView>
            )}
          </View>
        )}
      </KeyboardAvoidingView>

      {/* Run Button */}
      <View style={[styles.bottomBar, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
        <TouchableOpacity
          style={[
            styles.runButton,
            { 
              backgroundColor: selectedLanguage?.executable ? colors.success : colors.surfaceAlt,
              shadowColor: selectedLanguage?.executable ? colors.success : 'transparent',
            },
            isExecuting && styles.runButtonDisabled,
          ]}
          onPress={executeCode}
          disabled={isExecuting || !selectedLanguage?.executable}
        >
          {isExecuting ? (
            <ActivityIndicator size="small" color="#FFFFFF" />
          ) : (
            <>
              <Ionicons 
                name={selectedLanguage?.key === 'html' ? 'eye' : 'play'} 
                size={22} 
                color="#FFFFFF" 
              />
              <Text style={styles.runButtonText}>
                {selectedLanguage?.key === 'html' ? 'Preview' : 'Run'}
              </Text>
            </>
          )}
        </TouchableOpacity>
      </View>

      {/* Language Selection Modal */}
      <Modal visible={showLanguageModal} transparent animationType="slide" onRequestClose={() => setShowLanguageModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Select Language</Text>
              <TouchableOpacity onPress={() => setShowLanguageModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <FlatList
              data={languages}
              keyExtractor={(item) => item.key}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={[
                    styles.languageItem,
                    { borderBottomColor: colors.borderSubtle },
                    selectedLanguage?.key === item.key && { backgroundColor: colors.primary + '10' }
                  ]}
                  onPress={() => selectLanguage(item)}
                >
                  <View style={styles.languageItemLeft}>
                    <View style={[styles.langItemIcon, { backgroundColor: item.color + '20' }]}>
                      <Ionicons name={getIconName(item.icon)} size={22} color={item.color} />
                    </View>
                    <View style={styles.languageItemInfo}>
                      <Text style={[styles.languageItemName, { color: colors.text }]}>
                        {item.name}
                      </Text>
                      <Text style={[styles.languageItemVersion, { color: colors.textMuted }]}>
                        {item.version || item.extension} {item.type === 'addon' ? '• Addon' : ''}
                      </Text>
                    </View>
                  </View>
                  {item.executable && (
                    <View style={[styles.executableBadge, { backgroundColor: colors.success + '20' }]}>
                      <Ionicons name="checkmark-circle" size={12} color={colors.success} />
                      <Text style={[styles.executableText, { color: colors.success }]}>Run</Text>
                    </View>
                  )}
                </TouchableOpacity>
              )}
              ListFooterComponent={
                <TouchableOpacity
                  style={[styles.addAddonButton, { borderColor: colors.border }]}
                  onPress={() => {
                    setShowLanguageModal(false);
                    setShowAddonModal(true);
                  }}
                >
                  <Ionicons name="add-circle-outline" size={22} color={colors.primary} />
                  <Text style={[styles.addAddonText, { color: colors.primary }]}>Add Language Addon</Text>
                </TouchableOpacity>
              }
            />
          </View>
        </View>
      </Modal>

      {/* Templates Modal */}
      <Modal visible={showTemplateModal} transparent animationType="slide" onRequestClose={() => setShowTemplateModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>
                {selectedLanguage?.name} Templates
              </Text>
              <TouchableOpacity onPress={() => setShowTemplateModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <FlatList
              data={templates}
              keyExtractor={(item) => item.key}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={[styles.templateItem, { borderBottomColor: colors.borderSubtle }]}
                  onPress={() => applyTemplate(item)}
                >
                  <View style={styles.templateItemLeft}>
                    <Ionicons name="document-text" size={20} color={colors.primary} />
                    <View style={styles.templateInfo}>
                      <Text style={[styles.templateName, { color: colors.text }]}>
                        {item.name}
                      </Text>
                      {item.description && (
                        <Text style={[styles.templateDesc, { color: colors.textMuted }]} numberOfLines={1}>
                          {item.description}
                        </Text>
                      )}
                    </View>
                  </View>
                  {item.complexity && (
                    <View style={[styles.complexityBadge, { backgroundColor: getComplexityColor(item.complexity) + '20' }]}>
                      <Text style={[styles.complexityText, { color: getComplexityColor(item.complexity) }]}>
                        {item.complexity}
                      </Text>
                    </View>
                  )}
                </TouchableOpacity>
              )}
              ListEmptyComponent={
                <Text style={[styles.emptyText, { color: colors.textMuted }]}>
                  No templates available
                </Text>
              }
            />
          </View>
        </View>
      </Modal>

      {/* Files Modal */}
      <Modal visible={showFilesModal} transparent animationType="slide" onRequestClose={() => setShowFilesModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Saved Files</Text>
              <TouchableOpacity onPress={() => setShowFilesModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <FlatList
              data={savedFiles}
              keyExtractor={(item) => item.id}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={[styles.fileItem, { borderBottomColor: colors.borderSubtle }]}
                  onPress={() => loadFile(item)}
                >
                  <View style={styles.fileItemLeft}>
                    <Ionicons name="document" size={20} color={colors.accent} />
                    <View style={styles.fileItemInfo}>
                      <Text style={[styles.fileName, { color: colors.text }]}>{item.name}</Text>
                      <Text style={[styles.fileDate, { color: colors.textMuted }]}>
                        {new Date(item.updated_at).toLocaleDateString()}
                      </Text>
                    </View>
                  </View>
                  <TouchableOpacity
                    onPress={() => deleteFile(item.id)}
                    hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                  >
                    <Ionicons name="trash-outline" size={18} color={colors.error} />
                  </TouchableOpacity>
                </TouchableOpacity>
              )}
              ListEmptyComponent={
                <Text style={[styles.emptyText, { color: colors.textMuted }]}>
                  No saved files yet
                </Text>
              }
            />
          </View>
        </View>
      </Modal>

      {/* AI Modal */}
      <Modal visible={showAIModal} transparent animationType="slide" onRequestClose={() => setShowAIModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, styles.aiModalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.aiModalTitle}>
                <Ionicons name="sparkles" size={22} color={colors.primary} />
                <Text style={[styles.modalTitle, { color: colors.text }]}>AI Assistant</Text>
              </View>
              <TouchableOpacity onPress={() => setShowAIModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            {!selectedAIMode ? (
              <FlatList
                data={aiModes}
                keyExtractor={(item) => item.key}
                numColumns={2}
                contentContainerStyle={styles.aiModeGrid}
                renderItem={({ item }) => (
                  <TouchableOpacity
                    style={[styles.aiModeCard, { backgroundColor: colors.surfaceAlt, borderColor: colors.border }]}
                    onPress={() => askAI(item)}
                  >
                    <Ionicons 
                      name={
                        item.key === 'explain' ? 'bulb' :
                        item.key === 'debug' ? 'bug' :
                        item.key === 'optimize' ? 'rocket' :
                        item.key === 'complete' ? 'create' :
                        item.key === 'refactor' ? 'construct' :
                        item.key === 'document' ? 'document-text' :
                        item.key === 'test_gen' ? 'flask' :
                        item.key === 'security_audit' ? 'shield-checkmark' :
                        'swap-horizontal'
                      } 
                      size={28} 
                      color={colors.primary} 
                    />
                    <Text style={[styles.aiModeName, { color: colors.text }]}>{item.name}</Text>
                    <Text style={[styles.aiModeDesc, { color: colors.textMuted }]} numberOfLines={2}>
                      {item.description}
                    </Text>
                  </TouchableOpacity>
                )}
              />
            ) : (
              <View style={styles.aiResponseContainer}>
                <View style={styles.aiResponseHeader}>
                  <TouchableOpacity 
                    style={styles.aiBackButton}
                    onPress={() => {
                      setSelectedAIMode(null);
                      setAIResponse('');
                    }}
                  >
                    <Ionicons name="arrow-back" size={20} color={colors.primary} />
                    <Text style={[styles.aiBackText, { color: colors.primary }]}>Back</Text>
                  </TouchableOpacity>
                  <Text style={[styles.aiModeTitle, { color: colors.text }]}>{selectedAIMode.name}</Text>
                </View>
                
                {isAILoading ? (
                  <View style={styles.aiLoadingContainer}>
                    <ActivityIndicator size="large" color={colors.primary} />
                    <Text style={[styles.aiLoadingText, { color: colors.textSecondary }]}>
                      Analyzing code with GPT-4o...
                    </Text>
                  </View>
                ) : (
                  <ScrollView style={styles.aiResponseScroll}>
                    <Text style={[styles.aiResponseText, { color: colors.text }]}>
                      {aiResponse}
                    </Text>
                  </ScrollView>
                )}
              </View>
            )}
          </View>
        </View>
      </Modal>

      {/* Analysis Modal */}
      <Modal visible={showAnalysisModal} transparent animationType="slide" onRequestClose={() => setShowAnalysisModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, styles.analysisModalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Code Analysis</Text>
              <TouchableOpacity onPress={() => setShowAnalysisModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            {codeAnalysis && (
              <ScrollView style={styles.analysisContent}>
                <View style={[styles.analysisCard, { backgroundColor: colors.surfaceAlt }]}>
                  <Text style={[styles.analysisLabel, { color: colors.textSecondary }]}>Complexity</Text>
                  <View style={[styles.complexityDisplay, { backgroundColor: getComplexityColor(codeAnalysis.complexity) + '20' }]}>
                    <Text style={[styles.complexityValue, { color: getComplexityColor(codeAnalysis.complexity) }]}>
                      {codeAnalysis.complexity.toUpperCase()}
                    </Text>
                  </View>
                </View>
                
                <View style={styles.analysisGrid}>
                  <View style={[styles.analysisGridItem, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.analysisGridValue, { color: colors.text }]}>{codeAnalysis.lines_of_code}</Text>
                    <Text style={[styles.analysisGridLabel, { color: colors.textMuted }]}>Lines</Text>
                  </View>
                  <View style={[styles.analysisGridItem, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.analysisGridValue, { color: colors.text }]}>{codeAnalysis.cyclomatic_complexity}</Text>
                    <Text style={[styles.analysisGridLabel, { color: colors.textMuted }]}>Cyclomatic</Text>
                  </View>
                  <View style={[styles.analysisGridItem, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.analysisGridValue, { color: colors.text }]}>{codeAnalysis.functions_count}</Text>
                    <Text style={[styles.analysisGridLabel, { color: colors.textMuted }]}>Functions</Text>
                  </View>
                  <View style={[styles.analysisGridItem, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.analysisGridValue, { color: colors.text }]}>{codeAnalysis.classes_count}</Text>
                    <Text style={[styles.analysisGridLabel, { color: colors.textMuted }]}>Classes</Text>
                  </View>
                </View>
              </ScrollView>
            )}
          </View>
        </View>
      </Modal>

      {/* Settings Modal */}
      <Modal visible={showSettingsModal} transparent animationType="slide" onRequestClose={() => setShowSettingsModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Settings</Text>
              <TouchableOpacity onPress={() => setShowSettingsModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <ScrollView style={styles.settingsContent}>
              <TouchableOpacity
                style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]}
                onPress={toggleTheme}
              >
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.warning + '20' }]}>
                    <Ionicons name={theme === 'dark' ? 'moon' : 'sunny'} size={20} color={colors.warning} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Theme</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.textSecondary }]}>
                  {theme === 'dark' ? 'Dark' : 'Light'}
                </Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]}
                onPress={() => {
                  setShowSettingsModal(false);
                  setShowAddonModal(true);
                }}
              >
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.primary + '20' }]}>
                    <Ionicons name="extension-puzzle" size={20} color={colors.primary} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Language Addons</Text>
                </View>
                <Ionicons name="chevron-forward" size={20} color={colors.secondary} />
              </TouchableOpacity>
              
              <View style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]}>
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.accent + '20' }]}>
                    <Ionicons name="information-circle" size={20} color={colors.accent} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Version</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.textSecondary }]}>3.0.0 Quantum</Text>
              </View>
              
              <View style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]}>
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.success + '20' }]}>
                    <Ionicons name="sparkles" size={20} color={colors.success} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>AI Model</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.textSecondary }]}>GPT-4o</Text>
              </View>
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Add Addon Modal */}
      <AddAddonModal
        visible={showAddonModal}
        onClose={() => setShowAddonModal(false)}
        onAddonAdded={loadData}
        colors={colors}
      />
    </SafeAreaView>
  );
}

// Add Addon Modal Component
function AddAddonModal({
  visible,
  onClose,
  onAddonAdded,
  colors,
}: {
  visible: boolean;
  onClose: () => void;
  onAddonAdded: () => void;
  colors: typeof themes.dark;
}) {
  const [name, setName] = useState('');
  const [extension, setExtension] = useState('');
  const [description, setDescription] = useState('');
  const [version, setVersion] = useState('1.0');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name.trim() || !extension.trim()) {
      Alert.alert('Error', 'Name and extension are required');
      return;
    }

    setLoading(true);
    try {
      const languageKey = name.toLowerCase().replace(/[^a-z0-9]/g, '_');
      await axios.post(`${API_URL}/api/addons`, {
        language_key: languageKey,
        name: name.trim(),
        extension: extension.startsWith('.') ? extension : `.${extension}`,
        description: description.trim(),
        version: version.trim(),
        icon: 'code-slash',
        color: '#6B7280',
        executable: false,
      });
      
      Alert.alert('Success', 'Language addon added');
      setName('');
      setExtension('');
      setDescription('');
      setVersion('1.0');
      onAddonAdded();
      onClose();
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to add addon');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
      <View style={styles.modalOverlay}>
        <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
          <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
            <Text style={[styles.modalTitle, { color: colors.text }]}>Add Language Addon</Text>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color={colors.secondary} />
            </TouchableOpacity>
          </View>
          
          <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
            <ScrollView style={styles.addonForm}>
              <Text style={[styles.inputLabel, { color: colors.text }]}>Language Name *</Text>
              <TextInput
                style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                value={name}
                onChangeText={setName}
                placeholder="e.g., Rust, Go, Ruby"
                placeholderTextColor={colors.textMuted}
              />
              
              <Text style={[styles.inputLabel, { color: colors.text }]}>File Extension *</Text>
              <TextInput
                style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                value={extension}
                onChangeText={setExtension}
                placeholder="e.g., .rs, .go, .rb"
                placeholderTextColor={colors.textMuted}
              />
              
              <Text style={[styles.inputLabel, { color: colors.text }]}>Version</Text>
              <TextInput
                style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                value={version}
                onChangeText={setVersion}
                placeholder="e.g., 1.0, 2024"
                placeholderTextColor={colors.textMuted}
              />
              
              <Text style={[styles.inputLabel, { color: colors.text }]}>Description</Text>
              <TextInput
                style={[styles.textInput, styles.textArea, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                value={description}
                onChangeText={setDescription}
                placeholder="Brief description"
                placeholderTextColor={colors.textMuted}
                multiline
                numberOfLines={3}
              />
              
              <TouchableOpacity
                style={[styles.submitButton, { backgroundColor: colors.primary }]}
                onPress={handleSubmit}
                disabled={loading}
              >
                {loading ? (
                  <ActivityIndicator size="small" color="#FFFFFF" />
                ) : (
                  <Text style={styles.submitButtonText}>Add Language</Text>
                )}
              </TouchableOpacity>
            </ScrollView>
          </KeyboardAvoidingView>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingContent: {
    alignItems: 'center',
  },
  loadingTitle: {
    marginTop: 20,
    fontSize: 24,
    fontWeight: '700',
  },
  loadingSubtitle: {
    marginTop: 4,
    fontSize: 14,
  },
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
  },
  langIconBg: {
    width: 36,
    height: 36,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  languageName: {
    fontSize: 16,
    fontWeight: '600',
  },
  languageVersion: {
    fontSize: 11,
  },
  headerActions: {
    flexDirection: 'row',
    gap: 4,
  },
  headerButton: {
    padding: 8,
    borderRadius: 8,
  },
  toolbar: {
    paddingVertical: 8,
    borderBottomWidth: 0,
  },
  toolbarContent: {
    paddingHorizontal: 12,
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
    fontWeight: '500',
  },
  aiBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 10,
    gap: 10,
    borderBottomWidth: 1,
  },
  aiButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 8,
    borderWidth: 1,
  },
  aiButtonText: {
    fontSize: 14,
    fontWeight: '600',
  },
  aiBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  aiBadgeText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: '700',
  },
  analysisChip: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  analysisChipText: {
    fontSize: 11,
    fontWeight: '700',
  },
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
    paddingVertical: 8,
    borderBottomWidth: 1,
  },
  editorTabs: {
    flexDirection: 'row',
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
    fontSize: 13,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  extensionText: {
    fontSize: 13,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  execTimeText: {
    fontSize: 12,
    fontWeight: '600',
  },
  editorScroll: {
    flex: 1,
  },
  editorContent: {
    flexDirection: 'row',
    paddingVertical: 8,
  },
  lineNumbers: {
    paddingHorizontal: 10,
    paddingRight: 8,
    alignItems: 'flex-end',
    minWidth: 44,
    borderRightWidth: 1,
    borderRightColor: 'rgba(255,255,255,0.05)',
  },
  lineNumber: {
    fontSize: 13,
    lineHeight: 22,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  codeInput: {
    flex: 1,
    fontSize: 13,
    lineHeight: 22,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    paddingHorizontal: 12,
    textAlignVertical: 'top',
  },
  outputContainer: {
    height: SCREEN_HEIGHT * 0.28,
    borderTopWidth: 1,
  },
  outputHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 14,
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
    fontWeight: '600',
  },
  closeButton: {
    padding: 4,
  },
  outputScroll: {
    flex: 1,
    padding: 14,
  },
  outputText: {
    fontSize: 13,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    lineHeight: 20,
  },
  webPreview: {
    flex: 1,
  },
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
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  runButtonDisabled: {
    opacity: 0.6,
  },
  runButtonText: {
    color: '#FFFFFF',
    fontSize: 17,
    fontWeight: '700',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    maxHeight: SCREEN_HEIGHT * 0.75,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
  },
  aiModalContent: {
    maxHeight: SCREEN_HEIGHT * 0.85,
  },
  analysisModalContent: {
    maxHeight: SCREEN_HEIGHT * 0.5,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
  },
  aiModalTitle: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  languageItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  languageItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  langItemIcon: {
    width: 44,
    height: 44,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  languageItemInfo: {
    gap: 2,
  },
  languageItemName: {
    fontSize: 16,
    fontWeight: '600',
  },
  languageItemVersion: {
    fontSize: 12,
  },
  executableBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
    gap: 4,
  },
  executableText: {
    fontSize: 12,
    fontWeight: '600',
  },
  addAddonButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    paddingVertical: 18,
    margin: 16,
    borderWidth: 1.5,
    borderStyle: 'dashed',
    borderRadius: 12,
  },
  addAddonText: {
    fontSize: 15,
    fontWeight: '600',
  },
  templateItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  templateItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  templateInfo: {
    flex: 1,
    gap: 2,
  },
  templateName: {
    fontSize: 15,
    fontWeight: '500',
  },
  templateDesc: {
    fontSize: 12,
  },
  complexityBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
  },
  complexityText: {
    fontSize: 10,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  fileItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  fileItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  fileItemInfo: {
    gap: 2,
  },
  fileName: {
    fontSize: 15,
    fontWeight: '500',
  },
  fileDate: {
    fontSize: 12,
  },
  emptyText: {
    textAlign: 'center',
    paddingVertical: 40,
    fontSize: 14,
  },
  aiModeGrid: {
    padding: 16,
  },
  aiModeCard: {
    flex: 1,
    margin: 6,
    padding: 16,
    borderRadius: 14,
    borderWidth: 1,
    alignItems: 'center',
    minHeight: 130,
  },
  aiModeName: {
    fontSize: 14,
    fontWeight: '600',
    marginTop: 10,
  },
  aiModeDesc: {
    fontSize: 11,
    textAlign: 'center',
    marginTop: 4,
    lineHeight: 15,
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
    fontWeight: '500',
  },
  aiModeTitle: {
    fontSize: 16,
    fontWeight: '600',
  },
  aiLoadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
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
  analysisContent: {
    padding: 16,
  },
  analysisCard: {
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    alignItems: 'center',
  },
  analysisLabel: {
    fontSize: 12,
    marginBottom: 8,
  },
  complexityDisplay: {
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 20,
  },
  complexityValue: {
    fontSize: 16,
    fontWeight: '700',
  },
  analysisGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  analysisGridItem: {
    width: '47%',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  analysisGridValue: {
    fontSize: 28,
    fontWeight: '700',
  },
  analysisGridLabel: {
    fontSize: 12,
    marginTop: 4,
  },
  settingsContent: {
    paddingBottom: 20,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
  },
  settingItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  settingItemText: {
    fontSize: 16,
  },
  settingItemValue: {
    fontSize: 14,
  },
  addonForm: {
    padding: 20,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    marginTop: 16,
  },
  textInput: {
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
  },
  textArea: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  submitButton: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 12,
    marginTop: 24,
    marginBottom: 20,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
  },
});
