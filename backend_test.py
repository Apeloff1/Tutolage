#!/usr/bin/env python3
"""
CodeDock Synergy Integration API Testing Suite
Tests the new v12.0 Synergy Integration endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Base URL from the review request
BASE_URL = "https://sota-2026.preview.emergentagent.com"

def test_unified_context():
    """Test POST /api/synergy/context - Get unified user context"""
    print("🔍 Testing GET unified context...")
    
    url = f"{BASE_URL}/api/synergy/context"
    payload = {
        "user_id": "test_user",
        "include_recommendations": True,
        "include_insights": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: User context retrieved")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            
            # Check context structure
            context = data.get('context', {})
            if 'learning' in context and 'emotional' in context:
                print(f"   Learning modules completed: {context['learning'].get('modules_completed', 0)}")
                print(f"   Current emotional state: {context['emotional'].get('current_state', 'unknown')}")
            
            # Check recommendations
            if 'recommendations' in data:
                print(f"   Recommendations included: {len(data['recommendations'])} items")
            
            # Check insights
            if 'insights' in data:
                insights = data['insights']
                print(f"   Total AI interactions: {insights.get('total_ai_interactions', 0)}")
                print(f"   Interactions this week: {insights.get('interactions_this_week', 0)}")
                print(f"   Learning velocity: {insights.get('learning_velocity', 0)}")
                print(f"   Engagement trend: {insights.get('engagement_trend', 'unknown')}")
            
            return True
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_session_start():
    """Test POST /api/synergy/session/start - Start learning session"""
    print("🚀 Testing session start...")
    
    url = f"{BASE_URL}/api/synergy/session/start"
    payload = {
        "user_id": "test_user",
        "module_id": "gp_001",
        "session_type": "reading"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: Session started")
            print(f"   Session started: {data.get('session_started')}")
            print(f"   Module ID: {data.get('module_id')}")
            
            # Check emotional context
            emotional_context = data.get('emotional_context', {})
            print(f"   Detected emotion: {emotional_context.get('detected_emotion', 'unknown')}")
            print(f"   Stress level: {emotional_context.get('stress_level', 0)}")
            
            # Check adaptations
            adaptations = data.get('content_adaptations', [])
            print(f"   Content adaptations: {len(adaptations)} items")
            if adaptations:
                print(f"   Adaptations: {', '.join(adaptations)}")
            
            # Check recommendations
            print(f"   Recommended session length: {data.get('recommended_session_length', 0)} minutes")
            
            tips = data.get('tips', [])
            if tips:
                print(f"   Tips provided: {len(tips)} tips")
                print(f"   First tip: {tips[0][:50]}...")
            
            return True
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_session_update():
    """Test POST /api/synergy/session/update - Update session progress"""
    print("📈 Testing session update (progress tracking)...")
    
    url = f"{BASE_URL}/api/synergy/session/update"
    payload = {
        "user_id": "test_user",
        "module_id": "gp_001",
        "progress": 50.0,
        "time_spent_seconds": 300
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: Progress updated")
            print(f"   Progress updated: {data.get('progress_updated')}")
            print(f"   Current progress: {data.get('current_progress')}%")
            print(f"   XP earned: {data.get('xp_earned', 0)}")
            
            # Check achievements
            achievements = data.get('new_achievements', [])
            if achievements:
                print(f"   New achievements: {len(achievements)} unlocked")
                for achievement in achievements:
                    print(f"     - {achievement.get('name', 'Unknown')} (+{achievement.get('xp', 0)} XP)")
            else:
                print(f"   No new achievements unlocked")
            
            return True
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_ai_interaction_logging():
    """Test POST /api/synergy/ai/log - Log AI interaction"""
    print("🤖 Testing AI interaction logging...")
    
    url = f"{BASE_URL}/api/synergy/ai/log"
    payload = {
        "user_id": "test_user",
        "interaction_type": "code_generation",
        "prompt": "Create a function to reverse a string",
        "response": "def reverse_string(s): return s[::-1]"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: AI interaction logged")
            print(f"   Logged: {data.get('logged')}")
            print(f"   Interaction ID: {data.get('interaction_id', 'N/A')}")
            print(f"   Pattern updated: {data.get('pattern_updated')}")
            
            return True
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_unified_dashboard():
    """Test POST /api/synergy/dashboard - Get unified dashboard"""
    print("📊 Testing unified dashboard...")
    
    url = f"{BASE_URL}/api/synergy/dashboard"
    payload = {
        "user_id": "test_user",
        "time_range_days": 7
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: Dashboard data retrieved")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Period: {data.get('period')}")
            
            # Check learning data
            learning = data.get('learning', {})
            print(f"   Learning - Study minutes: {learning.get('total_study_minutes', 0)}")
            print(f"   Learning - Modules completed: {learning.get('modules_completed', 0)}")
            print(f"   Learning - Current streak: {learning.get('current_streak', 0)} days")
            print(f"   Learning - XP earned: {learning.get('xp_earned', 0)}")
            
            # Check AI usage
            ai_usage = data.get('ai_usage', {})
            print(f"   AI Usage - Total interactions: {ai_usage.get('total_interactions', 0)}")
            print(f"   AI Usage - Average per day: {ai_usage.get('avg_per_day', 0):.1f}")
            
            by_type = ai_usage.get('by_type', {})
            if by_type:
                print(f"   AI Usage by type:")
                for interaction_type, count in by_type.items():
                    print(f"     - {interaction_type}: {count}")
            
            # Check emotional wellness
            emotional = data.get('emotional_wellness', {})
            print(f"   Emotional - Current state: {emotional.get('current_state', 'unknown')}")
            print(f"   Emotional - Avg stress level: {emotional.get('avg_stress_level', 0):.1f}")
            print(f"   Emotional - Pomodoro sessions: {emotional.get('pomodoro_sessions', 0)}")
            
            # Check recommendations
            recommendations = data.get('recommendations', [])
            print(f"   Recommendations: {len(recommendations)} items")
            
            return True
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    """Run all synergy integration tests"""
    print("=" * 80)
    print("🧪 CODEDOCK SYNERGY INTEGRATION API TESTING SUITE")
    print("=" * 80)
    print(f"Base URL: {BASE_URL}")
    print(f"Test started at: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Unified Context", test_unified_context),
        ("Session Start", test_session_start),
        ("Session Update", test_session_update),
        ("AI Interaction Logging", test_ai_interaction_logging),
        ("Unified Dashboard", test_unified_dashboard),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 Running {test_name} test...")
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"   Result: {'✅ PASSED' if success else '❌ FAILED'}")
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    print()
    print(f"📈 OVERALL RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL SYNERGY INTEGRATION TESTS PASSED!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - CHECK LOGS ABOVE")
        return 1

if __name__ == "__main__":
    sys.exit(main())