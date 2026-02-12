# 🤝 Contributing to Attack Path Mapper

Thank you for your interest in contributing! This guide will help you get started.

## 🌟 Ways to Contribute

### 1. Report Bugs
Found a bug? Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Sample scan file (if applicable)

### 2. Suggest Features
Have an idea? Open an issue with:
- Clear feature description
- Use case / why it's valuable
- Potential implementation approach
- Examples of similar features elsewhere

### 3. Improve Documentation
Documentation is crucial! You can:
- Fix typos or unclear sections
- Add examples and tutorials
- Improve code comments
- Create video guides or blog posts

### 4. Submit Code
- Bug fixes
- New features
- Performance improvements
- Test coverage
- Code refactoring

### 5. Create Examples
- Real-world attack scenarios
- Integration examples
- Tool comparisons
- Case studies

## 🚀 Getting Started

### Setup Development Environment

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/attack-path-mapper.git
cd attack-path-mapper

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python attack_path_mapper.py sample_scan.json
```

### Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

## 📝 Code Guidelines

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused (single responsibility)
- Use type hints where appropriate

**Example:**
```python
def calculate_risk_score(severity: int, exploitability: float) -> float:
    """
    Calculate weighted risk score for an attack node.
    
    Args:
        severity: Vulnerability severity (1-10)
        exploitability: How easy to exploit (0-1)
    
    Returns:
        Weighted risk score (0-10)
    """
    return (severity * 0.7) + (exploitability * 10 * 0.3)
```

### Commit Messages
Use clear, descriptive commit messages:

```bash
# Good commits
git commit -m "Add T1059 Command and Scripting Interpreter technique"
git commit -m "Fix risk scoring calculation for edge cases"
git commit -m "Update README with Azure integration examples"

# Bad commits (too vague)
git commit -m "Update code"
git commit -m "Fix bug"
git commit -m "Changes"
```

### Testing
Test your changes:

```bash
# Test with basic example
python attack_path_mapper.py sample_scan.json

# Test with complex example
python attack_path_mapper.py example_scan_complex.json

# Test web interface
python web_visualizer.py
# Navigate to http://localhost:8000 and test manually
```

## 🎯 Priority Contributions

These are particularly valuable:

### High Priority
- [ ] Unit tests for core functions
- [ ] Integration with popular scanners (Nmap, Nessus, OpenVAS)
- [ ] More MITRE ATT&CK techniques
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)

### Medium Priority
- [ ] CVE database integration
- [ ] Historical attack path database
- [ ] Export to MITRE Navigator format
- [ ] PDF report generation
- [ ] API for programmatic access

### Enhancement Ideas
- [ ] Machine learning for path prediction
- [ ] Cloud-specific attack paths (AWS, Azure, GCP)
- [ ] Kubernetes/container attack paths
- [ ] Active Directory attack paths
- [ ] Collaborative analysis features

## 📚 Adding New Features

### Adding a New Vulnerability Type

1. **Add to the mapping** in `attack_path_mapper.py`:
```python
mapping = {
    'your_new_vuln': (
        AttackTechnique.YOUR_TECHNIQUE,  # MITRE technique
        8,                                # Severity (1-10)
        0.7,                              # Exploitability (0-1)
        ['prerequisite_vuln']             # Dependencies (optional)
    ),
}
```

2. **Update MITRE_MAPPING.md** with technique details

3. **Add example** to examples directory

4. **Test** with real scan data

### Adding a New MITRE Technique

1. **Add to enum** in `attack_path_mapper.py`:
```python
class AttackTechnique(Enum):
    YOUR_TECHNIQUE = ("T1234", "Technique Name", "Tactic")
```

2. **Document in MITRE_MAPPING.md**:
- Technique description
- When to use it
- Example attack paths
- References to MITRE ATT&CK

3. **Map vulnerabilities** to the new technique

### Adding Scanner Integration

Create a converter script in `scripts/` directory:

```python
#!/usr/bin/env python3
"""Convert YourScanner output to Attack Path Mapper format"""

def convert_your_scanner(input_file: str, output_file: str):
    # Parse scanner output
    # Map to vulnerability types
    # Generate JSON
    pass

