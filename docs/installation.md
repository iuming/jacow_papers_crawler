# Installation Guide

## Prerequisites

Before installing the JACoW Invincible Paper Crawler, ensure you have:

- **Python 3.7 or higher**
- **pip** package manager
- **Git** (for development installation)
- At least **1GB free disk space** for downloads

## Installation Methods

### Method 1: From Source (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/jacow-paper-crawler.git
   cd jacow-paper-crawler
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python main.py --help
   ```

### Method 2: Using Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/jacow-paper-crawler.git
   cd jacow-paper-crawler
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Or build manually**:
   ```bash
   docker build -t jacow-crawler .
   docker run -v $(pwd)/data:/app/data jacow-crawler --help
   ```

### Method 3: Development Installation

For contributors and developers:

1. **Clone and install in development mode**:
   ```bash
   git clone https://github.com/your-username/jacow-paper-crawler.git
   cd jacow-paper-crawler
   pip install -e .
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run tests**:
   ```bash
   python -m pytest tests/
   ```

## Configuration

### Basic Configuration

1. **Copy the example configuration**:
   ```bash
   cp config.ini.example config.ini
   ```

2. **Edit configuration** (optional):
   ```ini
   [download]
   max_file_size_mb = 100
   max_concurrent_downloads = 10
   retry_attempts = 3
   
   [paths]
   download_directory = ./data/papers
   log_directory = ./data/logs
   ```

### Environment Variables

You can also configure using environment variables:

```bash
export JACOW_MAX_FILE_SIZE=100
export JACOW_DOWNLOAD_DIR=./data/papers
export JACOW_LOG_LEVEL=INFO
```

## Verification

### Test Basic Functionality

```bash
# Test help command
python main.py --help

# Test with dry run
python main.py --individual --conference "IPAC2023" --dry-run

# Download a small test set
python main.py --individual --conference "IPAC2023" --max-papers 5
```

### Check Dependencies

```bash
python -c "import aiohttp, aiofiles, beautifulsoup4; print('All dependencies installed successfully!')"
```

## Troubleshooting

### Common Issues

1. **Permission Errors**:
   - Ensure you have write permissions to the download directory
   - On Linux/macOS, you might need to use `sudo` for system-wide installation

2. **SSL Certificate Errors**:
   - Update your certificates: `pip install --upgrade certifi`
   - Or set: `export SSL_CERT_FILE=$(python -m certifi)`

3. **Memory Issues**:
   - Reduce `max_concurrent_downloads` in config.ini
   - Increase system memory or use swap

4. **Network Timeouts**:
   - Check your internet connection
   - Increase `retry_attempts` in configuration

### Getting Help

- **Check the logs**: Look in `./data/logs/` for detailed error information
- **Create an issue**: [GitHub Issues](https://github.com/your-username/jacow-paper-crawler/issues)
- **Contact maintainer**: mliu@ihep.ac.cn

## Platform-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Paths use backslashes: `data\papers`
- Consider using Windows Subsystem for Linux (WSL)

### macOS

- Install Python via Homebrew: `brew install python`
- Xcode command line tools may be required: `xcode-select --install`

### Linux

- Most distributions work out of the box
- Install Python development headers if needed: `sudo apt-get install python3-dev`

## Next Steps

After installation:

1. Read the [Usage Guide](usage.md)
2. Check [Configuration Options](configuration.md)
3. Explore [Examples](../examples/)

---

**Need help?** Contact: mliu@ihep.ac.cn
