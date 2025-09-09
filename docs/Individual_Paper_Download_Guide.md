# 🎯 JACoW Individual Paper Download Guide

## 📊 Feature Comparison

### Original Feature: Conference Proceedings Mode
- **Characteristics**: Downloads complete conference proceedings PDF
- **File Size**: Usually very large (e.g., IPAC 2023 is 2.1GB)
- **Use Case**: Research requiring complete conference materials
- **Command**: `python main.py --year 2023`

### 🆕 New Feature: Individual Paper Mode
- **Characteristics**: Downloads independent PDF files for each paper
- **File Size**: Usually a few MB to tens of MB
- **Use Case**: Precise acquisition of specific papers, saves space
- **Command**: `python main.py --individual-papers --year 2023`

## 🚀 Usage

### Basic Usage

```bash
# Preview function - see what individual papers are available for download
python main.py --individual-papers --dry-run --year 2023 --max-papers 10

# Download the first 20 individual papers from 2023
python main.py --individual-papers --year 2023 --max-papers 20 --max-size 50
```

### Advanced Usage

```bash
# Download individual papers from specific conference
python main.py --individual-papers --conference IPAC --year 2023 --max-size 30

# Control concurrency and file size
python main.py --individual-papers --max-papers 50 --concurrent 3 --max-size 20

# Use custom output directory
python main.py --individual-papers --output-dir ./individual_papers --max-papers 30
```

### Recommended Workflow

1. **Step 1: Preview**
   ```bash
   python main.py --individual-papers --dry-run --year 2023 --max-papers 10 --verbose
   ```

2. **Step 2: Small Test**
   ```bash
   python main.py --individual-papers --year 2023 --max-papers 5 --max-size 20
   ```

3. **Step 3: Batch Download**
   ```bash
   python main.py --individual-papers --year 2023 --max-papers 100 --max-size 50
   ```

## 🎯 Parameter Description

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--individual-papers` | Enable individual paper mode | Required parameter |
| `--max-papers` | Limit number of papers to download | `--max-papers 20` |
| `--year` | Specify year | `--year 2023` |
| `--conference` | Specify conference | `--conference IPAC` |
| `--max-size` | File size limit (MB) | `--max-size 50` |
| `--dry-run` | Preview mode, no actual download | Recommended first use |

## 📁 File Organization

Individual papers will be organized in the following structure:

```
data/papers/
├── 2023/
│   ├── IPAC/
│   │   ├── individual_papers/
│   │   │   ├── MOPA001.pdf
│   │   │   ├── MOPA002.pdf
│   │   │   └── TUPB123.pdf
│   │   └── metadata/
│   └── LINAC/
└── 2022/
```

## ⚡ Performance Advantages

### Speed Comparison
- **Proceedings Mode**: Download 1 file of 2.1GB ≈ Takes considerable time
- **Individual Paper Mode**: Download 20 files of 5MB ≈ 100MB total, faster

### Storage Advantages
- **Precise Selection**: Only download needed papers
- **Avoid Redundancy**: No need to download entire proceedings then extract
- **Better Management**: Each paper as independent file, easier to reference

## 🔍 Paper Recognition Algorithm

The program automatically identifies individual papers:

✅ **Recognized as Individual Papers**:
- `MOPA001.pdf` (conference code + number)
- `TUPB123.pdf` (session code + number)
- `WEPL045.pdf` (standard paper number)

❌ **Recognized as Proceedings**:
- `ipac-23_proceedings_volume.pdf`
- `linac-proceedings-complete.pdf`
- `conference_full_papers.pdf`

## 🛡️ Safety Settings

Recommended safety parameters:

```bash
python main.py --individual-papers \
  --max-papers 50 \          # Limit quantity to avoid excessive downloads
  --max-size 30 \            # Limit size to avoid unexpected large files
  --concurrent 3 \           # Moderate concurrency to avoid server pressure
  --delay 1.0                # Request interval to stay polite
```

## 📈 Usage Recommendations

### Beginner Recommended
```bash
# Safe first attempt
python main.py --individual-papers --dry-run --year 2023 --max-papers 5
```

### Advanced Users
```bash
# Batch but controlled download
python main.py --individual-papers --year 2023 --max-papers 100 --max-size 30 --concurrent 3
```

### Professional Research
```bash
# Specific conference deep download
python main.py --individual-papers --conference IPAC --year 2023 --max-size 50 --verbose
```

## 🎉 Get Started

Experience individual paper download immediately:

```bash
python main.py --individual-papers --dry-run --year 2023 --max-papers 5 --verbose
```

This command will:
- ✅ Preview the first 5 individual papers from 2023
- ✅ Display detailed information (title, author, conference, etc.)
- ✅ Not actually download any files
- ✅ Let you understand available paper content

Enjoy a more precise and efficient JACoW paper download experience! 🚀
