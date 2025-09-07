import React, { useState } from 'react';
import { FileText, Play, Download, Settings, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import api from '../lib/api';

const SummarizeForm = () => {
  const [text, setText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [settings, setSettings] = useState({
    algorithm: 'textrank',
    maxLength: 150,
    language: 'en'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      toast.error('Please enter some text to summarize');
      return;
    }
    
    setLoading(true);
    setSummary('');
    
    try {
      const { data } = await api.post('/summarize', {
        text,
        max_length: settings.maxLength,
        algorithm: settings.algorithm,
        language: settings.language
      });
      
      setSummary(data.summary);
      toast.success('Summary generated successfully!');
    } catch (error) {
      console.error('Summarization failed:', error);
      toast.error('Failed to generate summary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePlayAudio = () => {
    toast.success('Audio playback started');
  };

  const handleDownload = () => {
    const blob = new Blob([summary], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'summary.txt';
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Summary downloaded');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          AI Text Summarizer
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Paste your text below and get an AI-powered summary in seconds
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Input Section */}
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Input Text
              </h2>
              <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                <FileText className="h-4 w-4" />
                <span>{text.length} characters</span>
              </div>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none"
                rows={12}
                placeholder="Paste your text here to get started..."
              />
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <select
                    value={settings.algorithm}
                    onChange={(e) => setSettings(prev => ({ ...prev, algorithm: e.target.value }))}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                  >
                    <option value="textrank">TextRank</option>
                    <option value="lsa">LSA</option>
                    <option value="lexrank">LexRank</option>
                    <option value="bert">BART</option>
                  </select>
                  
                  <input
                    type="number"
                    min="50"
                    max="500"
                    value={settings.maxLength}
                    onChange={(e) => setSettings(prev => ({ ...prev, maxLength: parseInt(e.target.value) }))}
                    className="w-20 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                    placeholder="Length"
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={loading || !text.trim()}
                  className="flex items-center space-x-2 px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Summarizing...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-4 w-4" />
                      <span>Summarize</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Settings Panel */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-2 mb-4">
              <Settings className="h-5 w-5 text-purple-600" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Settings
              </h3>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Algorithm
                </label>
                <select
                  value={settings.algorithm}
                  onChange={(e) => setSettings(prev => ({ ...prev, algorithm: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                >
                  <option value="textrank">TextRank (Fast)</option>
                  <option value="lsa">LSA (Balanced)</option>
                  <option value="lexrank">LexRank (Quality)</option>
                  <option value="bert">BART (Advanced)</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Max Length
                </label>
                <input
                  type="number"
                  min="50"
                  max="500"
                  value={settings.maxLength}
                  onChange={(e) => setSettings(prev => ({ ...prev, maxLength: parseInt(e.target.value) }))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Language
                </label>
                <select
                  value={settings.language}
                  onChange={(e) => setSettings(prev => ({ ...prev, language: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="it">Italian</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Summary Section */}
      {summary && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8"
        >
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-6 border border-purple-200 dark:border-purple-800">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                AI Summary
              </h2>
              <div className="flex items-center space-x-2">
                <button
                  onClick={handlePlayAudio}
                  className="p-2 bg-white dark:bg-gray-800 rounded-full shadow-sm hover:shadow-md transition-shadow"
                  title="Play audio"
                >
                  <Play className="h-4 w-4 text-purple-600" />
                </button>
                <button
                  onClick={handleDownload}
                  className="p-2 bg-white dark:bg-gray-800 rounded-full shadow-sm hover:shadow-md transition-shadow"
                  title="Download summary"
                >
                  <Download className="h-4 w-4 text-purple-600" />
                </button>
              </div>
            </div>
            
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
              {summary}
            </p>
            
            <div className="mt-4 flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
              <span>Algorithm: {settings.algorithm.toUpperCase()}</span>
              <span>Length: {summary.length} characters</span>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default SummarizeForm;


