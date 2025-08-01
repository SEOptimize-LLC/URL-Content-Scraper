import streamlit as st
import pandas as pd
import requests
import json
import time
from datetime import datetime
import os

# Configure Streamlit page
st.set_page_config(
    page_title="URL Content Scraper",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 URL Content Scraper")
st.markdown("Upload a CSV or Excel file containing URLs to scrape their content using Serper API")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Try to get API key from secrets, fall back to empty string
    default_api_key = st.secrets.get("SERPER_API_KEY", "")
    
    api_key = st.text_input(
        "Serper API Key", 
        type="password", 
        value=default_api_key,
        help="Enter your Serper API key or set it in Streamlit secrets"
    )
    
    if not api_key:
        st.warning("Please enter a Serper API key to continue")
    else:
        st.success("API key configured ✓")
    
    # Options
    st.subheader("Scraping Options")
    include_markdown = st.checkbox("Include Markdown", value=True)
    rate_limit = st.slider("Delay between requests (seconds)", 0.5, 5.0, 1.0, 0.5)

# Function to scrape URL using Serper API
def scrape_url(url, api_key, include_markdown=True):
    """Scrape content from a URL using Serper API"""
    
    api_url = "https://scrape.serper.dev"
    
    payload = json.dumps({
        "url": url,
        "includeMarkdown": include_markdown
    })
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", api_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Function to read URLs from uploaded file
def read_urls_from_file(uploaded_file):
    """Read URLs from CSV or Excel file"""
    
    try:
        # Get file extension
        file_name = uploaded_file.name
        file_extension = file_name.split('.')[-1].lower()
        
        # Read file based on extension
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        
        # Look for URL column (case-insensitive)
        url_columns = [col for col in df.columns if 'url' in col.lower()]
        
        if url_columns:
            url_column = url_columns[0]
        else:
            # If no URL column found, use the first column
            url_column = df.columns[0]
            st.warning(f"No 'URL' column found. Using '{url_column}' column instead.")
        
        # Extract URLs
        urls = df[url_column].dropna().tolist()
        return urls
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

# Main app content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload File")
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file containing URLs",
        type=['csv', 'xlsx', 'xls'],
        help="The file should contain a column with URLs (preferably named 'URL' or 'url')"
    )

if uploaded_file is not None:
    # Read URLs from file
    urls = read_urls_from_file(uploaded_file)
    
    if urls:
        with col2:
            st.subheader("📊 File Summary")
            st.info(f"Found {len(urls)} URLs in the uploaded file")
            
            # Show preview of URLs
            with st.expander("Preview URLs"):
                for i, url in enumerate(urls[:10], 1):
                    st.text(f"{i}. {url}")
                if len(urls) > 10:
                    st.text(f"... and {len(urls) - 10} more")
        
        # Scrape button
        if st.button("🚀 Start Scraping", type="primary", disabled=not api_key):
            if not api_key:
                st.error("Please enter a Serper API key in the sidebar to continue")
            else:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Results container
                results = []
                errors = []
                
                # Scrape each URL
                for i, url in enumerate(urls):
                    # Update progress
                    progress = (i + 1) / len(urls)
                    progress_bar.progress(progress)
                    status_text.text(f"Scraping URL {i + 1} of {len(urls)}: {url[:50]}...")
                    
                    # Scrape URL
                    result, error = scrape_url(url, api_key, include_markdown)
                    
                    if error:
                        errors.append({
                            'url': url,
                            'error': error
                        })
                    else:
                        results.append({
                            'url': url,
                            'title': result.get('title', 'N/A'),
                            'description': result.get('description', 'N/A'),
                            'content_length': len(result.get('text', '')) if result.get('text') else 0,
                            'markdown_length': len(result.get('markdown', '')) if result.get('markdown') else 0,
                            'full_result': result
                        })
                    
                    # Rate limiting
                    if i < len(urls) - 1:
                        time.sleep(rate_limit)
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success(f"✅ Scraping completed! Successfully scraped {len(results)} out of {len(urls)} URLs.")
                
                # Show results in tabs
                tab1, tab2, tab3 = st.tabs(["📊 Summary", "📝 Detailed Results", "❌ Errors"])
                
                with tab1:
                    if results:
                        # Create summary dataframe
                        summary_df = pd.DataFrame([
                            {
                                'URL': r['url'],
                                'Title': r['title'][:50] + '...' if len(r['title']) > 50 else r['title'],
                                'Description': r['description'][:50] + '...' if len(r['description']) > 50 else r['description'],
                                'Content Length': r['content_length'],
                                'Markdown Length': r['markdown_length']
                            }
                            for r in results
                        ])
                        
                        st.dataframe(summary_df, use_container_width=True)
                        
                        # Download button for summary
                        csv = summary_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Summary as CSV",
                            data=csv,
                            file_name=f"scraping_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                with tab2:
                    if results:
                        for i, result in enumerate(results):
                            with st.expander(f"🔗 {result['url'][:100]}..."):
                                st.subheader("Basic Info")
                                st.write(f"**Title:** {result['title']}")
                                st.write(f"**Description:** {result['description']}")
                                
                                # Show content preview
                                if result['full_result'].get('text'):
                                    st.subheader("Text Content Preview")
                                    st.text_area(
                                        "First 1000 characters",
                                        value=result['full_result']['text'][:1000] + "...",
                                        height=200,
                                        disabled=True
                                    )
                                
                                if include_markdown and result['full_result'].get('markdown'):
                                    st.subheader("Markdown Content Preview")
                                    st.text_area(
                                        "First 1000 characters",
                                        value=result['full_result']['markdown'][:1000] + "...",
                                        height=200,
                                        disabled=True
                                    )
                                
                                # Download individual result
                                result_json = json.dumps(result['full_result'], indent=2)
                                st.download_button(
                                    label="📥 Download Full Result as JSON",
                                    data=result_json,
                                    file_name=f"result_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json",
                                    key=f"download_{i}"
                                )
                
                with tab3:
                    if errors:
                        error_df = pd.DataFrame(errors)
                        st.dataframe(error_df, use_container_width=True)
                        
                        # Download errors
                        error_csv = error_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Errors as CSV",
                            data=error_csv,
                            file_name=f"scraping_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No errors occurred during scraping! 🎉")
                
                # Download all results as JSON
                if results:
                    all_results = {
                        'summary': {
                            'total_urls': len(urls),
                            'successful': len(results),
                            'failed': len(errors),
                            'timestamp': datetime.now().isoformat()
                        },
                        'results': [r['full_result'] for r in results],
                        'errors': errors
                    }
                    
                    all_results_json = json.dumps(all_results, indent=2)
                    st.download_button(
                        label="📥 Download All Results as JSON",
                        data=all_results_json,
                        file_name=f"all_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

else:
    # Instructions when no file is uploaded
    st.info("👆 Please upload a CSV or Excel file containing URLs to get started")
    
    st.subheader("📋 File Format Requirements")
    st.markdown("""
    Your file should contain URLs in one of the following formats:
    
    **Option 1: Column named 'URL' or 'url'**
    ```
    URL
    https://example.com
    https://another-site.com
    ```
    
    **Option 2: URLs in the first column**
    ```
    Website
    https://example.com
    https://another-site.com
    ```
    """)
    
    # Sample file download
    sample_data = pd.DataFrame({
        'URL': [
            'https://example.com',
            'https://www.python.org',
            'https://streamlit.io'
        ]
    })
    
    sample_csv = sample_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_csv,
        file_name="sample_urls.csv",
        mime="text/csv"
    )
