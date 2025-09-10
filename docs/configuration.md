# Configuration Guide

## Overview

The JACoW Invincible Paper Crawler offers flexible configuration through multiple methods:
- Command-line arguments (highest priority)
- Configuration files
- Environment variables
- Default values (lowest priority)

## Configuration File

### Location

The primary configuration file is `config.ini` in the project root directory. You can also specify a custom config file using the `--config` command-line argument.

### Format

The configuration uses the standard INI format with sections and key-value pairs:

```ini
[download]
max_file_size_mb = 100
max_concurrent_downloads = 10
retry_attempts = 3
timeout_seconds = 30
user_agent = JACoW-Crawler/1.0

[paths]
download_directory = ./data/papers
log_directory = ./data/logs
metadata_directory = ./data/metadata

[filtering]
skip_proceedings = true
min_file_size_kb = 100
allowed_extensions = .pdf,.ps
individual_paper_patterns = .*[A-Z]{2,4}\d{3}\.pdf$

[network]
rate_limit_delay = 1.0
max_retries = 3
connection_timeout = 30
read_timeout = 60

[logging]
level = INFO
console_output = true
file_output = true
max_log_size_mb = 50
backup_count = 5
```

## Configuration Sections

### [download] Section

Controls download behavior and limits:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `max_file_size_mb` | int | 100 | Maximum file size to download (MB) |
| `max_concurrent_downloads` | int | 10 | Number of simultaneous downloads |
| `retry_attempts` | int | 3 | Number of retry attempts for failed downloads |
| `timeout_seconds` | int | 30 | Request timeout in seconds |
| `user_agent` | str | JACoW-Crawler/1.0 | HTTP User-Agent header |

### [paths] Section

Defines file and directory locations:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `download_directory` | str | ./data/papers | Where papers are saved |
| `log_directory` | str | ./data/logs | Log file location |
| `metadata_directory` | str | ./data/metadata | Metadata and stats location |

### [filtering] Section

Controls what files are downloaded:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `skip_proceedings` | bool | true | Skip conference proceedings files |
| `min_file_size_kb` | int | 100 | Minimum file size to download (KB) |
| `allowed_extensions` | str | .pdf,.ps | Comma-separated list of extensions |
| `individual_paper_patterns` | str | See below | Regex patterns for individual papers |

#### Individual Paper Patterns

The `individual_paper_patterns` setting uses regex to identify individual papers vs proceedings:

```ini
# Default pattern matches: MOPA001.pdf, TUPAC123.pdf, etc.
individual_paper_patterns = .*[A-Z]{2,4}\d{3}\.pdf$

# Multiple patterns (separated by |)
individual_paper_patterns = .*[A-Z]{2,4}\d{3}\.pdf$|.*paper_\d+\.pdf$
```

### [network] Section

Network and rate limiting settings:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `rate_limit_delay` | float | 1.0 | Delay between requests (seconds) |
| `max_retries` | int | 3 | Maximum retry attempts |
| `connection_timeout` | int | 30 | Connection timeout (seconds) |
| `read_timeout` | int | 60 | Read timeout (seconds) |

### [logging] Section

Logging configuration:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `level` | str | INFO | Log level (DEBUG, INFO, WARNING, ERROR) |
| `console_output` | bool | true | Enable console logging |
| `file_output` | bool | true | Enable file logging |
| `max_log_size_mb` | int | 50 | Maximum log file size (MB) |
| `backup_count` | int | 5 | Number of backup log files |

## Environment Variables

You can override any configuration setting using environment variables with the prefix `JACOW_`:

```bash
# Override download settings
export JACOW_MAX_FILE_SIZE_MB=50
export JACOW_MAX_CONCURRENT_DOWNLOADS=5

# Override paths
export JACOW_DOWNLOAD_DIRECTORY=/path/to/papers
export JACOW_LOG_DIRECTORY=/path/to/logs

# Override network settings
export JACOW_RATE_LIMIT_DELAY=2.0
export JACOW_USER_AGENT="MyCustomCrawler/1.0"
```

