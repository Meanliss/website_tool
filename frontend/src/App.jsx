import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ToolGrid from './components/ToolGrid';
import GuideModal from './components/GuideModal';
import './App.css';

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
  }, []);

  // Calculate categories and stats after tools are loaded
  useEffect(() => {
    if (tools.length > 0) {
      calculateCategories();
      calculateStats();
    }
  }, [tools]);

  // Apply filters
  useEffect(() => {
    applyFilters();
  }, [tools, searchQuery, selectedCategories, selectedTags, toolType]);

  const fetchTools = async () => {
    try {
      // Fetch from local static JSON file
      const response = await fetch('/tools.json');
      const data = await response.json();
      setTools(data);
      setFilteredTools(data);
    } catch (error) {
      console.error('Error fetching tools:', error);
      setTools([]);
      setFilteredTools([]);
    }
  };

  const calculateCategories = () => {
    // Extract unique categories from tools
    const uniqueCategories = [...new Set(tools.map(t => t.category))].map(cat => ({
      value: cat,
      display_name: cat.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
    }));
    setCategories(uniqueCategories);
  };

  const calculateStats = () => {
    // Calculate stats from tools data
    const totalTools = tools.length;
    const externalTools = tools.filter(t => t.is_external).length;
    const internalTools = totalTools - externalTools;
    const categoryCount = {};
    
    tools.forEach(t => {
      categoryCount[t.category] = (categoryCount[t.category] || 0) + 1;
    });
    
    setStats({
      total_tools: totalTools,
      total_categories: Object.keys(categoryCount).length,
      tools_by_category: categoryCount,
      external_tools: externalTools,
      internal_tools: internalTools
    });
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
