#!/usr/bin/env python3
"""
Web Visualization Server for Attack Path Mapper
Provides interactive graph visualization using D3.js
"""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from attack_path_mapper import AttackPathMapper
import os


class VisualizationServer(SimpleHTTPRequestHandler):
    """HTTP server for attack path visualization"""
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_html_interface().encode())
        
        elif self.path.startswith('/analyze'):
            # Parse query parameters
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            scan_file = params.get('file', ['sample_scan.json'])[0]
            
            try:
                # Run analysis
                mapper = AttackPathMapper()
                mapper.load_scan_results(scan_file)
                mapper.build_attack_graph()
                paths = mapper.find_attack_paths(max_paths=5)
                
                # Convert to JSON for visualization
                graph_data = self._convert_to_viz_format(mapper, paths)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(graph_data).encode())
            
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        else:
            super().do_GET()
    
    def _convert_to_viz_format(self, mapper, paths):
        """Convert attack graph to D3.js compatible format"""
        nodes = []
        links = []
        node_set = set()
        
        # Add nodes from graph
        for node_id in mapper.graph.nodes():
            if node_id in ['START', 'END']:
                continue
            
            if node_id in mapper.attack_nodes:
                node_data = mapper.attack_nodes[node_id]
                nodes.append({
                    'id': node_id,
                    'name': node_data.description,
                    'severity': node_data.severity,
                    'exploitability': node_data.exploitability,
                    'technique': node_data.technique.value[1],
                    'tactic': node_data.technique.value[2],
                    'risk_score': node_data.get_risk_score()
                })
                node_set.add(node_id)
        
        # Add edges
        for source, target in mapper.graph.edges():
            if source in node_set and target in node_set:
                links.append({
                    'source': source,
                    'target': target,
                    'value': mapper.graph[source][target].get('weight', 1)
                })
        
        # Path information
        path_data = []
        for idx, path in enumerate(paths, 1):
            path_data.append({
                'id': idx,
                'risk': path.total_risk,
                'likelihood': path.likelihood,
                'impact': path.impact_score,
                'nodes': [node.id for node in path.nodes]
            })
        
        return {
            'nodes': nodes,
            'links': links,
            'paths': path_data
        }


