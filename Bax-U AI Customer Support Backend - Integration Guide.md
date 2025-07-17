# Bax-U AI Customer Support Backend - Integration Guide

## Overview

This comprehensive guide will walk you through integrating the Bax-U AI customer support backend with your Next.js frontend. The backend is built with Flask and integrates seamlessly with OpenAI's GPT-4o API to provide intelligent customer support for your Bax-U demo.

## Table of Contents

1. [Backend Setup](#backend-setup)
2. [API Endpoints](#api-endpoints)
3. [Frontend Integration](#frontend-integration)
4. [Error Handling](#error-handling)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

## Backend Setup

### Prerequisites

- Python 3.11+
- OpenAI API key
- Virtual environment (included in the project)

### Installation Steps

1. **Navigate to the backend directory:**
   ```bash
   cd bax-u-ai-backend
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies (already done):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_API_BASE=https://api.openai.com/v1
   FLASK_ENV=production
   PORT=5000
   ```

5. **Start the server:**
   ```bash
   python src/main.py
   ```

The server will run on `http://localhost:5000` and is configured to accept requests from any origin (CORS enabled).

## API Endpoints

### 1. Chat Endpoint

**URL:** `POST /api/chat`

**Purpose:** Send customer messages and receive AI responses

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "I'm looking for posture support for my back pain",
  "conversation_id": "optional-uuid-string",
  "user_context": {
    "page": "homepage",
    "product_interest": "posture_corrector"
  }
}
```

**Response (Success):**
```json
{
  "response": "I understand you're dealing with back pain. Bax-U's posture-correcting activewear is specifically designed to help with that...",
  "conversation_id": "uuid-string",
  "timestamp": "2025-07-16T16:42:20.123456",
  "status": "success"
}
```

**Response (Error):**
```json
{
  "error": "Message is required",
  "status": "error"
}
```

### 2. Health Check Endpoint

**URL:** `GET /api/health`

**Purpose:** Check if the backend service is running

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-16T16:42:20.123456",
  "service": "Bax-U AI Customer Support"
}
```

### 3. Configuration Endpoint

**URL:** `GET /api/config`

**Purpose:** Get frontend configuration settings

**Response:**
```json
{
  "max_message_length": 1000,
  "typing_delay": 500,
  "brand_name": "Bax-U",
  "welcome_message": "Hi! I'm here to help you with any questions about Bax-U products. How can I assist you today?"
}
```

### 4. Clear Conversation Endpoint

**URL:** `DELETE /api/conversations/{conversation_id}`

**Purpose:** Clear a specific conversation history

**Response:**
```json
{
  "status": "success",
  "message": "Conversation cleared"
}
```

## Frontend Integration

### React Component Example

Here's how to integrate the backend with your Next.js/React frontend:

```jsx
// components/ChatInterface.jsx
import { useState, useEffect, useRef } from 'react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [config, setConfig] = useState(null);
  const messagesEndRef = useRef(null);

  // Load configuration on component mount
  useEffect(() => {
    fetchConfig();
    // Add welcome message
    setMessages([{
      id: Date.now(),
      text: "Hi! I'm here to help you with any questions about Bax-U products. How can I assist you today?",
      isUser: false,
      timestamp: new Date().toISOString()
    }]);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchConfig = async () => {
    try {
      const response = await fetch('/api/config');
      const data = await response.json();
      setConfig(data);
    } catch (error) {
      console.error('Failed to fetch config:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: conversationId,
          user_context: {
            page: window.location.pathname,
            product_interest: getProductInterest()
          }
        })
      });

      const data = await response.json();

      if (data.status === 'success') {
        setConversationId(data.conversation_id);
        
        const aiMessage = {
          id: Date.now() + 1,
          text: data.response,
          isUser: false,
          timestamp: data.timestamp
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        // Handle error
        const errorMessage = {
          id: Date.now() + 1,
          text: data.error || 'Sorry, something went wrong. Please try again.',
          isUser: false,
          timestamp: new Date().toISOString(),
          isError: true
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Network error. Please check your connection and try again.',
        isUser: false,
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const getProductInterest = () => {
    // Logic to determine user's product interest based on current page
    const path = window.location.pathname;
    if (path.includes('men')) return 'mens_products';
    if (path.includes('women')) return 'womens_products';
    if (path.includes('posture')) return 'posture_corrector';
    return 'general';
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>Bax-U Support</h3>
      </div>
      
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.isUser ? 'user-message' : 'ai-message'} ${message.isError ? 'error-message' : ''}`}
          >
            <div className="message-content">
              {message.text}
            </div>
            <div className="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message ai-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          maxLength={config?.max_message_length || 1000}
          disabled={isLoading}
          rows={1}
        />
        <button
          onClick={sendMessage}
          disabled={!inputMessage.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
```

### CSS Styles

```css
/* styles/ChatInterface.module.css */
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 500px;
  width: 350px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.chat-header {
  padding: 16px;
  background: #007bff;
  color: white;
  border-radius: 12px 12px 0 0;
  text-align: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  word-wrap: break-word;
}

.user-message {
  align-self: flex-end;
}

.user-message .message-content {
  background: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 18px 18px 4px 18px;
}

.ai-message .message-content {
  background: #f1f3f4;
  color: #333;
  padding: 8px 12px;
  border-radius: 18px 18px 18px 4px;
}

.error-message .message-content {
  background: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

.message-timestamp {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
  text-align: right;
}

.ai-message .message-timestamp {
  text-align: left;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 12px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.chat-input {
  display: flex;
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  gap: 8px;
}

.chat-input textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 8px 16px;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  outline: none;
  max-height: 100px;
}

.chat-input textarea:focus {
  border-color: #007bff;
}

.send-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: background 0.2s;
}

.send-button:hover:not(:disabled) {
  background: #0056b3;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .chat-interface {
    width: 100%;
    height: 400px;
  }
}
```

### Integration in Your Main Page

```jsx
// pages/index.js or your main component
import ChatInterface from '../components/ChatInterface';

export default function HomePage() {
  return (
    <div className="homepage">
      {/* Your existing Bax-U homepage content */}
      <div className="hero-section">
        {/* Hero content */}
      </div>
      
      <div className="products-section">
        {/* Products content */}
      </div>
      
      {/* Chat interface positioned on the right side */}
      <div className="chat-widget">
        <ChatInterface />
      </div>
    </div>
  );
}
```

### Positioning the Chat Widget

```css
/* Position the chat widget on the right side */
.chat-widget {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}

/* Alternative: Embedded in the page layout */
.homepage {
  display: flex;
  gap: 20px;
}

.main-content {
  flex: 1;
}

.chat-widget {
  width: 350px;
  position: sticky;
  top: 20px;
  height: fit-content;
}
```

## Error Handling

### Backend Error Responses

The backend returns standardized error responses:

```json
{
  "error": "Error message",
  "status": "error"
}
```

Common error scenarios:
- **400**: Invalid request (missing message, message too long)
- **503**: OpenAI API unavailable
- **500**: Internal server error

### Frontend Error Handling

```jsx
const handleApiError = (error, data) => {
  let errorMessage = 'Something went wrong. Please try again.';
  
  if (data?.error) {
    errorMessage = data.error;
  } else if (error.name === 'TypeError') {
    errorMessage = 'Network error. Please check your connection.';
  }
  
  // Display error to user
  setMessages(prev => [...prev, {
    id: Date.now(),
    text: errorMessage,
    isUser: false,
    timestamp: new Date().toISOString(),
    isError: true
  }]);
};
```

## Testing

### Manual Testing

1. **Start the backend server:**
   ```bash
   cd bax-u-ai-backend
   source venv/bin/activate
   python src/main.py
   ```

2. **Test the health endpoint:**
   ```bash
   curl http://localhost:5000/api/health
   ```

3. **Test the chat endpoint:**
   ```bash
   curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me about Bax-U products"}'
   ```

### Automated Testing

Create a test file for your frontend:

```jsx
// __tests__/ChatInterface.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatInterface from '../components/ChatInterface';

// Mock fetch
global.fetch = jest.fn();

describe('ChatInterface', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('sends message and displays response', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        status: 'success',
        response: 'Hello! How can I help you?',
        conversation_id: 'test-id',
        timestamp: new Date().toISOString()
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');
    
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
    });
  });
});
```

## Deployment

### Environment Variables for Production

```env
OPENAI_API_KEY=your_production_openai_key
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=production
PORT=5000
SECRET_KEY=your_secure_secret_key
```

### Production Considerations

1. **Use a production WSGI server** (like Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. **Set up proper logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

3. **Implement rate limiting:**
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address
   
   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
   )
   ```

4. **Add request validation:**
   ```python
   from flask import request
   from werkzeug.exceptions import BadRequest
   
   @chat_bp.before_request
   def validate_request():
       if request.method == 'POST':
           if not request.is_json:
               raise BadRequest('Content-Type must be application/json')
   ```

## Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Ensure `flask-cors` is installed and configured
   - Check that `CORS(app, origins="*")` is set

2. **OpenAI API Errors:**
   - Verify API key is correct
   - Check API quota and billing
   - Ensure proper error handling for API failures

3. **Connection Issues:**
   - Verify server is running on correct port
   - Check firewall settings
   - Ensure frontend is making requests to correct URL

4. **Performance Issues:**
   - Implement connection pooling for OpenAI API
   - Add response caching for common queries
   - Use async processing for better performance

### Debug Mode

Enable debug mode for development:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Logging

Add comprehensive logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    logger.info(f"Received chat request from {request.remote_addr}")
    # ... rest of the function
```

This integration guide provides everything you need to successfully connect your Next.js frontend with the Bax-U AI customer support backend. The system is designed to be fast, reliable, and provide an excellent user experience for your demo clients.

