import React from 'react';
import './Sidebar.css';

function Sidebar({
  categories,
  stats,
  searchQuery,
  setSearchQuery,
  selectedCategories,
  setSelectedCategories,
  toolType,
  setToolType,
  viewMode,
  setViewMode,
  onReload
}) {
  const toggleCategory = (categoryValue) => {
    if (selectedCategories.includes(categoryValue)) {
      setSelectedCategories(selectedCategories.filter(c => c !== categoryValue));
    } else {
      setSelectedCategories([...selectedCategories, categoryValue]);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>🛠️</h2>
        <h3>Tool Hub</h3>
        <p>Centralized tools</p>
      </div>

      <div className="sidebar-section">
        {stats && (
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">{stats.total_tools}</div>
              <div className="stat-label">Tools</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{stats.total_categories}</div>
              <div className="stat-label">Categories</div>
            </div>
          </div>
        )}
      </div>

      <div className="sidebar-divider"></div>

      <div className="sidebar-section">
        <h4>🔍 Search</h4>
        <input
          type="text"
          className="search-input"
          placeholder="Search tools..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="sidebar-divider"></div>

      <div className="sidebar-section">
        <h4>📁 Categories</h4>
        <div className="category-list">
          {categories.map(category => (
            <label key={category.value} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedCategories.includes(category.value)}
                onChange={() => toggleCategory(category.value)}
              />
              <span>{category.display_name}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="sidebar-divider"></div>

      <div className="sidebar-section">
        <h4>🔗 Type</h4>
        <div className="radio-group">
          <label className="radio-label">
            <input
              type="radio"
              name="toolType"
              value="all"
              checked={toolType === 'all'}
              onChange={(e) => setToolType(e.target.value)}
            />
            <span>All</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              name="toolType"
              value="external"
              checked={toolType === 'external'}
              onChange={(e) => setToolType(e.target.value)}
            />
            <span>External Links</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              name="toolType"
              value="internal"
              checked={toolType === 'internal'}
              onChange={(e) => setToolType(e.target.value)}
            />
            <span>Internal Guides</span>
          </label>
        </div>
      </div>

      <div className="sidebar-divider"></div>

      <div className="sidebar-section">
        <h4>⚙️ Settings</h4>
        <button className="reload-button" onClick={onReload}>
          🔄 Reload Tools
        </button>
        
        <div className="view-mode-selector">
          <label className="view-mode-label">View Mode</label>
          <select 
            className="view-mode-select"
            value={viewMode}
            onChange={(e) => setViewMode(Number(e.target.value))}
          >
            <option value={4}>Compact (4 cols)</option>
            <option value={3}>Grid (3 cols)</option>
            <option value={2}>Grid (2 cols)</option>
            <option value={1}>List</option>
          </select>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
