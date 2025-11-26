import React from 'react';
import { useMacca } from '@/context/MaccaContext';
import { Badge } from '@/components/ui/badge';

const LearnerContextBar = () => {
  const { userProfile } = useMacca();

  const explanationText = userProfile.explanation_language === 'id' 
    ? 'Bahasa Indonesia' 
    : 'English';

  return (
    <div className="flex items-center gap-4 px-4 py-3 bg-slate-800/50 rounded-lg border border-cyan-500/20 mb-6">
      <div className="flex items-center gap-2">
        <span className="text-sm text-slate-400">Level:</span>
        <Badge variant="outline" className="bg-cyan-500/10 text-cyan-400 border-cyan-500/30">
          {userProfile.level}
        </Badge>
      </div>
      <div className="h-4 w-px bg-slate-700"></div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-slate-400">Goal:</span>
        <span className="text-sm text-slate-200">{userProfile.goal}</span>
      </div>
      <div className="h-4 w-px bg-slate-700"></div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-slate-400">Explanation:</span>
        <span className="text-sm text-cyan-400">{explanationText}</span>
      </div>
    </div>
  );
};

export default LearnerContextBar;
