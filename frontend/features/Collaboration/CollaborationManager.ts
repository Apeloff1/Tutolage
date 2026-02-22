// ============================================================================
// CODEDOCK QUANTUM NEXUS - Multiplayer Bridge Collaboration
// Real-time sessions with Y.js, WebRTC, color-coded cursors
// ============================================================================

import * as Y from 'yjs';
import { WebrtcProvider } from 'y-webrtc';
import { IndexeddbPersistence } from 'y-indexeddb';

// ============================================================================
// TYPES
// ============================================================================
export interface CollaboratorInfo {
  id: string;
  name: string;
  color: string;
  cursor?: CursorPosition;
  selection?: SelectionRange;
  isActive: boolean;
  joinedAt: Date;
}

export interface CursorPosition {
  line: number;
  column: number;
}

export interface SelectionRange {
  startLine: number;
  startColumn: number;
  endLine: number;
  endColumn: number;
}

export interface CollaborationSession {
  id: string;
  name: string;
  createdAt: Date;
  createdBy: string;
  participants: CollaboratorInfo[];
  maxParticipants: number;
  isPublic: boolean;
  code: string;
  language: string;
  chatMessages: ChatMessage[];
}

export interface ChatMessage {
  id: string;
  authorId: string;
  authorName: string;
  content: string;
  timestamp: Date;
  type: 'message' | 'system' | 'code-share';
}

export interface AwarenessState {
  user: CollaboratorInfo;
  cursor?: CursorPosition;
  selection?: SelectionRange;
}

// ============================================================================
// COLLABORATION COLORS
// ============================================================================
const COLLABORATOR_COLORS = [
  '#EF4444', // Red
  '#F59E0B', // Amber
  '#10B981', // Emerald
  '#3B82F6', // Blue
  '#8B5CF6', // Violet
  '#EC4899', // Pink
  '#06B6D4', // Cyan
  '#84CC16', // Lime
];

// ============================================================================
// COLLABORATION MANAGER CLASS
// ============================================================================
export class CollaborationManager {
  private doc: Y.Doc | null = null;
  private provider: WebrtcProvider | null = null;
  private persistence: IndexeddbPersistence | null = null;
  private awareness: any = null;
  
  private sessionId: string | null = null;
  private userId: string;
  private userName: string;
  private userColor: string;
  
  private codeText: Y.Text | null = null;
  private chatArray: Y.Array<ChatMessage> | null = null;
  private participantsMap: Y.Map<CollaboratorInfo> | null = null;
  
  private onCodeChangeCallbacks: ((code: string) => void)[] = [];
  private onParticipantChangeCallbacks: ((participants: CollaboratorInfo[]) => void)[] = [];
  private onChatMessageCallbacks: ((messages: ChatMessage[]) => void)[] = [];
  private onCursorChangeCallbacks: ((cursors: Map<string, CursorPosition>) => void)[] = [];

  constructor() {
    this.userId = this.generateUserId();
    this.userName = 'Anonymous';
    this.userColor = COLLABORATOR_COLORS[Math.floor(Math.random() * COLLABORATOR_COLORS.length)];
  }

  // ============================================================================
  // INITIALIZATION
  // ============================================================================
  private generateUserId(): string {
    return `user-${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 9)}`;
  }

  setUserInfo(name: string, color?: string): void {
    this.userName = name;
    if (color) this.userColor = color;
    this.updateAwareness();
  }

  // ============================================================================
  // SESSION MANAGEMENT
  // ============================================================================
  async createSession(name: string, initialCode: string = '', language: string = 'python'): Promise<string> {
    const sessionId = `codedock-${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 6)}`;
    await this.joinSession(sessionId, name, initialCode, language);
    return sessionId;
  }

  async joinSession(
    sessionId: string, 
    sessionName?: string, 
    initialCode?: string,
    language?: string
  ): Promise<void> {
    // Clean up existing session
    await this.leaveSession();

    this.sessionId = sessionId;
    this.doc = new Y.Doc();

    // Initialize shared types
    this.codeText = this.doc.getText('code');
    this.chatArray = this.doc.getArray('chat');
    this.participantsMap = this.doc.getMap('participants');

    // Set initial code if this is a new session
    if (initialCode && this.codeText.length === 0) {
      this.codeText.insert(0, initialCode);
    }

    // Setup IndexedDB persistence
    this.persistence = new IndexeddbPersistence(sessionId, this.doc);
    
    await new Promise<void>((resolve) => {
      this.persistence!.once('synced', () => {
        console.log('IndexedDB synced');
        resolve();
      });
    });

    // Setup WebRTC provider for real-time sync
    this.provider = new WebrtcProvider(sessionId, this.doc, {
      signaling: ['wss://signaling.yjs.dev', 'wss://y-webrtc-signaling-eu.herokuapp.com'],
      password: null,
      awareness: undefined,
      maxConns: 8,
      filterBcConns: true,
      peerOpts: {},
    });

    this.awareness = this.provider.awareness;

    // Set local awareness state
    this.updateAwareness();

    // Listen for changes
    this.setupListeners();

    // Add self to participants
    this.participantsMap.set(this.userId, {
      id: this.userId,
      name: this.userName,
      color: this.userColor,
      isActive: true,
      joinedAt: new Date(),
    });

    console.log(`Joined session: ${sessionId}`);
  }

