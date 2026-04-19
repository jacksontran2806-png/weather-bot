# 🌤️ Automated Weather Bot

A Python-based weather notification system that fetches real-time weather data and sends daily email reports. Built to learn API integration, email automation, and CI/CD pipelines.

## 🚀 Features

- Fetches current weather data from OpenWeatherMap API
- Sends formatted email reports via Gmail SMTP
- Automated daily execution using GitHub Actions
- Secure credential management with environment variables
- Error handling for invalid cities and API failures
- Command-line interface for manual queries

## 🛠️ Technologies Used

- **Python 3.14** - Core programming language
- **OpenWeatherMap API** - Weather data source
- **Gmail SMTP** - Email delivery
- **GitHub Actions** - Automated scheduling (cron jobs)
- **python-dotenv** - Environment variable management
- **requests** - HTTP API calls

## 📋 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/jacksontran2806-png/weather-bot.git
cd weather-bot
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file:
OPENWEATHER_API_KEY=your_api_key_here
EMAIL_PASSWORD=your_gmail_app_password_here

### 5. Run manually
```bash
python main.py "Ho Chi Minh City"
python main.py London
python main.py Sydney
```

## 🤖 Automated Scheduling

The bot runs automatically every day at 8:00 AM (Vietnam time) via GitHub Actions.

**Workflow:** `.github/workflows/daily-weather.yml`

To test the automation:
1. Go to the "Actions" tab on GitHub
2. Select "Daily Weather Report"
3. Click "Run workflow"

## 📚 What I Learned

- HTTP requests and REST API integration
- JSON parsing and data extraction
- SMTP protocol for email automation
- Environment variable security best practices
- GitHub Actions for CI/CD
- Error handling and input validation
- Command-line argument parsing

## 🎯 Future Improvements

- [ ] Add Discord webhook notifications
- [ ] Support multiple cities in one report
- [ ] Weather forecast (5-day prediction)
- [ ] Rich terminal UI with colors and formatting
- [ ] Web dashboard with Streamlit
- [ ] Database logging of weather history

## 📧 Contact

**Jackson Tran**  
Aspiring Cloud Engineer | Vietnam → Australia  
[GitHub](https://github.com/jacksontran2806-png)

---

*Built as part of my 6-month AI Engineering learning journey. Project #1 of many to come.*