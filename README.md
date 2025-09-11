# JACoW Invincible Paper Crawler

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**A powerful, asynchronous Python tool for downloading academic papers from JACoW (Joint Accelerator Conferences Website) with intelligent classification and size filtering.**

[Quick Start](#-quick-start) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

## ✨ Features

- 🎯 **Smart Paper Detection**: Automatically distinguishes individual papers from conference proceedings
- 📥 **Asynchronous Downloads**: High-performance concurrent downloading with configurable limits
- 🔍 **Intelligent Classification**: Organizes papers by conference, session, and year
- 💾 **Size Control**: Configurable file size limits to avoid unwanted large files (default: 100MB)
- 🚦 **Rate Limiting**: Respectful downloading with configurable delays and retry logic
- 📊 **Progress Tracking**: Real-time download progress with rich console output
- 🤖 **GitHub Actions**: Automated scheduled downloads with configurable parameters
- 🐳 **Docker Support**: Complete containerization for easy deployment
- 🔧 **Flexible Configuration**: Multiple configuration methods (CLI, files, environment variables)

## ✨ Features

- 🎯 **Smart Paper Detection**: Automatically distinguishes individual papers from conference proceedings
- 📥 **Asynchronous Downloads**: High-performance concurrent downloading with configurable limits
- 🔍 **Intelligent Classification**: Organizes papers by conference, session, and year
- 💾 **Size Control**: Configurable file size limits to avoid unwanted large files (default: 100MB)
- 🚦 **Rate Limiting**: Respectful downloading with configurable delays and retry logic
- 📊 **Progress Tracking**: Real-time download progress with rich console output
- 🐳 **Docker Support**: Complete containerization for easy deployment
- 🔧 **Flexible Configuration**: Multiple configuration methods (CLI, files, environment variables)

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- At least 1GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/iuming/jacow_papers_crawler.git
cd jacow_papers_crawler

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

### Basic Usage

```bash
# Download individual papers from IPAC2023
python main.py --individual --conference "IPAC2023" --max-papers 50

# Preview what would be downloaded (dry run)
python main.py --individual --conference "IPAC2023" --dry-run

# Download papers from specific session
python main.py --individual --conference "IPAC2023" --session "MOPA"
```

## 🤖 Automated Downloads with GitHub Actions

This project includes a powerful GitHub Action that can automatically download JACoW conference papers on a schedule or on-demand. Perfect for keeping your paper collection up-to-date without manual intervention.

### Quick Setup
1. Fork this repository
2. Go to `Actions` → `Download JACoW Conference Papers`
3. Click `Run workflow` and configure your parameters
4. Papers will be downloaded to the `data/papers` directory

### Features
- 📅 **Scheduled Downloads**: Automatic weekly downloads of new papers
- 🎛️ **Flexible Configuration**: Filter by conference, year, and paper count
- 📊 **Detailed Reporting**: Comprehensive download statistics and logs
- 💾 **Artifact Storage**: Downloaded papers saved as GitHub artifacts
- 🚨 **Failure Notifications**: Automatic issue creation on errors

[📖 Read the complete GitHub Action guide](docs/GitHub_Action_Download_Guide.md)

## 📖 Documentation

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Usage Guide](docs/usage.md) - Comprehensive usage examples
- [Configuration Guide](docs/configuration.md) - Configuration options
- [GitHub Action Guide](docs/GitHub_Action_Download_Guide.md) - Automated paper downloads
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute

## 🛠 Installation

### Method 1: From Source (Recommended)

```bash
git clone https://github.com/iuming/jacow_papers_crawler.git
cd jacow_papers_crawler
pip install -r requirements.txt
```

### Method 2: Using Docker

```bash
docker-compose up --build
```

### Method 3: Development Setup

```bash
git clone https://github.com/iuming/jacow_papers_crawler.git
cd jacow_papers_crawler
pip install -e .
pip install -r requirements-dev.txt
```

## 📋 Usage

### Command Line Interface

```bash
# Basic download
python main.py --individual --conference "IPAC2023"

# Advanced options
python main.py --individual \
    --conference "IPAC2023" \
    --session "MOPA,TUPAC" \
    --max-papers 100 \
    --verbose

# Using configuration file
python main.py --config my_config.ini --individual --conference "IPAC2023"
```

## 📋 Usage

### Command Line Interface

```bash
# Basic download
python main.py --individual --conference "IPAC2023"

# Advanced options
python main.py --individual \
    --conference "IPAC2023" \
    --session "MOPA,TUPAC" \
    --max-papers 100 \
    --verbose

# Using configuration file
python main.py --config my_config.ini --individual --conference "IPAC2023"
```

### Configuration

Edit `config.ini` to customize default settings:

```ini
[download]
max_file_size_mb = 100
max_concurrent_downloads = 10
retry_attempts = 3

[paths]
download_directory = ./data/papers
log_directory = ./data/logs
```

### Docker Usage

```bash
# Using Docker Compose
docker-compose run crawler --individual --conference "IPAC2023"

# Using Docker directly
docker run -v $(pwd)/data:/app/data jacow-crawler \
    --individual --conference "IPAC2023"
```

## 📁 Output Structure

```
data/
├── papers/
│   ├── IPAC2023/
│   │   ├── MOPA/
│   │   │   ├── MOPA001.pdf
│   │   │   └── MOPA002.pdf
│   │   └── TUPAC/
│   └── PAC2019/
├── logs/
│   └── crawler_2025-09-09.log
└── metadata/
    └── download_stats.json
```
## 🛠 Supported Conferences

The crawler supports all JACoW conferences including:
- **IPAC**: International Particle Accelerator Conference
- **PAC**: Particle Accelerator Conference  
- **EPAC**: European Particle Accelerator Conference
- **LINAC**: Linear Accelerator Conference
- **CYCLOTRONS**: International Conference on Cyclotrons
- **And many more...**

## 🔧 Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_individual.py

# Verify crawler functionality
python tests/verify.py
```

### Project Structure

```
jacow-paper-crawler/
├── main.py                 # CLI entry point
├── crawler/               # Core crawler modules
├── utils/                 # Utility functions
├── docs/                  # Documentation
├── tests/                 # Test suite
├── scripts/               # Helper scripts
├── examples/              # Usage examples
└── .github/               # GitHub workflows and templates
```

## 🤝 Contributing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- How to report bugs
- How to suggest enhancements  
- How to submit pull requests
- Code style guidelines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Security

For security vulnerabilities, please see our [Security Policy](SECURITY.md).

## �‍💻 Author

**Ming Liu**
- Email: mliu@ihep.ac.cn
- Institution: Institute of High Energy Physics (IHEP), Chinese Academy of Sciences
- GitHub: [iuming](https://github.com/iuming)

## 🙏 Acknowledgments

- JACoW collaboration for providing open access to conference proceedings
- The Python community for excellent libraries
- Contributors and users of this project

---

<div align="center">

**Built with ❤️ for the accelerator physics community**

[⭐ Star this project](https://github.com/iuming/jacow_papers_crawler) | [🐛 Report Bug](https://github.com/iuming/jacow_papers_crawler/issues) | [💡 Request Feature](https://github.com/iuming/jacow_papers_crawler/issues)

</div>
