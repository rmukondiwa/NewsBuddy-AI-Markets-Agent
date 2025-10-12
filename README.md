# FinanceBro AI Agent
## Name
Raphael Mukondiwa


### Project Purpose
- Phase 1: 
    -Adding a Markets Agent, called FinanceBro. This agent uses yahoo finance API to provide stock market information. Then the stock information, user input, and system instructions are sent to the GPT-O4-Mini model to generate a response.
- Phase 2:
   - Added a Weather Agent, called WeatherBro. This agent uses the API-Ninjas weather API to provide current weather information for a given city. The weather information, user input, and system instructions are sent to the GPT-4-Mini model to generate a response.
   - Added a News Sentiment Agent, called NewsBro. This agent uses the GNews API and Yfinance to provide current news articles for a given topic. The news articles, user input, and system instructions are sent to the GPT-4-Mini model to generate a response.


### Timeline

 * Start Date: September 25, 2025

 * Finish Date: October 12, 2025

 * Hours Spent: ~25 hours



### Attributions

 * Students with whom you collaborated:
    - Benita Besa (Helped with debugging issues with the frontend and backend connection, as well as issues deploying on my docker container locally)

 * Resources used for learning (including AI assistance):
    - CHATGPT with yfinance implementation and command line commands for running locally
    - YFinance python documentation online
    - Github Copilot assisted with understanding the initial ai agent codebase
 
 * Resources used directly (including AI assistance, others' code/images, etc.):
    - CHATGPT with yfinance implementation
    - CHATGPT helped with fixing my pipeline yaml bugs
    - YFinance python documentation online
    - Github Copilot assisted with debugging
    - Github Copilot assisted with writing some of the tests
    - Github Copilot assisted with writing documentation and some logs


### Running the Program

 * How to compile or deploy and run the program:
    - cp .env.example .env
    - Modify OpenAI API key, Model ID, and host in .env file
    - Modify the frontend/constants.js file to include relevant backend urls

    - Deploying on docker
        - docker compose up --build
    
    - Enter the URL given in the Docker logs in your browser

    - To run tests locally:
        - Enter pytest -v tests/ in terminal

 * Information about using the program (like data files needed, inputs, etc.):
    - The program utilizes the Yahoo Finance API to get stock market information. No additional data files are needed. (yfinance)
    - For lint testing, you will need to have flake8 installed. You can install it using pip:
        - pip install flake8
        - flake8 frontned/ backend/
    - For security checks, you will need to have bandit installed. You can install it using pip:
        - pip install bandit
        - bandit -r frontend/ backend/

 * Interesting data files:



### Notes

 * Features implemented:
    - A Markets AI Agent
    - A Weather AI Agent
    - A News Sentiment AI Agent
    - Backend logs
    - Tests for the Markets Agent
    - Tests for the Weather Agent
    - Tests for the News Agent
    - Added Constants file for backend urls

 * Features unimplemented:

 * Noteworthy Features:

 * Known Bugs:
    - Sometimes the agent won't respond with a stock price, but will instead respond with a general market overview. This is likely due to a rate limiting issue with the Yahoo Finance API. I tried to mitigate this by adding system instructions to the agent, but it is not foolproof. The only solution is to try again after some time has passed.
    - For some reason the GPT doesn't do well with a follow up questions related to the original question. For example, if the user asks "What is the stock price of AAPL?" and then follows up with "Why is it so high", the agent will not be able to answer the follow up question. This is likely due to the fact that the agent is not able to retain context from previous interactions. A possible solution would be to implement a memory system for the agent, but this is beyond the scope of this project right now.

 * Decisions, assumptions, or responses to user feedback:
    - For the purposes to deliver Phase1 on time, I decided to keep using yFinance library. Also slightly due to the amount of time I put into understanding it (sunk cost fallacy). 
    - My goal for Phase2 is to explore other api tools like Polygon and Alpaca for the next phase, which are more scalable and won't have rate limiting issues.

### Assignment Impressions
- I've learned a lot about how to build AI agents and using multiple APIs to get data. I've also learned a lot about how to deploy a full stack application using Docker and FastAPI. Overall, I think this was a great learning experience and I'm excited to continue building on what I've learned in future projects.


