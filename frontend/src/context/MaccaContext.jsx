import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || '';
const API = BACKEND_URL ? `${BACKEND_URL}/api` : '/api';

const MaccaContext = createContext();

export const useMacca = () => {
  const context = useContext(MaccaContext);
  if (!context) {
    throw new Error('useMacca must be used within MaccaProvider');
  }
  return context;
};

export const MaccaProvider = ({ children }) => {
  const [userProfile, setUserProfile] = useState({
    id: '',
    name: 'User',
    level: 'B1',
    goal: 'Job interview',
    explanation_language: 'id'
  });
  const [loading, setLoading] = useState(true);

  // Fetch user profile on mount
  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get(`${API}/user/profile`);
      setUserProfile(response.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateUserProfile = async (updates) => {
    try {
      const response = await axios.patch(`${API}/user/profile`, updates);
      setUserProfile(response.data);
      return response.data;
    } catch (error) {
      console.error('Error updating user profile:', error);
      throw error;
    }
  };

  const sendConversationTurn = async (userText, mode, audioBlob = null) => {
    try {
      if (audioBlob) {
        // Send audio
        console.log('Sending audio blob:', audioBlob.size, 'bytes, type:', audioBlob.type);
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        formData.append('mode', mode);
        
        console.log('Posting to:', `${API}/session/turn/audio`);
        const response = await axios.post(`${API}/session/turn/audio`, formData);
        console.log('Audio response received:', response.data);
        return response.data;
      } else {
        // Send text
        console.log('Posting text to:', `${API}/session/turn`);
        const response = await axios.post(`${API}/session/turn`, {
          user_text: userText,
          mode: mode
        });
        return response.data;
      }
    } catch (error) {
      console.error('Error sending conversation turn:', error);
      console.error('Error details:', error.response?.data);
      throw error;
    }
  };

  const analyzePronunciation = async (word, audioBlob = null) => {
    try {
      if (audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        formData.append('word', word);
        
        const response = await axios.post(`${API}/pronunciation/analyze/audio`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
      } else {
        const response = await axios.post(`${API}/pronunciation/analyze`, {
          word: word
        });
        return response.data;
      }
    } catch (error) {
      console.error('Error analyzing pronunciation:', error);
      throw error;
    }
  };

  const getLessons = async () => {
    try {
      const response = await axios.get(`${API}/lessons`);
      return response.data;
    } catch (error) {
      console.error('Error fetching lessons:', error);
      return [];
    }
  };

  const getLesson = async (lessonId) => {
    try {
      const response = await axios.get(`${API}/lessons/${lessonId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching lesson:', error);
      throw error;
    }
  };

  const value = {
    userProfile,
    loading,
    updateUserProfile,
    sendConversationTurn,
    analyzePronunciation,
    getLessons,
    getLesson
  };

  return <MaccaContext.Provider value={value}>{children}</MaccaContext.Provider>;
};
