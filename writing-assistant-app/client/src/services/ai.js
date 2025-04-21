import axios from 'axios';

const API_BASE = process.env.CLIENT_AI_BASE || 'http://localhost:8000';

export const fetchAISuggestions = async (text) => {
  try {
    const response = await axios.post(`${API_BASE}/api/ai/complete`, {
      text,
      max_length: 50,
      creativity: 0.7
    });
    return response.data.suggestions;
  } catch (error) {
    console.error('AI请求失败:', error);
    return [];
  }
};

export const expandText = async (text, mode = 'detailed') => {
  const response = await axios.post(`${API_BASE}/api/ai/expand`, {
    text,
    mode
  });
  return response.data.expanded;
};
