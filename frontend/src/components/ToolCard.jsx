import React from 'react';
import './ToolCard.css';

function ToolCard({ tool, onClick }) {
  const buttonText = tool.guide_content ? '📖 Guide' : '🔗 Open';
  
  return (
    <div className="tool-card" onClick={onClick}>
      <div className="tool-icon">{tool.icon}</div>
      <h3 className="tool-title">{tool.name}</h3>
      <p className="tool-description">{tool.description}</p>
      
      {tool.tags && tool.tags.length > 0 && (
        <div className="tool-tags">
          {tool.tags.slice(0, 3).map((tag, index) => (
            <span key={index} className="tool-tag">{tag}</span>
          ))}
        </div>
      )}
      
      <button className="tool-button">
        {buttonText}
      </button>
    </div>
  );
}

export default ToolCard;
