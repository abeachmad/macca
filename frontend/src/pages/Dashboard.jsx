import React from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '@/components/Layout';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MessageCircle, BookOpen, Mic2, TrendingUp } from 'lucide-react';
import { useMacca } from '@/context/MaccaContext';

const Dashboard = () => {
  const navigate = useNavigate();
  const { userProfile } = useMacca();

  const modes = [
    {
      id: 'live',
      title: 'Live Conversation',
      description: 'Practice free-form conversations with instant feedback',
      icon: MessageCircle,
      color: 'cyan',
      path: '/live-conversation'
    },
    {
      id: 'guided',
      title: 'Guided Lessons',
      description: 'Structured lessons for specific scenarios and goals',
      icon: BookOpen,
      color: 'blue',
      path: '/guided-lesson'
    },
    {
      id: 'pronunciation',
      title: 'Pronunciation Coach',
      description: 'Master difficult English sounds with targeted practice',
      icon: Mic2,
      color: 'purple',
      path: '/pronunciation-coach'
    }
  ];

  return (
    <Layout>
      <div className="max-w-6xl">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100 mb-2">
            Welcome back, {userProfile.name}! 👋
          </h1>
          <p className="text-slate-400">
            Choose a learning mode to continue improving your English
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-400">Current Level</p>
                  <p className="text-2xl font-bold text-cyan-400">{userProfile.level}</p>
                </div>
                <TrendingUp className="h-8 w-8 text-cyan-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardContent className="pt-6">
              <div>
                <p className="text-sm text-slate-400">Learning Goal</p>
                <p className="text-lg font-semibold text-slate-100 mt-1">{userProfile.goal}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardContent className="pt-6">
              <div>
                <p className="text-sm text-slate-400">Explanation Language</p>
                <p className="text-lg font-semibold text-slate-100 mt-1">
                  {userProfile.explanation_language === 'id' ? 'Bahasa Indonesia' : 'English'}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Mode Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {modes.map((mode) => {
            const Icon = mode.icon;
            return (
              <Card
                key={mode.id}
                className="bg-slate-800/50 border-slate-700 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer group"
                onClick={() => navigate(mode.path)}
              >
                <CardHeader>
                  <div className="h-12 w-12 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-4 group-hover:bg-cyan-500/30 transition-colors">
                    <Icon className="h-6 w-6 text-cyan-400" />
                  </div>
                  <CardTitle className="text-slate-100">{mode.title}</CardTitle>
                  <CardDescription className="text-slate-400">
                    {mode.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    className="w-full bg-cyan-500 hover:bg-cyan-600"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(mode.path);
                    }}
                  >
                    Start
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;