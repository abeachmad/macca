import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

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

  const sendConversationTurn = async (userText, mode) => {
    try {
      const response = await axios.post(`${API}/session/turn`, {
        user_text: userText,
        mode: mode
      });
      return response.data;
    } catch (error) {
      console.error('Error sending conversation turn:', error);
      throw error;
    }
  };

  const analyzePronunciation = async (word) => {
    try {
      const response = await axios.post(`${API}/pronunciation/analyze`, {
        word: word
      });
      return response.data;
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
