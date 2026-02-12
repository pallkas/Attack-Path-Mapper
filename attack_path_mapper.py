#!/usr/bin/env python3
"""
Attack Path Mapper - Strategic Security Analysis Tool
Converts scan results into actionable attack chains with MITRE ATT&CK mapping
"""

import json
import networkx as nx
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import sys
from datetime import datetime


class AttackTechnique(Enum):
    """MITRE ATT&CK Technique mappings"""
    BRUTE_FORCE = ("T1110", "Brute Force", "Credential Access")
    EXPLOIT_PUBLIC = ("T1190", "Exploit Public-Facing Application", "Initial Access")
    VALID_ACCOUNTS = ("T1078", "Valid Accounts", "Initial Access")
    PRIVILEGE_ESC = ("T1068", "Exploitation for Privilege Escalation", "Privilege Escalation")
    SQLI = ("T1190", "SQL Injection", "Initial Access")
    XSS = ("T1189", "Cross-Site Scripting", "Initial Access")
    DATA_EXFIL = ("T1048", "Exfiltration Over Alternative Protocol", "Exfiltration")
    LATERAL_MOVE = ("T1021", "Remote Services", "Lateral Movement")
    CREDENTIAL_DUMP = ("T1003", "OS Credential Dumping", "Credential Access")
    MISCONFIG_EXPLOIT = ("T1552", "Unsecured Credentials", "Credential Access")


@dataclass
class AttackNode:
    """Represents a single step in an attack path"""
    id: str
    description: str
    technique: AttackTechnique
    severity: int  # 1-10
    exploitability: float  # 0-1
    prerequisites: List[str]
    
    def get_risk_score(self) -> float:
        """Calculate weighted risk score"""
        return (self.severity * 0.7 + self.exploitability * 10 * 0.3)


@dataclass
class AttackPath:
    """Complete attack chain from entry to objective"""
    nodes: List[AttackNode]
    total_risk: float
    likelihood: float
    impact_score: int
    path_description: str


