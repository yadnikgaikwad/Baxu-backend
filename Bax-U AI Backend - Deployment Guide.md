# Bax-U AI Backend - Deployment Guide

## Quick Deployment Options

### Option 1: Local Development
```bash
cd bax-u-ai-backend
source venv/bin/activate
export OPENAI_API_KEY="your_key_here"
python src/main.py
```

### Option 2: Production Deployment with Gunicorn
```bash
cd bax-u-ai-backend
source venv/bin/activate
pip install gunicorn
export OPENAI_API_KEY="your_key_here"
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Option 3: Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

Build and run:
```bash
docker build -t bax-u-backend .
docker run -p 5000:5000 -e OPENAI_API_KEY="your_key" bax-u-backend
```

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_API_BASE`: OpenAI API base URL (default: https://api.openai.com/v1)

Optional:
- `FLASK_ENV`: Environment (development/production)
- `PORT`: Port number (default: 5000)
- `SECRET_KEY`: Flask secret key for sessions

## Frontend Integration Points

### Key Integration Steps:

1. **Update your Next.js API calls** to point to your backend:
   ```javascript
   const response = await fetch('/api/chat', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ message: userMessage })
   });
   ```

2. **Handle the response** in your chat component:
   ```javascript
   const data = await response.json();
   if (data.status === 'success') {
     setMessages(prev => [...prev, { text: data.response, isUser: false }]);
   }
   ```

3. **Add error handling** for network issues and API errors.

4. **Implement conversation management** using the `conversation_id` field.

## Testing Your Integration

1. Start the backend server
2. Open your Next.js frontend
3. Try sending messages through the chat interface
4. Verify responses are coming from the AI agent
5. Test error scenarios (network issues, invalid inputs)

## Performance Optimization

- Use connection pooling for OpenAI API calls
- Implement response caching for common queries
- Add rate limiting to prevent abuse
- Use async processing for better performance

## Security Considerations

- Never expose your OpenAI API key in frontend code
- Implement proper input validation
- Add rate limiting to prevent abuse
- Use HTTPS in production
- Validate and sanitize all user inputs

## Monitoring and Logging

Add logging to track usage and debug issues:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log all chat requests
logger.info(f"Chat request: {user_message}")
logger.info(f"AI response: {ai_response}")
```

Your backend is now ready for integration with your Next.js frontend!

