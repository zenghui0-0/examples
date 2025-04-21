import React, { useState, useRef, useEffect } from 'react';
import { View, TextInput, StyleSheet } from 'react-native';
import AISuggestions from '../AISuggestions/AISuggestions';
import EditorToolbar from './EditorToolbar';

const Editor = ({ initialContent, onSave }) => {
  const [content, setContent] = useState(initialContent || '');
  const [suggestions, setSuggestions] = useState([]);
  const inputRef = useRef(null);

  const handleTextChange = (text) => {
    setContent(text);
    analyzeForCompletion(text);
  };

  const analyzeForCompletion = debounce(async (text) => {
    if (text.length < 10) return;
    const lastSentence = extractLastSentence(text);
    const results = await fetchAISuggestions(lastSentence);
    setSuggestions(results);
  }, 500);

  const applySuggestion = (suggestion) => {
    const newText = `${content} ${suggestion}`;
    setContent(newText);
    setSuggestions([]);
  };

  return (
    <View style={styles.container}>
      <EditorToolbar onSave={() => onSave(content)} />
      <TextInput
        ref={inputRef}
        style={styles.input}
        multiline
        value={content}
        onChangeText={handleTextChange}
        placeholder="开始写作..."
      />
      <AISuggestions 
        suggestions={suggestions}
        onSelect={applySuggestion}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  input: { flex: 1, fontSize: 16, lineHeight: 24 }
});

export default Editor;
