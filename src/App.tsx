import React, { useState, useEffect } from 'react';
import { Brain, MessageCircle, Activity, Zap, BarChart3, Settings } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

interface TokenData {
  token: string;
  field_intensity: number;
  qualification: string;
}

interface ToneVector {
  joy: number;
  fear: number;
  anger: number;
  sadness: number;
  surprise: number;
}

interface ConversationEntry {
  id: string;
  timestamp: number;
  input: string;
  tone: {
    dominant_tone: string;
    intensity: number;
    vector: ToneVector;
  };
  tokens: TokenData[];
  response: string;
}

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [conversation, setConversation] = useState<ConversationEntry[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentTone, setCurrentTone] = useState<ToneVector>({
    joy: 0.2,
    fear: 0.1,
    anger: 0.1,
    sadness: 0.1,
    surprise: 0.1
  });

  // Simulate the RFM processing pipeline
  const processInput = async (text: string) => {
    setIsProcessing(true);
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simple tokenization
    const tokens = text.split(' ').map(token => ({
      token,
      field_intensity: Math.random() * 0.8,
      qualification: Math.random() > 0.7 ? 'UNSTABLE' : Math.random() > 0.4 ? 'AMBIGUOUS' : 'QUALIFIED'
    }));

    // Simulate tone analysis
    const toneVector: ToneVector = {
      joy: Math.max(0, Math.random() * 0.8 + (text.includes('happy') || text.includes('great') ? 0.3 : 0)),
      fear: Math.max(0, Math.random() * 0.6 + (text.includes('scared') || text.includes('worried') ? 0.4 : 0)),
      anger: Math.max(0, Math.random() * 0.5 + (text.includes('angry') || text.includes('mad') ? 0.5 : 0)),
      sadness: Math.max(0, Math.random() * 0.6 + (text.includes('sad') || text.includes('depressed') ? 0.4 : 0)),
      surprise: Math.max(0, Math.random() * 0.7 + (text.includes('wow') || text.includes('amazing') ? 0.3 : 0))
    };

    const dominantEmotion = Object.entries(toneVector).reduce((a, b) => 
      toneVector[a[0] as keyof ToneVector] > toneVector[b[0] as keyof ToneVector] ? a : b
    )[0];

    // Generate response based on tone
    let response = '';
    if (dominantEmotion === 'joy') {
      response = "I can sense the positive energy in your words! That's wonderful to hear.";
    } else if (dominantEmotion === 'fear') {
      response = "I'm picking up some anxiety in your message. Would you like to talk about what's concerning you?";
    } else if (dominantEmotion === 'anger') {
      response = "I can feel the intensity in your words. Sometimes it helps to express these feelings.";
    } else if (dominantEmotion === 'sadness') {
      response = "I sense some heaviness in what you're sharing. I'm here to listen.";
    } else {
      response = "That's quite interesting! Tell me more about your thoughts on this.";
    }

    const entry: ConversationEntry = {
      id: Date.now().toString(),
      timestamp: Date.now(),
      input: text,
      tone: {
        dominant_tone: dominantEmotion,
        intensity: Math.max(...Object.values(toneVector)),
        vector: toneVector
      },
      tokens,
      response
    };

    setConversation(prev => [...prev, entry]);
    setCurrentTone(toneVector);
    setIsProcessing(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      processInput(input.trim());
      setInput('');
    }
  };

  const radarData = Object.entries(currentTone).map(([emotion, value]) => ({
    emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
    value: Math.round(value * 100)
  }));

  const timelineData = conversation.slice(-10).map((entry, index) => ({
    time: index + 1,
    intensity: Math.round(entry.tone.intensity * 100),
    dominant: entry.tone.dominant_tone
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-12 h-12 text-purple-400 mr-3" />
            <h1 className="text-4xl font-bold text-white">RFM Companion AI</h1>
          </div>
          <p className="text-purple-200 text-lg">Resonant Field Mapping - Tier 4 Emotional Intelligence</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-2xl border border-white/20">
              <div className="flex items-center mb-4">
                <MessageCircle className="w-6 h-6 text-purple-400 mr-2" />
                <h2 className="text-xl font-semibold text-white">Conversation</h2>
              </div>
              
              {/* Conversation History */}
              <div className="h-96 overflow-y-auto mb-4 space-y-4 bg-black/20 rounded-lg p-4">
                {conversation.length === 0 ? (
                  <div className="text-center text-purple-200 py-8">
                    <Brain className="w-16 h-16 mx-auto mb-4 text-purple-400 opacity-50" />
                    <p>Start a conversation to see RFM analysis in action</p>
                  </div>
                ) : (
                  conversation.map((entry) => (
                    <div key={entry.id} className="space-y-2">
                      <div className="bg-blue-600/30 rounded-lg p-3 ml-8">
                        <p className="text-white">{entry.input}</p>
                      </div>
                      <div className="bg-purple-600/30 rounded-lg p-3 mr-8">
                        <p className="text-white">{entry.response}</p>
                        <div className="flex items-center mt-2 text-xs text-purple-200">
                          <Activity className="w-3 h-3 mr-1" />
                          <span>Tone: {entry.tone.dominant_tone}</span>
                          <span className="ml-2">Intensity: {Math.round(entry.tone.intensity * 100)}%</span>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Share your thoughts..."
                  className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white placeholder-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400"
                  disabled={isProcessing}
                />
                <button
                  type="submit"
                  disabled={isProcessing || !input.trim()}
                  className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800 disabled:opacity-50 text-white px-6 py-2 rounded-lg transition-colors flex items-center"
                >
                  {isProcessing ? (
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <Zap className="w-4 h-4" />
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Analytics Panel */}
          <div className="space-y-6">
            {/* Current Emotional State */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-2xl border border-white/20">
              <div className="flex items-center mb-4">
                <Activity className="w-6 h-6 text-purple-400 mr-2" />
                <h3 className="text-lg font-semibold text-white">Emotional Field</h3>
              </div>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#8b5cf6" />
                    <PolarAngleAxis dataKey="emotion" tick={{ fill: '#e9d5ff', fontSize: 12 }} />
                    <PolarRadiusAxis 
                      angle={90} 
                      domain={[0, 100]} 
                      tick={{ fill: '#e9d5ff', fontSize: 10 }}
                    />
                    <Radar
                      name="Intensity"
                      dataKey="value"
                      stroke="#8b5cf6"
                      fill="#8b5cf6"
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Intensity Timeline */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-2xl border border-white/20">
              <div className="flex items-center mb-4">
                <BarChart3 className="w-6 h-6 text-purple-400 mr-2" />
                <h3 className="text-lg font-semibold text-white">Intensity Timeline</h3>
              </div>
              <div className="h-32">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={timelineData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#8b5cf6" opacity={0.3} />
                    <XAxis 
                      dataKey="time" 
                      tick={{ fill: '#e9d5ff', fontSize: 10 }}
                      axisLine={{ stroke: '#8b5cf6' }}
                    />
                    <YAxis 
                      domain={[0, 100]}
                      tick={{ fill: '#e9d5ff', fontSize: 10 }}
                      axisLine={{ stroke: '#8b5cf6' }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1e1b4b', 
                        border: '1px solid #8b5cf6',
                        borderRadius: '8px',
                        color: '#e9d5ff'
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="intensity" 
                      stroke="#8b5cf6" 
                      strokeWidth={3}
                      dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* System Status */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-2xl border border-white/20">
              <div className="flex items-center mb-4">
                <Settings className="w-6 h-6 text-purple-400 mr-2" />
                <h3 className="text-lg font-semibold text-white">System Status</h3>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-purple-200">Token Qualifier</span>
                  <span className="text-green-400">Active</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-purple-200">Tone Engine</span>
                  <span className="text-green-400">Active</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-purple-200">Field Shift Detection</span>
                  <span className="text-green-400">Active</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-purple-200">Memory Graph</span>
                  <span className="text-green-400">Active</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-purple-200">Conversations</span>
                  <span className="text-purple-300">{conversation.length}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-purple-200">
          <p>RFM Tier 4 - Resonant Field Mapping Companion AI</p>
          <p className="text-sm opacity-75">Symbolic emotional architecture for empathic AI</p>
        </div>
      </div>
    </div>
  );
};

export default App;