import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Download, 
  Share2, 
  Star, 
  Play, 
  Pause, 
  Volume2,
  Tag,
  Calendar,
  FileText,
  Clock,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const DocumentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [document, setDocument] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [feedback, setFeedback] = useState({
    helpful: null,
    rating: 0,
    comments: ''
  });

  useEffect(() => {
    // Simulate fetching document data
    const mockDocument = {
      id: id,
      title: 'Sample Document: AI and Machine Learning in Healthcare',
      content: `Artificial Intelligence (AI) and Machine Learning (ML) are revolutionizing healthcare by enabling more accurate diagnoses, personalized treatments, and improved patient outcomes. These technologies are being integrated into various aspects of healthcare, from medical imaging and drug discovery to patient monitoring and administrative tasks.

The application of AI in medical imaging has shown remarkable success in detecting diseases such as cancer, diabetic retinopathy, and cardiovascular conditions. Machine learning algorithms can analyze medical images with accuracy comparable to or exceeding that of human radiologists, while also reducing the time required for analysis.

In drug discovery, AI is accelerating the process of identifying potential therapeutic compounds and predicting their effectiveness. This has the potential to significantly reduce the time and cost of bringing new drugs to market, ultimately benefiting patients worldwide.

Personalized medicine is another area where AI is making significant contributions. By analyzing patient data, including genetic information, medical history, and lifestyle factors, AI can help healthcare providers develop tailored treatment plans that are more effective and have fewer side effects.

However, the integration of AI in healthcare also presents challenges, including data privacy concerns, the need for regulatory oversight, and ensuring that these technologies are accessible to all patients regardless of their socioeconomic status.`,
      summary: 'This document discusses the transformative impact of AI and Machine Learning in healthcare, covering applications in medical imaging, drug discovery, and personalized medicine, while also addressing associated challenges and considerations.',
      tags: ['AI', 'Healthcare', 'Machine Learning', 'Medical Imaging', 'Drug Discovery', 'Personalized Medicine'],
      entities: ['Artificial Intelligence', 'Machine Learning', 'Healthcare', 'Medical Imaging', 'Drug Discovery'],
      topics: ['Technology', 'Medicine', 'Research', 'Innovation'],
      sentiment: 'positive',
      language: 'en',
      fileType: 'pdf',
      fileSize: '2.3 MB',
      createdAt: '2024-01-15T10:30:00Z',
      processingTime: '2.5s',
      compressionRatio: 0.15
    };
    
    setDocument(mockDocument);
  }, [id]);

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
    toast.success(isPlaying ? 'Audio paused' : 'Audio playing');
  };

  const handleFeedback = (type, value) => {
    setFeedback(prev => ({ ...prev, [type]: value }));
  };

  const submitFeedback = () => {
    if (feedback.helpful === null) {
      toast.error('Please rate the summary');
      return;
    }
    toast.success('Feedback submitted successfully!');
  };

  if (!document) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Dashboard</span>
        </button>
        
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              {document.title}
            </h1>
            <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-1">
                <FileText className="h-4 w-4" />
                <span>{document.fileType.toUpperCase()}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Calendar className="h-4 w-4" />
                <span>{new Date(document.createdAt).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="h-4 w-4" />
                <span>{document.processingTime}</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
              <Share2 className="h-5 w-5" />
            </button>
            <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
              <Download className="h-5 w-5" />
            </button>
            <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
              <Star className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Summary Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-6 border border-purple-200 dark:border-purple-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              AI Summary
            </h2>
            <div className="flex items-center space-x-2">
              <button
                onClick={handlePlayPause}
                className="p-2 bg-white dark:bg-gray-800 rounded-full shadow-sm hover:shadow-md transition-shadow"
              >
                {isPlaying ? (
                  <Pause className="h-4 w-4 text-purple-600" />
                ) : (
                  <Play className="h-4 w-4 text-purple-600" />
                )}
              </button>
              <button className="p-2 bg-white dark:bg-gray-800 rounded-full shadow-sm hover:shadow-md transition-shadow">
                <Volume2 className="h-4 w-4 text-purple-600" />
              </button>
            </div>
          </div>
          
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
            {document.summary}
          </p>
          
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center space-x-4">
              <span>Compression: {(document.compressionRatio * 100).toFixed(1)}%</span>
              <span>Language: {document.language.toUpperCase()}</span>
              <span>Sentiment: {document.sentiment}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Tag className="h-4 w-4" />
              <span>{document.tags.length} tags</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Tags and Entities */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Tags
          </h3>
          <div className="flex flex-wrap gap-2">
            {document.tags.map((tag, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Key Entities
          </h3>
          <div className="flex flex-wrap gap-2">
            {document.entities.map((entity, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-sm"
              >
                {entity}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Full Content */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Full Content
        </h3>
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
            {document.content}
          </p>
        </div>
      </div>

      {/* Feedback Section */}
      <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Rate this Summary
        </h3>
        
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Was this summary helpful?
            </p>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => handleFeedback('helpful', true)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                  feedback.helpful === true
                    ? 'border-green-500 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300'
                    : 'border-gray-300 dark:border-gray-600 hover:border-green-500'
                }`}
              >
                <ThumbsUp className="h-4 w-4" />
                <span>Yes</span>
              </button>
              <button
                onClick={() => handleFeedback('helpful', false)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                  feedback.helpful === false
                    ? 'border-red-500 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300'
                    : 'border-gray-300 dark:border-gray-600 hover:border-red-500'
                }`}
              >
                <ThumbsDown className="h-4 w-4" />
                <span>No</span>
              </button>
            </div>
          </div>
          
          <div>
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Rating (1-5)
            </p>
            <div className="flex items-center space-x-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => handleFeedback('rating', star)}
                  className={`text-2xl transition-colors ${
                    star <= feedback.rating
                      ? 'text-yellow-400'
                      : 'text-gray-300 dark:text-gray-600'
                  }`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Comments (optional)
            </label>
            <textarea
              value={feedback.comments}
              onChange={(e) => handleFeedback('comments', e.target.value)}
              placeholder="Share your thoughts about this summary..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              rows={3}
            />
          </div>
          
          <button
            onClick={submitFeedback}
            className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
          >
            Submit Feedback
          </button>
        </div>
      </div>
    </div>
  );
};

export default DocumentDetail;