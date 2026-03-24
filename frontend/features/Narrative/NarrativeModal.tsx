/**
 * Text-to-Narrative Engine Modal v11.5
 * Story, Dialogue & Quest Generation Pipeline
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

interface NarrativeModalProps {
  visible: boolean;
  onClose: () => void;
  colors: any;
}

type NarrativeType = 'story' | 'character' | 'dialogue' | 'quest' | 'lore';
type Genre = 'fantasy' | 'sci-fi' | 'horror' | 'mystery' | 'adventure';

export const NarrativeModal = memo(function NarrativeModal({
  visible, onClose, colors
}: NarrativeModalProps) {
  const [selectedType, setSelectedType] = useState<NarrativeType | null>(null);
  const [genre, setGenre] = useState<Genre>('fantasy');
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
      const res = await fetch(`${API_URL}/api/narrative/info`);
      const data = await res.json();
      setInfo(data);
    } catch (e) {
      console.error('Failed to fetch narrative info:', e);
    }
  };

  const genres: { id: Genre; name: string; icon: string; color: string }[] = [
    { id: 'fantasy', name: 'Fantasy', icon: 'sparkles', color: '#8B5CF6' },
    { id: 'sci-fi', name: 'Sci-Fi', icon: 'rocket', color: '#06B6D4' },
    { id: 'horror', name: 'Horror', icon: 'skull', color: '#EF4444' },
    { id: 'mystery', name: 'Mystery', icon: 'search', color: '#F59E0B' },
    { id: 'adventure', name: 'Adventure', icon: 'compass', color: '#10B981' },
  ];

  const narrativeTypes: { id: NarrativeType; name: string; icon: string; desc: string }[] = [
    { id: 'story', name: 'Full Story', icon: 'book', desc: 'Complete story arc' },
    { id: 'character', name: 'Character', icon: 'person', desc: 'Detailed character' },
    { id: 'dialogue', name: 'Dialogue', icon: 'chatbubbles', desc: 'Conversations' },
    { id: 'quest', name: 'Quest', icon: 'flag', desc: 'Missions & objectives' },
    { id: 'lore', name: 'Lore', icon: 'library', desc: 'World-building' },
  ];

  const generate = async () => {
    if (!selectedType || !prompt.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const endpoints: Record<NarrativeType, string> = {
        story: 'generate-story',
        character: 'generate-character',
        dialogue: 'generate-dialogue',
        quest: 'generate-quest',
        lore: 'generate-lore'
      };

      const bodies: Record<NarrativeType, any> = {
        story: { premise: prompt, genre, tone: 'epic', structure: 'three_act', length: 'medium', include_characters: true, include_locations: true },
        character: { description: prompt, role: 'protagonist', archetype: 'hero', backstory_depth: 'detailed' },
        dialogue: { context: prompt, characters: ['Character A', 'Character B'], mood: 'neutral', purpose: 'exposition', length: 10, include_choices: true },
        quest: { description: prompt, quest_type: 'main', difficulty: 'medium', estimated_time: 'medium', include_subquests: true },
        lore: { topic: prompt, category: 'history', depth: 'moderate', format: 'document' }
      };

      const res = await fetch(`${API_URL}/api/narrative/${endpoints[selectedType]}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodies[selectedType])
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error('Narrative generation error:', e);
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
              <Ionicons name="book" size={24} color="#F59E0B" />
              <Text style={[localStyles.title, { color: colors.text }]}>Text to Narrative</Text>
            </View>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color={colors.textSecondary} />
            </TouchableOpacity>
          </View>

          <ScrollView style={localStyles.content} showsVerticalScrollIndicator={false}>
            {/* Info Banner */}
            {info && (
              <View style={[localStyles.infoBanner, { backgroundColor: '#F59E0B15' }]}>
                <Text style={[localStyles.infoText, { color: colors.text }]}>
                  {info.story_structures?.length} Story Structures • {info.character_archetypes?.length} Archetypes • {info.quest_templates?.length} Quest Types
                </Text>
              </View>
            )}

            {/* Genre Selection */}
            <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Genre</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={localStyles.genreRow}>
              {genres.map((g) => (
                <TouchableOpacity
                  key={g.id}
                  style={[
                    localStyles.genreChip,
                    { backgroundColor: genre === g.id ? g.color + '30' : colors.surfaceAlt }
                  ]}
                  onPress={() => setGenre(g.id)}
                >
                  <Ionicons name={g.icon as any} size={18} color={g.color} />
                  <Text style={[localStyles.genreText, { color: genre === g.id ? g.color : colors.text }]}>
                    {g.name}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>

            {/* Narrative Type */}
            <Text style={[localStyles.sectionTitle, { color: colors.text }]}>Create</Text>
            <View style={localStyles.typeGrid}>
              {narrativeTypes.map((type) => (
                <TouchableOpacity
                  key={type.id}
                  style={[
                    localStyles.typeCard,
                    { 
                      backgroundColor: selectedType === type.id ? '#F59E0B20' : colors.surfaceAlt,
                      borderColor: selectedType === type.id ? '#F59E0B' : colors.border
                    }
                  ]}
                  onPress={() => setSelectedType(type.id)}
                >
                  <Ionicons name={type.icon as any} size={22} color={selectedType === type.id ? '#F59E0B' : colors.textMuted} />
                  <Text style={[localStyles.typeName, { color: colors.text }]}>{type.name}</Text>
                  <Text style={[localStyles.typeDesc, { color: colors.textMuted }]}>{type.desc}</Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Prompt Input */}
            {selectedType && (
              <View style={localStyles.promptSection}>
                <Text style={[localStyles.sectionTitle, { color: colors.text }]}>
                  {selectedType === 'story' ? 'Story Premise' : 
                   selectedType === 'character' ? 'Character Description' :
                   selectedType === 'dialogue' ? 'Scene Context' :
                   selectedType === 'quest' ? 'Quest Description' : 'Lore Topic'}
                </Text>
                <TextInput
                  style={[localStyles.promptInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
                  placeholder={selectedType === 'story' ? 'A hero discovers an ancient artifact that...' : 
                               selectedType === 'character' ? 'A mysterious wanderer with a hidden past...' :
                               selectedType === 'dialogue' ? 'Two rivals meet at a crossroads...' :
                               selectedType === 'quest' ? 'Retrieve the stolen crown from...' : 
                               'The ancient order of...'}  
                  placeholderTextColor={colors.textMuted}
                  value={prompt}
                  onChangeText={setPrompt}
                  multiline
                  numberOfLines={4}
                />
                <TouchableOpacity
                  style={[localStyles.generateBtn, { backgroundColor: loading ? colors.surfaceAlt : '#F59E0B' }]}
                  onPress={generate}
                  disabled={loading || !prompt.trim()}
                >
                  {loading ? (
                    <ActivityIndicator color="#FFF" />
                  ) : (
                    <>
                      <Ionicons name="create" size={20} color="#FFF" />
                      <Text style={localStyles.generateText}>Generate Narrative</Text>
                    </>
                  )}
                </TouchableOpacity>
              </View>
            )}

            {/* Result */}
            {result && (
              <View style={[localStyles.resultSection, { backgroundColor: colors.surfaceAlt }]}>
                <Text style={[localStyles.resultTitle, { color: colors.text }]}>Generated Content</Text>
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
  genreRow: { marginBottom: 20 },
  genreChip: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 14, paddingVertical: 10, borderRadius: 10, marginRight: 10, gap: 8 },
  genreText: { fontSize: 14, fontWeight: '600' },
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
