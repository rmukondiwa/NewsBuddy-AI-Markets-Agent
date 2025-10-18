# NewsBuddy AI Markets Agent 🤖📈

A comprehensive AI-powered multi-agent system that provides intelligent assistance for market analysis, news sentiment tracking, weather information, and web scraping capabilities. Built with FastAPI, Docker, and modern AI technologies.

![AI Agents Demo](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## Features

### Intelligent Agent System
- **Gateway Agent**: Smart routing system that directs user queries to the most appropriate specialized agent
- **Multi-Agent Architecture**: Modular design with specialized agents for different domains

### Specialized Agents

#### News Sentiment Agent
- Real-time news sentiment analysis for stocks and companies
- Integration with financial markets data
- Powered by GNews API and LangChain
- Provides comprehensive market sentiment reports

#### Markets Agent
- Live financial market data and analysis
- Stock price tracking and historical data
- Market trend analysis
- Powered by Yahoo Finance API

#### Weather Agent
- Current weather conditions and forecasts
- Location-based weather information
- Weather data integration for market analysis

#### Web Scraping Agent
- Intelligent web content extraction
- Automated data collection from websites
- Content analysis and summarization

#### Chat Agent
- General conversational AI capabilities
- Fallback agent for general queries
- Context-aware responses

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Nginx)       │◄───┤   (FastAPI)     │
│   Port: 6083    │    │   Port: 6003    │
└─────────────────┘    └─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Gateway Agent       │
                    └───────────┬───────────┘
                                │
            ┌───────┬───────┬───┴───┬───────┬────────┐
            │       │       │       │       │        │
         ┌──▼──┐ ┌──▼──┐ ┌──▼──┐ ┌──▼──┐ ┌──▼───┐ ┌▼┐
         │News │ │Mkts │ │Wthr │ │Scrp │ │Chat  │ │.│
         │Agent│ │Agent│ │Agent│ │Agent│ │Agent │ │.│
         └─────┘ └─────┘ └─────┘ └─────┘ └──────┘ └─┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- GNews API key (optional, for news features)

### 1. Clone the Repository
```bash
git clone https://github.com/rmukondiwa/NewsBuddy-AI-Markets-Agent.git
cd ai_agents_rtm45
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
APP_NAME=AI Agents System
CORS_ORIGINS=http://localhost:6083,http://127.0.0.1:6083

# Optional (for enhanced news features)
GNEWS_API_KEY=your_gnews_api_key_here
```

### 3. Launch with Docker Compose
```bash
docker-compose up --build
```

### 4. Access the Application
- **Frontend**: http://localhost:6083
- **Backend API**: http://localhost:6003
- **Health Check**: http://localhost:6003/health

## 🛠️ Development

### Project Structure
```
ai_agents_rtm45/
├── docker-compose.yml          # Multi-service orchestration
├── .env                       # Environment configuration
├── README.md                  # Project documentation
├── INSTALL.md                 # Installation guide
├── backend/                   # FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py           # FastAPI application
│       ├── llm.py            # LLM integration
│       └── agents/           # Agent implementations
│           ├── base_agent.py
│           ├── gateway_agent.py
│           ├── news_agent.py
│           ├── markets_agent.py
│           ├── weather_agent.py
│           ├── chat_agent.py
│           └── scraping_agent.py
├── frontend/                  # Static web frontend
│   ├── Dockerfile
│   ├── bin/inject-env.sh
│   └── public/
│       ├── index.html        # Main interface
│       ├── app.js           # Frontend logic
│       └── *.html           # Specialized agent UIs
└── tests/                    # Test suite
    ├── test_newsAgent.py
    ├── test_marketsAgents.py
    └── test_weatherAgent.py
```

### Local Development Setup
1. **Backend Development**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 6000
```

2. **Frontend Development**:
```bash
cd frontend/public
python -m http.server 8080
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_newsAgent.py -v

# Run with coverage
pytest tests/ --cov=backend/app/agents
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /health` - Health check endpoint
- `POST /api/chat` - Main chat interface for all agents

### Example Usage
```bash
# Health check
curl http://localhost:6003/health

# Chat with agents
curl -X POST http://localhost:6003/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the sentiment for AAPL stock today?"}'
```

## Agent Capabilities

### News Sentiment Agent
- **Trigger Words**: "news", "sentiment", "media coverage"
- **Capabilities**: 
  - Real-time news sentiment analysis
  - Company-specific news tracking
  - Market sentiment correlation

### Markets Agent
- **Trigger Words**: "stock", "market", "price", "financial"
- **Capabilities**:
  - Live stock prices
  - Historical market data
  - Financial analysis

### Weather Agent
- **Trigger Words**: "weather", "forecast", "temperature"
- **Capabilities**:
  - Current weather conditions
  - Weather forecasts
  - Location-based weather data

### Scraping Agent
- **Trigger Words**: "scrape", "extract", "website data"
- **Capabilities**:
  - Web content extraction
  - Automated data collection
  - Content summarization

## Dependencies

### Backend Dependencies
- **FastAPI** (0.111.0) - Modern web framework
- **OpenAI** (≥1.40.0) - AI model integration
- **LangChain** (0.3.4) - AI application framework
- **yfinance** (0.2.66) - Financial data
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP client

### Frontend Dependencies
- **Vanilla JavaScript** - No framework dependencies
- **Modern CSS** - Responsive design
- **Nginx** - Web server (in Docker)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for LLM access |
| `APP_NAME` | Yes | Application name |
| `CORS_ORIGINS` | Yes | Allowed CORS origins |
| `GNEWS_API_KEY` | No | GNews API for enhanced news features |

## 🧪 Testing

The project includes comprehensive test coverage for all agents:

- **Unit Tests**: Individual agent functionality
- **Integration Tests**: Agent interaction testing
- **API Tests**: Endpoint validation

Run tests with detailed output:
```bash
pytest tests/ -v --tb=short
```

## Deployment

### Docker Production Deployment
```bash
# Build and run in production mode
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Health Monitoring
- Backend health: `http://your-domain:6003/health`
- Container health checks included in docker-compose.yml

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Agents
1. Create new agent in `backend/app/agents/`
2. Inherit from `BaseAgent`
3. Add to `GatewayAgent.agents` dictionary
4. Update gateway agent routing logic
5. Add corresponding tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.