  async leaveSession(): Promise<void> {
    if (this.participantsMap) {
      this.participantsMap.delete(this.userId);
    }

    if (this.provider) {
      this.provider.destroy();
      this.provider = null;
    }

    if (this.persistence) {
      await this.persistence.destroy();
      this.persistence = null;
    }

    if (this.doc) {
      this.doc.destroy();
      this.doc = null;
    }

    this.codeText = null;
    this.chatArray = null;
    this.participantsMap = null;
    this.awareness = null;
    this.sessionId = null;
  }

  // ============================================================================
  // AWARENESS
  // ============================================================================
  private updateAwareness(): void {
    if (!this.awareness) return;

    const state: AwarenessState = {
      user: {
        id: this.userId,
        name: this.userName,
        color: this.userColor,
        isActive: true,
        joinedAt: new Date(),
      },
    };

    this.awareness.setLocalState(state);
  }

  updateCursor(position: CursorPosition): void {
    if (!this.awareness) return;

    const currentState = this.awareness.getLocalState() || {};
    this.awareness.setLocalState({
      ...currentState,
      cursor: position,
    });
  }

  updateSelection(selection: SelectionRange | null): void {
    if (!this.awareness) return;

    const currentState = this.awareness.getLocalState() || {};
    this.awareness.setLocalState({
      ...currentState,
      selection,
    });
  }

  // ============================================================================
  // LISTENERS
  // ============================================================================
  private setupListeners(): void {
    // Code changes
    if (this.codeText) {
      this.codeText.observe((event) => {
        const code = this.codeText?.toString() || '';
        this.onCodeChangeCallbacks.forEach(cb => cb(code));
      });
    }

    // Chat messages
    if (this.chatArray) {
      this.chatArray.observe((event) => {
        const messages = this.chatArray?.toArray() || [];
        this.onChatMessageCallbacks.forEach(cb => cb(messages));
      });
    }

    // Participants
    if (this.participantsMap) {
      this.participantsMap.observe((event) => {
        const participants = Array.from(this.participantsMap?.values() || []);
        this.onParticipantChangeCallbacks.forEach(cb => cb(participants));
      });
    }

    // Awareness (cursors)
    if (this.awareness) {
      this.awareness.on('change', () => {
        const states = this.awareness.getStates();
        const cursors = new Map<string, CursorPosition>();
        
        states.forEach((state: AwarenessState, clientId: number) => {
          if (state.cursor && state.user && state.user.id !== this.userId) {
            cursors.set(state.user.id, state.cursor);
          }
        });
        
        this.onCursorChangeCallbacks.forEach(cb => cb(cursors));
      });
    }
  }

  // ============================================================================
  // CODE OPERATIONS
  // ============================================================================
  getCode(): string {
    return this.codeText?.toString() || '';
  }

  setCode(code: string): void {
    if (!this.codeText || !this.doc) return;

    this.doc.transact(() => {
      this.codeText!.delete(0, this.codeText!.length);
      this.codeText!.insert(0, code);
    });
  }

  insertText(index: number, text: string): void {
    if (!this.codeText) return;
    this.codeText.insert(index, text);
  }

  deleteText(index: number, length: number): void {
    if (!this.codeText) return;
    this.codeText.delete(index, length);
  }

  // ============================================================================
  // CHAT OPERATIONS
  // ============================================================================
  sendMessage(content: string, type: ChatMessage['type'] = 'message'): void {
    if (!this.chatArray) return;

    const message: ChatMessage = {
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      authorId: this.userId,
      authorName: this.userName,
      content,
      timestamp: new Date(),
      type,
    };

    this.chatArray.push([message]);
  }

  getMessages(): ChatMessage[] {
    return this.chatArray?.toArray() || [];
  }

  // ============================================================================
  // PARTICIPANT OPERATIONS
  // ============================================================================
  getParticipants(): CollaboratorInfo[] {
    if (!this.participantsMap) return [];
    return Array.from(this.participantsMap.values());
  }

  getParticipantCount(): number {
    return this.participantsMap?.size || 0;
  }

  // ============================================================================
  // CALLBACKS
  // ============================================================================
  onCodeChange(callback: (code: string) => void): () => void {
    this.onCodeChangeCallbacks.push(callback);
    return () => {
      this.onCodeChangeCallbacks = this.onCodeChangeCallbacks.filter(cb => cb !== callback);
    };
  }

  onParticipantChange(callback: (participants: CollaboratorInfo[]) => void): () => void {
    this.onParticipantChangeCallbacks.push(callback);
    return () => {
      this.onParticipantChangeCallbacks = this.onParticipantChangeCallbacks.filter(cb => cb !== callback);
    };
  }

  onChatMessage(callback: (messages: ChatMessage[]) => void): () => void {
    this.onChatMessageCallbacks.push(callback);
    return () => {
      this.onChatMessageCallbacks = this.onChatMessageCallbacks.filter(cb => cb !== callback);
    };
  }

  onCursorChange(callback: (cursors: Map<string, CursorPosition>) => void): () => void {
    this.onCursorChangeCallbacks.push(callback);
    return () => {
      this.onCursorChangeCallbacks = this.onCursorChangeCallbacks.filter(cb => cb !== callback);
    };
  }

  // ============================================================================
  // STATUS
  // ============================================================================
  isConnected(): boolean {
    return !!this.provider && this.provider.connected;
  }

  getSessionId(): string | null {
    return this.sessionId;
  }

  getUserId(): string {
    return this.userId;
  }

  getUserColor(): string {
    return this.userColor;
  }
}

// ============================================================================
// SINGLETON
// ============================================================================
export const collaborationManager = new CollaborationManager();

export default collaborationManager;
