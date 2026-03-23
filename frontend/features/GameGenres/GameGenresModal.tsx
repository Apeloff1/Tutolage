/**
 * Game Genres Modal v11.2.0
 * Complete Game Development Pipeline
 */

import React, { useState, useEffect } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput,
  Modal, ActivityIndicator, Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';
const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface GameGenresModalProps {
  visible: boolean;
  onClose: () => void;
  colors: any;
}

export const GameGenresModal: React.FC<GameGenresModalProps> = ({
  visible, onClose, colors
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [genres, setGenres] = useState<any[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<any>(null);
  const [selectedSubgenre, setSelectedSubgenre] = useState<any>(null);
  const [showProjectForm, setShowProjectForm] = useState(false);
  
  // Project form
  const [projectName, setProjectName] = useState('');
  const [projectDesc, setProjectDesc] = useState('');
  const [projectResult, setProjectResult] = useState<any>(null);

  useEffect(() => {
    if (visible) {
      loadGenres();
    }
  }, [visible]);

  const loadGenres = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/game-genres/all`);
      const data = await response.json();
      setGenres(data.genres || []);
    } catch (error) {
      console.error('Failed to load genres:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadGenreDetails = async (genreKey: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/game-genres/${genreKey}`);
      const data = await response.json();
      setSelectedGenre(data);
    } catch (error) {
      console.error('Failed to load genre:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadSubgenreDetails = async (genreKey: string, subgenreKey: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/game-genres/${genreKey}/${subgenreKey}`);
      const data = await response.json();
      setSelectedSubgenre(data);
    } catch (error) {
      console.error('Failed to load subgenre:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const createProject = async () => {
    if (!projectName.trim() || !selectedGenre || !selectedSubgenre) return;
    setIsLoading(true);
    try {
      const genreKey = genres.find(g => g.name === selectedGenre.name)?.key;
      const subgenreKey = Object.entries(selectedGenre.subgenres || {}).find(
        ([_, v]: [string, any]) => v.name === selectedSubgenre.subgenre?.name
      )?.[0];
      
      const response = await fetch(`${API_URL}/api/game-genres/create-project`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: projectName,
          genre: genreKey,
          subgenre: subgenreKey,
          description: projectDesc,
          target_platform: 'pc',
          art_style: 'stylized',
          scope: 'indie'
        })
      });
      const data = await response.json();
      setProjectResult(data);
    } catch (error) {
      console.error('Project creation failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const goBack = () => {
    if (projectResult) {
      setProjectResult(null);
      setShowProjectForm(false);
    } else if (showProjectForm) {
      setShowProjectForm(false);
    } else if (selectedSubgenre) {
      setSelectedSubgenre(null);
    } else if (selectedGenre) {
      setSelectedGenre(null);
    } else {
      onClose();
    }
  };

  const renderGenresList = () => (
    <ScrollView style={styles.genresList} contentContainerStyle={styles.genresContent}>
      <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>
        {genres.length} Genres • 39+ Subgenres
      </Text>
      {genres.map((genre) => (
        <TouchableOpacity
          key={genre.key}
          style={[styles.genreCard, { backgroundColor: colors.surfaceAlt }]}
          onPress={() => loadGenreDetails(genre.key)}
        >
          <Text style={styles.genreIcon}>{genre.icon}</Text>
          <View style={styles.genreInfo}>
            <Text style={[styles.genreName, { color: colors.text }]}>{genre.name}</Text>
            <Text style={[styles.genreDesc, { color: colors.textMuted }]}>{genre.description}</Text>
          </View>
          <View style={[styles.subgenreCount, { backgroundColor: colors.primary + '20' }]}>
            <Text style={[styles.subgenreCountText, { color: colors.primary }]}>{genre.subgenre_count}</Text>
          </View>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );

  const renderGenreDetails = () => {
    if (!selectedGenre) return null;
    const subgenres = Object.entries(selectedGenre.subgenres || {});
    
    return (
      <ScrollView style={styles.genreDetails}>
        <View style={[styles.genreHeader, { backgroundColor: colors.surfaceAlt }]}>
          <Text style={styles.genreDetailIcon}>{selectedGenre.icon}</Text>
          <Text style={[styles.genreDetailName, { color: colors.text }]}>{selectedGenre.name}</Text>
          <Text style={[styles.genreDetailDesc, { color: colors.textMuted }]}>{selectedGenre.description}</Text>
        </View>
        
        <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>Subgenres</Text>
        {subgenres.map(([key, subgenre]: [string, any]) => (
          <TouchableOpacity
            key={key}
            style={[styles.subgenreCard, { backgroundColor: colors.surfaceAlt }]}
            onPress={() => loadSubgenreDetails(genres.find(g => g.name === selectedGenre.name)?.key, key)}
          >
            <View style={styles.subgenreInfo}>
              <Text style={[styles.subgenreName, { color: colors.text }]}>{subgenre.name}</Text>
              {subgenre.examples && (
                <Text style={[styles.subgenreExamples, { color: colors.textMuted }]}>
                  {subgenre.examples.slice(0, 3).join(' • ')}
                </Text>
              )}
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </TouchableOpacity>
        ))}
      </ScrollView>
    );
  };

  const renderSubgenreDetails = () => {
    if (!selectedSubgenre) return null;
    const subgenre = selectedSubgenre.subgenre;
    const pipeline = selectedSubgenre.pipeline;
    
    return (
      <ScrollView style={styles.subgenreDetails}>
        <View style={[styles.subgenreHeader, { backgroundColor: colors.surfaceAlt }]}>
          <Text style={[styles.subgenreDetailName, { color: colors.text }]}>{subgenre?.name}</Text>
          {subgenre?.examples && (
            <View style={styles.examplesRow}>
              {subgenre.examples.map((ex: string) => (
                <View key={ex} style={[styles.exampleTag, { backgroundColor: colors.primary + '20' }]}>
                  <Text style={[styles.exampleText, { color: colors.primary }]}>{ex}</Text>
                </View>
              ))}
            </View>
          )}
        </View>

        {subgenre?.mechanics && (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>Core Mechanics</Text>
            <View style={styles.mechanicsGrid}>
              {subgenre.mechanics.map((m: string) => (
                <View key={m} style={[styles.mechanicTag, { backgroundColor: colors.surfaceAlt }]}>
                  <Ionicons name="game-controller" size={14} color={colors.secondary} />
                  <Text style={[styles.mechanicText, { color: colors.text }]}>{m.replace(/_/g, ' ')}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {subgenre?.assets_needed && (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>Assets Needed</Text>
            <View style={styles.assetsGrid}>
              {subgenre.assets_needed.map((a: string) => (
                <View key={a} style={[styles.assetTag, { backgroundColor: colors.surfaceAlt }]}>
                  <Ionicons name="cube" size={14} color="#10B981" />
                  <Text style={[styles.assetText, { color: colors.text }]}>{a.replace(/_/g, ' ')}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {pipeline && (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>Development Pipeline</Text>
            {Object.entries(pipeline).map(([phase, items]: [string, any]) => (
              <View key={phase} style={[styles.pipelinePhase, { backgroundColor: colors.surfaceAlt }]}>
                <Text style={[styles.phaseName, { color: colors.text }]}>{phase.replace(/_/g, ' ')}</Text>
                {Array.isArray(items) && items.map((item: string, idx: number) => (
                  <Text key={idx} style={[styles.phaseItem, { color: colors.textMuted }]}>• {item}</Text>
                ))}
              </View>
            ))}
          </View>
        )}

        <TouchableOpacity
          style={[styles.createProjectBtn, { backgroundColor: colors.primary }]}
          onPress={() => setShowProjectForm(true)}
        >
          <Ionicons name="rocket" size={20} color="#FFF" />
          <Text style={styles.createProjectText}>Create Game Project</Text>
        </TouchableOpacity>
      </ScrollView>
    );
  };

  const renderProjectForm = () => (
    <ScrollView style={styles.projectForm}>
      <View style={[styles.formHeader, { backgroundColor: colors.surfaceAlt }]}>
        <Ionicons name="rocket" size={32} color={colors.primary} />
        <Text style={[styles.formTitle, { color: colors.text }]}>New Game Project</Text>
        <Text style={[styles.formSubtitle, { color: colors.textMuted }]}>
          {selectedSubgenre?.subgenre?.name} • {selectedGenre?.name}
        </Text>
      </View>

      <Text style={[styles.inputLabel, { color: colors.textMuted }]}>Project Name *</Text>
      <TextInput
        style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
        value={projectName}
        onChangeText={setProjectName}
        placeholder="My Awesome Game"
        placeholderTextColor={colors.textMuted}
      />

      <Text style={[styles.inputLabel, { color: colors.textMuted }]}>Description</Text>
      <TextInput
        style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border, minHeight: 100 }]}
        value={projectDesc}
        onChangeText={setProjectDesc}
        placeholder="Describe your game idea..."
        placeholderTextColor={colors.textMuted}
        multiline
      />

      <TouchableOpacity
        style={[styles.createBtn, { backgroundColor: colors.primary }]}
        onPress={createProject}
        disabled={isLoading || !projectName.trim()}
      >
        {isLoading ? (
          <ActivityIndicator color="#FFF" />
        ) : (
          <>
            <Ionicons name="create" size={20} color="#FFF" />
            <Text style={styles.createBtnText}>Generate Project Spec</Text>
          </>
        )}
      </TouchableOpacity>
    </ScrollView>
  );

  const renderProjectResult = () => {
    if (!projectResult) return null;
    return (
      <ScrollView style={styles.projectResult}>
        <View style={[styles.resultHeader, { backgroundColor: colors.surfaceAlt }]}>
          <Ionicons name="checkmark-circle" size={32} color="#10B981" />
          <Text style={[styles.resultTitle, { color: colors.text }]}>{projectResult.name}</Text>
          <Text style={[styles.resultId, { color: colors.textMuted }]}>ID: {projectResult.id}</Text>
        </View>

        {projectResult.mechanics && (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>Mechanics</Text>
            <Text style={[styles.resultText, { color: colors.text }]}>{projectResult.mechanics.join(', ')}</Text>
          </View>
        )}

        {projectResult.assets_required && (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textMuted }]}>Assets Required</Text>
            <Text style={[styles.resultText, { color: colors.text }]}>{projectResult.assets_required.join(', ')}</Text>
          </View>
        )}

        {projectResult.ai_specification && (
          <View style={[styles.aiSpec, { backgroundColor: colors.surfaceAlt }]}>
            <Text style={[styles.aiSpecTitle, { color: colors.text }]}>AI-Generated Specification</Text>
            <Text style={[styles.aiSpecText, { color: colors.text }]}>{projectResult.ai_specification}</Text>
          </View>
        )}
      </ScrollView>
    );
  };

  return (
    <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={[styles.header, { borderBottomColor: colors.border }]}>
          <TouchableOpacity onPress={goBack} style={styles.backBtn}>
            <Ionicons name={selectedGenre || selectedSubgenre ? "arrow-back" : "close"} size={24} color={colors.text} />
          </TouchableOpacity>
          <View style={styles.headerTitle}>
            <Ionicons name="game-controller" size={24} color="#F59E0B" />
            <Text style={[styles.title, { color: colors.text }]}>Game Genres</Text>
          </View>
          <View style={{ width: 40 }} />
        </View>

        {isLoading ? (
          <ActivityIndicator size="large" color={colors.primary} style={styles.loader} />
        ) : projectResult ? (
          renderProjectResult()
        ) : showProjectForm ? (
          renderProjectForm()
        ) : selectedSubgenre ? (
          renderSubgenreDetails()
        ) : selectedGenre ? (
          renderGenreDetails()
        ) : (
          renderGenresList()
        )}
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingVertical: 14, borderBottomWidth: 1 },
  backBtn: { width: 40, height: 40, justifyContent: 'center', alignItems: 'center' },
  headerTitle: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  title: { fontSize: 18, fontWeight: '700' },
  loader: { flex: 1, justifyContent: 'center' },
  genresList: { flex: 1 },
  genresContent: { padding: 16, gap: 12 },
  sectionTitle: { fontSize: 13, fontWeight: '600', marginBottom: 12, textTransform: 'uppercase' },
  genreCard: { flexDirection: 'row', alignItems: 'center', padding: 16, borderRadius: 12, gap: 14 },
  genreIcon: { fontSize: 32 },
  genreInfo: { flex: 1 },
  genreName: { fontSize: 16, fontWeight: '700' },
  genreDesc: { fontSize: 13, marginTop: 2 },
  subgenreCount: { width: 32, height: 32, borderRadius: 16, justifyContent: 'center', alignItems: 'center' },
  subgenreCountText: { fontSize: 14, fontWeight: '700' },
  genreDetails: { flex: 1, padding: 16 },
  genreHeader: { padding: 20, borderRadius: 16, alignItems: 'center', marginBottom: 16 },
  genreDetailIcon: { fontSize: 48 },
  genreDetailName: { fontSize: 22, fontWeight: '800', marginTop: 12 },
  genreDetailDesc: { fontSize: 14, textAlign: 'center', marginTop: 8 },
  subgenreCard: { flexDirection: 'row', alignItems: 'center', padding: 16, borderRadius: 12, marginBottom: 8 },
  subgenreInfo: { flex: 1 },
  subgenreName: { fontSize: 15, fontWeight: '600' },
  subgenreExamples: { fontSize: 12, marginTop: 4 },
  subgenreDetails: { flex: 1, padding: 16 },
  subgenreHeader: { padding: 20, borderRadius: 16, marginBottom: 16 },
  subgenreDetailName: { fontSize: 20, fontWeight: '800' },
  examplesRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 12 },
  exampleTag: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 16 },
  exampleText: { fontSize: 12, fontWeight: '600' },
  section: { marginBottom: 20 },
  mechanicsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  mechanicTag: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 16 },
  mechanicText: { fontSize: 12, fontWeight: '600', textTransform: 'capitalize' },
  assetsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  assetTag: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 16 },
  assetText: { fontSize: 12, fontWeight: '600', textTransform: 'capitalize' },
  pipelinePhase: { padding: 16, borderRadius: 12, marginBottom: 12 },
  phaseName: { fontSize: 14, fontWeight: '700', textTransform: 'capitalize', marginBottom: 8 },
  phaseItem: { fontSize: 13, lineHeight: 22 },
  createProjectBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 16, borderRadius: 12, gap: 10, marginTop: 8 },
  createProjectText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
  projectForm: { flex: 1, padding: 16 },
  formHeader: { padding: 20, borderRadius: 16, alignItems: 'center', marginBottom: 20 },
  formTitle: { fontSize: 20, fontWeight: '800', marginTop: 12 },
  formSubtitle: { fontSize: 14, marginTop: 4 },
  inputLabel: { fontSize: 13, fontWeight: '600', marginBottom: 8, marginTop: 16 },
  textInput: { padding: 14, borderRadius: 12, borderWidth: 1 },
  createBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 16, borderRadius: 12, gap: 10, marginTop: 24 },
  createBtnText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
  projectResult: { flex: 1, padding: 16 },
  resultHeader: { padding: 20, borderRadius: 16, alignItems: 'center', marginBottom: 16 },
  resultTitle: { fontSize: 20, fontWeight: '800', marginTop: 12 },
  resultId: { fontSize: 12, marginTop: 4 },
  resultText: { fontSize: 14, lineHeight: 22 },
  aiSpec: { padding: 16, borderRadius: 12, marginTop: 16 },
  aiSpecTitle: { fontSize: 14, fontWeight: '700', marginBottom: 12 },
  aiSpecText: { fontSize: 13, lineHeight: 22 },
});
