
# Fetch HTTP Endpoint Health Checker

This project is a Python-based utility for monitoring the health of HTTP endpoints. It periodically sends HTTP requests to a list of endpoints defined in a YAML configuration file, evaluates their health based on response status and latency, and logs their availability percentage.

## Features
- Sends HTTP requests to multiple endpoints periodically.
- Tracks and logs the health (`UP` or `DOWN`) of each endpoint.
- Calculates and logs the cumulative availability percentage of each domain.
- Handles HTTP errors gracefully.
- Easy to configure via a YAML file.
- Optional detailed prints for availability percentages via the `--detailed` flag.

---

## Prerequisites
- **Python 3.8 or higher** must be installed on your system.
  - Note: Ensure Python is accessible from your terminal:
    - On Windows, check "Add Python to PATH" during installation or manually add it to your environment variables.
    - On Linux and Mac, Python is usually pre-installed. If you installed Python manually, ensure it is added to your PATH by modifying your shell configuration file (e.g., `.bashrc` or `.zshrc`).
- The following Python libraries are required:
  - `pyyaml` for parsing YAML files.
  - `requests` for sending HTTP requests.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ahmedr2/Fetch-Take-Home-Exercise-SRE.git
   cd Fetch-Take-Home-Exercise-SRE
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a YAML configuration file listing the endpoints you want to monitor. A sample configuration file (`sample_config.yaml`) is provided in the repository.

### Example `sample_config.yaml`:
```yaml
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: Fetch Index Page
  url: https://fetch.com/

- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: Fetch Careers Page
  url: https://fetch.com/careers

- body: '{"foo":"bar"}'
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  method: POST
  name: Fetch Some Fake Post Endpoint
  url: https://fetch.com/some/post/endpoint

- name: Fetch Rewards Index Page
  url: https://www.fetchrewards.com/
```

---

## Usage

Run the program with the path to the YAML configuration file:

```bash
python main.py sample_config.yaml
```

### Optional Flags

- **Enable detailed output for availability percentages**:
   ```bash
   python main.py sample_config.yaml --detailed
   ```

### Example Output
1. **With detailed output disabled**:
   ```
   fetch.com has 67% availability percentage
   www.fetchrewards.com has 100% availability percentage
   ```
2. **With detailed output enabled**:
   ```
   2025-01-08 12:00:00,169 - Endpoint 'fetch index page' (https://fetch.com/) is UP.
   2025-01-08 12:00:00,211 - Endpoint 'fetch careers page' (https://fetch.com/careers) is UP.
   2025-01-08 12:00:00,252 - Endpoint 'fetch some fake post endpoint' (https://fetch.com/some/post/endpoint) is DOWN.
   2025-01-08 12:00:00,354 - Endpoint 'fetch rewards index page' (https://www.fetchrewards.com/) is UP.
   2025-01-08 12:00:00,354 - fetch.com has 67% availability percentage
   2025-01-08 12:00:00,354 - www.fetchrewards.com has 100% availability percentage
   ```


---

## How It Works

1. The program reads a YAML configuration file containing the list of HTTP endpoints.
2. Every 15 seconds, it:
   - Sends an HTTP request to each endpoint.
   - Evaluates the health of the endpoint based on:
     - HTTP status code (`2xx` is considered healthy).
     - Response latency (<500ms is considered healthy).
   - Tracks and logs cumulative availability percentages for each domain.
3. The program continues until manually stopped (e.g., via `CTRL+C`).

---

## Error Handling

- Catches network errors (e.g., timeouts, connection issues) and marks the endpoint as `DOWN`.

---

## Stopping the Program

To stop the monitoring, press `CTRL+C`. The program will exit gracefully.

---

## Troubleshooting

1. **Missing Dependencies**: Ensure all required packages are installed using:
   ```bash
   pip install -r requirements.txt
   ```
2. **Invalid YAML File**: Use an online YAML linter (e.g., [YAML Lint](https://www.yamllint.com/)) to validate the file.

---