def get_html_interface():
    """Generate HTML interface with D3.js visualization"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Attack Path Mapper</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        h1 {
            font-size: 3em;
            background: linear-gradient(90deg, #00d4ff, #ff00e5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }
        
        .subtitle {
            color: #a0a0a0;
            font-size: 1.2em;
        }
        
        .controls {
            background: rgba(0, 0, 0, 0.4);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .control-group {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        input[type="text"] {
            flex: 1;
            min-width: 300px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 5px;
            color: #e0e0e0;
            font-size: 1em;
        }
        
        button {
            padding: 12px 30px;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border: none;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1em;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }
        
        .graph-container {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
        }
        
        #attack-graph {
            width: 100%;
            height: 600px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .stats-panel, .paths-panel {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .panel-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #00d4ff;
            border-bottom: 2px solid rgba(0, 212, 255, 0.3);
            padding-bottom: 10px;
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .stat-label {
            color: #a0a0a0;
        }
        
        .stat-value {
            color: #00d4ff;
            font-weight: bold;
        }
        
        .path-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 10px;
            border-left: 3px solid;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .path-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .path-item.critical {
            border-left-color: #ff4444;
        }
        
        .path-item.high {
            border-left-color: #ff8800;
        }
        
        .path-item.medium {
            border-left-color: #ffcc00;
        }
        
        .path-item.low {
            border-left-color: #44ff44;
        }
        
        .path-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .path-metrics {
            display: flex;
            gap: 15px;
            font-size: 0.9em;
            color: #a0a0a0;
            margin-top: 8px;
        }
        
        .node {
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .node:hover {
            stroke-width: 3px;
            filter: brightness(1.5);
        }
        
        .link {
            stroke: rgba(0, 212, 255, 0.3);
            stroke-width: 2px;
            fill: none;
        }
        
        .link-highlighted {
            stroke: #00d4ff;
            stroke-width: 3px;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .node-label {
            fill: #e0e0e0;
            font-size: 11px;
            pointer-events: none;
            text-anchor: middle;
        }
        
        .tooltip {
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #00d4ff;
            border-radius: 5px;
            padding: 10px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            max-width: 300px;
            z-index: 1000;
        }
        
        .tooltip.active {
            opacity: 1;
        }
        
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.7);
            padding: 15px;
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #00d4ff;
        }
        
        @media (max-width: 1200px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Attack Path Mapper</h1>
            <p class="subtitle">Strategic Security Analysis & Threat Modeling</p>
        </header>
        
        <div class="controls">
            <div class="control-group">
                <input type="text" id="scan-file" placeholder="Enter scan results file (e.g., sample_scan.json)" value="sample_scan.json">
                <button onclick="analyzeAttackPaths()">🔍 Analyze Attack Paths</button>
                <button onclick="exportReport()">📄 Export Report</button>
            </div>
        </div>
        
        <div class="main-content">
            <div class="graph-container">
                <div class="legend">
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ff4444;"></div>
                        <span>Critical (9-10)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ff8800;"></div>
                        <span>High (7-8)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ffcc00;"></div>
                        <span>Medium (5-6)</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #44ff44;"></div>
                        <span>Low (1-4)</span>
                    </div>
                </div>
                <div id="attack-graph"></div>
                <div class="tooltip"></div>
            </div>
            
            <div class="sidebar">
                <div class="stats-panel">
                    <h3 class="panel-title">📊 Analysis Statistics</h3>
                    <div class="stat-item">
                        <span class="stat-label">Total Vulnerabilities:</span>
                        <span class="stat-value" id="total-vulns">-</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Attack Paths Found:</span>
                        <span class="stat-value" id="total-paths">-</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Highest Risk Score:</span>
                        <span class="stat-value" id="max-risk">-</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Average Exploitability:</span>
                        <span class="stat-value" id="avg-exploit">-</span>
                    </div>
                </div>
                
                <div class="paths-panel">
                    <h3 class="panel-title">🎯 Attack Paths</h3>
                    <div id="paths-list">
                        <p class="loading">Run analysis to see attack paths...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentData = null;
        
        function getSeverityColor(severity) {
            if (severity >= 9) return '#ff4444';
            if (severity >= 7) return '#ff8800';
            if (severity >= 5) return '#ffcc00';
            return '#44ff44';
        }
        
        function getSeverityClass(risk) {
            if (risk >= 70) return 'critical';
            if (risk >= 50) return 'high';
            if (risk >= 30) return 'medium';
            return 'low';
        }
        
        async function analyzeAttackPaths() {
            const scanFile = document.getElementById('scan-file').value;
            const graphContainer = document.getElementById('attack-graph');
            
            graphContainer.innerHTML = '<p class="loading">Analyzing attack paths...</p>';
            
            try {
                const response = await fetch(`/analyze?file=${encodeURIComponent(scanFile)}`);
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                currentData = data;
                renderGraph(data);
                updateStats(data);
                updatePathsList(data);
                
            } catch (error) {
                graphContainer.innerHTML = `<p class="loading" style="color: #ff4444;">Error: ${error.message}</p>`;
            }
        }
        
        function renderGraph(data) {
            const container = document.getElementById('attack-graph');
            container.innerHTML = '';
            
            const width = container.clientWidth;
            const height = 600;
            
            const svg = d3.select('#attack-graph')
                .append('svg')
                .attr('width', width)
                .attr('height', height);
            
            // Create force simulation
            const simulation = d3.forceSimulation(data.nodes)
                .force('link', d3.forceLink(data.links).id(d => d.id).distance(150))
                .force('charge', d3.forceManyBody().strength(-500))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('collision', d3.forceCollide().radius(40));
            
            // Draw links
            const link = svg.append('g')
                .selectAll('path')
                .data(data.links)
                .join('path')
                .attr('class', 'link')
                .attr('marker-end', 'url(#arrowhead)');
            
            // Define arrowhead marker
            svg.append('defs').append('marker')
                .attr('id', 'arrowhead')
                .attr('viewBox', '-0 -5 10 10')
                .attr('refX', 25)
                .attr('refY', 0)
                .attr('orient', 'auto')
                .attr('markerWidth', 8)
                .attr('markerHeight', 8)
                .append('path')
                .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
                .attr('fill', 'rgba(0, 212, 255, 0.6)');
            
            // Draw nodes
            const node = svg.append('g')
                .selectAll('circle')
                .data(data.nodes)
                .join('circle')
                .attr('class', 'node')
                .attr('r', d => 10 + d.severity * 2)
                .attr('fill', d => getSeverityColor(d.severity))
                .attr('stroke', '#fff')
                .attr('stroke-width', 2)
                .call(drag(simulation))
                .on('mouseover', showTooltip)
                .on('mouseout', hideTooltip);
            
            // Add labels
            const label = svg.append('g')
                .selectAll('text')
                .data(data.nodes)
                .join('text')
                .attr('class', 'node-label')
                .text(d => d.name.substring(0, 20) + (d.name.length > 20 ? '...' : ''));
            
            // Update positions on simulation tick
            simulation.on('tick', () => {
                link.attr('d', d => {
                    const dx = d.target.x - d.source.x;
                    const dy = d.target.y - d.source.y;
                    const dr = Math.sqrt(dx * dx + dy * dy);
                    return `M${d.source.x},${d.source.y}A${dr},${dr} 0 0,1 ${d.target.x},${d.target.y}`;
                });
                
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
                
                label
                    .attr('x', d => d.x)
                    .attr('y', d => d.y + 35);
            });
        }
        
        function drag(simulation) {
            function dragstarted(event) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }
            
            function dragged(event) {
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }
            
            function dragended(event) {
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }
            
            return d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended);
        }
        
        function showTooltip(event, d) {
            const tooltip = document.querySelector('.tooltip');
            tooltip.innerHTML = `
                <strong>${d.name}</strong><br>
                <strong>Technique:</strong> ${d.technique}<br>
                <strong>Tactic:</strong> ${d.tactic}<br>
                <strong>Severity:</strong> ${d.severity}/10<br>
                <strong>Exploitability:</strong> ${(d.exploitability * 100).toFixed(0)}%<br>
                <strong>Risk Score:</strong> ${d.risk_score.toFixed(2)}
            `;
            tooltip.style.left = (event.pageX + 10) + 'px';
            tooltip.style.top = (event.pageY + 10) + 'px';
            tooltip.classList.add('active');
        }
        
        function hideTooltip() {
            document.querySelector('.tooltip').classList.remove('active');
        }
        
        function updateStats(data) {
            document.getElementById('total-vulns').textContent = data.nodes.length;
            document.getElementById('total-paths').textContent = data.paths.length;
            
            const maxRisk = Math.max(...data.paths.map(p => p.risk));
            document.getElementById('max-risk').textContent = maxRisk.toFixed(2);
            
            const avgExploit = data.nodes.reduce((sum, n) => sum + n.exploitability, 0) / data.nodes.length;
            document.getElementById('avg-exploit').textContent = (avgExploit * 100).toFixed(0) + '%';
        }
        
        function updatePathsList(data) {
            const pathsList = document.getElementById('paths-list');
            pathsList.innerHTML = '';
            
            data.paths.forEach(path => {
                const pathItem = document.createElement('div');
                pathItem.className = `path-item ${getSeverityClass(path.risk)}`;
                pathItem.innerHTML = `
                    <div class="path-title">Path #${path.id}</div>
                    <div class="path-metrics">
                        <span>Risk: ${path.risk.toFixed(2)}</span>
                        <span>|</span>
                        <span>Impact: ${path.impact}/10</span>
                        <span>|</span>
                        <span>Likelihood: ${(path.likelihood * 100).toFixed(0)}%</span>
                    </div>
                `;
                pathItem.onclick = () => highlightPath(path);
                pathsList.appendChild(pathItem);
            });
        }
        
        function highlightPath(path) {
            d3.selectAll('.link').classed('link-highlighted', false);
            d3.selectAll('.node').style('opacity', 0.3);
            
            const nodeSet = new Set(path.nodes);
            d3.selectAll('.node').filter(d => nodeSet.has(d.id)).style('opacity', 1);
            
            d3.selectAll('.link')
                .filter(d => nodeSet.has(d.source.id) && nodeSet.has(d.target.id))
                .classed('link-highlighted', true);
        }
        
        function exportReport() {
            if (!currentData) {
                alert('Please run analysis first');
                return;
            }
            
            let report = 'ATTACK PATH MAPPER - ANALYSIS REPORT\\n';
            report += '='.repeat(80) + '\\n\\n';
            report += `Total Vulnerabilities: ${currentData.nodes.length}\\n`;
            report += `Attack Paths Found: ${currentData.paths.length}\\n\\n`;
            
            currentData.paths.forEach(path => {
                report += `Attack Path #${path.id}\\n`;
                report += `-`.repeat(40) + '\\n';
                report += `Risk Score: ${path.risk.toFixed(2)}\\n`;
                report += `Impact: ${path.impact}/10\\n`;
                report += `Likelihood: ${(path.likelihood * 100).toFixed(0)}%\\n\\n`;
            });
            
            const blob = new Blob([report], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `attack_report_${new Date().toISOString().split('T')[0]}.txt`;
            a.click();
        }
    </script>
</body>
</html>
    """


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     🌐 Attack Path Mapper - Web Visualization Server         ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    os.chdir('/home/claude')
    
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, VisualizationServer)
    
    print(f"\n[+] Server started at http://localhost:8000")
    print(f"[+] Open your browser and navigate to the URL above")
    print(f"[+] Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server stopped")


if __name__ == "__main__":
    main()
