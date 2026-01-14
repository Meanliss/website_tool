import React from 'react';
import ToolCard from './ToolCard';
import './ToolGrid.css';

function ToolGrid({ tools, columns, onToolClick }) {
  return (
    <div 
      className="tool-grid" 
      style={{ 
        gridTemplateColumns: `repeat(${columns}, 1fr)` 
      }}
    >
      {tools.map(tool => (
        <ToolCard
          key={tool.id}
          tool={tool}
          onClick={() => onToolClick(tool)}
        />
      ))}
    </div>
  );
}

export default ToolGrid;
