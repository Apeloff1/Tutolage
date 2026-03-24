/**
 * Text-to-World Engine Modal v11.5
 * Environment & World Generation Pipeline
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

interface WorldEngineModalProps {
  visible: boolean;
  onClose: () => void;
  colors: any;
}

type WorldStyle = 'fantasy' | 'sci-fi' | 'post-apocalyptic' | 'historical' | 'modern';
type GenerationType = 'world' | 'terrain' | 'architecture' | 'atmosphere';

export const WorldEngineModal = memo(function WorldEngineModal({
  visible, onClose, colors
}: WorldEngineModalProps) {
  const [selectedType, setSelectedType] = useState<GenerationType | null>(null);
  const [style, setStyle] = useState<WorldStyle>('fantasy');
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
      const res = await fetch(`${API_URL}/api/world-engine/info`);
      const data = await res.json();
      setInfo(data);
    } catch (e) {
      console.error('Failed to fetch world engine info:', e);
    }
  };

  const styles_list: { id: WorldStyle; name: string; icon: string; color: string }[] = [
    { id: 'fantasy', name: 'Fantasy', icon: 'sparkles', color: '#8B5CF6' },
    { id: 'sci-fi', name: 'Sci-Fi', icon: 'planet', color: '#06B6D4' },
    { id: 'post-apocalyptic', name: 'Post-Apocalyptic', icon: 'skull', color: '#EF4444' },
    { id: 'historical', name: 'Historical', icon: 'time', color: '#F59E0B' },
    { id: 'modern', name: 'Modern', icon: 'business', color: '#10B981' },
  ];

  const generationTypes: { id: GenerationType; name: string; icon: string; desc: string }[] = [
    { id: 'world', name: 'Full World', icon: 'globe', desc: 'Complete environment' },
    { id: 'terrain', name: 'Terrain', icon: 'layers', desc: 'Heightmaps & features' },
    { id: 'architecture', name: 'Architecture', icon: 'business', desc: 'Buildings & structures' },
    { id: 'atmosphere', name: 'Atmosphere', icon: 'cloud', desc: 'Sky, weather, mood' },
  ];

  const generate = async () => {
    if (!selectedType || !prompt.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const endpoint = selectedType === 'world' ? 'generate' : selectedType;
      const body = selectedType === 'world' ? {
        prompt,
        style,
        scale: 'medium',
        detail_level: 'high',
        include_terrain: true,
        include_structures: true,
        include_vegetation: true,
        include_atmosphere: true
      } : {
        description: prompt,
        ...(selectedType === 'terrain' && { terrain_type: 'mixed', features: ['rivers', 'mountains'] }),
        ...(selectedType === 'architecture' && { style: style === 'fantasy' ? 'medieval' : 'modern', condition: 'intact', interior: true }),
        ...(selectedType === 'atmosphere' && { time_of_day: 'day', weather: 'clear', mood: 'neutral' })
      };

      const res = await fetch(`${API_URL}/api/world-engine/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error('World generation error:', e);
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
              <Ionicons name="globe" size={24} color="#10B981" />
              <Text style={[localStyles.title, { color: colors.text }]}>Text to World</Text>
            </View>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color={colors.textSecondary} />
            </TouchableOpacity>
          </View>

          <ScrollView style={localStyles.content} showsVerticalScrollIndicator={false}>
            {/* Info Banner */}
            {info && (
              <View style={[localStyles.infoBanner, { backgroundColor: '#10B98115' }]}>
                <Text style={[localStyles.infoText, { color: colors.text }]}>
                  {info.total_presets} Presets • {info.terrain_generators?.length} Generators • Export to {info.export_formats?.length} formats
                </Text>
              </View>
            )}

            {/* Style Selection */}
            <Text style={[localStyles.sectionTitle, { color: colors.text }]}>World Style</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={localStyles.styleRow}>
              {styles_list.map((s) => (
                <TouchableOpacity
                  key={s.id}
                  style={[
                    localStyles.styleChip,
                    { backgroundColor: style === s.id ? s.color + '30' : colors.surfaceAlt }
                  ]}
                  onPress={() => setStyle(s.id)}
                >
                  <Ionicons name={s.icon as any} size={18} color={s.color} />
                  <Text style={[localStyles.styleText, { color: style === s.id ? s.color : colors.text }]}>
                    {s.name}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>

            {/* Generation Type */}
            <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Generate</Text>
            <View style={localStyles.typeGrid}>
              {generationTypes.map((type) => (
                <TouchableOpacity
                  key={type.id}
                  style={[
                    localStyles.typeCard,
                    { 
                      backgroundColor: selectedType === type.id ? '#10B98120' : colors.surfaceAlt,
                      borderColor: selectedType === type.id ? '#10B981' : colors.border
                    }
                  ]}
                  onPress={() => setSelectedType(type.id)}
                >
                  <Ionicons name={type.icon as any} size={24} color={selectedType === type.id ? '#10B981' : colors.textMuted} />
                  <Text style={[localStyles.typeName, { color: colors.text }]}>{type.name}</Text>
                  <Text style={[localStyles.typeDesc, { color: colors.textMuted }]}>{type.desc}</Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Prompt Input */}
            {selectedType && (
              <View style={localStyles.promptSection}>
                <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Describe Your World</Text>
                <TextInput
                  style={[localStyles.promptInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                  placeholder="A mystical forest with ancient ruins, glowing mushrooms, and a hidden waterfall..."
                  placeholderTextColor={colors.textMuted}
                  value={prompt}
                  onChangeText={setPrompt}
                  multiline
                  numberOfLines={4}
                />
                <TouchableOpacity
                  style={[localStyles.generateBtn, { backgroundColor: loading ? colors.surfaceAlt : '#10B981' }]}
                  onPress={generate}
                  disabled={loading || !prompt.trim()}
                >
                  {loading ? (
                    <ActivityIndicator color="#FFF" />
                  ) : (
                    <>
                      <Ionicons name="sparkles" size={20} color="#FFF" />
                      <Text style={localStyles.generateText}>Generate World</Text>
                    </>
                  )}
                </TouchableOpacity>
              </View>
            )}

            {/* Result */}
            {result && (
              <View style={[localStyles.resultSection, { backgroundColor: colors.surfaceAlt }]}>
                <Text style={[localStyles.resultTitle, { color: colors.text }]}>Generated World</Text>
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
  styleRow: { marginBottom: 20 },
  styleChip: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 14, paddingVertical: 10, borderRadius: 10, marginRight: 10, gap: 8 },
  styleText: { fontSize: 14, fontWeight: '600' },
  typeGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 20 },
  typeCard: { width: (SCREEN_WIDTH - 58) / 2, padding: 16, borderRadius: 12, borderWidth: 2, alignItems: 'center' },
  typeName: { fontSize: 14, fontWeight: '700', marginTop: 8 },
  typeDesc: { fontSize: 12, marginTop: 4, textAlign: 'center' },
  promptSection: { marginBottom: 20 },
  promptInput: { padding: 14, borderRadius: 12, borderWidth: 1, fontSize: 14, minHeight: 100, textAlignVertical: 'top', marginBottom: 12 },
  generateBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 14, borderRadius: 12, gap: 10 },
  generateText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
  resultSection: { padding: 14, borderRadius: 12, marginBottom: 20 },
  resultTitle: { fontSize: 14, fontWeight: '700', marginBottom: 10 },
  resultScroll: { maxHeight: 250 },
  resultText: { fontSize: 12, lineHeight: 18, fontFamily: 'monospace' },
});
