# 🎯 Attack Path Mapper

> **Strategic Security Analysis & Threat Modeling Tool**
> 
> Converts vulnerability scan results into actionable attack chains with MITRE ATT&CK mapping and risk scoring

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🚀 What It Does

Attack Path Mapper takes vulnerability scan results and transforms them into **strategic attack chains** that show:

- **HOW** an attacker would actually compromise your system
- **WHICH** vulnerabilities matter most in context
- **WHAT** the complete attack path looks like from entry to objective

Instead of a flat list of vulnerabilities, you get:

```
Open SSH → Weak Password → Privilege Escalation → Data Exfiltration
   ↓            ↓                   ↓                      ↓
 T1110        T1078               T1068                  T1048
Risk: 7.0    Risk: 7.0          Risk: 8.4              Risk: 9.4
```

## ✨ Features

### Core Analysis Engine
- **Graph-Based Attack Modeling**: Uses NetworkX to build attack dependency graphs
- **MITRE ATT&CK Integration**: Maps vulnerabilities to ATT&CK techniques and tactics
- **Risk Scoring Algorithm**: Calculates weighted risk based on severity and exploitability
- **Attack Path Discovery**: Automatically finds highest-risk attack chains
- **Multi-Path Analysis**: Identifies up to 5 different attack scenarios

### Interactive Web Visualization
- **D3.js Force-Directed Graph**: Beautiful, interactive attack path visualization
- **Real-Time Analysis**: Web interface for instant feedback
- **Path Highlighting**: Click paths to highlight them on the graph
- **Severity Color Coding**: Visual risk assessment at a glance
- **Responsive Design**: Works on desktop and mobile

### Professional Reporting
- **Detailed Attack Reports**: Complete breakdown of each attack path
- **MITRE ATT&CK Mapping**: Shows technique IDs, names, and tactics
- **Prioritized Recommendations**: Risk-ranked remediation guidance
- **Exportable Results**: Save reports for documentation and compliance

## 📋 Requirements

```bash
Python 3.8+
networkx>=2.6.3
```

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/attack-path-mapper.git
cd attack-path-mapper

# Install dependencies
pip install -r requirements.txt

# Create a sample scan file
python attack_path_mapper.py --demo

# Run analysis
python attack_path_mapper.py sample_scan.json
```

## 🎮 Usage

### Command Line Interface

**Basic Analysis:**
```bash
python attack_path_mapper.py scan_results.json
```

**Create Demo Data:**
```bash
python attack_path_mapper.py --demo
```

**Output:**
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
Generated: 2026-02-05 14:30:00
Total Vulnerabilities Analyzed: 6
Attack Paths Identified: 3
════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
ATTACK PATH #1
────────────────────────────────────────────────────────────────
Risk Score: 84.40/100
Likelihood: 70%
Impact: 10/10

Attack Chain:
  1. [T1190] SQL injection in login form
     Technique: SQL Injection
     Tactic: Initial Access
     Severity: 9/10 | Exploitability: 80%

  2. [T1068] Sudo misconfiguration allows privilege escalation
     Technique: Exploitation for Privilege Escalation
     Tactic: Privilege Escalation
     Severity: 9/10 | Exploitability: 60%

  3. [T1048] No egress filtering - data exfiltration possible
     Technique: Exfiltration Over Alternative Protocol
     Tactic: Exfiltration
     Severity: 10/10 | Exploitability: 80%

Full Path: SQL injection in login form → Sudo misconfiguration 
           allows privilege escalation → No egress filtering - 
           data exfiltration possible
```

### Web Interface

**Start the web server:**
```bash
python web_visualizer.py
```

**Then open your browser to:**
```
http://localhost:8000
```

**Features:**
- Interactive force-directed graph visualization
- Click and drag nodes to explore relationships
- Hover over nodes for detailed information
- Click attack paths in the sidebar to highlight them
- Real-time statistics and metrics
- Export reports directly from the browser

## 📁 Input Format

Attack Path Mapper accepts JSON files with this structure:

```json
{
  "scan_date": "2026-02-05",
  "target": "192.168.1.100",
  "vulnerabilities": [
    {
      "id": "ssh_weak_auth",
      "type": "ssh_weak_auth",
      "description": "SSH with weak password authentication",
      "port": 22,
      "service": "SSH"
    },
    {
      "id": "web_sqli",
      "type": "web_sqli",
      "description": "SQL injection in login form",
      "port": 80,
      "service": "HTTP"
    }
  ]
}
```

### Supported Vulnerability Types

| Type | MITRE ATT&CK | Severity | Description |
|------|-------------|----------|-------------|
| `ssh_weak_auth` | T1110 | 7/10 | Weak SSH authentication |
| `web_sqli` | T1190 | 9/10 | SQL injection vulnerability |
| `web_xss` | T1189 | 6/10 | Cross-site scripting |
| `misconfigured_s3` | T1552 | 8/10 | Public S3 bucket |
| `privilege_escalation` | T1068 | 9/10 | Privilege escalation path |
| `credential_reuse` | T1078 | 7/10 | Credential reuse across services |
| `data_exfiltration` | T1048 | 10/10 | Data exfiltration capability |
| `open_port` | T1190 | 5/10 | Open network port |

