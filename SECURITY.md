# Security Policy

## Supported Versions

The following versions of the JACoW Invincible Paper Crawler are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of the JACoW Invincible Paper Crawler seriously. If you discover a security vulnerability, please follow these guidelines:

### How to Report

1. **Email**: Send a detailed report to mliu@ihep.ac.cn
2. **Subject**: Use "SECURITY VULNERABILITY - JACoW Crawler" in the subject line
3. **Encryption**: For sensitive vulnerabilities, consider using PGP encryption

### What to Include

Please include as much of the following information as possible:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and severity
- **Reproduction**: Step-by-step instructions to reproduce
- **Environment**: Operating system, Python version, dependencies
- **Proof of Concept**: If applicable, include PoC code (responsibly)
- **Suggested Fix**: If you have ideas for fixing the issue

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 24 hours
- **Initial Assessment**: Initial assessment within 72 hours
- **Regular Updates**: We'll provide updates every 7 days
- **Resolution Timeline**: We aim to resolve critical issues within 30 days

### Our Commitment

- We will not pursue legal action against security researchers who report vulnerabilities responsibly
- We will acknowledge your contribution (unless you prefer to remain anonymous)
- We will keep you informed throughout the resolution process

## Security Best Practices

### For Users

1. **Keep Updated**: Always use the latest version
2. **Verify Downloads**: Check file integrity when downloading papers
3. **Network Security**: Use secure networks when crawling
4. **Access Control**: Protect your downloaded papers appropriately
5. **Configuration**: Review and secure your configuration files

### For Developers

1. **Input Validation**: All inputs are validated and sanitized
2. **Secure Defaults**: Default configurations prioritize security
3. **Minimal Permissions**: Request only necessary permissions
4. **Error Handling**: Errors don't expose sensitive information
5. **Dependencies**: Regular dependency security audits

## Known Security Considerations

### Network Requests
- The crawler makes HTTP/HTTPS requests to JACoW websites
- All requests include appropriate rate limiting
- No sensitive credentials are transmitted

### File Downloads
- Downloaded files are validated for type and size
- Filenames are sanitized to prevent directory traversal
- Files are stored in designated directories only

### Configuration
- Configuration files may contain paths and preferences
- No passwords or API keys are stored in configuration
- File permissions are set appropriately

### Logging
- Logs may contain URLs and paper titles
- No personal information is logged
- Log files should be protected appropriately

## Vulnerability Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1**: Acknowledgment sent
3. **Day 3**: Initial assessment completed
4. **Day 7**: Regular status update
5. **Day 14**: Regular status update
6. **Day 21**: Regular status update
7. **Day 30**: Target resolution date
8. **Post-Fix**: Public disclosure (coordinated)

## Security Updates

Security updates will be:
- Released as patch versions (e.g., 1.0.1)
- Documented in CHANGELOG.md
- Announced in GitHub releases
- Tagged with security labels

## Scope

This security policy covers:
- The main crawler application
- All included modules and utilities
- Documentation and examples
- CI/CD pipelines and workflows

This policy does not cover:
- Third-party dependencies (report to their maintainers)
- JACoW websites themselves (contact JACoW directly)
- User-specific configurations or deployments

## Contact Information

- **Security Contact**: mliu@ihep.ac.cn
- **Project Maintainer**: Ming Liu
- **Institution**: Institute of High Energy Physics (IHEP), Chinese Academy of Sciences

## Recognition

We maintain a security hall of fame for researchers who responsibly disclose vulnerabilities:

<!-- Security researchers will be listed here -->

Thank you for helping keep the JACoW Invincible Paper Crawler secure! 🔒

---
**Last Updated**: September 9, 2025
**Policy Version**: 1.0
