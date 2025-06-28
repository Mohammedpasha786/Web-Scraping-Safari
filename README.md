# Web-Scraping-Safari
# GitHub Trending Repository Scraper

A Python web scraper that extracts the top 5 trending repositories from GitHub's trending page and saves the results to a CSV file.

## 🎯 Overview

This project uses Python's `requests` and `Beautiful Soup` libraries to scrape GitHub's trending page and extract repository information. The scraper is designed to be robust and handle changes in GitHub's page structure through multiple parsing strategies.

## 📋 Features

- ✅ Scrapes top 5 trending repositories from GitHub
- ✅ Extracts repository names and links
- ✅ Saves results to CSV with proper formatting
- ✅ Robust parsing with multiple fallback strategies
- ✅ Comprehensive logging and error handling
- ✅ Timestamped output files
- ✅ Clean, readable code with documentation

## 🛠️ Technologies Used

- **Python 3.7+**
- **requests** - For HTTP requests
- **Beautiful Soup 4** - For HTML parsing
- **csv** - For CSV file operations
- **logging** - For comprehensive logging

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/github-trending-scraper.git
cd github-trending-scraper
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Usage
```bash
python github_trending_scraper.py
```

### Expected Output
```
🚀 GitHub Trending Repository Scraper
==================================================
2025-06-28 10:30:15,123 - INFO - Starting GitHub trending repositories scraper
2025-06-28 10:30:15,123 - INFO - Target: Top 5 repositories
2025-06-28 10:30:15,124 - INFO - Fetching trending page: https://github.com/trending
2025-06-28 10:30:16,234 - INFO - Successfully fetched page. Status code: 200
2025-06-28 10:30:16,456 - INFO - Found 25 repositories using selector: article.Box-row
2025-06-28 10:30:16,457 - INFO - Found repository 1: getzep / graphiti
2025-06-28 10:30:16,458 - INFO - Found repository 2: microsoft / generative-ai-for-beginners
2025-06-28 10:30:16,459 - INFO - Found repository 3: pydantic / pydantic-ai
2025-06-28 10:30:16,460 - INFO - Found repository 4: bregman-arie / devops-interview-questions
2025-06-28 10:30:16,461 - INFO - Found repository 5: Stirling-Tools / Stirling-PDF
2025-06-28 10:30:16,462 - INFO - Successfully parsed 5 repositories
2025-06-28 10:30:16,463 - INFO - Successfully saved 5 repositories to trending_repositories_20250628_103016.csv

🎉 Successfully scraped 5 trending repositories!
📁 Saved to: trending_repositories_20250628_103016.csv
📊 Results:
--------------------------------------------------------------------------------
1. getzep / graphiti
   🔗 https://github.com/getzep/graphiti

2. microsoft / generative-ai-for-beginners
   🔗 https://github.com/microsoft/generative-ai-for-beginners

3. pydantic / pydantic-ai
   🔗 https://github.com/pydantic/pydantic-ai

4. bregman-arie / devops-interview-questions
   🔗 https://github.com/bregman-arie/devops-interview-questions

5. Stirling-Tools / Stirling-PDF
   🔗 https://github.com/Stirling-Tools/Stirling-PDF

✅ Scraping completed successfully!
```

## 📁 Output

The scraper generates a CSV file with the following structure:

| Column Name | Description |
|-------------|-------------|
| repository_name | The name of the trending repository |
| link | The full GitHub URL to the repository |

### Sample CSV Output
```csv
repository_name,link
getzep / graphiti,https://github.com/getzep/graphiti
microsoft / generative-ai-for-beginners,https://github.com/microsoft/generative-ai-for-beginners
pydantic / pydantic-ai,https://github.com/pydantic/pydantic-ai
bregman-arie / devops-interview-questions,https://github.com/bregman-arie/devops-interview-questions
Stirling-Tools / Stirling-PDF,https://github.com/Stirling-Tools/Stirling-PDF
```

## 🏗️ Project Structure

```
github-trending-scraper/
├── github_trending_scraper.py    # Main scraper script
├── requirements.txt              # Python dependencies
├── README.md                    # This file
├── trending_repositories_sample.csv  # Sample output
└── .gitignore                   # Git ignore file
```

## 🔧 How It Works

### 1. **Web Request**
- Uses `requests` with proper headers to mimic a real browser
- Implements session management for efficient requests
- Includes timeout and error handling

### 2. **HTML Parsing**
- Uses `Beautiful Soup` for robust HTML parsing
- Implements multiple CSS selectors for resilience
- Handles dynamic page structure changes

### 3. **Data Extraction**
- Extracts repository names and links
- Cleans and normalizes text data
- Handles various link formats

### 4. **Data Storage**
- Saves data to CSV with proper encoding
- Uses timestamped filenames
- Includes proper headers and formatting

## 🛡️ Robustness Features

### Multiple Parsing Strategies
The scraper uses several CSS selectors to find repositories:
1. `article.Box-row` (primary)
2. `.Box-row` (fallback)
3. `article[class*="Box-row"]` (partial match)
4. `.repo-list-item` (alternative)
5. `[data-testid="repository-item"]` (test ID based)

### Error Handling
- Comprehensive try-catch blocks
- Detailed logging for debugging
- Graceful failure with informative messages
- Network timeout handling

### Data Validation
- Checks for valid repository names and links
- Handles malformed URLs
- Removes extra whitespace and formatting

## 📊 Technical Approach

### Web Scraping Strategy
1. **Respectful Scraping**: Uses appropriate delays and headers
2. **Browser Simulation**: Mimics real browser behavior
3. **Multiple Selectors**: Handles page structure changes
4. **Error Recovery**: Continues processing even if some elements fail

### Data Processing Pipeline
```
GitHub Trending Page → HTTP Request → HTML Content → 
Beautiful Soup Parser → Repository Extraction → 
Data Cleaning → CSV Export
```

## 🔍 Troubleshooting

### Common Issues

**1. No repositories found**
- GitHub may have changed their HTML structure
- Check the logs for parsing errors
- The script includes multiple fallback selectors

**2. Network errors**
- Check your internet connection
- GitHub might be temporarily unavailable
- The script includes retry logic

**3. Permission errors**
- Ensure you have write permissions in the directory
- Check if the CSV file is open in another program

### Debug Mode
To enable more detailed logging, modify the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Considerations

- **Single Request**: Efficient single-page scraping
- **Memory Usage**: Processes data incrementally
- **Network**: Respects GitHub's servers with reasonable delays
- **File I/O**: Uses efficient CSV writing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request


## ⚠️ Ethical Considerations

- **Rate Limiting**: Script includes appropriate delays
- **Terms of Service**: Always respect GitHub's ToS
- **Data Usage**: Only scrapes publicly available information
- **Attribution**: Gives credit to GitHub as the data source

## 🔮 Future Enhancements

- [ ] Support for different time periods (daily, weekly, monthly)
- [ ] Language-specific trending repositories
- [ ] Additional metadata extraction (stars, forks, description)
- [ ] Export to multiple formats (JSON, Excel)
- [ ] Scheduling and automation features
- [ ] Web interface for easier usage

