# MITRE ATT&CK Technique Mapping Reference

This document details how Attack Path Mapper maps vulnerabilities to MITRE ATT&CK techniques.

## Supported Techniques

### Initial Access

#### T1190: Exploit Public-Facing Application
**Vulnerabilities:**
- SQL Injection (`web_sqli`)
- Cross-Site Scripting (`web_xss`)
- Open ports without authentication (`open_port`)

**Description:** Adversaries may attempt to exploit a weakness in an Internet-facing computer or program using software, data, or commands to cause unintended behavior.

**Examples in Attack Paths:**
```
[Open Port 27017] MongoDB without auth → [T1190] Initial Access
[Web SQLi] Login form injection → [T1190] Initial Access
```

#### T1078: Valid Accounts
**Vulnerabilities:**
- Credential reuse (`credential_reuse`)
- Weak passwords (`ssh_weak_auth`)

**Description:** Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access.

**Examples in Attack Paths:**
```
[SSH Weak Auth] → [Credential Dump] → [T1078] Valid Accounts → Lateral Movement
```

---

### Credential Access

#### T1110: Brute Force
**Vulnerabilities:**
- Weak SSH authentication (`ssh_weak_auth`)

**Description:** Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained.

**Examples in Attack Paths:**
```
[SSH Port 22 Open] → [T1110] Brute Force → [Weak Password] → Access Gained
```

#### T1003: OS Credential Dumping
**Vulnerabilities:**
- Privilege escalation vulnerabilities that allow credential access
- Memory dump capabilities

**Description:** Adversaries may attempt to dump credentials to obtain account login information.

**Examples in Attack Paths:**
```
[Privilege Escalation] → [T1003] Credential Dumping → [Password Hashes] → Lateral Movement
```

#### T1552: Unsecured Credentials
**Vulnerabilities:**
- Misconfigured S3 buckets (`misconfigured_s3`)
- Hardcoded credentials (`credential_reuse`)

**Description:** Adversaries may search compromised systems to find and obtain insecurely stored credentials.

**Examples in Attack Paths:**
```
[Public S3 Bucket] → [T1552] Exposed Credentials → [Cloud Access]
```

---

### Privilege Escalation

#### T1068: Exploitation for Privilege Escalation
**Vulnerabilities:**
- Sudo misconfigurations (`privilege_escalation`)
- Docker group membership
- SUID binaries

**Description:** Adversaries may exploit software vulnerabilities in an attempt to elevate privileges.

**Examples in Attack Paths:**
```
[Initial Access] → [Docker Group] → [T1068] Privilege Escalation → [Root Access]
```

---

### Lateral Movement

#### T1021: Remote Services
**Vulnerabilities:**
- SSH with weak authentication
- Credential reuse across services

**Description:** Adversaries may use Valid Accounts to log into a service specifically designed to accept remote connections.

**Examples in Attack Paths:**
```
[Compromised Credentials] → [T1021] SSH Lateral Movement → [Additional Hosts]
```

---

### Exfiltration

#### T1048: Exfiltration Over Alternative Protocol
**Vulnerabilities:**
- No egress filtering (`data_exfiltration`)
- Unrestricted outbound connections

**Description:** Adversaries may steal data by exfiltrating it over a different protocol than that of the existing command and control channel.

**Examples in Attack Paths:**
```
[Data Access] → [No Egress Filtering] → [T1048] DNS Tunneling → [Data Exfiltrated]
```

---

## Attack Path Examples by Tactic

### Full Kill Chain Example 1: Web Application Compromise

```
┌─────────────────────────────────────────────────────────────┐
│ Initial Access                                               │
│ [T1190] SQL Injection in login form                         │
│ Severity: 9/10 | Exploitability: 80%                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Privilege Escalation                                         │
│ [T1068] Docker group privilege escalation                   │
│ Severity: 9/10 | Exploitability: 60%                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Credential Access                                            │
│ [T1003] Dump password hashes from /etc/shadow               │
│ Severity: 8/10 | Exploitability: 70%                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Exfiltration                                                 │
│ [T1048] Exfiltrate data over DNS (no egress filtering)      │
│ Severity: 10/10 | Exploitability: 80%                       │
└─────────────────────────────────────────────────────────────┘

Total Risk: 88.2/100
Attack Vector: Web → Docker → Credentials → Exfiltration
```

### Full Kill Chain Example 2: Cloud Misconfiguration

```
┌─────────────────────────────────────────────────────────────┐
│ Initial Access                                               │
│ [T1552] Public S3 bucket with AWS credentials               │
│ Severity: 8/10 | Exploitability: 90%                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Credential Access                                            │
│ [T1078] Use valid AWS credentials                           │
│ Severity: 7/10 | Exploitability: 100%                       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Exfiltration                                                 │
│ [T1048] Download all S3 data                                │
│ Severity: 10/10 | Exploitability: 100%                      │
└─────────────────────────────────────────────────────────────┘

Total Risk: 86.0/100
Attack Vector: Misconfiguration → Valid Credentials → Data Theft
```

---

## Tactic Coverage Matrix

| Tactic | Techniques Covered | Vulnerability Types |
|--------|-------------------|---------------------|
| **Initial Access** | T1190, T1078, T1189 | SQLi, XSS, Open Ports, Weak Auth |
| **Credential Access** | T1110, T1003, T1552 | Brute Force, Credential Dump, Exposed Creds |
| **Privilege Escalation** | T1068 | Sudo, Docker, SUID |
| **Lateral Movement** | T1021 | SSH, RDP, Credential Reuse |
| **Exfiltration** | T1048 | No Egress Filtering |

---

## Adding New Techniques

To add a new MITRE ATT&CK technique:

1. **Add to the enum** in `attack_path_mapper.py`:
```python
class AttackTechnique(Enum):
    YOUR_TECHNIQUE = ("T1234", "Technique Name", "Tactic Name")
```

2. **Add to the vulnerability mapping**:
```python
mapping = {
    'your_vuln_type': (
        AttackTechnique.YOUR_TECHNIQUE,
        8,                                # Severity
        0.7,                              # Exploitability
        ['prerequisite_vuln_id']          # Prerequisites
    ),
}
```

3. **Update this documentation** with the new technique details.

---

## References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [ATT&CK for CTI](https://attack.mitre.org/resources/getting-started/)

---

## Technique Selection Criteria

When mapping vulnerabilities to techniques, we consider:

1. **Accuracy**: Does the technique accurately describe the attack action?
2. **Specificity**: Is there a more specific technique available?
3. **Context**: Does the technique fit in the overall attack chain?
4. **Industry Usage**: Is this technique commonly referenced in CTI?

---

## Future Enhancements

Planned technique additions:
- [ ] T1059: Command and Scripting Interpreter
- [ ] T1053: Scheduled Task/Job
- [ ] T1486: Data Encrypted for Impact
- [ ] T1562: Impair Defenses
- [ ] T1210: Exploitation of Remote Services
- [ ] T1133: External Remote Services
- [ ] T1566: Phishing

---

Last Updated: February 2026
Version: 1.0
