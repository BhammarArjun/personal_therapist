# Socratic AI Chatbot 🧠💬

A philosophical AI companion that embodies the wisdom of Socrates, designed to provide thoughtful guidance through daily conversations while maintaining long-term memory of user interactions.

## ✨ Features

### Core Functionality
- **Socratic Dialogue**: Engages users through guided questioning and philosophical inquiry
- **Persistent Memory**: Intelligently stores and recalls important user information across sessions
- **Cost Tracking**: Real-time monitoring of API usage and associated costs
- **Streaming Responses**: Real-time conversation flow with immediate feedback
- **Smart Memory Filtering**: Advanced guardrails to determine what information is worth preserving

### AI-Powered Capabilities
- **Philosophical Guidance**: Practical wisdom application to real-world challenges
- **Personalized Conversations**: Adapts responses based on stored user context
- **Concern Detection**: Monitors for potentially harmful content or concerning patterns
- **Natural Interaction**: Warm, encouraging presence without AI-specific language

## 🏗️ Architecture & Flow

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │────│   Main Bot       │────│   Memory        │
│                 │    │   (bot.py)       │    │   (memory.json) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Guardrail      │
                       │   (guardrail.py) │
                       └──────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Gemini API     │
                       │   (Response)     │
                       └──────────────────┘
```

### Conversation Flow

1. **Session Initialization**
   - User provides unique ID for personalized experience
   - System loads existing memory for context continuity
   - Socratic system prompt is initialized with user memory

2. **Input Processing**
   - User input is captured and processed
   - Guardrail system evaluates if input contains memory-worthy information
   - Concerning content detection runs in parallel

3. **Memory Management**
   - Important information is extracted and timestamped
   - User-specific memory is updated in JSON storage
   - Context is maintained across conversation turns

4. **AI Response Generation**
   - Gemini 2.0 Flash model generates philosophical responses
   - Streaming output provides real-time interaction
   - Token usage is tracked for cost monitoring

## 🛡️ Smart Guardrails

### Memory Filtering Intelligence
The system uses advanced filtering to determine what information deserves long-term storage:

- **Personal Information**: Names, professions, preferences, goals
- **Important Context**: Relationships, significant events, aspirations
- **Selective Storage**: Only factual and preference data, avoiding assumptions
- **Concern Detection**: Monitors for harmful ideation or crisis indicators

### Safety Considerations
- **Content Monitoring**: Detects abnormal thought patterns or concerning content
- **Crisis Detection**: Flags potential self-harm or dangerous intentions
- **Privacy Protection**: Stores only essential information with user consent
- **Balanced Sensitivity**: Avoids over-triggering on philosophical discussions

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Groq API key (for guardrail processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd socratic-ai-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install google-genai python-dotenv pydantic groq
   ```

3. **Configure environment variables**
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the chatbot**
   ```bash
   python bot.py
   ```

### Usage

1. Enter your unique user ID when prompted
2. Introduce yourself to establish initial context
3. Engage in philosophical dialogue with your AI companion
4. End the session with commands like "quit chat" or "exit chat"

## 💰 Cost Management

The system provides transparent cost tracking:
- **Real-time Monitoring**: Tracks input/output tokens per conversation
- **Usage Statistics**: Displays total API calls and associated costs
- **Cost Breakdown**: Separate tracking for input ($0.10/M tokens) and output ($0.40/M tokens)

## 📁 File Structure

```
├── bot.py              # Main chatbot application
├── guardrail.py        # Memory filtering and safety checks
├── system_prompt.txt   # Socratic personality definition
├── memory.json         # Persistent user memory storage
├── .env               # API keys and environment variables
└── README.md          # Project documentation
```

## 🎯 Key Design Principles

### Philosophical Approach
- **Socratic Method**: Guided questioning to encourage self-discovery
- **Practical Wisdom**: Focus on actionable insights for real-world challenges
- **Encouraging Presence**: Warm, supportive interaction style
- **Meaningful Dialogue**: Purposeful conversations that add value

### Technical Excellence
- **Efficient Memory**: Smart filtering prevents information overload
- **Cost Optimization**: Monitoring tools help manage API expenses
- **Error Handling**: Graceful degradation when API calls fail
- **User Experience**: Streaming responses and clear interaction patterns

---

*"The unexamined life is not worth living."* - Socrates

Ready to embark on a journey of philosophical discovery? Let the river of wisdom flow! 🌊
