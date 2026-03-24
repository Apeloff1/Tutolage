/**
 * Command Palette v11.3.0
 * Unified access to all CodeDock features with clean, organized UI
 */

import React, { useState, useEffect } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput,
  Modal, Dimensions, Animated,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface CommandPaletteProps {
  visible: boolean;
  onClose: () => void;
  onSelectAction: (action: string) => void;
  colors: any;
}

interface FeatureCategory {
  id: string;
  name: string;
  icon: string;
  color: string;
  features: Feature[];
}

interface Feature {
  id: string;
  name: string;
  icon: string;
  description: string;
  shortcut?: string;
}

const FEATURE_CATEGORIES: FeatureCategory[] = [
  {
    id: 'code',
    name: 'Code',
    icon: 'code-slash',
    color: '#3B82F6',
    features: [
      { id: 'run', name: 'Run Code', icon: 'play', description: 'Execute current code', shortcut: '⌘R' },
      { id: 'compile', name: 'Compile', icon: 'build', description: 'Compile and check errors', shortcut: '⌘B' },
      { id: 'format', name: 'Format', icon: 'code-working', description: 'Auto-format code' },
      { id: 'hub', name: 'CodeHub', icon: 'cloud', description: 'Cloud code library' },
    ]
  },
  {
    id: 'ai',
    name: 'AI Tools',
    icon: 'sparkles',
    color: '#8B5CF6',
    features: [
      { id: 'ai_pipeline', name: 'AI Generate', icon: 'flash', description: 'Text-to-code generation' },
      { id: 'debugger', name: 'AI Debug', icon: 'bug', description: 'Autonomous debugging' },
      { id: 'code_to_app', name: 'Code to App', icon: 'apps', description: 'Generate full apps' },
      { id: 'imagine', name: 'Imagine', icon: 'image', description: 'AI image generation' },
      { id: 'multi_agent', name: 'Multi-Agent', icon: 'people', description: 'Agent swarm systems' },
      { id: 'sota', name: 'SOTA 2026', icon: 'rocket', description: 'Predictive AI & Auto-refactor' },
      { id: 'sota_extended', name: 'SOTA Extended', icon: 'flash', description: '15+ bleeding edge upgrades' },
    ]
  },
  {
    id: 'academy',
    name: 'Academy',
    icon: 'school',
    color: '#EC4899',
    features: [
      { id: 'reading_corner', name: 'Reading Corner', icon: 'library', description: '1600+ hours • Full-stack library' },
      { id: 'learning_hub', name: 'Learning Hub', icon: 'rocket', description: '6-layer redundant learning • 1320hrs' },
      { id: 'immersive_tutor', name: 'Immersive Tutor', icon: 'school', description: 'Jeeves Synergy • Gamification • ZPD' },
      { id: 'jeeves_eq', name: 'Jeeves EQ', icon: 'heart', description: 'Emotional Intelligence Dashboard' },
      { id: 'physics_academy', name: 'Physics', icon: 'nuclear', description: '315hrs • Mechanics, collisions, fluids' },
      { id: 'math_academy', name: 'Mathematics', icon: 'calculator', description: '340hrs • Linear algebra, calculus, noise' },
      { id: 'cs_academy', name: 'Computer Science', icon: 'code-slash', description: '600hrs • Data structures, graphics, AI' },
      { id: 'jeeves', name: 'Jeeves AI Tutor', icon: 'chatbubbles', description: '1255hr knowledge base' },
    ]
  },
  {
    id: 'learn',
    name: 'Learn',
    icon: 'book',
    color: '#10B981',
    features: [
      { id: 'masterclass', name: 'Masterclass', icon: 'school', description: '2860+ hours of courses' },
      { id: 'education', name: 'Challenges', icon: 'game-controller', description: 'Coding challenges' },
      { id: 'curriculum', name: 'Curriculum', icon: 'library', description: 'CS Bible & courses' },
    ]
  },
  {
    id: 'create',
    name: 'Create',
    icon: 'create',
    color: '#F59E0B',
    features: [
      { id: 'hybrid_pipeline', name: 'Hybrid Pipeline', icon: 'rocket', description: 'Complete game from text' },
      { id: 'world_engine', name: 'World Engine', icon: 'globe', description: 'Text-to-Environment' },
      { id: 'narrative', name: 'Narrative', icon: 'book', description: 'Stories, quests, dialogue' },
      { id: 'logic_engine', name: 'Logic Engine', icon: 'code-working', description: 'Mechanics & AI behavior' },
      { id: 'assets', name: 'Asset Pipeline', icon: 'cube', description: '2D sprites & 3D models' },
      { id: 'games', name: 'Game Builder', icon: 'game-controller', description: '11 genres, full pipeline' },
      { id: 'music', name: 'Music Studio', icon: 'musical-notes', description: 'Game audio generation' },
    ]
  },
  {
    id: 'tools',
    name: 'Pro Tools',
    icon: 'construct',
    color: '#EF4444',
    features: [
      { id: 'advanced', name: 'Advanced Tools', icon: 'analytics', description: 'Benchmark, verify, starlog' },
      { id: 'vault', name: 'Vault', icon: 'filing', description: 'Save code & assets' },
      { id: 'export_github', name: 'Export & GitHub', icon: 'git-branch', description: 'PDF, GitHub push/pull' },
      { id: 'collab', name: 'Live Collab', icon: 'people-circle', description: 'AI Pair programming' },
      { id: 'intelligence', name: 'Code Intel', icon: 'bulb', description: 'Auto-docs, tests, review' },
      { id: 'ai_interactions_log', name: 'AI Interactions Log', icon: 'document-text', description: 'Direct-to-Jeeves AI history' },
      { id: 'dashboard', name: 'Dashboard', icon: 'stats-chart', description: 'Analytics & progress tracking' },
    ]
  },
];

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  visible, onClose, onSelectAction, colors
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [filteredFeatures, setFilteredFeatures] = useState<Feature[]>([]);

  useEffect(() => {
    if (searchQuery.trim()) {
      const allFeatures = FEATURE_CATEGORIES.flatMap(cat => 
        cat.features.map(f => ({ ...f, categoryColor: cat.color }))
      );
      const filtered = allFeatures.filter(f => 
        f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        f.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredFeatures(filtered);
      setSelectedCategory(null);
    } else {
      setFilteredFeatures([]);
    }
  }, [searchQuery]);

  const handleFeatureSelect = (featureId: string) => {
    onSelectAction(featureId);
    setSearchQuery('');
    setSelectedCategory(null);
  };

  const renderCategories = () => (
    <View style={styles.categoriesGrid}>
      {FEATURE_CATEGORIES.map(category => (
        <TouchableOpacity
          key={category.id}
          style={[styles.categoryCard, { backgroundColor: category.color + '15' }]}
          onPress={() => setSelectedCategory(category.id)}
        >
          <View style={[styles.categoryIcon, { backgroundColor: category.color + '25' }]}>
            <Ionicons name={category.icon as any} size={24} color={category.color} />
          </View>
          <Text style={[styles.categoryName, { color: colors.text }]}>{category.name}</Text>
          <Text style={[styles.categoryCount, { color: colors.textMuted }]}>
            {category.features.length} features
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderCategoryFeatures = () => {
    const category = FEATURE_CATEGORIES.find(c => c.id === selectedCategory);
    if (!category) return null;

    return (
      <View style={styles.featuresList}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => setSelectedCategory(null)}
        >
          <Ionicons name="arrow-back" size={20} color={colors.text} />
          <Text style={[styles.backText, { color: colors.text }]}>Back</Text>
        </TouchableOpacity>
        
        <View style={[styles.categoryHeader, { backgroundColor: category.color + '15' }]}>
          <Ionicons name={category.icon as any} size={28} color={category.color} />
          <Text style={[styles.categoryTitle, { color: colors.text }]}>{category.name}</Text>
        </View>

        {category.features.map(feature => (
          <TouchableOpacity
            key={feature.id}
            style={[styles.featureRow, { backgroundColor: colors.surfaceAlt }]}
            onPress={() => handleFeatureSelect(feature.id)}
          >
            <View style={[styles.featureIcon, { backgroundColor: category.color + '20' }]}>
              <Ionicons name={feature.icon as any} size={20} color={category.color} />
            </View>
            <View style={styles.featureInfo}>
              <Text style={[styles.featureName, { color: colors.text }]}>{feature.name}</Text>
              <Text style={[styles.featureDesc, { color: colors.textMuted }]}>{feature.description}</Text>
            </View>
            {feature.shortcut && (
              <View style={[styles.shortcutBadge, { backgroundColor: colors.surface }]}>
                <Text style={[styles.shortcutText, { color: colors.textMuted }]}>{feature.shortcut}</Text>
              </View>
            )}
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  const renderSearchResults = () => (
    <View style={styles.searchResults}>
      <Text style={[styles.searchResultsTitle, { color: colors.textMuted }]}>
        {filteredFeatures.length} result{filteredFeatures.length !== 1 ? 's' : ''}
      </Text>
      {filteredFeatures.map((feature: any) => (
        <TouchableOpacity
          key={feature.id}
          style={[styles.featureRow, { backgroundColor: colors.surfaceAlt }]}
          onPress={() => handleFeatureSelect(feature.id)}
        >
          <View style={[styles.featureIcon, { backgroundColor: (feature.categoryColor || colors.primary) + '20' }]}>
            <Ionicons name={feature.icon as any} size={20} color={feature.categoryColor || colors.primary} />
          </View>
          <View style={styles.featureInfo}>
            <Text style={[styles.featureName, { color: colors.text }]}>{feature.name}</Text>
            <Text style={[styles.featureDesc, { color: colors.textMuted }]}>{feature.description}</Text>
          </View>
        </TouchableOpacity>
      ))}
    </View>
  );

  return (
    <Modal
      visible={visible}
      animationType="fade"
      transparent
      onRequestClose={onClose}
    >
      <TouchableOpacity 
        style={styles.overlay} 
        activeOpacity={1} 
        onPress={onClose}
      >
        <TouchableOpacity 
          activeOpacity={1} 
          style={[styles.palette, { backgroundColor: colors.surface }]}
        >
          {/* Search Bar */}
          <View style={[styles.searchContainer, { borderBottomColor: colors.border }]}>
            <Ionicons name="search" size={20} color={colors.textMuted} />
            <TextInput
              style={[styles.searchInput, { color: colors.text }]}
              placeholder="Search features..."
              placeholderTextColor={colors.textMuted}
              value={searchQuery}
              onChangeText={setSearchQuery}
              autoFocus
            />
            {searchQuery ? (
              <TouchableOpacity onPress={() => setSearchQuery('')}>
                <Ionicons name="close-circle" size={20} color={colors.textMuted} />
              </TouchableOpacity>
            ) : null}
          </View>

          {/* Content */}
          <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
            {searchQuery.trim() ? (
              renderSearchResults()
            ) : selectedCategory ? (
              renderCategoryFeatures()
            ) : (
              renderCategories()
            )}
          </ScrollView>

          {/* Footer */}
          <View style={[styles.footer, { borderTopColor: colors.border }]}>
            <Text style={[styles.footerText, { color: colors.textMuted }]}>
              Press ESC to close • Type to search
            </Text>
          </View>
        </TouchableOpacity>
      </TouchableOpacity>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  palette: {
    width: '100%',
    maxWidth: 500,
    maxHeight: SCREEN_HEIGHT * 0.75,
    borderRadius: 16,
    overflow: 'hidden',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
    gap: 12,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    padding: 0,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  categoryCard: {
    width: (SCREEN_WIDTH - 76) / 2,
    maxWidth: 220,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  categoryIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  categoryName: {
    fontSize: 15,
    fontWeight: '700',
  },
  categoryCount: {
    fontSize: 12,
    marginTop: 4,
  },
  featuresList: {
    gap: 8,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 8,
    marginBottom: 8,
  },
  backText: {
    fontSize: 14,
    fontWeight: '600',
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  categoryTitle: {
    fontSize: 20,
    fontWeight: '800',
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderRadius: 10,
    gap: 12,
  },
  featureIcon: {
    width: 40,
    height: 40,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureInfo: {
    flex: 1,
  },
  featureName: {
    fontSize: 15,
    fontWeight: '600',
  },
  featureDesc: {
    fontSize: 12,
    marginTop: 2,
  },
  shortcutBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  shortcutText: {
    fontSize: 11,
    fontFamily: 'monospace',
  },
  searchResults: {
    gap: 8,
  },
  searchResultsTitle: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  footer: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderTopWidth: 1,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
  },
});
