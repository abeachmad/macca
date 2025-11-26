import React, { useState } from 'react';
import Layout from '@/components/Layout';
import LearnerContextBar from '@/components/LearnerContextBar';
import VoiceInput from '@/components/VoiceInput';
import ChatMessage from '@/components/ChatMessage';
import { Card } from '@/components/ui/card';
import { useMacca } from '@/context/MaccaContext';
import { ScrollArea } from '@/components/ui/scroll-area';

const LiveConversation = () => {
  const { sendConversationTurn } = useMacca();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: "Hi! I'm Macca, your English speaking coach. Let's have a natural conversation. What would you like to talk about today?",
      feedback: null
    }
  ]);
  const [isThinking, setIsThinking] = useState(false);

  const handleSendMessage = async (userText) => {
    // Add user message
    const userMessage = { role: 'user', text: userText, feedback: null };
    setMessages(prev => [...prev, userMessage]);
    
    // Show thinking state
    setIsThinking(true);
    
    try {
      // Send to backend
      const response = await sendConversationTurn(userText, 'live');
      
      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        text: response.macca_text,
        feedback: response.feedback
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: "Sorry, I encountered an error. Let's try again.",
        feedback: null
      }]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-100 mb-2">Live Conversation</h1>
          <p className="text-slate-400">Practice natural conversations with real-time feedback</p>
        </div>

        <LearnerContextBar />

        <Card className="bg-slate-800/50 border-slate-700">
          <ScrollArea className="h-[500px] p-6">
            {messages.map((msg, index) => (
              <ChatMessage
                key={index}
                role={msg.role}
                text={msg.text}
                feedback={msg.feedback}
              />
            ))}
            {isThinking && <ChatMessage isThinking={true} />}
          </ScrollArea>
          
          <div className="p-6 border-t border-slate-700">
            <VoiceInput
              onSubmit={handleSendMessage}
              disabled={isThinking}
              placeholder="Type or speak your message..."
            />
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default LiveConversation;