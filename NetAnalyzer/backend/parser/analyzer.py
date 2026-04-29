import sys
import json
import logging
from collections import defaultdict
from scapy.all import rdpcap, IP, TCP, UDP, ICMP, DNS
import time

# Disable Scapy warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def analyze_pcap(file_path):
    try:
        packets = rdpcap(file_path)
    except Exception as e:
        print(json.dumps({"error": f"Failed to read pcap file: {str(e)}"}))
        sys.exit(1)

    analysis = {
        "summary": {
            "total_packets": len(packets),
            "start_time": None,
            "end_time": None,
            "duration": 0
        },
        "protocols": defaultdict(int),
        "sizes": defaultdict(int),
        "timeline": defaultdict(int),
        "top_talkers": defaultdict(lambda: {"count": 0, "protocol": ""}),
        "threats": []
    }

    if not packets:
        print(json.dumps(analysis))
        sys.exit(0)

    # Convert timestamps
    analysis["summary"]["start_time"] = float(packets[0].time)
    analysis["summary"]["end_time"] = float(packets[-1].time)
    analysis["summary"]["duration"] = analysis["summary"]["end_time"] - analysis["summary"]["start_time"]

    # Tracking for threats
    syn_scans = defaultdict(int)
    suspicious_ports = {22, 23, 3389, 445}

    for pkt in packets:
        # Size distribution
        size = len(pkt)
        if size < 64:
            analysis["sizes"]["< 64 bytes"] += 1
        elif size <= 256:
            analysis["sizes"]["64 - 256 bytes"] += 1
        elif size <= 1024:
            analysis["sizes"]["257 - 1024 bytes"] += 1
        else:
            analysis["sizes"]["> 1024 bytes"] += 1

        # Timeline (bucket by second)
        timestamp = int(pkt.time)
        analysis["timeline"][timestamp] += 1

        # Check IP layer
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            proto = "Other"

            # Check protocols
            if TCP in pkt:
                proto = "TCP"
                # Threat: Port scan (SYN packets)
                if pkt[TCP].flags == 'S':
                    syn_scans[src_ip] += 1
                # Threat: Suspicious Ports
                if pkt[TCP].dport in suspicious_ports or pkt[TCP].sport in suspicious_ports:
                    analysis["threats"].append({
                        "type": "Suspicious Port Activity",
                        "src": src_ip,
                        "dst": dst_ip,
                        "description": f"Traffic on port {pkt[TCP].dport if pkt[TCP].dport in suspicious_ports else pkt[TCP].sport}"
                    })
                # Check HTTP manually as Scapy HTTP requires an extension
                if pkt[TCP].dport == 80 or pkt[TCP].sport == 80:
                    proto = "HTTP"
            elif UDP in pkt:
                proto = "UDP"
                if DNS in pkt:
                    proto = "DNS"
            elif ICMP in pkt:
                proto = "ICMP"

            analysis["protocols"][proto] += 1

            # Top talkers
            talker_key = f"{src_ip} -> {dst_ip}"
            analysis["top_talkers"][talker_key]["count"] += 1
            analysis["top_talkers"][talker_key]["protocol"] = proto

    # Process syn scans for threats
    for ip, count in syn_scans.items():
        if count > 20:  # Arbitrary threshold for port scan
            analysis["threats"].append({
                "type": "Possible Port Scan",
                "src": ip,
                "dst": "Multiple",
                "description": f"High rate of SYN packets ({count}) from this IP."
            })

    # Format data for frontend
    result = {
        "summary": analysis["summary"],
        "protocols": dict(analysis["protocols"]),
        "sizes": dict(analysis["sizes"]),
        "timeline": [{"time": k, "count": v} for k, v in sorted(analysis["timeline"].items())],
        "top_talkers": [{"connection": k, "count": v["count"], "protocol": v["protocol"]} 
                        for k, v in sorted(analysis["top_talkers"].items(), key=lambda item: item[1]["count"], reverse=True)[:10]],
        "threats": analysis["threats"]
    }

    print(json.dumps(result))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No pcap file provided"}))
        sys.exit(1)
    
    file_path = sys.argv[1]
    analyze_pcap(file_path)
