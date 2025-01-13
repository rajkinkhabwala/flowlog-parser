import csv
from collections import defaultdict
import argparse
import socket

def parse_lookup_table(file_path: str):
    """
    Parse the lookup table and return a dictionary with (port, protocol) as key and tag as value.
    """
    
    lookup_table = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print(row)
            port = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup_table[(port, protocol)] = tag
    return lookup_table

def parse_flow_logs(file_path):
    """
    Parse the flow log file and return a list of log entries as tuples.
    """
    logs = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 14 and parts[0] == '2':  # Ensure it has atleast all the columns of version 2
                dst_port = parts[6].strip()
                protocol = get_protocol_name(int(parts[7].strip()))
                logs.append((dst_port, protocol))
    return logs

def map_logs_to_tags(logs: list, lookup_table: dict):
    """
    Map logs to tags using the lookup table and calculate counts.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    for dst_port, protocol in logs:
        protocol = protocol.lower()
        tag = lookup_table.get((dst_port, protocol), 'Untagged')
        tag_counts[tag] += 1
        port_protocol_counts[(dst_port, protocol)] += 1
    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    """
    Write the output to a file.
    """
    with open(output_file, 'w') as f:
        f.write("Tag Counts:\n")
        f.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            f.write(f"{tag},{count}\n")

        f.write("\nPort/Protocol Combination Counts:\n")
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            f.write(f"{port},{protocol},{count}\n")

def get_protocol_name(decimal_proto: int):
    """Protocol name from the decimal value of that protocol.

    Args:
        decimal_proto (int): IANA decimal values.

    Returns:
        str: name of the protocol
    """       
    prefix = "IPPROTO_"
    table = {num:name[len(prefix):] 
          for name,num in vars(socket).items()
            if name.startswith(prefix)}
    return table[decimal_proto].strip().lower()

def main():
    parser = argparse.ArgumentParser(description="Parse flow logs and map to tags.")
    parser.add_argument("--flow_logs", required=True, help="Path to the flow log file.")
    parser.add_argument("--lookup_table", required=True, help="Path to the lookup table file.")
    parser.add_argument("--output", required=True, help="Path to the output file.")

    args = parser.parse_args()

    lookup_table = parse_lookup_table(args.lookup_table)
    flow_logs = parse_flow_logs(args.flow_logs)
    tag_counts, port_protocol_counts = map_logs_to_tags(flow_logs, lookup_table)
    write_output(tag_counts, port_protocol_counts, args.output)

if __name__ == "__main__":
    main()
