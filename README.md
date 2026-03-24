# CodeDock - Ultimate Coding Platform v15.0

<div align="center">

![CodeDock Logo](https://img.shields.io/badge/CodeDock-v15.0-6366F1?style=for-the-badge&logo=code&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Expo](https://img.shields.io/badge/Expo-SDK_53-000020?style=for-the-badge&logo=expo&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

**The Ultimate AI-Powered Coding Education & Game Development Platform**

*Learn. Build. Create. Master.*

[Getting Started](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Vision

CodeDock is more than a coding platform—it's a **comprehensive learning ecosystem** that combines:

- **Intelligent AI Tutoring** with Jeeves, your personalized English butler AI companion
- **Game Development Pipelines** for creating NPCs, mechanics, and animations from natural language
- **Immersive Learning** with gamification, achievements, and managed learning curves
- **Co-Coding Mode** where Jeeves collaborates with you in real-time

Our mission is to make coding education **engaging, effective, and enjoyable** while providing professional-grade tools for game development.

---

## ✨ Features

### 🤖 Jeeves AI Tutor
- **20x Expanded Knowledge Base** - 2000+ concepts across 6 domains
- **3 System Law Blurbs** - 45,000 characters of pedagogical instruction
- **3 Self-Learning Matrices** - SAM, CLOM, KREM for optimal learning
- **Voice & Personality** - Young English butler persona with directional guidance
- **ChromaDB RAG** - Long-term memory for personalized tutoring

### 🎮 Text-to-X Pipelines
- **Text-to-NPC Pipeline** - Generate complete NPCs with personality, dialogue, AI behaviors
- **Text-to-Game-Logic Pipeline** - Create combat systems, economies, progression mechanics
- **Text-to-Animation Pipeline** - Generate skeletons, keyframes, blend trees, state machines

### 📚 Learning Systems
- **Immersive Tutor** - Zone of Proximal Development tracking, Socratic dialogue
- **Gamification** - XP, levels (50), achievements (15), daily quests, streak rewards
- **Multi-Layer Learning** - 6 redundant pathways, 1320+ hours of content
- **Managed Learning Curve** - 4 stages (Onboarding → Foundation → Growth → Mastery)

### 💻 IDE & Development
- **Multi-Language Support** - 70+ programming languages
- **AI Code Completion** - GPT-4o powered assistance
- **Live Preview** - Real-time code execution
- **Collaboration** - Real-time multi-user editing

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.10+
- MongoDB (local or Atlas)
- Expo CLI (`npm install -g expo-cli`)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/codedock.git
cd codedock
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install Frontend Dependencies**
```bash
cd ../frontend
yarn install
# or
npm install
```

4. **Environment Setup**

Create `.env` files in both `backend/` and `frontend/` directories:

**backend/.env**
```env
MONGO_URL=mongodb://localhost:27017/codedock
EMERGENT_LLM_KEY=your_key_here  # Optional for AI features
```

**frontend/.env**
```env
EXPO_PUBLIC_BACKEND_URL=http://localhost:8001
```

5. **Start the Backend**
```bash
cd backend
uvicorn server:app --reload --port 8001
```

6. **Start the Frontend**
```bash
cd frontend
npx expo start
```

### Quick Commands

```bash
# Backend
pip install -r backend/requirements.txt
cd backend && uvicorn server:app --reload --port 8001

# Frontend
cd frontend && npx expo start
```

---

## 🏗️ Architecture

```
codedock/
├── backend/                    # FastAPI Backend
│   ├── routes/
│   │   ├── npc_pipeline.py          # Text-to-NPC
│   │   ├── game_logic_pipeline.py   # Text-to-Game-Logic
│   │   ├── animation_pipeline.py    # Text-to-Animation
│   │   ├── jeeves_core.py           # Jeeves Core (Laws, Matrices, RAG)
│   │   ├── jeeves_synergy.py        # Learning Integration
│   │   ├── jeeves_hyperion.py       # 20x Knowledge Base
│   │   ├── jeeves_voice.py          # Voice & Personality
│   │   ├── immersive_tutor.py       # Gamification & ZPD
│   │   ├── learning_engine.py       # Multi-layer Learning
│   │   ├── synergy.py               # Session & Analytics
│   │   └── ... (40+ route files)
│   ├── services/
│   │   └── database.py              # MongoDB Service
│   ├── requirements.txt
│   └── server.py                    # FastAPI App
│
├── frontend/                   # Expo React Native
│   ├── app/
│   │   └── index.tsx               # Main App
│   ├── components/
│   │   ├── CodeEditor.tsx
│   │   ├── CommandPalette.tsx
│   │   └── AchievementNotification.tsx
│   ├── features/
│   │   ├── ImmersiveTutor/
│   │   ├── LearningHub/
│   │   └── Dashboard/
│   ├── store/
│   │   ├── appStore.ts
│   │   └── modalStore.ts
│   └── package.json
│
└── README.md
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | High-performance Python API framework |
| MongoDB | Document database for flexible schemas |
| Motor | Async MongoDB driver |
| ChromaDB | Vector database for RAG memory |
| Pydantic | Data validation and serialization |

### Frontend
| Technology | Purpose |
|------------|---------|
| Expo (SDK 53) | Cross-platform React Native framework |
| TypeScript | Type-safe JavaScript |
| Zustand | Lightweight state management |
| React Navigation | Native navigation |
| expo-haptics | Mobile haptic feedback |

### AI/ML
| Technology | Purpose |
|------------|---------|
| OpenAI GPT-4o | Code generation and tutoring |
| ChromaDB | Semantic search and RAG |
| Emergent LLM Key | Universal API access |

---

## 📖 API Documentation

### Core Pipelines

#### Text-to-NPC Pipeline
```bash
# Generate NPC from description
POST /api/npc-pipeline/generate
{
  "description": "A wise old wizard with a mysterious past",
  "include_dialogue": true,
  "include_quests": true
}
```

#### Text-to-Game-Logic Pipeline
```bash
# Generate combat system
POST /api/game-logic-pipeline/combat/generate
{
  "style": "turn_based",
  "include_magic": true,
  "party_based": true
}
```

#### Text-to-Animation Pipeline
```bash
# Generate skeleton
POST /api/animation-pipeline/rig/generate
{
  "description": "humanoid character",
  "include_fingers": true,
  "include_face_rig": true
}
```

### Jeeves Core
```bash
# Get system laws
GET /api/jeeves-core/system-laws/all

# Get self-learning matrices
GET /api/jeeves-core/matrices

# Start co-coding session
POST /api/jeeves-core/co-coding/session
{
  "user_id": "user_1",
  "pipeline": "npc",
  "initial_prompt": "Create a merchant NPC",
  "skill_level": "intermediate"
}

# Store memory
POST /api/jeeves-core/memory/store
{
  "memory_type": "learning_session",
  "content": "User learned about loops",
  "metadata": {"topic": "python", "duration": 30}
}
```

---

## 📸 Screenshots

### To Capture:

1. **Main IDE View**
   - Location: Homepage with code editor
   - Shows: Multi-language editor, AI panel, live preview

2. **Command Palette**
   - Location: Press the grid icon
   - Shows: All features organized by category

3. **Immersive Tutor Modal**
   - Location: Command Palette → Learn → Immersive Tutor
   - Shows: XP progress, daily quests, achievements, learning stages

4. **Jeeves AI Chat**
   - Location: Command Palette → Learn → Jeeves AI Tutor
   - Shows: Conversational tutoring interface

5. **Learning Hub**
   - Location: Command Palette → Learn → Learning Hub
   - Shows: 6-layer learning system, domain cards

6. **Dashboard**
   - Location: Command Palette → Tools → Dashboard
   - Shows: Analytics, progress charts, session history

7. **NPC Pipeline Output**
   - Location: API response or dedicated UI
   - Shows: Generated NPC with personality, dialogue tree, stats

---

## 🎬 Demo Video

### Sections to Record:

1. **Introduction** (30s)
   - Show CodeDock loading
   - Quick tour of the interface

2. **Jeeves Co-Coding** (2min)
   - Start a co-coding session
   - Show Jeeves helping write code
   - Demonstrate prompt refinement

3. **NPC Pipeline** (1min)
   - Enter natural language description
   - Show generated NPC with all components

4. **Learning Journey** (1.5min)
   - Show progression through stages
   - Complete a daily quest
   - Earn an achievement

5. **Multi-Language Coding** (1min)
   - Switch between languages
   - Show AI assistance in different contexts

---

## 🎓 Learning Stages

CodeDock implements a **managed learning curve** with four stages:

| Stage | Hours | Focus | Scaffolding |
|-------|-------|-------|-------------|
| 🌱 **Onboarding** | 0-5 | Confidence Building | Heavy |
| 🏗️ **Foundation** | 5-50 | Core Concepts | Moderate |
| 📈 **Growth** | 50-200 | Advanced Application | Light |
| 👑 **Mastery** | 200+ | Expertise | Minimal |

---

## 🧠 Jeeves System Laws

Jeeves operates under three comprehensive instruction blurbs:

### Blurb 1: Teaching Philosophy (15,000 chars)
- Zone of Proximal Development
- Constructivist Learning
- Metacognitive Development
- Mastery-Based Progression
- Emotional Intelligence

### Blurb 2: Co-Coding Protocol (15,000 chars)
- Collaborative Ownership
- Think-Aloud Protocol
- Graduated Handoff
- Error Embracing
- Prompt Refinement

### Blurb 3: Quality Standards (15,000 chars)
- Code Quality Standards
- Testing Requirements
- Documentation Standards
- Security Best Practices
- Architecture Principles

---

## 🔄 Self-Learning Matrices

### SAM - Skill Acquisition Matrix
Tracks and optimizes learner skill development across 10 domains.

### CLOM - Cognitive Load Optimization Matrix
Manages cognitive load to keep learners in the optimal zone (40-70%).

### KREM - Knowledge Retention & Evolution Matrix
Ensures maximal retention through spaced repetition and retrieval practice.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT-4o
- Expo team for the amazing framework
- FastAPI for the high-performance backend
- ChromaDB for vector search capabilities
- All contributors and learners using CodeDock

---

<div align="center">

**Built with ❤️ for learners everywhere**

[⬆ Back to Top](#codedock---ultimate-coding-platform-v150)

</div>
