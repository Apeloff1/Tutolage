/**
 * Text-to-Logic Engine Modal v11.5
 * Game Mechanics, Rules & AI Behavior Generation Pipeline
 */

import React, { useState, useEffect, memo } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput,
  Modal, ActivityIndicator, Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import Constants from 'expo-constants';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const API_URL = Constants.expoConfig?.extra?.apiUrl || process.env.EXPO_PUBLIC_BACKEND_URL || '';

interface LogicEngineModalProps {
  visible: boolean;
  onClose: () => void;
  colors: any;
}

type LogicType = 'mechanic' | 'ai' | 'rules' | 'procedural' | 'balance';
type MechanicCategory = 'combat' | 'crafting' | 'progression' | 'economy';

export const LogicEngineModal = memo(function LogicEngineModal({
  visible, onClose, colors
}: LogicEngineModalProps) {
  const [selectedType, setSelectedType] = useState<LogicType | null>(null);
  const [category, setCategory] = useState<MechanicCategory>('combat');
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [info, setInfo] = useState<any>(null);

  useEffect(() => {
    if (visible) {
      fetchInfo();
    }
  }, [visible]);

  const fetchInfo = async () => {
    try {
      const res = await fetch(`${API_URL}/api/game-logic/info`);
      const data = await res.json();
      setInfo(data);
    } catch (e) {
      console.error('Failed to fetch logic engine info:', e);
    }
  };

  const categories: { id: MechanicCategory; name: string; icon: string; color: string }[] = [
    { id: 'combat', name: 'Combat', icon: 'flash', color: '#EF4444' },
    { id: 'crafting', name: 'Crafting', icon: 'construct', color: '#F59E0B' },
    { id: 'progression', name: 'Progression', icon: 'trending-up', color: '#10B981' },
    { id: 'economy', name: 'Economy', icon: 'cash', color: '#3B82F6' },
  ];

  const logicTypes: { id: LogicType; name: string; icon: string; desc: string }[] = [
    { id: 'mechanic', name: 'Mechanic', icon: 'cog', desc: 'Game systems' },
    { id: 'ai', name: 'AI Behavior', icon: 'hardware-chip', desc: 'Enemy/NPC AI' },
    { id: 'rules', name: 'Rule System', icon: 'list', desc: 'Game rules' },
    { id: 'procedural', name: 'Procedural', icon: 'shuffle', desc: 'Random systems' },
    { id: 'balance', name: 'Balance', icon: 'analytics', desc: 'Tuning & curves' },
  ];

  const generate = async () => {
    if (!selectedType || !prompt.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const endpoints: Record<LogicType, string> = {
        mechanic: 'generate-mechanic',
        ai: 'generate-ai',
        rules: 'generate-rules',
        procedural: 'generate-procedural',
        balance: 'balance'
      };

      const bodies: Record<LogicType, any> = {
        mechanic: { description: prompt, mechanic_type: category, complexity: 'medium', target_platform: 'all', genre: 'action_rpg', include_formulas: true, include_balance: true },
        ai: { entity_type: 'enemy', description: prompt, behavior_style: 'balanced', intelligence_level: 'medium', include_state_machine: true, include_behavior_tree: true },
        rules: { system_type: 'physics', description: prompt, realism_level: 'arcade', complexity: 'medium' },
        procedural: { system_type: 'loot', description: prompt, randomness: 0.5, constraints: [] },
        balance: { mechanic_description: prompt, player_power_curve: 'linear', difficulty_scaling: 'adaptive', target_session_length: 30 }
      };

      const res = await fetch(`${API_URL}/api/game-logic/${endpoints[selectedType]}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodies[selectedType])
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error('Logic generation error:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal visible={visible} animationType="slide" transparent onRequestClose={onClose}>
      <View style={localStyles.overlay}>
        <View style={[localStyles.modal, { backgroundColor: colors.surface }]}>
          {/* Header */}
          <View style={[localStyles.header, { borderBottomColor: colors.border }]}>
            <View style={localStyles.headerTitle}>
              <Ionicons name="code-working" size={24} color="#3B82F6" />
              <Text style={[localStyles.title, { color: colors.text }]}>Text to Logic</Text>
            </View>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color={colors.textSecondary} />
            </TouchableOpacity>
          </View>

          <ScrollView style={localStyles.content} showsVerticalScrollIndicator={false}>
            {/* Info Banner */}
            {info && (
              <View style={[localStyles.infoBanner, { backgroundColor: '#3B82F615' }]}>
                <Text style={[localStyles.infoText, { color: colors.text }]}>
                  {info.mechanic_types?.length} Mechanic Types • {info.ai_templates?.length} AI Templates • Export to {info.output_formats?.length} formats
                </Text>
              </View>
            )}

            {/* Category Selection */}
            <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Category</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={localStyles.categoryRow}>
              {categories.map((c) => (
                <TouchableOpacity
                  key={c.id}
                  style={[
                    localStyles.categoryChip,
                    { backgroundColor: category === c.id ? c.color + '30' : colors.surfaceAlt }
                  ]}
                  onPress={() => setCategory(c.id)}
                >
                  <Ionicons name={c.icon as any} size={18} color={c.color} />
                  <Text style={[localStyles.categoryText, { color: category === c.id ? c.color : colors.text }]}>
                    {c.name}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>

            {/* Logic Type */}
            <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Generate</Text>
            <View style={localStyles.typeGrid}>
              {logicTypes.map((type) => (
                <TouchableOpacity
                  key={type.id}
                  style={[
                    localStyles.typeCard,
                    { 
                      backgroundColor: selectedType === type.id ? '#3B82F620' : colors.surfaceAlt,
                      borderColor: selectedType === type.id ? '#3B82F6' : colors.border
                    }
                  ]}
                  onPress={() => setSelectedType(type.id)}
                >
                  <Ionicons name={type.icon as any} size={22} color={selectedType === type.id ? '#3B82F6' : colors.textMuted} />
                  <Text style={[localStyles.typeName, { color: colors.text }]}>{type.name}</Text>
                  <Text style={[localStyles.typeDesc, { color: colors.textMuted }]}>{type.desc}</Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Prompt Input */}
            {selectedType && (
              <View style={localStyles.promptSection}>
                <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Describe the System</Text>
                <TextInput
                  style={[localStyles.promptInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                  placeholder={selectedType === 'mechanic' ? 'A turn-based combat system with elemental weaknesses...' : 
                               selectedType === 'ai' ? 'A boss enemy that adapts to player patterns...' :
                               selectedType === 'rules' ? 'Physics system with realistic gravity and collision...' :
                               selectedType === 'procedural' ? 'Loot system with tiered rarities and modifiers...' : 
                               'Balance the difficulty curve for a 30-minute session...'}
                  placeholderTextColor={colors.textMuted}
                  value={prompt}
                  onChangeText={setPrompt}
                  multiline
                  numberOfLines={4}
                />
                <TouchableOpacity
                  style={[localStyles.generateBtn, { backgroundColor: loading ? colors.surfaceAlt : '#3B82F6' }]}
                  onPress={generate}
                  disabled={loading || !prompt.trim()}
                >
                  {loading ? (
                    <ActivityIndicator color="#FFF" />
                  ) : (
                    <>
                      <Ionicons name="code-slash" size={20} color="#FFF" />
                      <Text style={localStyles.generateText}>Generate Logic</Text>
                    </>
                  )}
                </TouchableOpacity>
              </View>
            )}

            {/* Result */}
            {result && (
              <View style={[localStyles.resultSection, { backgroundColor: colors.surfaceAlt }]}>
                <Text style={[localStyles.resultTitle, { color: colors.text }]}>Generated System</Text>
                <ScrollView style={localStyles.resultScroll} nestedScrollEnabled>
                  <Text style={[localStyles.resultText, { color: colors.text }]}>
                    {JSON.stringify(result, null, 2)}
                  </Text>
                </ScrollView>
              </View>
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
});

const localStyles = StyleSheet.create({
  overlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  modal: { maxHeight: '90%', borderTopLeftRadius: 20, borderTopRightRadius: 20 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingVertical: 14, borderBottomWidth: 1 },
  headerTitle: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  title: { fontSize: 18, fontWeight: '700' },
  content: { padding: 16 },
  infoBanner: { padding: 12, borderRadius: 10, marginBottom: 16 },
  infoText: { fontSize: 13, fontWeight: '600', textAlign: 'center' },
  sectionTitle: { fontSize: 16, fontWeight: '700', marginBottom: 12 },
  categoryRow: { marginBottom: 20 },
  categoryChip: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 14, paddingVertical: 10, borderRadius: 10, marginRight: 10, gap: 8 },
  categoryText: { fontSize: 14, fontWeight: '600' },
  typeGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 20 },
  typeCard: { width: (SCREEN_WIDTH - 58) / 2, padding: 14, borderRadius: 12, borderWidth: 2, alignItems: 'center' },
  typeName: { fontSize: 13, fontWeight: '700', marginTop: 8 },
  typeDesc: { fontSize: 11, marginTop: 4, textAlign: 'center' },
  promptSection: { marginBottom: 20 },
  promptInput: { padding: 14, borderRadius: 12, borderWidth: 1, fontSize: 14, minHeight: 100, textAlignVertical: 'top', marginBottom: 12 },
  generateBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 14, borderRadius: 12, gap: 10 },
  generateText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
  resultSection: { padding: 14, borderRadius: 12, marginBottom: 20 },
  resultTitle: { fontSize: 14, fontWeight: '700', marginBottom: 10 },
  resultScroll: { maxHeight: 250 },
  resultText: { fontSize: 12, lineHeight: 18, fontFamily: 'monospace' },
});
