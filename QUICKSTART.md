# 🚀 Quick Start Guide

Get up and running with Attack Path Mapper in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Step 1: Clone or Download

```bash
# Option 1: Clone the repository
git clone https://github.com/yourusername/attack-path-mapper.git
cd attack-path-mapper

# Option 2: Download and extract the ZIP
# Then navigate to the folder in terminal
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! Just one dependency: NetworkX.

## First Run - Demo Mode

Let's create a sample scan and analyze it:

```bash
# Create a sample scan file
python attack_path_mapper.py --demo

# Analyze it
python attack_path_mapper.py sample_scan.json
```

You should see output like this:

```
╔═══════════════════════════════════════════════════════════════╗
║           🎯 ATTACK PATH MAPPER v1.0                         ║
║     Strategic Security Analysis & Threat Modeling Tool        ║
╚═══════════════════════════════════════════════════════════════╝

[+] Loaded 6 vulnerabilities
[*] Building attack graph...
[+] Created graph with 6 nodes and 8 edges
[*] Analyzing attack paths...

════════════════════════════════════════════════════════════════
🎯 ATTACK PATH MAPPER - THREAT ANALYSIS REPORT
════════════════════════════════════════════════════════════════

ATTACK PATH #1
Risk Score: 84.40/100
Likelihood: 70%
Impact: 10/10
...
```

## Web Interface

Want the fancy interactive visualization? Run the web server:

```bash
python web_visualizer.py
```

Then open your browser to: **http://localhost:8000**

You'll see:
- Interactive graph with drag-and-drop nodes
- Real-time statistics
- Clickable attack paths
- Beautiful visualizations

## Using Your Own Scan Data

### Step 1: Create Your Scan JSON

Create a file called `my_scan.json`:

```json
{
  "scan_date": "2026-02-05",
  "target": "your-target.com",
  "vulnerabilities": [
    {
      "id": "vuln_1",
      "type": "ssh_weak_auth",
      "description": "SSH with weak authentication",
      "port": 22,
      "service": "SSH"
    },
    {
      "id": "vuln_2",
      "type": "web_sqli",
      "description": "SQL injection in login",
      "port": 443,
      "service": "HTTPS"
    }
  ]
}
```

### Step 2: Run Analysis

```bash
python attack_path_mapper.py my_scan.json
```

### Step 3: Review Results

The tool will:
1. Build an attack graph
2. Find attack paths
3. Calculate risk scores
4. Generate a report file

Report saved to: `attack_report_YYYYMMDD_HHMMSS.txt`

## Supported Vulnerability Types

Just use these types in your JSON:

| Type | Description |
|------|-------------|
| `ssh_weak_auth` | Weak SSH authentication |
| `web_sqli` | SQL injection |
| `web_xss` | Cross-site scripting |
| `misconfigured_s3` | Public S3 bucket |
| `privilege_escalation` | Privilege escalation path |
| `credential_reuse` | Credential reuse |
| `data_exfiltration` | Data exfiltration risk |
| `open_port` | Exposed service |

## Common Use Cases

### Security Assessment Report
```bash
# Scan your target
nmap -sV -oX scan.xml target.com

# Convert to JSON (use your preferred tool)
# ...

# Analyze
python attack_path_mapper.py scan.json
```

### Red Team Planning
```bash
# Use the web interface for interactive planning
python web_visualizer.py

# Open browser to http://localhost:8000
# Click paths to visualize attack chains
```

### Vulnerability Prioritization
```bash
# Run analysis
python attack_path_mapper.py pentest_results.json

# Check the RECOMMENDATIONS section for prioritized fixes
```

## Tips & Tricks

### Tip 1: Focus on High-Risk Paths
The tool ranks paths by risk. Focus remediation on Path #1 first!

### Tip 2: Use the Web Interface for Presentations
The D3.js visualization makes great screenshots for reports and presentations.

### Tip 3: Export Reports
Reports are automatically saved to timestamped files. Perfect for documentation.

### Tip 4: Compare Before/After
Run the tool before and after fixes to show improvement in risk posture.

## Troubleshooting

### "ModuleNotFoundError: No module named 'networkx'"
```bash
pip install networkx
```

### "FileNotFoundError: sample_scan.json not found"
```bash
python attack_path_mapper.py --demo
```

### Web interface not loading
Make sure you're navigating to http://localhost:8000, not https://

### No attack paths found
This means your vulnerabilities don't form complete chains. Try adding more related vulnerabilities.

## What's Next?

- Read the [full README](README.md) for detailed documentation
- Check [MITRE_MAPPING.md](MITRE_MAPPING.md) for technique details
- Try the complex example: `python attack_path_mapper.py example_scan_complex.json`
- Customize the tool by adding your own vulnerability types

## Need Help?

- Check the [README](README.md) for comprehensive documentation
- Look at the example files for reference
- Open an issue on GitHub if you find bugs

---

**Ready to secure some systems? Let's go! 🚀**

Made with ❤️ for security professionals and students
