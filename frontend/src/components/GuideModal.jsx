import React, { useEffect } from 'react';
import './GuideModal.css';

function GuideModal({ tool, onClose }) {
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [onClose]);

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <div className="modal-header">
          <h2>
            <span className="modal-icon">{tool.icon}</span>
            {tool.name}
          </h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        
        <div className="modal-body">
          <div 
            className="guide-content"
            dangerouslySetInnerHTML={{ 
              __html: parseMarkdown(tool.guide_content) 
            }}
          />
        </div>
        
        <div className="modal-footer">
          <button className="close-button" onClick={onClose}>
            Close (ESC)
          </button>
        </div>
      </div>
    </div>
  );
}

// Simple markdown parser (basic support)
function parseMarkdown(text) {
  if (!text) return '';
  
  return text
    // Headers
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    // Code blocks
    .replace(/```(.*?)```/gis, '<pre><code>$1</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank">$1</a>')
    // Line breaks
    .replace(/\n/gim, '<br/>');
}

export default GuideModal;
