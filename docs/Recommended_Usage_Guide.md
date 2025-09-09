# 🎯 JACoW Crawler Recommended Usage Guide

## 1. First Use - Preview Before Download
```bash
# Check what conferences and papers are available in 2023
python main.py --dry-run --year 2023

# Check paper situation for IPAC conference
python main.py --dry-run --conference IPAC --year 2023
```

## 2. Safe Download Strategy
```bash
# Limit size to avoid accidentally downloading oversized files
python main.py --max-size 50 --year 2023

# Use moderate concurrency (recommended 2-5)
python main.py --concurrent 3 --year 2023
```

## 3. Batch Download Recommendations
```bash
# Download by year in batches
python main.py --year 2023 --output-dir downloads/2023
python main.py --year 2022 --output-dir downloads/2022

# Download by conference in batches  
python main.py --conference IPAC --output-dir downloads/IPAC
python main.py --conference LINAC --output-dir downloads/LINAC
```

## 4. Monitoring and Resume
```bash
# Enable verbose logging
python main.py --verbose --year 2023

# Support resume downloads
python main.py --resume --year 2023
```

## 5. Actual Test Results Reference
Based on our testing:
- **✅ IPAC 2023**: Found 2 large PDF files
- **✅ Network stability**: 100% success connection rate
- **⚠️ File size**: Some conference proceedings are very large (>1GB), recommend using --max-size limit

## 6. Best Practices
1. **Always --dry-run first**: Preview content to avoid unexpected downloads
2. **Set size limits**: --max-size 100 (avoid oversized files)
3. **Reasonable concurrency**: --concurrent 3 (avoid putting pressure on server)
4. **Batch processing**: Download by year or conference separately
5. **Monitor progress**: --verbose to view detailed information

## 7. Troubleshooting
If you encounter 404 errors:
- Normal phenomenon, different years have different URL structures
- Program will automatically retry and fallback
- Use --verbose to view detailed information

Start your first crawl:
```bash
python main.py --dry-run --year 2023 --max-size 100 --verbose
```
