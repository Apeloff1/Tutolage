import React, { useState, useEffect, useCallback } from 'react';
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
  type: 'builtin' | 'addon';
}

interface ExecutionResult {
  status: 'success' | 'error' | 'timeout' | 'pending';
  output: string;
  error: string;
  execution_time_ms: number;
}

interface Template {
  name: string;
  code: string;
}

interface SavedFile {
  id: string;
  name: string;
  language: string;
  code: string;
  updated_at: string;
}

// Theme configuration
const themes = {
  dark: {
    background: '#0D1117',
    surface: '#161B22',
    surfaceAlt: '#21262D',
    primary: '#58A6FF',
    secondary: '#8B949E',
    text: '#E6EDF3',
    textSecondary: '#8B949E',
    border: '#30363D',
    success: '#3FB950',
    error: '#F85149',
    warning: '#D29922',
    codeBackground: '#0D1117',
  },
  light: {
    background: '#FFFFFF',
    surface: '#F6F8FA',
    surfaceAlt: '#EAEEF2',
    primary: '#0969DA',
    secondary: '#57606A',
    text: '#24292F',
    textSecondary: '#57606A',
    border: '#D0D7DE',
    success: '#1A7F37',
    error: '#CF222E',
    warning: '#9A6700',
    codeBackground: '#F6F8FA',
  },
};

