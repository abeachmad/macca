import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { MessageCircle, BookOpen, Mic2, Target } from 'lucide-react';

const Welcome = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: MessageCircle,
      title: 'Live Conversation',
      description: 'Practice natural English conversations with AI feedback'
    },
    {
      icon: BookOpen,
      title: 'Guided Lessons',
      description: 'Structured learning paths for specific scenarios'
    },
    {
      icon: Mic2,
      title: 'Pronunciation Coach',
      description: 'Master difficult sounds with targeted practice'
    },
    {
      icon: Target,
      title: 'Personalized Goals',
      description: 'Track progress tailored to your learning objectives'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            Macca
          </h1>
          <p className="text-2xl text-slate-300 mb-2">AI English Speaking Coach</p>
          <p className="text-lg text-slate-400 mb-8">Untuk pelajar Indonesia | For Indonesian learners</p>
          <Button
            onClick={() => navigate('/dashboard')}
            size="lg"
            className="bg-cyan-500 hover:bg-cyan-600 text-white px-8 py-6 text-lg rounded-full"
          >
            Get Started →
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card
                key={index}
                className="p-6 bg-slate-800/50 border-slate-700 hover:border-cyan-500/50 transition-all duration-300 hover:scale-105"
              >
                <div className="h-12 w-12 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-4">
                  <Icon className="h-6 w-6 text-cyan-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-100 mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-400">{feature.description}</p>
              </Card>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <p className="text-slate-400 mb-4">Ready to improve your English speaking skills?</p>
          <Button
            onClick={() => navigate('/dashboard')}
            variant="outline"
            className="border-cyan-500 text-cyan-400 hover:bg-cyan-500/10"
          >
            Start Learning Now
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Welcome;