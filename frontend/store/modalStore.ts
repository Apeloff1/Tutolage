/**
 * CodeDock Modal Management Store v12.0
 * 
 * Centralized modal state management using Zustand
 * Replaces 60+ useState hooks for modal visibility
 */

import { create } from 'zustand';

// All modals in the application
export type ModalType = 
  | 'language'
  | 'template'
  | 'files'
  | 'settings'
  | 'ai'
  | 'bible'
  | 'compiler'
  | 'pipeline'
  | 'learning'
  | 'collaboration'
  | 'hub'
  | 'aiSuggestions'
  | 'tutorial'
  | 'aiPipeline'
  | 'curriculum'
  | 'vault'
  | 'advanced'
  | 'codeToApp'
  | 'imagine'
  | 'debugger'
  | 'musicPipeline'
  | 'education'
  | 'jeeves'
  | 'masterclass'
  | 'assetPipeline'
  | 'gameGenres'
  | 'commandPalette'
  | 'multiAgent'
  | 'sota'
  | 'codeIntelligence'
  | 'liveCollab'
  | 'worldEngine'
  | 'narrative'
  | 'logicEngine'
  | 'physicsAcademy'
  | 'mathAcademy'
  | 'csAcademy'
  | 'hybridPipeline'
  | 'sotaExtended'
  | 'immersiveLearning'
  | 'readingCorner'
  | 'jeevesEQ'
  | 'exportGitHub'
  | 'aiInteractionsLog'
  | 'dashboard'
  | 'learningHub'
  | 'immersiveTutor'
  | null;

interface ModalState {
  activeModal: ModalType;
  modalHistory: ModalType[];
  modalData: Record<string, any>;
  
  // Actions
  openModal: (modal: ModalType, data?: any) => void;
  closeModal: () => void;
  closeAllModals: () => void;
  setModalData: (key: string, value: any) => void;
  getModalData: (key: string) => any;
  goBack: () => void;
}

export const useModalStore = create<ModalState>((set, get) => ({
  activeModal: null,
  modalHistory: [],
  modalData: {},
  
  openModal: (modal, data) => set((state) => {
    const newHistory = state.activeModal 
      ? [...state.modalHistory, state.activeModal]
      : state.modalHistory;
    return {
      activeModal: modal,
      modalHistory: newHistory.slice(-5), // Keep last 5 in history
      modalData: data ? { ...state.modalData, [modal || '']: data } : state.modalData,
    };
  }),
  
  closeModal: () => set((state) => ({
    activeModal: null,
    modalHistory: state.modalHistory,
  })),
  
  closeAllModals: () => set({
    activeModal: null,
    modalHistory: [],
    modalData: {},
  }),
  
  setModalData: (key, value) => set((state) => ({
    modalData: { ...state.modalData, [key]: value },
  })),
  
  getModalData: (key) => get().modalData[key],
  
  goBack: () => set((state) => {
    const newHistory = [...state.modalHistory];
    const previousModal = newHistory.pop() || null;
    return {
      activeModal: previousModal,
      modalHistory: newHistory,
    };
  }),
}));

// Selector hooks for common patterns
export const useActiveModal = () => useModalStore((state) => state.activeModal);
export const useModalActions = () => useModalStore((state) => ({
  openModal: state.openModal,
  closeModal: state.closeModal,
  closeAllModals: state.closeAllModals,
  goBack: state.goBack,
}));

export default useModalStore;