export default function CodeDock() {
  // State
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [languages, setLanguages] = useState<Language[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<Language | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [showFilesModal, setShowFilesModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showAddonModal, setShowAddonModal] = useState(false);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [savedFiles, setSavedFiles] = useState<SavedFile[]>([]);
  const [currentFileName, setCurrentFileName] = useState('untitled');
  const [showOutput, setShowOutput] = useState(false);
  const [showWebPreview, setShowWebPreview] = useState(false);
  const [htmlPreview, setHtmlPreview] = useState('');
  const [loading, setLoading] = useState(true);

  const colors = themes[theme];

  // Load initial data
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // Load theme from storage
      const savedTheme = await AsyncStorage.getItem('theme');
      if (savedTheme) setTheme(savedTheme as 'dark' | 'light');

      // Load languages from API
      const langResponse = await axios.get(`${API_URL}/api/languages`);
      const langs = langResponse.data.languages || [];
      setLanguages(langs);

      // Set default language (Python)
      const defaultLang = langs.find((l: Language) => l.key === 'python');
      if (defaultLang) {
        setSelectedLanguage(defaultLang);
        loadTemplates('python');
      }

      // Load saved files
      loadFiles();
    } catch (error) {
      console.error('Failed to load data:', error);
      // Set fallback languages
      setLanguages([
        { key: 'python', name: 'Python', extension: '.py', icon: 'logo-python', color: '#3776AB', executable: true, type: 'builtin' },
        { key: 'html', name: 'HTML', extension: '.html', icon: 'logo-html5', color: '#E34F26', executable: true, type: 'builtin' },
        { key: 'javascript', name: 'JavaScript', extension: '.js', icon: 'logo-javascript', color: '#F7DF1E', executable: true, type: 'builtin' },
        { key: 'cpp', name: 'C++', extension: '.cpp', icon: 'code-slash', color: '#00599C', executable: true, type: 'builtin' },
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
    await AsyncStorage.setItem('theme', newTheme);
  };

  const selectLanguage = (lang: Language) => {
    setSelectedLanguage(lang);
    setShowLanguageModal(false);
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    loadTemplates(lang.key);
  };

  const executeCode = async () => {
    if (!code.trim() || !selectedLanguage) return;

    setIsExecuting(true);
    setOutput('');
    setShowOutput(true);
    setShowWebPreview(false);

    try {
      // For HTML, show preview directly
      if (selectedLanguage.key === 'html') {
        setHtmlPreview(code);
        setShowWebPreview(true);
        setShowOutput(false);
        setOutput('HTML rendered in preview');
        return;
      }

      // For JavaScript, execute in WebView
      if (selectedLanguage.key === 'javascript') {
        const response = await axios.post(`${API_URL}/api/execute`, {
          code,
          language: selectedLanguage.key,
        });
        
        // Execute the wrapped JS code in a hidden WebView context
        const wrappedCode = response.data.result.output;
        setHtmlPreview(`
          <html>
          <head><style>body { font-family: monospace; padding: 20px; background: ${colors.codeBackground}; color: ${colors.text}; }</style></head>
          <body>
          <pre id="output"></pre>
          <script>
            try {
              var result = ${wrappedCode};
              document.getElementById('output').textContent = result.status === 'success' ? result.output : 'Error: ' + result.error;
            } catch(e) {
              document.getElementById('output').textContent = 'Error: ' + e.message;
            }
          </script>
          </body>
          </html>
        `);
        setShowWebPreview(true);
        return;
      }

      // For other languages, execute on server
      const response = await axios.post(`${API_URL}/api/execute`, {
        code,
        language: selectedLanguage.key,
        timeout_seconds: 10,
      });

      const result: ExecutionResult = response.data.result;
      
      if (result.status === 'success') {
        setOutput(result.output || 'Program executed successfully (no output)');
      } else if (result.status === 'timeout') {
        setOutput(`Timeout: ${result.error}`);
      } else {
        setOutput(`Error: ${result.error || 'Unknown error'}`);
      }
    } catch (error: any) {
      setOutput(`Execution failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsExecuting(false);
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
      Alert.alert('Success', 'File saved successfully');
      loadFiles();
    } catch (error: any) {
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
  };

  const clearCode = () => {
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
  };

  const getIconName = (icon: string): any => {
    const iconMap: { [key: string]: string } = {
      'logo-python': 'logo-python',
      'logo-html5': 'logo-html5',
      'logo-javascript': 'logo-javascript',
      'logo-css3': 'logo-css3',
      'code-slash': 'code-slash',
      'code-working': 'code-working',
      'document-text': 'document-text',
      'server': 'server',
    };
    return iconMap[icon] || 'code-slash';
  };

  if (loading) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: colors.background }]}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={[styles.loadingText, { color: colors.text }]}>Loading CodeDock...</Text>
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
              <Ionicons
                name={getIconName(selectedLanguage.icon)}
                size={20}
                color={selectedLanguage.color}
              />
              <Text style={[styles.languageName, { color: colors.text }]}>
                {selectedLanguage.name}
              </Text>
              <Ionicons name="chevron-down" size={16} color={colors.secondary} />
            </>
          )}
        </TouchableOpacity>
        
        <View style={styles.headerActions}>
          <TouchableOpacity
            style={styles.headerButton}
            onPress={toggleTheme}
          >
            <Ionicons
              name={theme === 'dark' ? 'sunny' : 'moon'}
              size={20}
              color={colors.secondary}
            />
          </TouchableOpacity>
          
          <TouchableOpacity
            style={styles.headerButton}
            onPress={() => setShowSettingsModal(true)}
          >
            <Ionicons name="settings-outline" size={20} color={colors.secondary} />
          </TouchableOpacity>
        </View>
      </View>

      {/* Toolbar */}
      <View style={[styles.toolbar, { backgroundColor: colors.surfaceAlt, borderBottomColor: colors.border }]}>
        <TouchableOpacity
          style={[styles.toolButton, { backgroundColor: colors.surface }]}
          onPress={() => setShowTemplateModal(true)}
        >
          <Ionicons name="flash" size={16} color={colors.primary} />
          <Text style={[styles.toolButtonText, { color: colors.text }]}>Templates</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.toolButton, { backgroundColor: colors.surface }]}
          onPress={() => setShowFilesModal(true)}
        >
          <Ionicons name="folder" size={16} color={colors.warning} />
          <Text style={[styles.toolButtonText, { color: colors.text }]}>Files</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.toolButton, { backgroundColor: colors.surface }]}
          onPress={saveFile}
        >
          <Ionicons name="save" size={16} color={colors.success} />
          <Text style={[styles.toolButtonText, { color: colors.text }]}>Save</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.toolButton, { backgroundColor: colors.surface }]}
          onPress={clearCode}
        >
          <Ionicons name="trash" size={16} color={colors.error} />
          <Text style={[styles.toolButtonText, { color: colors.text }]}>Clear</Text>
        </TouchableOpacity>
      </View>

      {/* Main Content */}
      <KeyboardAvoidingView
        style={styles.mainContent}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
      >
        {/* Code Editor */}
        <View style={[styles.editorContainer, { backgroundColor: colors.codeBackground }]}>
          <View style={[styles.editorHeader, { borderBottomColor: colors.border }]}>
            <TextInput
              style={[styles.fileNameInput, { color: colors.text }]}
              value={currentFileName}
              onChangeText={setCurrentFileName}
              placeholder="filename"
              placeholderTextColor={colors.secondary}
            />
            <Text style={[styles.extensionText, { color: colors.secondary }]}>
              {selectedLanguage?.extension || ''}
            </Text>
          </View>
          
          <ScrollView style={styles.editorScroll} keyboardShouldPersistTaps="handled">
            <View style={styles.editorContent}>
              <View style={styles.lineNumbers}>
                {code.split('\n').map((_, index) => (
                  <Text key={index} style={[styles.lineNumber, { color: colors.secondary }]}>
                    {index + 1}
                  </Text>
                ))}
                {code === '' && <Text style={[styles.lineNumber, { color: colors.secondary }]}>1</Text>}
              </View>
              
              <TextInput
                style={[styles.codeInput, { color: colors.text }]}
                value={code}
                onChangeText={setCode}
                multiline
                autoCapitalize="none"
                autoCorrect={false}
                spellCheck={false}
                placeholder="Start coding here..."
                placeholderTextColor={colors.secondary}
                textAlignVertical="top"
              />
            </View>
          </ScrollView>
        </View>

        {/* Output/Preview Section */}
        {(showOutput || showWebPreview) && (
          <View style={[styles.outputContainer, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
            <View style={[styles.outputHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.outputTitle, { color: colors.text }]}>
                {showWebPreview ? 'Preview' : 'Output'}
              </Text>
              <TouchableOpacity
                onPress={() => {
                  setShowOutput(false);
                  setShowWebPreview(false);
                }}
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
            { backgroundColor: selectedLanguage?.executable ? colors.success : colors.secondary },
            isExecuting && styles.runButtonDisabled,
          ]}
          onPress={executeCode}
          disabled={isExecuting || !selectedLanguage?.executable}
        >
          {isExecuting ? (
            <ActivityIndicator size="small" color="#FFFFFF" />
          ) : (
            <>
              <Ionicons name="play" size={20} color="#FFFFFF" />
              <Text style={styles.runButtonText}>
                {selectedLanguage?.key === 'html' ? 'Preview' : 'Run'}
              </Text>
            </>
          )}
        </TouchableOpacity>
      </View>

      {/* Language Selection Modal */}
      <Modal
        visible={showLanguageModal}
        transparent
        animationType="slide"
        onRequestClose={() => setShowLanguageModal(false)}
      >
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
                    { borderBottomColor: colors.border },
                    selectedLanguage?.key === item.key && { backgroundColor: colors.surfaceAlt }
                  ]}
                  onPress={() => selectLanguage(item)}
                >
                  <View style={styles.languageItemLeft}>
                    <Ionicons name={getIconName(item.icon)} size={24} color={item.color} />
                    <View style={styles.languageItemInfo}>
                      <Text style={[styles.languageItemName, { color: colors.text }]}>
                        {item.name}
                      </Text>
                      <Text style={[styles.languageItemDesc, { color: colors.secondary }]}>
                        {item.extension} {item.type === 'addon' ? '(Addon)' : ''}
                      </Text>
                    </View>
                  </View>
                  {item.executable && (
                    <View style={[styles.executableBadge, { backgroundColor: colors.success + '20' }]}>
                      <Text style={[styles.executableText, { color: colors.success }]}>Executable</Text>
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
                  <Ionicons name="add-circle-outline" size={24} color={colors.primary} />
                  <Text style={[styles.addAddonText, { color: colors.primary }]}>Add Language Addon</Text>
                </TouchableOpacity>
              }
            />
          </View>
        </View>
      </Modal>

      {/* Templates Modal */}
      <Modal
        visible={showTemplateModal}
        transparent
        animationType="slide"
        onRequestClose={() => setShowTemplateModal(false)}
      >
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
              keyExtractor={(item) => item.name}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={[styles.templateItem, { borderBottomColor: colors.border }]}
                  onPress={() => applyTemplate(item)}
                >
                  <Ionicons name="document-text" size={20} color={colors.primary} />
                  <Text style={[styles.templateName, { color: colors.text }]}>
                    {item.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </Text>
                </TouchableOpacity>
              )}
              ListEmptyComponent={
                <Text style={[styles.emptyText, { color: colors.secondary }]}>
                  No templates available
                </Text>
              }
            />
          </View>
        </View>
      </Modal>

      {/* Files Modal */}
      <Modal
        visible={showFilesModal}
        transparent
        animationType="slide"
        onRequestClose={() => setShowFilesModal(false)}
      >
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
                  style={[styles.fileItem, { borderBottomColor: colors.border }]}
                  onPress={() => loadFile(item)}
                >
                  <View style={styles.fileItemLeft}>
                    <Ionicons name="document" size={20} color={colors.primary} />
                    <View style={styles.fileItemInfo}>
                      <Text style={[styles.fileName, { color: colors.text }]}>{item.name}</Text>
                      <Text style={[styles.fileDate, { color: colors.secondary }]}>
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
                <Text style={[styles.emptyText, { color: colors.secondary }]}>
                  No saved files yet
                </Text>
              }
            />
          </View>
        </View>
      </Modal>

      {/* Settings Modal */}
      <Modal
        visible={showSettingsModal}
        transparent
        animationType="slide"
        onRequestClose={() => setShowSettingsModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Settings</Text>
              <TouchableOpacity onPress={() => setShowSettingsModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <View style={styles.settingsContent}>
              <TouchableOpacity
                style={[styles.settingItem, { borderBottomColor: colors.border }]}
                onPress={toggleTheme}
              >
                <View style={styles.settingItemLeft}>
                  <Ionicons
                    name={theme === 'dark' ? 'moon' : 'sunny'}
                    size={24}
                    color={colors.primary}
                  />
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Theme</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.secondary }]}>
                  {theme === 'dark' ? 'Dark' : 'Light'}
                </Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.settingItem, { borderBottomColor: colors.border }]}
                onPress={() => {
                  setShowSettingsModal(false);
                  setShowAddonModal(true);
                }}
              >
                <View style={styles.settingItemLeft}>
                  <Ionicons name="extension-puzzle" size={24} color={colors.warning} />
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Language Addons</Text>
                </View>
                <Ionicons name="chevron-forward" size={20} color={colors.secondary} />
              </TouchableOpacity>
              
              <View style={[styles.settingItem, { borderBottomColor: colors.border }]}>
                <View style={styles.settingItemLeft}>
                  <Ionicons name="information-circle" size={24} color={colors.secondary} />
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Version</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.secondary }]}>2.0.0</Text>
              </View>
            </View>
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
        icon: 'code-slash',
        color: '#6B7280',
        executable: false,
      });
      
      Alert.alert('Success', 'Language addon added successfully');
      setName('');
      setExtension('');
      setDescription('');
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
                placeholderTextColor={colors.secondary}
              />
              
              <Text style={[styles.inputLabel, { color: colors.text }]}>File Extension *</Text>
              <TextInput
                style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                value={extension}
                onChangeText={setExtension}
                placeholder="e.g., .rs, .go, .rb"
                placeholderTextColor={colors.secondary}
              />
              
              <Text style={[styles.inputLabel, { color: colors.text }]}>Description</Text>
              <TextInput
                style={[styles.textInput, styles.textArea, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                value={description}
                onChangeText={setDescription}
                placeholder="Brief description of the language"
                placeholderTextColor={colors.secondary}
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
  loadingText: {
    marginTop: 16,
    fontSize: 16,
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
    gap: 8,
  },
  languageName: {
    fontSize: 16,
    fontWeight: '600',
  },
  headerActions: {
    flexDirection: 'row',
    gap: 8,
  },
  headerButton: {
    padding: 8,
  },
  toolbar: {
    flexDirection: 'row',
    paddingHorizontal: 12,
    paddingVertical: 8,
    gap: 8,
    borderBottomWidth: 1,
  },
  toolButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
    gap: 6,
  },
  toolButtonText: {
    fontSize: 13,
    fontWeight: '500',
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
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderBottomWidth: 1,
  },
  fileNameInput: {
    fontSize: 14,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  extensionText: {
    fontSize: 14,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  editorScroll: {
    flex: 1,
  },
  editorContent: {
    flexDirection: 'row',
    paddingVertical: 8,
  },
  lineNumbers: {
    paddingHorizontal: 12,
    paddingRight: 8,
    alignItems: 'flex-end',
    minWidth: 40,
  },
  lineNumber: {
    fontSize: 14,
    lineHeight: 22,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  codeInput: {
    flex: 1,
    fontSize: 14,
    lineHeight: 22,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    paddingRight: 16,
    textAlignVertical: 'top',
  },
  outputContainer: {
    height: SCREEN_HEIGHT * 0.3,
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
  outputTitle: {
    fontSize: 14,
    fontWeight: '600',
  },
  outputScroll: {
    flex: 1,
    padding: 16,
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
    borderRadius: 10,
    gap: 8,
  },
  runButtonDisabled: {
    opacity: 0.6,
  },
  runButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    maxHeight: SCREEN_HEIGHT * 0.7,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
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
    fontWeight: '600',
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
  languageItemInfo: {
    gap: 2,
  },
  languageItemName: {
    fontSize: 16,
    fontWeight: '500',
  },
  languageItemDesc: {
    fontSize: 12,
  },
  executableBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  executableText: {
    fontSize: 11,
    fontWeight: '500',
  },
  addAddonButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    margin: 16,
    borderWidth: 1,
    borderStyle: 'dashed',
    borderRadius: 10,
  },
  addAddonText: {
    fontSize: 15,
    fontWeight: '500',
  },
  templateItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  templateName: {
    fontSize: 15,
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
    paddingVertical: 32,
    fontSize: 14,
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
    gap: 12,
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
    fontWeight: '500',
    marginBottom: 8,
    marginTop: 16,
  },
  textInput: {
    borderWidth: 1,
    borderRadius: 8,
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
    borderRadius: 10,
    marginTop: 24,
    marginBottom: 20,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});
