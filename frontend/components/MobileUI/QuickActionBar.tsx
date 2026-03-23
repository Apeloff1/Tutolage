/**
 * QuickActionBar Component v11.4
 * Clean, minimal action bar with power-aware animations
 */

import React, { memo, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';

interface QuickAction {
  id: string;
  icon: keyof typeof Ionicons.glyphMap;
  label?: string;
  color: string;
  badge?: string | number;
  onPress: () => void;
}

interface QuickActionBarProps {
  primaryAction: QuickAction;
  secondaryActions: QuickAction[];
  colors: any;
  reduceAnimations?: boolean;
}

export const QuickActionBar = memo(function QuickActionBar({
  primaryAction,
  secondaryActions,
  colors,
  reduceAnimations = false,
}: QuickActionBarProps) {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (reduceAnimations) return;

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
  }, [reduceAnimations, pulseAnim]);

  const handlePress = (action: QuickAction) => {
    if (Platform.OS === 'ios') {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light).catch(() => {});
    }
    action.onPress();
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.surface }]}>
      {/* Primary Action (AI) */}
      <Animated.View style={[styles.primaryWrapper, !reduceAnimations && { transform: [{ scale: pulseAnim }] }]}>
        <TouchableOpacity
          style={[
            styles.primaryButton,
            { backgroundColor: primaryAction.color + '15', borderColor: primaryAction.color + '40' }
          ]}
          onPress={() => handlePress(primaryAction)}
          activeOpacity={0.7}
        >
          <Ionicons name={primaryAction.icon} size={20} color={primaryAction.color} />
          {primaryAction.label && (
            <Text style={[styles.primaryLabel, { color: primaryAction.color }]}>
              {primaryAction.label}
            </Text>
          )}
          {primaryAction.badge && (
            <View style={[styles.badge, { backgroundColor: primaryAction.color }]}>
              <Text style={styles.badgeText}>{primaryAction.badge}</Text>
            </View>
          )}
        </TouchableOpacity>
      </Animated.View>

      {/* Secondary Actions */}
      <View style={styles.secondaryContainer}>
        {secondaryActions.map((action) => (
          <TouchableOpacity
            key={action.id}
            style={[styles.secondaryButton, { backgroundColor: action.color + '15' }]}
            onPress={() => handlePress(action)}
            activeOpacity={0.7}
          >
            <Ionicons name={action.icon} size={18} color={action.color} />
            {action.badge && (
              <View style={[styles.miniBadge, { backgroundColor: action.color }]}>
                <Text style={styles.miniBadgeText}>{action.badge}</Text>
              </View>
            )}
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    gap: 12,
  },
  primaryWrapper: {
    flex: 1,
  },
  primaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    borderWidth: 1.5,
    gap: 8,
  },
  primaryLabel: {
    fontSize: 15,
    fontWeight: '700',
  },
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    marginLeft: 4,
  },
  badgeText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: '700',
  },
  secondaryContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  secondaryButton: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  miniBadge: {
    position: 'absolute',
    top: -4,
    right: -4,
    minWidth: 16,
    height: 16,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 4,
  },
  miniBadgeText: {
    color: '#FFFFFF',
    fontSize: 9,
    fontWeight: '700',
  },
});
