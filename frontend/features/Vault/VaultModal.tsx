/**
 * Vault System Modal v11.0.0
 * Manage Code Blocks, Assets, Database Schemas, and Learning Data
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput,
  Modal, ActivityIndicator, Dimensions, Platform, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';

interface VaultModalProps {
  visible: boolean;
  onClose: () => void;
  colors: any;
  currentCode?: string;
  currentLanguage?: string;
  onLoadCode?: (code: string, language: string) => void;
}

type VaultTab = 'code' | 'assets' | 'database' | 'learning';

interface CodeBlock {
  id: string;
  title: string;
  description?: string;
  code: string;
  language: string;
  tags: string[];
  category?: string;
  line_count: number;
  created_at: string;
}

interface VaultInfo {
  vaults: {
    code_blocks: { count: number };
    assets: { count: number };
    database_schemas: { count: number };
    learning_data: { count: number };
  };
}

export const VaultModal: React.FC<VaultModalProps> = ({
  visible, onClose, colors, currentCode, currentLanguage, onLoadCode
}) => {
  const [activeTab, setActiveTab] = useState<VaultTab>('code');
  const [isLoading, setIsLoading] = useState(false);
  const [vaultInfo, setVaultInfo] = useState<VaultInfo | null>(null);
  
  // Code Blocks state
  const [codeBlocks, setCodeBlocks] = useState<CodeBlock[]>([]);
  const [showAddCode, setShowAddCode] = useState(false);
  const [newCodeTitle, setNewCodeTitle] = useState('');
  const [newCodeDesc, setNewCodeDesc] = useState('');
  const [newCodeTags, setNewCodeTags] = useState('');
  const [newCodeCategory, setNewCodeCategory] = useState('');
  
  // Assets state
  const [assets, setAssets] = useState<any[]>([]);
  
  // Database state
  const [schemas, setSchemas] = useState<any[]>([]);
  
  // Learning state
  const [learningData, setLearningData] = useState<any[]>([]);
  const [showAddNote, setShowAddNote] = useState(false);
  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');

  useEffect(() => {
    if (visible) {
      loadVaultInfo();
      loadCodeBlocks();
    }
  }, [visible]);

  const loadVaultInfo = async () => {
    try {
      const response = await fetch(`${API_URL}/api/vault/info`);
      const data = await response.json();
      setVaultInfo(data);
    } catch (error) {
      console.error('Failed to load vault info:', error);
    }
  };

  const loadCodeBlocks = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/vault/code`);
      const data = await response.json();
      setCodeBlocks(data.blocks || []);
    } catch (error) {
      console.error('Failed to load code blocks:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadAssets = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/vault/asset`);
      const data = await response.json();
      setAssets(data.assets || []);
    } catch (error) {
      console.error('Failed to load assets:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadSchemas = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/vault/database`);
      const data = await response.json();
      setSchemas(data.schemas || []);
    } catch (error) {
      console.error('Failed to load schemas:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadLearningData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/vault/learning`);
      const data = await response.json();
      setLearningData(data.items || []);
    } catch (error) {
      console.error('Failed to load learning data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const saveCurrentCode = async () => {
    if (!currentCode?.trim() || !newCodeTitle.trim()) {
      Alert.alert('Error', 'Please provide a title and ensure there is code to save');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/vault/code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: newCodeTitle,
          description: newCodeDesc,
          code: currentCode,
          language: currentLanguage || 'python',
          tags: newCodeTags.split(',').map(t => t.trim()).filter(Boolean),
          category: newCodeCategory || 'general',
        }),
      });

      if (response.ok) {
        Alert.alert('Success', 'Code saved to vault!');
        setShowAddCode(false);
        setNewCodeTitle('');
        setNewCodeDesc('');
        setNewCodeTags('');
        setNewCodeCategory('');
        loadCodeBlocks();
        loadVaultInfo();
      } else {
        throw new Error('Failed to save');
      }
    } catch (error: any) {
      Alert.alert('Error', `Failed to save code: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteCodeBlock = async (id: string) => {
    Alert.alert('Delete', 'Are you sure you want to delete this code block?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Delete',
        style: 'destructive',
        onPress: async () => {
          try {
            await fetch(`${API_URL}/api/vault/code/${id}`, { method: 'DELETE' });
            loadCodeBlocks();
            loadVaultInfo();
          } catch (error) {
            Alert.alert('Error', 'Failed to delete code block');
          }
        },
      },
    ]);
  };

  const saveNote = async () => {
    if (!noteTitle.trim()) {
      Alert.alert('Error', 'Please provide a title');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/vault/learning`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data_type: 'note',
          title: noteTitle,
          content: noteContent,
          metadata: {},
        }),
      });

      if (response.ok) {
        Alert.alert('Success', 'Note saved!');
        setShowAddNote(false);
        setNoteTitle('');
        setNoteContent('');
        loadLearningData();
        loadVaultInfo();
      }
    } catch (error: any) {
      Alert.alert('Error', `Failed to save note: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTabChange = (tab: VaultTab) => {
    setActiveTab(tab);
    if (tab === 'code' && codeBlocks.length === 0) loadCodeBlocks();
    if (tab === 'assets' && assets.length === 0) loadAssets();
    if (tab === 'database' && schemas.length === 0) loadSchemas();
    if (tab === 'learning' && learningData.length === 0) loadLearningData();
  };

  const renderTabs = () => (
    <View style={[styles.tabs, { borderBottomColor: colors.border }]}>
      {[
        { key: 'code', label: '💻', count: vaultInfo?.vaults?.code_blocks?.count || 0 },
        { key: 'assets', label: '📁', count: vaultInfo?.vaults?.assets?.count || 0 },
        { key: 'database', label: '🗄️', count: vaultInfo?.vaults?.database_schemas?.count || 0 },
        { key: 'learning', label: '📝', count: vaultInfo?.vaults?.learning_data?.count || 0 },
      ].map((tab) => (
        <TouchableOpacity
          key={tab.key}
          style={[
            styles.tab,
            activeTab === tab.key && { borderBottomColor: colors.primary, borderBottomWidth: 2 }
          ]}
          onPress={() => handleTabChange(tab.key as VaultTab)}
        >
          <Text style={styles.tabIcon}>{tab.label}</Text>
          <Text style={[styles.tabCount, { color: activeTab === tab.key ? colors.primary : colors.textSecondary }]}>
            {tab.count}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderCodeTab = () => (
    <ScrollView style={styles.tabContent} showsVerticalScrollIndicator={false}>
      {currentCode && (
        <TouchableOpacity
          style={[styles.addBtn, { backgroundColor: colors.primary }]}
          onPress={() => setShowAddCode(true)}
        >
          <Ionicons name="add" size={20} color="#FFF" />
          <Text style={styles.addBtnText}>Save Current Code to Vault</Text>
        </TouchableOpacity>
      )}

      {showAddCode && (
        <View style={[styles.addForm, { backgroundColor: colors.cardBackground, borderColor: colors.border }]}>
          <TextInput
            style={[styles.input, { backgroundColor: colors.codeBackground, color: colors.text, borderColor: colors.border }]}
            placeholder="Title *"
            placeholderTextColor={colors.textSecondary}
            value={newCodeTitle}
            onChangeText={setNewCodeTitle}
          />
          <TextInput
            style={[styles.input, { backgroundColor: colors.codeBackground, color: colors.text, borderColor: colors.border }]}
            placeholder="Description (optional)"
            placeholderTextColor={colors.textSecondary}
            value={newCodeDesc}
            onChangeText={setNewCodeDesc}
            multiline
          />
          <TextInput
            style={[styles.input, { backgroundColor: colors.codeBackground, color: colors.text, borderColor: colors.border }]}
            placeholder="Tags (comma-separated)"
            placeholderTextColor={colors.textSecondary}
            value={newCodeTags}
            onChangeText={setNewCodeTags}
          />
          <TextInput
            style={[styles.input, { backgroundColor: colors.codeBackground, color: colors.text, borderColor: colors.border }]}
            placeholder="Category"
            placeholderTextColor={colors.textSecondary}
            value={newCodeCategory}
            onChangeText={setNewCodeCategory}
          />
          <View style={styles.formActions}>
            <TouchableOpacity
              style={[styles.formBtn, { backgroundColor: colors.error }]}
              onPress={() => setShowAddCode(false)}
            >
              <Text style={styles.formBtnText}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.formBtn, { backgroundColor: colors.success }]}
              onPress={saveCurrentCode}
              disabled={isLoading}
            >
              {isLoading ? <ActivityIndicator color="#FFF" size="small" /> : <Text style={styles.formBtnText}>Save</Text>}
            </TouchableOpacity>
          </View>
        </View>
      )}

      {isLoading && !showAddCode ? (
        <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 40 }} />
      ) : codeBlocks.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={[styles.emptyIcon]}>📭</Text>
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>No code blocks saved yet</Text>
        </View>
      ) : (
        codeBlocks.map((block) => (
          <View key={block.id} style={[styles.codeCard, { backgroundColor: colors.cardBackground, borderColor: colors.border }]}>
            <View style={styles.codeCardHeader}>
              <View style={styles.codeCardInfo}>
                <Text style={[styles.codeCardTitle, { color: colors.text }]}>{block.title}</Text>
                <View style={styles.codeCardMeta}>
                  <Text style={[styles.codeCardLang, { color: colors.primary }]}>{block.language}</Text>
                  <Text style={[styles.codeCardLines, { color: colors.textSecondary }]}>{block.line_count} lines</Text>
                </View>
              </View>
              <View style={styles.codeCardActions}>
                <TouchableOpacity
                  style={[styles.iconBtn, { backgroundColor: colors.primary }]}
                  onPress={() => onLoadCode?.(block.code, block.language)}
                >
                  <Ionicons name="code-slash" size={16} color="#FFF" />
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.iconBtn, { backgroundColor: colors.error }]}
                  onPress={() => deleteCodeBlock(block.id)}
                >
                  <Ionicons name="trash" size={16} color="#FFF" />
                </TouchableOpacity>
              </View>
            </View>
            {block.description && (
              <Text style={[styles.codeCardDesc, { color: colors.textSecondary }]} numberOfLines={2}>
                {block.description}
              </Text>
            )}
            {block.tags?.length > 0 && (
              <View style={styles.tagsList}>
                {block.tags.map((tag, i) => (
                  <View key={i} style={[styles.tag, { backgroundColor: colors.primary + '20' }]}>
                    <Text style={[styles.tagText, { color: colors.primary }]}>{tag}</Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        ))
      )}
    </ScrollView>
  );

  const renderAssetsTab = () => (
    <ScrollView style={styles.tabContent} showsVerticalScrollIndicator={false}>
      {isLoading ? (
        <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 40 }} />
      ) : assets.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyIcon}>📁</Text>
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>No assets saved yet</Text>
        </View>
      ) : (
        assets.map((asset) => (
          <View key={asset.id} style={[styles.assetCard, { backgroundColor: colors.cardBackground, borderColor: colors.border }]}>
            <Text style={[styles.assetName, { color: colors.text }]}>{asset.name}</Text>
            <Text style={[styles.assetType, { color: colors.textSecondary }]}>{asset.asset_type}</Text>
          </View>
        ))
      )}
    </ScrollView>
  );

  const renderDatabaseTab = () => (
    <ScrollView style={styles.tabContent} showsVerticalScrollIndicator={false}>
      {isLoading ? (
        <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 40 }} />
      ) : schemas.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyIcon}>🗄️</Text>
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>No database schemas saved yet</Text>
        </View>
      ) : (
        schemas.map((schema) => (
          <View key={schema.id} style={[styles.schemaCard, { backgroundColor: colors.cardBackground, borderColor: colors.border }]}>
            <Text style={[styles.schemaName, { color: colors.text }]}>{schema.name}</Text>
            <Text style={[styles.schemaType, { color: colors.textSecondary }]}>{schema.schema_type}</Text>
          </View>
        ))
      )}
    </ScrollView>
  );

  const renderLearningTab = () => (
    <ScrollView style={styles.tabContent} showsVerticalScrollIndicator={false}>
      <TouchableOpacity
        style={[styles.addBtn, { backgroundColor: colors.primary }]}
        onPress={() => setShowAddNote(true)}
      >
        <Ionicons name="add" size={20} color="#FFF" />
        <Text style={styles.addBtnText}>Add Note</Text>
      </TouchableOpacity>

      {showAddNote && (
        <View style={[styles.addForm, { backgroundColor: colors.cardBackground, borderColor: colors.border }]}>
          <TextInput
            style={[styles.input, { backgroundColor: colors.codeBackground, color: colors.text, borderColor: colors.border }]}
            placeholder="Note Title *"
            placeholderTextColor={colors.textSecondary}
            value={noteTitle}
            onChangeText={setNoteTitle}
          />
          <TextInput
            style={[styles.input, { backgroundColor: colors.codeBackground, color: colors.text, borderColor: colors.border, minHeight: 80 }]}
            placeholder="Note Content"
            placeholderTextColor={colors.textSecondary}
            value={noteContent}
            onChangeText={setNoteContent}
            multiline
          />
          <View style={styles.formActions}>
            <TouchableOpacity style={[styles.formBtn, { backgroundColor: colors.error }]} onPress={() => setShowAddNote(false)}>
              <Text style={styles.formBtnText}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.formBtn, { backgroundColor: colors.success }]} onPress={saveNote} disabled={isLoading}>
              {isLoading ? <ActivityIndicator color="#FFF" size="small" /> : <Text style={styles.formBtnText}>Save</Text>}
            </TouchableOpacity>
          </View>
        </View>
      )}

      {isLoading && !showAddNote ? (
        <ActivityIndicator size="large" color={colors.primary} style={{ marginTop: 40 }} />
      ) : learningData.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyIcon}>📝</Text>
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>No learning data saved yet</Text>
        </View>
      ) : (
        learningData.map((item) => (
          <View key={item.id} style={[styles.noteCard, { backgroundColor: colors.cardBackground, borderColor: colors.border }]}>
            <View style={[styles.noteType, { backgroundColor: colors.primary + '20' }]}>
              <Text style={[styles.noteTypeText, { color: colors.primary }]}>{item.data_type}</Text>
            </View>
            <Text style={[styles.noteTitle, { color: colors.text }]}>{item.title}</Text>
            {item.content && (
              <Text style={[styles.noteContent, { color: colors.textSecondary }]} numberOfLines={3}>{item.content}</Text>
            )}
          </View>
        ))
      )}
    </ScrollView>
  );

  return (
    <Modal visible={visible} animationType="slide" transparent={false}>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={[styles.header, { borderBottomColor: colors.border }]}>
          <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
            <Ionicons name="close" size={24} color={colors.text} />
          </TouchableOpacity>
          <Text style={[styles.title, { color: colors.text }]}>🏦 Vault</Text>
          <View style={styles.placeholder} />
        </View>

        {renderTabs()}
        
        {activeTab === 'code' && renderCodeTab()}
        {activeTab === 'assets' && renderAssetsTab()}
        {activeTab === 'database' && renderDatabaseTab()}
        {activeTab === 'learning' && renderLearningTab()}
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: Platform.OS === 'ios' ? 50 : 30 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  closeBtn: { padding: 8 },
  title: { fontSize: 20, fontWeight: 'bold' },
  placeholder: { width: 40 },
  tabs: { flexDirection: 'row', borderBottomWidth: 1 },
  tab: { flex: 1, paddingVertical: 12, alignItems: 'center' },
  tabIcon: { fontSize: 20 },
  tabCount: { fontSize: 11, fontWeight: '600', marginTop: 2 },
  tabContent: { flex: 1, padding: 16 },
  addBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', padding: 12, borderRadius: 8, gap: 8, marginBottom: 16 },
  addBtnText: { color: '#FFF', fontSize: 14, fontWeight: '600' },
  addForm: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 16 },
  input: { borderWidth: 1, borderRadius: 8, padding: 12, fontSize: 14, marginBottom: 12 },
  formActions: { flexDirection: 'row', justifyContent: 'flex-end', gap: 8 },
  formBtn: { paddingHorizontal: 16, paddingVertical: 8, borderRadius: 6 },
  formBtnText: { color: '#FFF', fontSize: 14, fontWeight: '600' },
  emptyState: { alignItems: 'center', paddingTop: 60 },
  emptyIcon: { fontSize: 48, marginBottom: 12 },
  emptyText: { fontSize: 14 },
  codeCard: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 12 },
  codeCardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  codeCardInfo: { flex: 1 },
  codeCardTitle: { fontSize: 16, fontWeight: '600' },
  codeCardMeta: { flexDirection: 'row', gap: 8, marginTop: 4 },
  codeCardLang: { fontSize: 12, fontWeight: '600' },
  codeCardLines: { fontSize: 12 },
  codeCardActions: { flexDirection: 'row', gap: 8 },
  iconBtn: { width: 32, height: 32, borderRadius: 6, justifyContent: 'center', alignItems: 'center' },
  codeCardDesc: { fontSize: 13, marginTop: 8 },
  tagsList: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: 8 },
  tag: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 10 },
  tagText: { fontSize: 11, fontWeight: '500' },
  assetCard: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 12 },
  assetName: { fontSize: 16, fontWeight: '600' },
  assetType: { fontSize: 12, marginTop: 4 },
  schemaCard: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 12 },
  schemaName: { fontSize: 16, fontWeight: '600' },
  schemaType: { fontSize: 12, marginTop: 4 },
  noteCard: { padding: 16, borderRadius: 12, borderWidth: 1, marginBottom: 12 },
  noteType: { alignSelf: 'flex-start', paddingHorizontal: 8, paddingVertical: 3, borderRadius: 10, marginBottom: 8 },
  noteTypeText: { fontSize: 10, fontWeight: '600', textTransform: 'uppercase' },
  noteTitle: { fontSize: 16, fontWeight: '600' },
  noteContent: { fontSize: 13, marginTop: 6, lineHeight: 18 },
});

export default VaultModal;
