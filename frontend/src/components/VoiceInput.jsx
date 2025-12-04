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
        const stream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            sampleRate: 16000
          } 
        });
        
        audioChunksRef.current = [];
        
        // Use webm format (better browser support)
        const options = { mimeType: 'audio/webm' };
        mediaRecorderRef.current = new MediaRecorder(stream, options);
        
        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0) {
            console.log('Audio chunk received:', event.data.size, 'bytes');
            audioChunksRef.current.push(event.data);
          }
        };
        
        mediaRecorderRef.current.onstop = async () => {
          console.log('Recording stopped. Total chunks:', audioChunksRef.current.length);
          
          if (audioChunksRef.current.length === 0) {
            console.error('No audio data recorded');
            alert('No audio detected. Please try again and speak louder.');
            stream.getTracks().forEach(track => track.stop());
            return;
          }
          
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          console.log('Audio blob created:', audioBlob.size, 'bytes');
          
          if (audioBlob.size < 1000) {
            console.error('Audio too short:', audioBlob.size, 'bytes');
            alert('Recording too short. Please speak for at least 1 second.');
            stream.getTracks().forEach(track => track.stop());
            return;
          }
          
          await onSubmit(null, audioBlob); // Send audio instead of text
          stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorderRef.current.onerror = (event) => {
          console.error('MediaRecorder error:', event.error);
          alert('Recording error: ' + event.error);
        };
        
        // Start recording with timeslice to get data chunks
        mediaRecorderRef.current.start(100); // Get data every 100ms
        console.log('Recording started');
        setMicState('recording');
      } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Please allow microphone access to use voice input.');
      }
    } else if (micState === 'recording') {
      // Stop recording
      console.log('Stopping recording...');
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
        className={`${getMicButtonClass()} h-14 w-14`}
      >
        {micState === 'recording' ? (
          <MicOff className="h-7 w-7" />
        ) : (
          <Mic className="h-7 w-7" />
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
