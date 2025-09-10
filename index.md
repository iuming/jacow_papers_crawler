---
layout: default
title: JACoW Invincible Paper Crawler
description: A powerful, asynchronous Python tool for downloading academic papers from JACoW
---

# JACoW Invincible Paper Crawler

A powerful, asynchronous Python tool for downloading academic papers from JACoW (Joint Accelerator Conferences Website) with intelligent classification and size filtering.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download individual papers from a specific conference
python main.py --individual --conference "IPAC2023" --max-papers 50

# Download all papers from a conference session
python main.py --conference "IPAC2023" --session "MOPA"
```

## ✨ Features

- **Asynchronous Downloads**: High-performance concurrent downloading
- **Smart Filtering**: Automatically detects individual papers vs proceedings
- **Size Control**: Configurable file size limits (default: 100MB)
- **Session Organization**: Downloads papers by conference sessions
- **Progress Tracking**: Real-time download progress with rich console output
- **Robust Error Handling**: Comprehensive retry logic and error recovery

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
- [Configuration](docs/configuration.md)
- [API Reference](docs/api.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🔧 Installation

### Prerequisites
- Python 3.9+
- pip package manager

### From Source
```bash
git clone https://github.com/your-username/jacow-paper-crawler.git
cd jacow-paper-crawler
pip install -r requirements.txt
```

### Using Docker
```bash
docker-compose up --build
```

## 📊 Supported Conferences

The crawler supports all JACoW conferences including:
- IPAC (International Particle Accelerator Conference)
- PAC (Particle Accelerator Conference)
- EPAC (European Particle Accelerator Conference)
- LINAC (Linear Accelerator Conference)
- And many more...

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ming Liu**
- Email: mliu@ihep.ac.cn
- Institution: Institute of High Energy Physics (IHEP), Chinese Academy of Sciences
- Date: September 9, 2025

## 🔒 Security

For security vulnerabilities, please see our [Security Policy](SECURITY.md).

---

*Built with ❤️ for the accelerator physics community*
