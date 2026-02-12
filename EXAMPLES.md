# Attack Path Mapper - Example Scenarios

This directory contains various example scan scenarios demonstrating different attack paths and use cases.

## Example 1: Basic Web Application Attack

**File:** `example_basic_webapp.json`

**Scenario:** Simple web application with SQL injection and privilege escalation

**Attack Path:**
```
SQL Injection → Privilege Escalation → Data Exfiltration
```

**Key Learning:** Shows a classic web app compromise chain

---

## Example 2: Cloud Misconfiguration

**File:** `example_cloud_breach.json`

**Scenario:** AWS environment with misconfigured S3 and exposed credentials

**Attack Path:**
```
Public S3 Bucket → Exposed Credentials → Lateral Movement → Data Exfiltration
```

**Key Learning:** Cloud security misconfigurations can lead to direct data access

---

## Example 3: Network Penetration

**File:** `example_network_pentest.json`

**Scenario:** Corporate network with weak authentication and lateral movement opportunities

**Attack Path:**
```
Weak SSH → Credential Reuse → Lateral Movement → Domain Admin
```

**Key Learning:** Shows how initial access can lead to complete network compromise

---

## Example 4: Complex Multi-Vector Attack

**File:** `example_scan_complex.json`

**Scenario:** Enterprise environment with multiple entry points and privilege escalation paths

**Attack Paths (Multiple):**
1. Web → Database → Exfiltration
2. SSH → Docker Escape → Root
3. S3 → Credentials → Cloud Account

**Key Learning:** Real-world environments have multiple attack vectors

---

## Example 5: IoT/Embedded Device

**File:** `example_iot_device.json`

**Scenario:** IoT device with default credentials and no encryption

**Attack Path:**
```
Default Credentials → Firmware Extraction → Backdoor Installation
```

**Key Learning:** IoT devices often have fundamental security issues

---

## How to Use These Examples

### Run Analysis
```bash
python attack_path_mapper.py examples/example_basic_webapp.json
```

### View in Web Interface
```bash
python web_visualizer.py
# Then navigate to http://localhost:8000
# Enter: examples/example_basic_webapp.json
```

### Compare Scenarios
```bash
# Run each example and compare risk scores
python attack_path_mapper.py examples/example_cloud_breach.json > cloud_report.txt
python attack_path_mapper.py examples/example_network_pentest.json > network_report.txt
```

---

## Creating Your Own Examples

Use these examples as templates. Key elements:

1. **Realistic vulnerabilities** - Based on real-world findings
2. **Clear attack chains** - Vulnerabilities should logically connect
3. **Varied severity** - Mix of critical and medium risks
4. **Multiple paths** - Show different ways to achieve objectives

---

## Example Risk Comparisons

| Scenario | Highest Risk Path | Max Impact | Fastest Path |
|----------|------------------|------------|--------------|
| Basic Web App | 84.4/100 | 10/10 | 3 steps |
| Cloud Breach | 86.0/100 | 10/10 | 2 steps |
| Network Pentest | 78.2/100 | 9/10 | 4 steps |
| Complex Multi | 88.5/100 | 10/10 | 3 steps |
| IoT Device | 72.8/100 | 8/10 | 2 steps |

---

## Learning Resources

Each example demonstrates different security concepts:

- **Basic Web App**: OWASP Top 10, web security fundamentals
- **Cloud Breach**: Cloud security, IAM misconfigurations
- **Network Pentest**: Lateral movement, credential security
- **Complex Multi**: Enterprise security, defense in depth
- **IoT Device**: Embedded security, supply chain risks

---

## Contributing Examples

Have a great example scenario? Consider:
1. Base it on real (anonymized) findings
2. Include clear descriptions
3. Map to MITRE ATT&CK
4. Document the learning objectives

---

*These examples are for educational and authorized testing purposes only.*
