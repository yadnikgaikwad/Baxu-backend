# Bax-U AI Customer Support Backend

A complete backend solution for integrating AI customer support into your Bax-U e-commerce demo. Built with Flask and OpenAI GPT-4o API.

## 🚀 Quick Start

1. **Extract the solution:**
   ```bash
   unzip bax-u-backend-solution.zip
   cd bax-u-ai-backend
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the server:**
   ```bash
   python src/main.py
   ```

The server will start on `http://localhost:5000`

## 📁 What's Included

- **`src/`** - Complete Flask backend application
- **`integration_guide.md`** - Detailed frontend integration guide
- **`deployment_guide.md`** - Production deployment instructions
- **`system_prompt.txt`** - AI agent system prompt for Bax-U brand
- **`backend_architecture.md`** - Technical architecture overview

## 🔧 API Endpoints

- **POST `/api/chat`** - Send messages to AI agent
- **GET `/api/health`** - Health check
- **GET `/api/config`** - Frontend configuration
- **DELETE `/api/conversations/{id}`** - Clear conversation

## 🎯 Frontend Integration

### React Component Example:
```jsx
const sendMessage = async (message) => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  
  const data = await response.json();
  if (data.status === 'success') {
    // Display AI response: data.response
  }
};
```

## 🔐 Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key

Optional:
- `OPENAI_API_BASE` - API base URL (default: https://api.openai.com/v1)
- `FLASK_ENV` - Environment (development/production)
- `PORT` - Port number (default: 5000)

## 🚀 Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## 📖 Documentation

- **`integration_guide.md`** - Complete frontend integration guide with React examples
- **`deployment_guide.md`** - Production deployment and scaling guide
- **`backend_architecture.md`** - Technical architecture and design decisions

## 🎨 Features

- ✅ Fast, optimized responses (< 2 seconds)
- ✅ Conversation memory management
- ✅ Brand-specific AI personality for Bax-U
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive error handling
- ✅ Production-ready architecture
- ✅ Rate limiting and security features
- ✅ Mobile-responsive chat interface

## 🤖 AI Agent Capabilities

The AI agent is specifically trained for Bax-U and can:
- Answer product questions about posture correctors and activewear
- Provide sizing and fit guidance
- Explain benefits and features
- Handle customer support inquiries
- Maintain brand voice and values
- Guide customers to relevant products

## 🔧 Customization

To modify the AI agent's behavior:
1. Edit `src/routes/chat.py` - Update the system prompt
2. Adjust response parameters (temperature, max_tokens)
3. Add custom business logic for specific use cases

## 📞 Support

For integration help or questions:
1. Check the `integration_guide.md` for detailed examples
2. Review the `deployment_guide.md` for production setup
3. Test using the included HTML interface at `http://localhost:5000`

## 🏗️ Architecture

- **Backend**: Flask with OpenAI GPT-4o integration
- **Database**: SQLite (easily replaceable)
- **CORS**: Enabled for all origins
- **Security**: Input validation, rate limiting ready
- **Performance**: Optimized for sub-2-second responses

Your AI customer support agent is ready to integrate with your Next.js frontend!