if __name__ == "__main__":
    # CLI handling
    pass
```

## 🔍 Pull Request Process

1. **Update documentation** if needed
   - README.md for new features
   - MITRE_MAPPING.md for new techniques
   - EXAMPLES.md for new examples

2. **Test thoroughly**
   - Run existing examples
   - Add new examples for your feature
   - Test web interface if affected

3. **Create pull request**
   - Clear title describing the change
   - Detailed description in the PR body
   - Reference any related issues
   - Include screenshots for UI changes

4. **PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
How you tested the changes

## Screenshots
If applicable

## Related Issues
Closes #123
```

## 🐛 Bug Fix Guidelines

### Before Fixing
1. Reproduce the bug
2. Understand root cause
3. Check if it affects other areas

### When Fixing
1. Fix the root cause, not symptoms
2. Add comments explaining the fix
3. Consider edge cases
4. Test thoroughly

### After Fixing
1. Verify the fix works
2. Check for regressions
3. Update tests if needed
4. Document in commit message

## 📊 Example Contribution Workflow

```bash
# 1. Start from main branch
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/add-rdp-technique

# 3. Make changes
# Edit attack_path_mapper.py
# Add RDP technique to AttackTechnique enum
# Add 'rdp_weak_auth' to vulnerability mapping

# 4. Test changes
python attack_path_mapper.py sample_scan.json

# 5. Update documentation
# Edit MITRE_MAPPING.md with RDP technique details

# 6. Commit changes
git add attack_path_mapper.py MITRE_MAPPING.md
git commit -m "Add T1021.001 RDP technique support

- Add RDP to AttackTechnique enum
- Map rdp_weak_auth vulnerability type
- Document in MITRE_MAPPING.md
- Tested with sample scan data"

# 7. Push to your fork
git push origin feature/add-rdp-technique

# 8. Open pull request on GitHub
```

## 🎨 Style Preferences

### Code Style
- **Indentation:** 4 spaces (not tabs)
- **Line length:** Max 100 characters
- **Imports:** Group by standard lib, third-party, local
- **Quotes:** Single quotes for strings, double for docstrings

### Documentation Style
- **Markdown:** Use proper headers (# ## ###)
- **Code blocks:** Include language identifier
- **Links:** Use descriptive text, not "click here"
- **Lists:** Parallel structure in bullet points

### Naming Conventions
- **Classes:** PascalCase (e.g., `AttackPathMapper`)
- **Functions:** snake_case (e.g., `calculate_risk_score`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_PATHS`)
- **Variables:** snake_case (e.g., `total_risk`)

## 🚫 What Not to Do

- Don't submit large PRs with multiple unrelated changes
- Don't break existing functionality
- Don't ignore code style guidelines
- Don't add dependencies without discussion
- Don't copy code without attribution
- Don't include sensitive data in examples

## ✅ Code Review Process

### What Reviewers Look For
- Code quality and style
- Test coverage
- Documentation updates
- Performance impact
- Security implications
- Breaking changes

### Response Times
- Initial review: Within 3-5 days
- Follow-up reviews: Within 2 days
- Merge after approval: Within 1 day

### If Changes Are Requested
- Address feedback promptly
- Ask questions if unclear
- Push new commits (don't force push)
- Re-request review when ready

## 📞 Getting Help

### Questions?
- Open a GitHub issue with the "question" label
- Include context and what you've tried
- Be specific about what you need help with

### Discussion?
- Open a GitHub discussion
- Use for design decisions
- Brainstorm features
- Architecture questions

### Security Issues?
- **Do NOT open public issues**
- Email directly: [your-email@example.com]
- We'll respond within 24 hours
- Follow responsible disclosure

## 🏆 Recognition

Contributors will be:
- Listed in README.md contributors section
- Mentioned in release notes
- Given credit in commit messages
- Invited to join the core team (for regular contributors)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution matters, whether it's:
- A typo fix
- A new feature
- A bug report
- A star on GitHub

Thank you for making Attack Path Mapper better! 🎯

---

**Questions?** Open an issue or start a discussion!

**Last Updated:** February 2026
