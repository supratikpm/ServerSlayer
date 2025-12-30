import os
import subprocess
import platform
import json
import re
import sys
from typing import List, Dict, Optional, Any

# Initial Knowledge Base (in a real agent, this might be loaded from a file or config)
KNOWLEDGE_BASE = {
    "protected_ports": [3306, 5432, 27017, 6379, 1433, 22],
    "protected_processes": [
        "antigravity", "gemini", "cursor", "vscode", "code", "jetbrains",
        "docker", "postgres", "mysqld", "mongod", "redis-server", "sqlservr", "ngrok", "ssh"
    ],
    "frameworks": {
        "node": {"default_ports": [3000, 3001, 8000, 8080], "processes": ["node", "npm", "yarn", "bun"]},
        "python": {"default_ports": [8000, 5000], "processes": ["python", "python3", "uvicorn", "gunicorn"]},
        "java": {"default_ports": [8080], "processes": ["java", "mvn", "gradle", "tomcat"]},
        "ruby": {"default_ports": [3000], "processes": ["ruby", "rails", "puma"]},
        "go": {"default_ports": [8080], "processes": ["go", "main", "exe"]},
        "php": {"default_ports": [8000], "processes": ["php", "apache2", "httpd", "nginx"]}
    }
}

SYSTEM_OS = platform.system()

