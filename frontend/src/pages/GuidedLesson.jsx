import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import LearnerContextBar from '@/components/LearnerContextBar';
import VoiceInput from '@/components/VoiceInput';
import ChatMessage from '@/components/ChatMessage';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { useMacca } from '@/context/MaccaContext';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';

const GuidedLesson = () => {
  const { sendConversationTurn, getLesson } = useMacca();
  const [lesson, setLesson] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);

  useEffect(() => {
    loadLesson();
  }, []);

  const loadLesson = async () => {
    try {
      const lessonData = await getLesson('lesson_1');
      setLesson(lessonData);
      setCurrentStep(lessonData.current_step);
      
      // Initial greeting
      setMessages([{
        role: 'assistant',
        text: `Welcome to today's lesson: "${lessonData.title}". ${lessonData.subtitle} Let's start with Step 1: Warm-up. Tell me a bit about yourself!`,
        feedback: null
      }]);
    } catch (error) {
      console.error('Error loading lesson:', error);
    }
  };

  const handleSendMessage = async (userText) => {
    // Add user message
    const userMessage = { role: 'user', text: userText, feedback: null };
    setMessages(prev => [...prev, userMessage]);
    
    // Show thinking state
    setIsThinking(true);
    
    try {
      // Send to backend
      const response = await sendConversationTurn(userText, 'guided');
      
      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        text: response.macca_text,
        feedback: response.feedback
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Check if should move to next step
      if (response.feedback?.step_complete && currentStep < lesson.steps.length) {
        setCurrentStep(prev => prev + 1);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsThinking(false);
    }
  };

  if (!lesson) {
    return (
      <Layout>
        <div className="max-w-4xl">
          <p className="text-slate-400">Loading lesson...</p>
        </div>
      </Layout>
    );
  }

  const progressPercent = (currentStep / lesson.steps.length) * 100;

  return (
    <Layout>
      <div className="max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-100 mb-2">Guided Lesson</h1>
          <p className="text-slate-400">Follow structured steps to master specific scenarios</p>
        </div>

        <LearnerContextBar />

        {/* Lesson Info Card */}
        <Card className="bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border-cyan-500/30 mb-6">
          <CardHeader>
            <CardTitle className="text-2xl text-slate-100">{lesson.title}</CardTitle>
            <CardDescription className="text-slate-300 text-base">{lesson.subtitle}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-400">Progress</span>
                <span className="text-sm text-cyan-400 font-semibold">Step {currentStep} of {lesson.steps.length}</span>
              </div>
              <Progress value={progressPercent} className="h-2" />
              
              <div className="mt-4 space-y-2">
                {lesson.steps.map((step, index) => (
                  <div
                    key={index}
                    className={`flex items-center gap-3 text-sm ${
                      index + 1 === currentStep
                        ? 'text-cyan-400 font-semibold'
                        : index + 1 < currentStep
                        ? 'text-slate-500'
                        : 'text-slate-400'
                    }`}
                  >
                    <div className={`h-6 w-6 rounded-full flex items-center justify-center border ${
                      index + 1 === currentStep
                        ? 'bg-cyan-500/20 border-cyan-400'
                        : index + 1 < currentStep
                        ? 'bg-green-500/20 border-green-500'
                        : 'border-slate-600'
                    }`}>
                      {index + 1 < currentStep ? '✓' : index + 1}
                    </div>
                    <span>{step}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Conversation */}
        <Card className="bg-slate-800/50 border-slate-700">
          <ScrollArea className="h-[400px] p-6">
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
              placeholder="Type or speak your answer..."
            />
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default GuidedLesson;