## Command-Line Arguments

Command-line arguments have the highest priority and override all other settings:

```bash
# Override concurrent downloads
python main.py --max-concurrent 5

# Override output directory
python main.py --output-dir /custom/path

# Override file size limit
python main.py --max-size 50
```

## Configuration Examples

### Conservative Configuration

For slow networks or when being respectful to servers:

```ini
[download]
max_concurrent_downloads = 3
retry_attempts = 5
timeout_seconds = 60

[network]
rate_limit_delay = 2.0
connection_timeout = 45
read_timeout = 90
```

### Aggressive Configuration

For fast networks and when time is critical:

```ini
[download]
max_concurrent_downloads = 20
retry_attempts = 2
timeout_seconds = 15

[network]
rate_limit_delay = 0.5
connection_timeout = 15
read_timeout = 30
```

### Large File Configuration

For downloading large conference proceedings:

```ini
[download]
max_file_size_mb = 500
max_concurrent_downloads = 5

[filtering]
skip_proceedings = false
min_file_size_kb = 1000
```

### Development Configuration

For testing and development:

```ini
[download]
max_file_size_mb = 10
max_concurrent_downloads = 2

[logging]
level = DEBUG
console_output = true
file_output = true

[filtering]
skip_proceedings = true
```

## Custom Configuration Files

### Creating Custom Configs

```bash
# Copy the default config
cp config.ini config_conservative.ini

# Edit for your needs
nano config_conservative.ini

# Use the custom config
python main.py --config config_conservative.ini
```

### Multiple Environments

```bash
# Different configs for different purposes
config.ini                  # Default
config_development.ini      # Development
config_production.ini       # Production
config_conservative.ini     # Slow networks
config_aggressive.ini       # Fast networks
```

## Configuration Validation

The crawler validates configuration on startup and will report errors:

```bash
# Check configuration
python main.py --dry-run --verbose

# This will show:
# - Configuration source (file, env, defaults)
# - Validation results
# - Effective settings
```

### Common Validation Errors

1. **Invalid file paths**: Ensure directories exist or can be created
2. **Invalid numbers**: Check that numeric values are positive
3. **Invalid patterns**: Regex patterns must be valid
4. **Resource limits**: Ensure settings don't exceed system capabilities

## Performance Tuning

### For Different Network Conditions

**Fast, reliable network**:
```ini
max_concurrent_downloads = 15
rate_limit_delay = 0.5
timeout_seconds = 20
```

**Slow or unreliable network**:
```ini
max_concurrent_downloads = 3
rate_limit_delay = 3.0
timeout_seconds = 60
retry_attempts = 5
```

### For Different Hardware

**High-memory system**:
```ini
max_concurrent_downloads = 20
max_file_size_mb = 200
```

**Limited resources**:
```ini
max_concurrent_downloads = 3
max_file_size_mb = 50
```

## Security Considerations

### Safe User Agents

Use descriptive, non-deceptive user agents:
```ini
user_agent = UniversityResearch-JACoWCrawler/1.0 (contact: researcher@university.edu)
```

### File Path Security

Ensure download paths are secure:
```ini
download_directory = /safe/download/path
# Avoid: download_directory = /
```

### Rate Limiting

Respect server resources:
```ini
rate_limit_delay = 1.0  # Minimum recommended
max_concurrent_downloads = 10  # Don't overwhelm servers
```

## Troubleshooting Configuration

### Check Current Configuration

```python
python -c "
from utils.config import Config
config = Config()
config.print_current_config()
"
```

### Debug Configuration Loading

```bash
python main.py --verbose --dry-run 2>&1 | grep -i config
```

### Common Issues

1. **Config file not found**: Check file path and permissions
2. **Invalid syntax**: Validate INI format
3. **Type errors**: Ensure numeric values are numbers
4. **Permission errors**: Check write access to directories

---

**Related Documentation**:
- [Installation Guide](installation.md)
- [Usage Guide](usage.md)
- [Usage Guide](usage.md)