def run_command(command: List[str]) -> str:
    """Executes a system command and returns stdout."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Some commands return non-zero if nothing found (like grep), so run smoothly
        return ""
    except Exception as e:
        return ""

def get_listening_ports() -> List[Dict[str, Any]]:
    """
    Returns a list of dicts: {'port': int, 'pid': int, 'protocol': str}
    """
    ports = []
    
    if SYSTEM_OS == "Windows":
        # Using netstat -ano | findstr LISTENING
        # Output format: TCP 0.0.0.0:8080 0.0.0.0:0 LISTENING 1234
        output = run_command(["netstat", "-ano"])
        for line in output.splitlines():
            if "LISTENING" in line:
                parts = line.split()
                if len(parts) >= 5:
                    protocol = parts[0]
                    local_addr = parts[1]
                    pid = parts[-1]
                    
                    if ":" in local_addr:
                        port_str = local_addr.split(":")[-1]
                        if port_str.isdigit() and pid.isdigit():
                            ports.append({
                                "port": int(port_str),
                                "pid": int(pid),
                                "protocol": protocol
                            })
                            
    else: # macOS / Linux
        # lsof -iTCP -sTCP:LISTEN -n -P
        output = run_command(["lsof", "-iTCP", "-sTCP:LISTEN", "-n", "-P"])
        # Format: COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
        for line in output.splitlines()[1:]: # Skip header
            parts = line.split()
            if len(parts) >= 9:
                pid = parts[1]
                proto = parts[4] # usually IPv4/IPv6
                
                # Address is likely parts[8] on Linux or parts[8] on macOS variants
                # Actually, standard lsof outputs Name at the end: *:3000 (LISTEN)
                name_field = parts[8]
                if ":" in name_field:
                    port_str = name_field.split(":")[-1].split("(")[0] # Handle "(LISTEN)" if attached
                    if "->" in port_str: # handle established if leaky logic
                        continue
                    if port_str.isdigit():
                         ports.append({
                            "port": int(port_str),
                            "pid": int(pid),
                            "protocol": "TCP"
                        })

    return ports

def get_process_info(pid: int) -> Dict[str, Any]:
    """
    Returns {'pid': int, 'name': str, 'cmdline': str, 'status': str}
    """
    info = {"pid": pid, "name": "Unknown", "cmdline": "", "status": "Unknown"}
    
    if SYSTEM_OS == "Windows":
        # tasklist /FI "PID eq 1234" /FO CSV /NH
        output = run_command(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"])
        if output:
            parts = output.split('","')
            if len(parts) >= 1:
                info["name"] = parts[0].strip('"')
        
        # Get command line via wmic (expensive but needed for detection)
        wmic_out = run_command(["wmic", "process", "where", f"processid={pid}", "get", "commandline"])
        if wmic_out:
            lines = wmic_out.splitlines()
            if len(lines) > 1:
                # First line is header, second is content
                cmd = lines[1].strip()
                if cmd: info["cmdline"] = cmd

    else:
        # ps -p <pid> -o comm,args (comm=name, args=cmdline)
        # Using -ww to prevent truncation on some systems
        output = run_command(["ps", "-p", str(pid), "-o", "comm,args"])
        lines = output.splitlines()
        if len(lines) > 1:
            # Simple heuristic, full parsing is complex
            info["cmdline"] = lines[1].strip()
            # Name is usually the first token
            info["name"] = info["cmdline"].split()[0]

    return info

def is_protected(process_info: Dict[str, Any], port: int) -> tuple[bool, str]:
    """
    Checks if a process is protected.
    Returns (is_protected, reason)
    """
    name = process_info["name"].lower()
    cmdline = process_info["cmdline"].lower()
    
    # Check Ports
    if port in KNOWLEDGE_BASE["protected_ports"]:
        return True, f"Protected Port {port}"
    
    # Check Process Names
    for protected in KNOWLEDGE_BASE["protected_processes"]:
        if protected in name or protected in cmdline:
            return True, f"Protected Process Keyword: {protected}"
            
    return False, ""

def classify_server(process_info: Dict[str, Any], port: int) -> str:
    """
    Returns a classification string: 'Node', 'Python', 'Java', 'Unknown'
    """
    name = process_info["name"].lower()
    cmd = process_info["cmdline"].lower()
    
    for fw, data in KNOWLEDGE_BASE["frameworks"].items():
        # Check process names
        for p_name in data["processes"]:
            if p_name in name or p_name in cmd:
                return fw.capitalize()
    
    return "Unknown"

def kill_process(pid: int, force: bool = False) -> bool:
    """Kills a process. Returns True if successful."""
    try:
        if SYSTEM_OS == "Windows":
            args = ["taskkill", "/PID", str(pid)]
            if force:
                args.append("/F")
            subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            args = ["kill"]
            if force:
                args.append("-9")
            args.append(str(pid))
            subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Agent Tool Wrapper
def server_slayer_tool(action: str, scope: str = "project", idle_only: bool = False, 
                      force: bool = False, specific_port: Optional[int] = None):
    """
    Main entry point for the agent tool.
    actions: 'detect', 'list', 'kill'
    """
    
    # 1. Discovery
    listening = get_listening_ports()
    targets = []
    
    results = [] # Detailed report
    
    for l in listening:
        pid = l['pid']
        port = l['port']
        
        info = get_process_info(pid)
        protected, reason = is_protected(info, port)
        classification = classify_server(info, port)
        
        # Scope filtering (simplified for this tool script)
        # In a real agent, we'd check "project" by comparing CWD of process to workspace
        # For now, we rely on heuristics or assume all dev ports are relevant if scoped
        
        entry = {
            "port": port,
            "pid": pid,
            "name": info["name"],
            "cmd": info["cmdline"],
            "type": classification,
            "protected": protected,
            "reason": reason,
            "status": "Active" # TODO: Implement idle check
        }
        
        results.append(entry)
        
        # Determine if target
        is_target = False
        if specific_port:
            if port == specific_port:
                is_target = True
        elif action == "kill":
            # Filter logic
            if not protected:
                # If project scope, we ideally check paths, but here we'll assume non-system/unknown is valid
                if classification != "Unknown":
                    is_target = True
                
        if is_target:
             targets.append(entry)

    # 2. Execution
    if action == "list" or action == "detect":
        # Format output as a nice markdown table
        output = "| Port | PID | Type | Protected | Reason | Process |\n"
        output += "|------|-----|------|-----------|--------|---------|\n"
        for r in results:
            prot_str = "YES" if r["protected"] else "No"
            # Truncate cmd
            cmd_short = (r["cmd"][:40] + '..') if len(r["cmd"]) > 40 else r["cmd"]
            output += f"| {r['port']} | {r['pid']} | {r['type']} | {prot_str} | {r['reason']} | {cmd_short} |\n"
        return output
        
    elif action == "kill":
        report = []
        killed_count = 0
        for t in targets:
            if t["protected"]:
                report.append(f"SKIPPED {t['port']} (Protected: {t['reason']})")
                continue
            
            # Perform Kill
            success = kill_process(t["pid"], force)
            if success:
                 report.append(f"⚔️ KILLED {t['port']} (PID {t['pid']})")
                 killed_count += 1
            else:
                 report.append(f"❌ FAILED {t['port']} (PID {t['pid']})")
        
        # Add success message with star prompt
        if killed_count > 0:
            report.append("")
            report.append("=" * 50)
            report.append("⚔️ Stray servers slain! Ready to code! 🚀")
            report.append("")
            report.append("⭐ Star if this saved you: https://github.com/supratikpm/ServerSlayer")
            report.append("=" * 50)
        
        return "\n".join(report)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ServerSlayer Tool")
    parser.add_argument("action", choices=["list", "detect", "kill"], help="Action to perform")
    parser.add_argument("--scope", default="project", help="Scope: project, system, chat")
    parser.add_argument("--idle-only", action="store_true", help="Kill only idle servers")
    parser.add_argument("--force", action="store_true", help="Force kill")
    parser.add_argument("--port", type=int, help="Specific port to target")
    
    args = parser.parse_args()
    
    print(server_slayer_tool(args.action, args.scope, args.idle_only, args.force, args.port))
