import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Mic, MicOff } from 'lucide-react';

// States: idle, recording, thinking
const VoiceInput = ({ onSubmit, disabled = false, placeholder = "Type or speak..." }) => {
  const [micState, setMicState] = useState('idle'); // idle | recording | thinking
  const [inputText, setInputText] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const handleMicClick = async () => {
    if (micState === 'idle') {
      try {
        // Start recording
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current = [];
        
        mediaRecorderRef.current.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };
        
        mediaRecorderRef.current.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
          await onSubmit(null, audioBlob); // Send audio instead of text
          stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorderRef.current.start();
        setMicState('recording');
      } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Please allow microphone access to use voice input.');
      }
    } else if (micState === 'recording') {
      // Stop recording
      mediaRecorderRef.current.stop();
      setMicState('idle');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setMicState('thinking');
    
    try {
      await onSubmit(inputText, null);
      setInputText('');
    } catch (error) {
      console.error('Error submitting:', error);
    } finally {
      setMicState('idle');
    }
  };

  const getPlaceholder = () => {
    if (micState === 'recording') return 'Listening...';
    if (micState === 'thinking') return 'Macca is thinking...';
    return placeholder;
  };

  const getMicButtonClass = () => {
    const baseClass = "transition-all duration-300";
    if (micState === 'recording') {
      return `${baseClass} bg-red-500 hover:bg-red-600 animate-pulse`;
    }
    if (micState === 'thinking') {
      return `${baseClass} bg-slate-600 cursor-not-allowed`;
    }
    return `${baseClass} bg-cyan-500 hover:bg-cyan-600`;
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2">
      <Input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder={getPlaceholder()}
        disabled={disabled || micState === 'thinking'}
        className="flex-1 bg-slate-800 border-slate-700 text-slate-100 placeholder:text-slate-500 focus:border-cyan-500"
      />
      <Button
        type="button"
        onClick={handleMicClick}
        disabled={disabled || micState === 'thinking'}
        className={getMicButtonClass()}
        size="icon"
      >
        {micState === 'recording' ? (
          <MicOff className="h-4 w-4" />
        ) : (
          <Mic className="h-4 w-4" />
        )}
      </Button>
      <Button
        type="submit"
        disabled={disabled || !inputText.trim() || micState === 'thinking'}
        className="bg-cyan-500 hover:bg-cyan-600"
      >
        Send
      </Button>
    </form>
  );
};

export default VoiceInput;
