import React, { useState } from 'react';
import Layout from '@/components/Layout';
import LearnerContextBar from '@/components/LearnerContextBar';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useMacca } from '@/context/MaccaContext';
import { Mic, Volume2 } from 'lucide-react';

const PronunciationCoach = () => {
  const { analyzePronunciation, userProfile } = useMacca();
  const [selectedSound, setSelectedSound] = useState(null);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [completedWords, setCompletedWords] = useState([]);

  const practiceWords = [
    {
      id: 1,
      sound: '/æ/',
      name: 'Short A',
      difficulty: 'easy',
      examples: ['cat', 'bat', 'map', 'glad']
    },
    {
      id: 2,
      sound: '/ɪ/',
      name: 'Short I',
      difficulty: 'easy',
      examples: ['sit', 'bit', 'hit', 'fit']
    },
    {
      id: 3,
      sound: '/ɛ/',
      name: 'Short E',
      difficulty: 'easy',
      examples: ['bed', 'red', 'pen', 'ten']
    },
    {
      id: 4,
      sound: '/ʌ/',
      name: 'Short U',
      difficulty: 'easy',
      examples: ['cup', 'bus', 'run', 'sun']
    },
    {
      id: 5,
      sound: '/r/',
      name: 'R sound',
      difficulty: 'medium',
      examples: ['red', 'road', 'berry', 'correct']
    },
    {
      id: 6,
      sound: '/v/',
      name: 'V sound',
      difficulty: 'medium',
      examples: ['very', 'voice', 'live', 'have']
    },
    {
      id: 7,
      sound: '/l/',
      name: 'L sound',
      difficulty: 'medium',
      examples: ['light', 'love', 'hello', 'ball']
    },
    {
      id: 8,
      sound: '/w/',
      name: 'W sound',
      difficulty: 'medium',
      examples: ['water', 'want', 'away', 'swim']
    },
    {
      id: 9,
      sound: '/θ/',
      name: 'TH (voiceless)',
      difficulty: 'hard',
      examples: ['think', 'thank', 'three', 'mouth']
    },
    {
      id: 10,
      sound: '/ð/',
      name: 'TH (voiced)',
      difficulty: 'hard',
      examples: ['this', 'that', 'the', 'mother']
    },
    {
      id: 11,
      sound: '/ʃ/',
      name: 'SH sound',
      difficulty: 'hard',
      examples: ['ship', 'shop', 'fish', 'wash']
    },
    {
      id: 12,
      sound: '/tʃ/',
      name: 'CH sound',
      difficulty: 'hard',
      examples: ['chair', 'church', 'watch', 'teach']
    }
  ];

  const speakWord = (word) => {
    const utterance = new SpeechSynthesisUtterance(word);
    utterance.lang = 'en-US';
    utterance.rate = 0.8;
    window.speechSynthesis.speak(utterance);
  };

  const handlePracticeWord = async () => {
    if (!selectedSound) return;
    const word = selectedSound.examples[currentWordIndex];
    setIsRecording(true);
    setFeedback(null);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        setIsRecording(false);
        setIsAnalyzing(true);
        
        try {
          const result = await analyzePronunciation(word, audioBlob);
          setFeedback(result);
          
          // Auto advance if score >= 80
          if (result && result.length > 0 && result[0].score >= 80) {
            setTimeout(() => {
              if (currentWordIndex < selectedSound.examples.length - 1) {
                setCurrentWordIndex(prev => prev + 1);
                setCompletedWords(prev => [...prev, word]);
                setFeedback(null);
              } else {
                setCompletedWords(prev => [...prev, word]);
              }
            }, 2000);
          }
        } catch (error) {
          console.error('Error analyzing:', error);
        } finally {
          setIsAnalyzing(false);
        }
        
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setTimeout(() => mediaRecorder.stop(), 3000);
    } catch (error) {
      console.error('Microphone error:', error);
      setIsRecording(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'medium': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'hard': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'excellent': return 'bg-green-500 text-white';
      case 'good': return 'bg-blue-500 text-white';
      case 'needs_work': return 'bg-yellow-500 text-slate-900';
      default: return 'bg-slate-500 text-white';
    }
  };

  return (
    <Layout>
      <div className="max-w-6xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-100 mb-2">Pronunciation Coach</h1>
          <p className="text-slate-400">Master difficult English sounds with targeted practice</p>
        </div>

        <LearnerContextBar />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Sound List */}
          <div>
            <h2 className="text-xl font-semibold text-slate-100 mb-4">Practice Sounds</h2>
            <div className="space-y-3">
              {practiceWords.map((item) => (
                <Card
                  key={item.id}
                  className={`cursor-pointer transition-all ${
                    selectedSound?.id === item.id
                      ? 'bg-cyan-500/20 border-cyan-500'
                      : 'bg-slate-800/50 border-slate-700 hover:border-cyan-500/50'
                  }`}
                  onClick={() => {
                    setSelectedSound(item);
                    setCurrentWordIndex(0);
                    setFeedback(null);
                    setCompletedWords([]);
                  }}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-lg font-semibold text-cyan-400">{item.sound}</span>
                          <span className="text-slate-300">{item.name}</span>
                        </div>
                        <Badge variant="outline" className={getDifficultyColor(item.difficulty)}>
                          {item.difficulty}
                        </Badge>
                      </div>
                      <Volume2 className="h-5 w-5 text-slate-400" />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Right: Practice Area */}
          <div>
            {selectedSound ? (
              <div className="space-y-4">
                <Card className="bg-slate-800/50 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-slate-100">
                      Practice: {selectedSound.sound} - {selectedSound.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <p className="text-sm text-slate-400 mb-3">Example words:</p>
                        <div className="grid grid-cols-2 gap-3">
                          {selectedSound.examples.map((word, index) => (
                            <Card key={index} className="bg-slate-900/50 border-slate-700">
                              <CardContent className="p-4">
                                <div className="flex items-center justify-between">
                                  <span className="text-lg font-medium text-slate-200">{word}</span>
                                  <Button
                                    size="icon"
                                    variant="ghost"
                                    className="h-8 w-8 text-cyan-400 hover:bg-cyan-500/20"
                                    onClick={() => speakWord(word)}
                                  >
                                    <Volume2 className="h-4 w-4" />
                                  </Button>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </div>

                      <div className="pt-4 border-t border-slate-700">
                        <div className="text-center mb-4">
                          <p className="text-sm text-slate-400 mb-2">Word {currentWordIndex + 1} of {selectedSound.examples.length}</p>
                          <p className="text-2xl font-bold text-cyan-400 mb-1">
                            Say: "{selectedSound.examples[currentWordIndex]}"
                          </p>
                          {completedWords.length > 0 && (
                            <p className="text-sm text-green-400">✓ Completed: {completedWords.join(', ')}</p>
                          )}
                        </div>
                        <div className="flex justify-center">
                          <Button
                            size="lg"
                            className={`h-16 w-16 rounded-full transition-all ${
                              isRecording
                                ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                                : 'bg-cyan-500 hover:bg-cyan-600'
                            }`}
                            onClick={handlePracticeWord}
                            disabled={isAnalyzing || currentWordIndex >= selectedSound.examples.length}
                          >
                            <Mic className="h-8 w-8" />
                          </Button>
                        </div>
                        {isRecording && (
                          <p className="text-sm text-red-400 mt-3 text-center">🎤 Recording... Speak now!</p>
                        )}
                        {isAnalyzing && (
                          <p className="text-sm text-cyan-400 mt-3 text-center">⏳ Analyzing your pronunciation...</p>
                        )}
                        {currentWordIndex >= selectedSound.examples.length && completedWords.length === selectedSound.examples.length && (
                          <p className="text-lg text-green-400 mt-3 text-center font-semibold">🎉 All words completed! Great job!</p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Pronunciation Feedback */}
                {feedback && feedback.length > 0 && (
                  <Card className="bg-slate-800/50 border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-slate-100">Pronunciation Feedback</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {feedback.map((item, index) => (
                          <div key={index} className="p-4 bg-slate-900/50 rounded-lg border border-slate-700">
                            <div className="flex items-start justify-between mb-2">
                              <div>
                                <span className="text-lg font-semibold text-slate-200">{item.word}</span>
                                <span className="text-sm text-slate-400 ml-2">({item.target_sound})</span>
                              </div>
                              <Badge className={getStatusColor(item.status)}>
                                {item.status === 'needs_work' ? 'Needs work' : item.status}
                              </Badge>
                            </div>
                            <div className="mb-2">
                              <div className="flex items-center gap-2">
                                <span className="text-sm text-slate-400">Score:</span>
                                <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                                  <div
                                    className={`h-full ${
                                      item.score >= 80 ? 'bg-green-500' : item.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                                    }`}
                                    style={{ width: `${item.score}%` }}
                                  ></div>
                                </div>
                                <span className="text-sm text-slate-300 font-semibold">{item.score}%</span>
                              </div>
                            </div>
                            <div className="text-sm text-cyan-400">
                              💡 {userProfile.explanation_language === 'id' ? item.tip_id : item.tip_en}
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            ) : (
              <Card className="bg-slate-800/50 border-slate-700 h-full flex items-center justify-center">
                <CardContent className="text-center py-16">
                  <Mic className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                  <p className="text-slate-400">Select a sound from the left to start practicing</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default PronunciationCoach;