class AttackPathMapper:
    """Core engine for building and analyzing attack paths"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.vulnerabilities: List[Dict] = []
        self.attack_nodes: Dict[str, AttackNode] = {}
        
    def load_scan_results(self, scan_file: str) -> None:
        """Load and parse scan results from JSON"""
        try:
            with open(scan_file, 'r') as f:
                data = json.load(f)
                self.vulnerabilities = data.get('vulnerabilities', [])
                print(f"[+] Loaded {len(self.vulnerabilities)} vulnerabilities")
        except Exception as e:
            print(f"[!] Error loading scan file: {e}")
            sys.exit(1)
    
    def build_attack_graph(self) -> None:
        """Convert vulnerabilities into attack graph"""
        print("[*] Building attack graph...")
        
        # Create attack nodes from vulnerabilities
        for vuln in self.vulnerabilities:
            node = self._vulnerability_to_node(vuln)
            if node:
                self.attack_nodes[node.id] = node
                self.graph.add_node(node.id, data=node)
        
        # Create edges based on attack flow logic
        self._create_attack_edges()
        
        print(f"[+] Created graph with {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges")
    
    def _vulnerability_to_node(self, vuln: Dict) -> AttackNode:
        """Convert vulnerability data to AttackNode"""
        vuln_type = vuln.get('type', '').lower()
        
        # Map vulnerability types to attack techniques
        mapping = {
            'ssh_weak_auth': (AttackTechnique.BRUTE_FORCE, 7, 0.7, []),
            'open_port': (AttackTechnique.EXPLOIT_PUBLIC, 5, 0.5, []),
            'web_sqli': (AttackTechnique.SQLI, 9, 0.8, []),
            'web_xss': (AttackTechnique.XSS, 6, 0.6, []),
            'misconfigured_s3': (AttackTechnique.MISCONFIG_EXPLOIT, 8, 0.9, []),
            'privilege_escalation': (AttackTechnique.PRIVILEGE_ESC, 9, 0.6, ['ssh_weak_auth', 'web_sqli']),
            'credential_reuse': (AttackTechnique.VALID_ACCOUNTS, 7, 0.7, ['ssh_weak_auth', 'web_sqli']),
            'data_exfiltration': (AttackTechnique.DATA_EXFIL, 10, 0.8, ['privilege_escalation', 'misconfigured_s3']),
        }
        
        if vuln_type in mapping:
            technique, severity, exploitability, prereqs = mapping[vuln_type]
            return AttackNode(
                id=vuln.get('id', vuln_type),
                description=vuln.get('description', f'{vuln_type} vulnerability'),
                technique=technique,
                severity=severity,
                exploitability=exploitability,
                prerequisites=prereqs
            )
        
        return None
    
    def _create_attack_edges(self) -> None:
        """Create directed edges representing attack flow"""
        for node_id, node in self.attack_nodes.items():
            # Connect prerequisites
            for prereq in node.prerequisites:
                if prereq in self.attack_nodes:
                    weight = node.get_risk_score()
                    self.graph.add_edge(prereq, node_id, weight=weight)
            
            # If no prerequisites, it's an entry point
            if not node.prerequisites:
                self.graph.add_edge('START', node_id, weight=0)
    
    def find_attack_paths(self, max_paths: int = 5) -> List[AttackPath]:
        """Find highest-risk attack paths through the graph"""
        print("[*] Analyzing attack paths...")
        
        # Add virtual END node for data exfiltration/compromise nodes
        end_node_types = ['data_exfiltration', 'privilege_escalation']
        for node_id, node in self.attack_nodes.items():
            if any(end_type in node_id for end_type in end_node_types):
                self.graph.add_edge(node_id, 'END', weight=node.get_risk_score())
        
        paths = []
        try:
            # Find all simple paths from START to END
            all_paths = list(nx.all_simple_paths(self.graph, 'START', 'END'))
            
            for path in all_paths[:max_paths]:
                attack_path = self._evaluate_path(path)
                if attack_path:
                    paths.append(attack_path)
            
            # Sort by total risk
            paths.sort(key=lambda x: x.total_risk, reverse=True)
            
        except nx.NetworkXNoPath:
            print("[!] No complete attack paths found")
        
        return paths[:max_paths]
    
    def _evaluate_path(self, path: List[str]) -> AttackPath:
        """Calculate risk metrics for an attack path"""
        # Filter out START and END nodes
        actual_nodes = [self.attack_nodes[node_id] for node_id in path[1:-1]]
        
        if not actual_nodes:
            return None
        
        # Calculate metrics
        total_risk = sum(node.get_risk_score() for node in actual_nodes)
        likelihood = min(node.exploitability for node in actual_nodes)
        impact_score = max(node.severity for node in actual_nodes)
        
        # Generate path description
        path_desc = " → ".join([node.description for node in actual_nodes])
        
        return AttackPath(
            nodes=actual_nodes,
            total_risk=total_risk,
            likelihood=likelihood,
            impact_score=impact_score,
            path_description=path_desc
        )
    
    def generate_report(self, paths: List[AttackPath]) -> str:
        """Generate detailed attack path report"""
        report = []
        report.append("=" * 80)
        report.append("🎯 ATTACK PATH MAPPER - THREAT ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Vulnerabilities Analyzed: {len(self.vulnerabilities)}")
        report.append(f"Attack Paths Identified: {len(paths)}")
        report.append("=" * 80)
        report.append("")
        
        for idx, path in enumerate(paths, 1):
            report.append(f"{'─' * 80}")
            report.append(f"ATTACK PATH #{idx}")
            report.append(f"{'─' * 80}")
            report.append(f"Risk Score: {path.total_risk:.2f}/100")
            report.append(f"Likelihood: {path.likelihood * 100:.0f}%")
            report.append(f"Impact: {path.impact_score}/10")
            report.append("")
            report.append("Attack Chain:")
            
            for step, node in enumerate(path.nodes, 1):
                report.append(f"  {step}. [{node.technique.value[0]}] {node.description}")
                report.append(f"     Technique: {node.technique.value[1]}")
                report.append(f"     Tactic: {node.technique.value[2]}")
                report.append(f"     Severity: {node.severity}/10 | Exploitability: {node.exploitability * 100:.0f}%")
                report.append("")
            
            report.append(f"Full Path: {path.path_description}")
            report.append("")
        
        report.append("=" * 80)
        report.append("RECOMMENDATIONS:")
        report.append("=" * 80)
        
        # Generate prioritized recommendations
        node_dict = {}
        for path in paths:
            for node in path.nodes:
                node_dict[node.id] = node
        
        # Sort by risk score
        sorted_nodes = sorted(node_dict.values(), key=lambda x: x.get_risk_score(), reverse=True)
        
        for idx, node in enumerate(sorted_nodes[:5], 1):
            report.append(f"{idx}. Remediate: {node.description}")
            report.append(f"   Priority: {'CRITICAL' if node.severity >= 8 else 'HIGH' if node.severity >= 6 else 'MEDIUM'}")
            report.append("")
        
        return "\n".join(report)


def create_sample_scan():
    """Create a sample scan results file for testing"""
    sample_data = {
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
            },
            {
                "id": "misconfigured_s3",
                "type": "misconfigured_s3",
                "description": "Publicly accessible S3 bucket",
                "service": "AWS S3"
            },
            {
                "id": "privilege_escalation",
                "type": "privilege_escalation",
                "description": "Sudo misconfiguration allows privilege escalation",
                "service": "Linux"
            },
            {
                "id": "credential_reuse",
                "type": "credential_reuse",
                "description": "Same credentials used across multiple services",
                "service": "Multiple"
            },
            {
                "id": "data_exfiltration",
                "type": "data_exfiltration",
                "description": "No egress filtering - data exfiltration possible",
                "service": "Network"
            }
        ]
    }
    
    with open('/home/claude/sample_scan.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("[+] Created sample scan file: sample_scan.json")


def main():
    """Main execution flow"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║           🎯 ATTACK PATH MAPPER v1.0                         ║
    ║     Strategic Security Analysis & Threat Modeling Tool        ║
    ║                                                               ║
    ║     Converts vulnerabilities into actionable attack chains    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) < 2:
        print("Usage: python attack_path_mapper.py <scan_results.json>")
        print("\nTo create a sample scan file, run:")
        print("  python attack_path_mapper.py --demo")
        sys.exit(1)
    
    if sys.argv[1] == '--demo':
        create_sample_scan()
        print("\nNow run: python attack_path_mapper.py sample_scan.json")
        sys.exit(0)
    
    # Initialize mapper
    mapper = AttackPathMapper()
    
    # Load scan results
    mapper.load_scan_results(sys.argv[1])
    
    # Build attack graph
    mapper.build_attack_graph()
    
    # Find attack paths
    paths = mapper.find_attack_paths(max_paths=5)
    
    if not paths:
        print("[!] No viable attack paths found")
        sys.exit(0)
    
    # Generate report
    report = mapper.generate_report(paths)
    print("\n" + report)
    
    # Save to file
    output_file = f"attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(f"/home/claude/{output_file}", 'w') as f:
        f.write(report)
    
    print(f"\n[+] Report saved to: {output_file}")


if __name__ == "__main__":
    main()
