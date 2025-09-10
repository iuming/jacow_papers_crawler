# JACoW Invincible Paper Crawler

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**A powerful, asynchronous Python tool for downloading academic papers from JACoW (Joint Accelerator Conferences Website) with intelligent classification and size filtering.**

</div>

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
```

### Basic Usage

```bash
# Download individual papers from a specific conference
python main.py --individual --conference "IPAC2023" --max-papers 50

# Download all papers from a conference session
python main.py --conference "IPAC2023" --session "MOPA"

# Dry run to see what would be downloaded
python main.py --dry-run --conference "IPAC2023"
```

## 📖 Quick Navigation

- [📚 Installation Guide](installation.md) - Detailed setup instructions
- [🔧 Usage Guide](usage.md) - Comprehensive usage examples
- [⚙️ Configuration](configuration.md) - Configuration options and settings
- [📝 Project Summary](PROJECT_SUMMARY.md) - Technical overview and architecture

## 📊 Supported Conferences

The crawler supports all JACoW conferences including:

- **IPAC** (International Particle Accelerator Conference)
- **PAC** (Particle Accelerator Conference)
- **EPAC** (European Particle Accelerator Conference)
- **LINAC** (Linear Accelerator Conference)
- **ECRIS** (Electron Cyclotron Resonance Ion Sources)
- **PCaPAC** (Personal Computers and Particle Accelerator Controls)
- **And many more...**

## 🎯 Use Cases

### For Researchers
- **Literature Review**: Quickly download all papers from relevant conferences
- **Trend Analysis**: Track research trends across multiple years
- **Reference Collection**: Build comprehensive paper collections by topic

### For Librarians
- **Archive Building**: Create institutional repositories of conference proceedings
- **Metadata Extraction**: Organize papers with automatic classification
- **Batch Processing**: Efficiently handle large-scale downloads

### For Students
- **Study Materials**: Access latest research in accelerator physics
- **Citation Research**: Find relevant papers for thesis work
- **Conference Preparation**: Download papers before attending conferences

## 🔧 Advanced Features

### Intelligent Paper Detection
The crawler can distinguish between:
- Individual research papers (typically 3-8 pages)
- Conference proceedings (large PDF files)
- Supplementary materials
- Presentation slides

### Robust Error Handling
- Automatic retry mechanisms
- Network timeout handling
- Rate limiting compliance
- Graceful failure recovery

### Progress Monitoring
- Real-time download progress
- Detailed logging
- Statistics reporting
- Error summaries

## 📈 Performance

- **Concurrent Downloads**: Up to 10 simultaneous connections
- **Smart Filtering**: Avoids downloading large proceedings
- **Memory Efficient**: Streams large files to disk
- **Resumable**: Can continue interrupted downloads

## 🛡️ Ethical Usage

This tool is designed for legitimate academic and research purposes:

- ✅ Respects server rate limits
- ✅ Includes appropriate delays between requests
- ✅ Only downloads publicly available papers
- ✅ Follows robots.txt guidelines

Please use responsibly and in accordance with JACoW's terms of service.

## 🤝 Contributing

We welcome contributions! Whether it's:

- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Code contributions

See our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 👨‍💻 Author

**Ming Liu**  
📧 mliu@ihep.ac.cn  
🏢 Institute of High Energy Physics (IHEP), Chinese Academy of Sciences  
📅 September 2025

---

<div align="center">
<em>Built with ❤️ for the accelerator physics community</em>
</div>
