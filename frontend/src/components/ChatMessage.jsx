import React from 'react';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

const ChatMessage = ({ role, text, feedback, isThinking = false }) => {
  const isUser = role === 'user';

  if (isThinking) {
    return (
      <div className="flex justify-start mb-4">
        <Card className="max-w-[80%] p-4 bg-slate-800 border-slate-700">
          <div className="flex items-center gap-2 text-slate-400 text-sm mb-2">
            <span>Macca is analyzing your speech...</span>
          </div>
          <Skeleton className="h-4 w-full mb-2 bg-slate-700" />
          <Skeleton className="h-4 w-3/4 bg-slate-700" />
        </Card>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <Card className={`max-w-[80%] p-4 ${
        isUser 
          ? 'bg-cyan-500/20 border-cyan-500/30' 
          : 'bg-slate-800 border-slate-700'
      }`}>
        <div className={`text-sm ${isUser ? 'text-cyan-100' : 'text-slate-100'}`}>
          {text}
        </div>
        {feedback && !isUser && (
          <div className="mt-3 pt-3 border-t border-slate-700">
            <div className="text-xs text-slate-400 mb-1">Feedback:</div>
            {feedback.grammar_ok !== undefined && (
              <div className="text-xs text-slate-300">
                Grammar: {feedback.grammar_ok ? '✓ Good' : '✗ Needs work'}
              </div>
            )}
            {feedback.fluency_score !== undefined && (
              <div className="text-xs text-slate-300">
                Fluency: {feedback.fluency_score}/100
              </div>
            )}
            {feedback.tip_id && (
              <div className="text-xs text-cyan-400 mt-1">
                💡 {feedback.tip_id}
              </div>
            )}
            {feedback.encouragement_id && (
              <div className="text-xs text-green-400 mt-1">
                ✨ {feedback.encouragement_id}
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  );
};

export default ChatMessage;
