import React, { useState, useEffect } from 'react';
import { Search as SearchIcon, Filter, SortAsc, Grid, List, X } from 'lucide-react';
import { motion } from 'framer-motion';

const Search = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [filters, setFilters] = useState({
    fileType: 'all',
    dateRange: 'all',
    tags: []
  });
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('relevance');
  const [isLoading, setIsLoading] = useState(false);

  // Mock search results
  const mockResults = [
    {
      id: '1',
      title: 'AI and Machine Learning in Healthcare',
      summary: 'This document discusses the transformative impact of AI and Machine Learning in healthcare...',
      tags: ['AI', 'Healthcare', 'Machine Learning'],
      fileType: 'pdf',
      createdAt: '2024-01-15',
      relevance: 0.95
    },
    {
      id: '2',
      title: 'The Future of Renewable Energy',
      summary: 'An analysis of renewable energy technologies and their potential to reshape the global energy landscape...',
      tags: ['Energy', 'Renewable', 'Sustainability'],
      fileType: 'docx',
      createdAt: '2024-01-14',
      relevance: 0.87
    },
    {
      id: '3',
      title: 'Blockchain Technology Applications',
      summary: 'Exploring various applications of blockchain technology beyond cryptocurrency...',
      tags: ['Blockchain', 'Technology', 'Cryptocurrency'],
      fileType: 'pptx',
      createdAt: '2024-01-13',
      relevance: 0.82
    }
  ];

  useEffect(() => {
    if (searchQuery) {
      setIsLoading(true);
      // Simulate search delay
      setTimeout(() => {
        setSearchResults(mockResults);
        setIsLoading(false);
      }, 500);
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const handleSearch = (e) => {
    e.preventDefault();
    // Search logic would go here
  };

  const clearFilters = () => {
    setFilters({
      fileType: 'all',
      dateRange: 'all',
      tags: []
    });
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Search Documents
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Find your documents using keywords, tags, or semantic search
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-8">
        <form onSubmit={handleSearch} className="relative">
          <div className="relative">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search documents, summaries, or tags..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Filters and Controls */}
      <div className="mb-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          {/* Filters */}
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <Filter className="h-4 w-4" />
              <span>Filters</span>
            </button>
            
            <select
              value={filters.fileType}
              onChange={(e) => setFilters(prev => ({ ...prev, fileType: e.target.value }))}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="all">All File Types</option>
              <option value="pdf">PDF</option>
              <option value="docx">DOCX</option>
              <option value="pptx">PPTX</option>
              <option value="txt">TXT</option>
            </select>
            
            <select
              value={filters.dateRange}
              onChange={(e) => setFilters(prev => ({ ...prev, dateRange: e.target.value }))}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="all">All Time</option>
              <option value="today">Today</option>
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="year">This Year</option>
            </select>
            
            <button
              onClick={clearFilters}
              className="text-sm text-purple-600 hover:text-purple-700 transition-colors"
            >
              Clear Filters
            </button>
          </div>

          {/* View Controls */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="relevance">Relevance</option>
                <option value="date">Date</option>
                <option value="title">Title</option>
                <option value="fileType">File Type</option>
              </select>
            </div>
            
            <div className="flex items-center space-x-1 border border-gray-300 dark:border-gray-600 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-600' : 'text-gray-400 hover:text-gray-600'}`}
              >
                <Grid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-600' : 'text-gray-400 hover:text-gray-600'}`}
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Search Results */}
      <div className="mb-8">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>
        ) : searchResults.length > 0 ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {searchResults.length} results found
              </p>
              <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                <SortAsc className="h-4 w-4" />
                <span>Sorted by {sortBy}</span>
              </div>
            </div>
            
            <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}>
              {searchResults.map((result, index) => (
                <motion.div
                  key={result.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow cursor-pointer"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                        {result.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-3">
                        {result.summary}
                      </p>
                    </div>
                    <span className="ml-2 px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded">
                      {result.fileType.toUpperCase()}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex flex-wrap gap-1">
                      {result.tags.map((tag, tagIndex) => (
                        <span
                          key={tagIndex}
                          className="px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs rounded"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-500">
                      {result.createdAt}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        ) : searchQuery ? (
          <div className="text-center py-12">
            <SearchIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No results found
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Try adjusting your search terms or filters
            </p>
          </div>
        ) : (
          <div className="text-center py-12">
            <SearchIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Start searching
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Enter a search term to find your documents
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;