## 🎨 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Scan Results (JSON)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              AttackPathMapper Core Engine                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Parse vulnerabilities                            │  │
│  │  2. Convert to AttackNodes with MITRE mapping        │  │
│  │  3. Build directed graph with dependencies           │  │
│  │  4. Run path-finding algorithms                      │  │
│  │  5. Calculate risk scores                            │  │
│  │  6. Prioritize attack chains                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
┌─────────────────────┐   ┌─────────────────────┐
│  Terminal Report    │   │  Web Visualization   │
│  • Detailed paths   │   │  • Interactive graph │
│  • MITRE mapping    │   │  • D3.js rendering   │
│  • Recommendations  │   │  • Real-time stats   │
└─────────────────────┘   └─────────────────────┘
```

## 🧮 Risk Scoring Algorithm

The risk score for each node is calculated as:

```python
risk_score = (severity * 0.7) + (exploitability * 10 * 0.3)
```

**Where:**
- **Severity** (1-10): How bad would exploitation be?
- **Exploitability** (0-1): How easy is it to exploit?

**Path Risk** is the sum of all node risk scores in the chain.

**Example:**
```
Node 1: Severity=9, Exploitability=0.8 → Risk=7.7
Node 2: Severity=8, Exploitability=0.6 → Risk=7.4
Node 3: Severity=10, Exploitability=0.9 → Risk=9.7
─────────────────────────────────────────────────
Total Path Risk: 24.8/30 (82.7%)
```

## 🎯 Use Cases

### Security Assessments
- Prioritize vulnerabilities by actual exploitability
- Show clients HOW attacks would unfold
- Focus remediation on high-impact paths

### Red Team Planning
- Identify realistic attack vectors
- Plan multi-stage attacks
- Map MITRE ATT&CK coverage

### Blue Team Defense
- Understand attacker perspective
- Prioritize defensive controls
- Test detection capabilities

### Academic/Learning
- Understand attack methodology
- Learn MITRE ATT&CK framework
- Visualize security concepts

## 📊 Example Output

### Attack Path #1: Critical Risk
```
Risk Score: 84.40/100 ⚠️
Likelihood: 70%
Impact: 10/10

┌─────────────────────────────────────────────────────────┐
│ Step 1: Initial Access                                  │
│ [T1190] SQL injection in login form                     │
│ Severity: 9/10 | Exploitability: 80%                    │
├─────────────────────────────────────────────────────────┤
│ Step 2: Privilege Escalation                            │
│ [T1068] Sudo misconfiguration                           │
│ Severity: 9/10 | Exploitability: 60%                    │
├─────────────────────────────────────────────────────────┤
│ Step 3: Exfiltration                                    │
│ [T1048] No egress filtering                             │
│ Severity: 10/10 | Exploitability: 80%                   │
└─────────────────────────────────────────────────────────┘

Recommendation: CRITICAL - Remediate SQL injection 
immediately. This is the entry point for the highest-risk 
attack path.
```

## 🛠️ Extending the Tool

### Adding New Vulnerability Types

Edit the `_vulnerability_to_node()` method in `attack_path_mapper.py`:

```python
mapping = {
    'your_vuln_type': (
        AttackTechnique.YOUR_TECHNIQUE,  # MITRE technique
        8,                                # Severity (1-10)
        0.7,                              # Exploitability (0-1)
        ['prerequisite_vuln']             # Dependencies
    ),
}
```

### Custom MITRE ATT&CK Techniques

Add to the `AttackTechnique` enum:

```python
class AttackTechnique(Enum):
    YOUR_TECHNIQUE = ("T1234", "Technique Name", "Tactic")
```

## 🤝 Integration

### With Nmap
```bash
# Run nmap with XML output
nmap -sV -oX scan.xml target.com

# Convert to JSON (use your preferred converter)
# Then run Attack Path Mapper
python attack_path_mapper.py scan.json
```

### With OpenVAS
```bash
# Export OpenVAS results as JSON
# Run Attack Path Mapper
python attack_path_mapper.py openvas_results.json
```

### With Custom Scanners
Just format your results to match the input JSON structure!

## 📈 Performance

- **Small scans** (1-10 vulnerabilities): < 1 second
- **Medium scans** (10-50 vulnerabilities): 1-3 seconds
- **Large scans** (50-200 vulnerabilities): 3-10 seconds

Graph complexity: O(V + E) where V = vulnerabilities, E = dependency edges

## 🔒 Security Considerations

⚠️ **This tool is for AUTHORIZED security testing only**

- Always get permission before scanning networks
- Never use on systems you don't own or have explicit authorization to test
- Results should be handled as sensitive security data
- Follow responsible disclosure practices

## 🏆 Why This Tool Stands Out

### For Students/New Grads
- **Demonstrates strategic thinking**: Not just finding bugs, but understanding how they chain together
- **Blue + Red team crossover**: Shows offensive and defensive mindset
- **Real-world applicable**: Solves actual pentesting workflow problem
- **Uncommon for undergrads**: Most security projects are simple scanners or exploits

### For Professionals
- **Saves time**: Automates attack chain analysis
- **Improves reporting**: Visual, easy-to-understand results
- **Risk prioritization**: Focus on what matters
- **Framework aligned**: Maps to MITRE ATT&CK for compliance

## 📝 Contributing

Contributions welcome! Ideas for improvements:

- [ ] Integration with CVE database
- [ ] Machine learning for path prediction
- [ ] More MITRE ATT&CK techniques
- [ ] Cloud-specific attack paths (AWS, Azure, GCP)
- [ ] Container/Kubernetes attack paths
- [ ] Historical attack path database
- [ ] Collaborative features for team assessments

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- MITRE ATT&CK Framework
- NetworkX library
- D3.js visualization library
- The security research community

---

**⭐ If you find this tool useful, please star the repository!**

Made with ❤️ for the security community
