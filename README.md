# URL Content Scraper - Streamlit App

A simple yet powerful Streamlit application that connects to the Serper API to scrape content from multiple URLs. Upload a CSV or Excel file containing URLs, and the app will scrape the content from each URL and provide downloadable results.

## Features

- 📁 **File Upload Support**: Accepts CSV and Excel files (.csv, .xlsx, .xls)
- 🔍 **Bulk URL Scraping**: Process multiple URLs in one go
- ⚡ **Rate Limiting**: Configurable delay between requests to avoid overwhelming the API
- 📊 **Results Summary**: View scraped data in a clean, organized table
- 📝 **Detailed Results**: Access full content for each scraped URL
- ❌ **Error Handling**: Track and download failed requests
- 💾 **Multiple Export Options**: Download results as CSV or JSON
- 🎨 **User-Friendly Interface**: Clean and intuitive Streamlit interface

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd url-scraper-streamlit
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. The app will open in your default web browser at `http://localhost:8501`

3. **Configure the API Key** (optional):
   - The app comes with a default API key
   - You can enter your own Serper API key in the sidebar

4. **Upload your file**:
   - Click on "Browse files" or drag and drop a CSV/Excel file
   - The file should contain a column with URLs (preferably named 'URL' or 'url')
   - If no URL column is found, the app will use the first column

5. **Configure scraping options**:
   - Toggle "Include Markdown" to include markdown content in the results
   - Adjust the delay between requests (0.5 to 5 seconds)

6. **Start scraping**:
   - Click the "Start Scraping" button
   - Monitor the progress bar as URLs are processed

7. **View and download results**:
   - **Summary tab**: Overview of all scraped URLs with basic info
   - **Detailed Results tab**: Full content preview for each URL
   - **Errors tab**: List of URLs that failed to scrape
   - Download results in CSV or JSON format

## File Format Requirements

Your input file should be structured in one of these formats:

### Option 1: Column named 'URL' or 'url'
```
URL
https://example.com
https://another-site.com
```

### Option 2: URLs in the first column
```
Website
https://example.com
https://another-site.com
```

## API Configuration

The app uses the Serper API for web scraping. You'll need an API key from [Serper](https://serper.dev/).

The default API key is provided in the app, but it's recommended to use your own key for production use.

## Dependencies

- **streamlit**: Web app framework
- **pandas**: Data manipulation and file handling
- **requests**: HTTP requests to Serper API
- **openpyxl**: Excel file support

## Deployment on Streamlit Cloud

1. Push your code to a GitHub repository

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)

3. Click "New app" and connect your GitHub repository

4. Select the repository, branch, and main file path (app.py)

5. Click "Deploy"

### Environment Variables (Optional)

If you want to keep your API key secure, you can set it as a secret in Streamlit Cloud:

1. In your Streamlit Cloud app settings, go to "Secrets"
2. Add:
```toml
SERPER_API_KEY = "your-api-key-here"
```

3. Update the code to read from secrets:
```python
api_key = st.text_input("Serper API Key", type="password", value=st.secrets.get("SERPER_API_KEY", "default-key"))
```

## Troubleshooting

### Common Issues

1. **"No URL column found" warning**:
   - Ensure your file has a column named 'URL' or 'url'
   - The app will use the first column if no URL column is found

2. **Rate limit errors**:
   - Increase the delay between requests in the sidebar
   - Check your API key limits with Serper

3. **Empty results**:
   - Verify the URLs are accessible
   - Check if the websites block automated scraping
   - Ensure your API key is valid

## Features Breakdown

### Scraping Options
- **Include Markdown**: When enabled, the API returns both plain text and markdown formatted content
- **Rate Limiting**: Prevents overwhelming the API with too many requests in quick succession

### Export Options
- **Summary CSV**: Basic information about each scraped URL
- **Individual JSON**: Full content for each URL
- **All Results JSON**: Complete dataset including metadata and errors
- **Error CSV**: List of failed URLs with error messages

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the Serper API documentation
3. Open an issue in the GitHub repository

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
