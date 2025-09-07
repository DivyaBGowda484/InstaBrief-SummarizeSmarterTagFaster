import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, Settings, Play, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const NewDocument = () => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [summarySettings, setSummarySettings] = useState({
    algorithm: 'textrank',
    maxLength: 150,
    language: 'en'
  });
  const [isProcessing, setIsProcessing] = useState(false);

  const onDrop = (acceptedFiles) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      status: 'pending',
      progress: 0
    }));
    
    setUploadedFiles(prev => [...prev, ...newFiles]);
    toast.success(`${acceptedFiles.length} file(s) uploaded successfully`);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'text/plain': ['.txt']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: true
  });

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const processFiles = async () => {
    if (uploadedFiles.length === 0) {
      toast.error('Please upload at least one file');
      return;
    }

    setIsProcessing(true);
    
    try {
      // Simulate processing
      for (let i = 0; i < uploadedFiles.length; i++) {
        setUploadedFiles(prev => 
          prev.map(file => 
            file.id === uploadedFiles[i].id 
              ? { ...file, status: 'processing', progress: 50 }
              : file
          )
        );
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setUploadedFiles(prev => 
          prev.map(file => 
            file.id === uploadedFiles[i].id 
              ? { ...file, status: 'completed', progress: 100 }
              : file
          )
        );
      }
      
      toast.success('All files processed successfully!');
    } catch (error) {
      toast.error('Processing failed. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Upload New Document
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Upload your documents to get AI-powered summaries and smart tags
        </p>
      </div>

      {/* Upload Area */}
      <div className="mb-8">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors duration-200 ${
            isDragActive
              ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-purple-400 dark:hover:border-purple-500'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
          </p>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            or click to browse files
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-500">
            Supports PDF, DOCX, PPTX, and TXT files (max 10MB each)
          </p>
        </div>
      </div>

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Uploaded Files ({uploadedFiles.length})
          </h3>
          <div className="space-y-3">
            {uploadedFiles.map((file) => (
              <motion.div
                key={file.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-center space-x-3">
                  <FileText className="h-8 w-8 text-blue-500" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {file.file.name}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {(file.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {file.status === 'processing' && (
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 border-2 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {file.progress}%
                      </span>
                    </div>
                  )}
                  
                  {file.status === 'completed' && (
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm text-green-600 dark:text-green-400">
                        Completed
                      </span>
                    </div>
                  )}
                  
                  <button
                    onClick={() => removeFile(file.id)}
                    className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Summary Settings */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Summary Settings
          </h3>
          <Settings className="h-5 w-5 text-gray-400" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Algorithm
            </label>
            <select
              value={summarySettings.algorithm}
              onChange={(e) => setSummarySettings(prev => ({ ...prev, algorithm: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
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
              value={summarySettings.maxLength}
              onChange={(e) => setSummarySettings(prev => ({ ...prev, maxLength: parseInt(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Language
            </label>
            <select
              value={summarySettings.language}
              onChange={(e) => setSummarySettings(prev => ({ ...prev, language: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
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

      {/* Action Buttons */}
      <div className="flex justify-end space-x-4">
        <button
          onClick={processFiles}
          disabled={uploadedFiles.length === 0 || isProcessing}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
        >
          {isProcessing ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Processing...</span>
            </>
          ) : (
            <>
              <Play className="h-4 w-4" />
              <span>Process Documents</span>
            </>
          )}
        </button>
        
        <button className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 flex items-center space-x-2">
          <Download className="h-4 w-4" />
          <span>Download All</span>
        </button>
      </div>
    </div>
  );
};

export default NewDocument;