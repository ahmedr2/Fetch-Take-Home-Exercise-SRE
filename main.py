import argparse
import yaml
import requests
import time
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Health check for HTTP endpoints.")
    parser.add_argument(
        "config_file", type=str, help="Path to the YAML configuration file containing HTTP endpoints."
    )
    parser.add_argument(
        "--detailed", action="store_true", help="Enable detailed prints for availability percentage."
    )
    args = parser.parse_args()
    return args.config_file, args.detailed

# Parse YAML configuration file
def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            if not isinstance(config, list):
                raise ValueError("YAML configuration must be a list of endpoints.")
            return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

# Send an HTTP request and determine the status of the endpoint
def check_endpoint(endpoint):
    url = endpoint.get("url")
    method = endpoint.get("method", "GET").upper()
    headers = endpoint.get("headers", {})
    body = endpoint.get("body", None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=5)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if 200 <= response.status_code < 300 and latency < 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Calculate availability percentage
def calculate_availability(status_counts):
    total_requests = status_counts["UP"] + status_counts["DOWN"]
    if total_requests == 0:
        return 0
    return round(100 * (status_counts["UP"] / total_requests))

# Main monitoring loop
def monitor_endpoints(endpoints, detailed):
    domain_status = defaultdict(lambda: {"UP": 0, "DOWN": 0})

    try:
        while True:
            for endpoint in endpoints:
                name = endpoint.get("name", "Unknown")
                url = endpoint.get("url")

                domain = url.split("//")[-1].split("/")[0]  # Extract domain from URL
                status = check_endpoint(endpoint)
                domain_status[domain][status] += 1

                if detailed:
                    logging.info(f"Endpoint '{name}' ({url}) is {status}.")

            # Log cumulative availability percentages
            for domain, status_counts in domain_status.items():
                availability = calculate_availability(status_counts)
                if detailed:
                    logging.info(f"{domain} has {availability}% availability percentage")
                else:
                    print(f"{domain} has {availability}% availability percentage")

            time.sleep(15)  # Wait 15 seconds before the next cycle

    except KeyboardInterrupt:
        if detailed:
            logging.info("Monitoring stopped by user.")

# Main function
def main():
    config_file, detailed = parse_arguments()
    endpoints = parse_yaml(config_file)
    monitor_endpoints(endpoints, detailed)

if __name__ == "__main__":
    main()
