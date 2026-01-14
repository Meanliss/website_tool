import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ToolGrid from './components/ToolGrid';
import GuideModal from './components/GuideModal';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [tools, setTools] = useState([]);
  const [filteredTools, setFilteredTools] = useState([]);
  const [categories, setCategories] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedTool, setSelectedTool] = useState(null);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [toolType, setToolType] = useState('all'); // all, external, internal
  const [viewMode, setViewMode] = useState(4); // number of columns

  // Fetch initial data
  useEffect(() => {
    fetchTools();
    fetchCategories();
    fetchStats();
  }, []);

  // Apply filters
  useEffect(() => {
    applyFilters();
  }, [tools, searchQuery, selectedCategories, selectedTags, toolType]);

  const fetchTools = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/tools`);
      setTools(response.data);
      setFilteredTools(response.data);
    } catch (error) {
      console.error('Error fetching tools:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/categories`);
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const applyFilters = () => {
    let filtered = [...tools];

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(tool =>
        tool.name.toLowerCase().includes(query) ||
        tool.description.toLowerCase().includes(query) ||
        tool.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }

    // Category filter
    if (selectedCategories.length > 0) {
      filtered = filtered.filter(tool =>
        selectedCategories.includes(tool.category)
      );
    }

    // Tag filter
    if (selectedTags.length > 0) {
      filtered = filtered.filter(tool =>
        selectedTags.some(tag => tool.tags.includes(tag))
      );
    }

    // Type filter
    if (toolType === 'external') {
      filtered = filtered.filter(tool => tool.is_external);
    } else if (toolType === 'internal') {
      filtered = filtered.filter(tool => !tool.is_external);
    }

    setFilteredTools(filtered);
  };

  const handleToolClick = (tool) => {
    if (tool.guide_content) {
      setSelectedTool(tool);
    } else if (tool.url) {
      window.open(tool.url, '_blank');
    }
  };

  const handleCloseGuide = () => {
    setSelectedTool(null);
  };

  return (
    <div className="app">
      <Sidebar
        categories={categories}
        stats={stats}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        selectedCategories={selectedCategories}
        setSelectedCategories={setSelectedCategories}
        toolType={toolType}
        setToolType={setToolType}
        viewMode={viewMode}
        setViewMode={setViewMode}
        onReload={fetchTools}
      />
      
      <main className="main-content">
        <Header />
        
        <div className="tools-container">
          {filteredTools.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <h3>No tools found</h3>
              <p>Try adjusting your filters or search query</p>
            </div>
          ) : (
            <>
              <div className="results-count">
                Found <strong>{filteredTools.length}</strong> tool(s)
              </div>
              <ToolGrid
                tools={filteredTools}
                columns={viewMode}
                onToolClick={handleToolClick}
              />
            </>
          )}
        </div>
      </main>

      {selectedTool && (
        <GuideModal
          tool={selectedTool}
          onClose={handleCloseGuide}
        />
      )}
    </div>
  );
}

export default App;
