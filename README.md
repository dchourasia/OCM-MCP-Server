# OpenShift Cluster Manager (OCM) MCP Server

This FastMCP server provides tools and resources to interact with the OpenShift Cluster Manager API, allowing an LLM to perform operations like listing clusters, getting cluster details, creating, and deleting clusters.

## Prerequisites

- Python 3.10+
- `fastmcp` library installed
- An OpenShift Cluster Manager API Token

## Setup

1.  **Clone the `jlowin-fastmcp` repository (if you haven't already):**
    ```bash
    git clone https://github.com/jlowin/fastmcp.git
    cd fastmcp
    ```

2.  **Navigate to this example's directory:**
    ```bash
    cd examples/openshift_cluster_manager
    ```

3.  **Install dependencies (including FastMCP if not installed globally):**
    We recommend using `uv`.
    ```bash
    uv venv .venv  # Create a virtual environment (optional, but recommended)
    source .venv/bin/activate # Or .venv\Scripts\activate on Windows
    uv pip install -r requirements.txt 
    # If requirements.txt doesn't exist, create one with:
    # fastmcp
    # httpx
    # pydantic
    # pydantic-settings
    ```
    Alternatively, if you have FastMCP installed globally or in your project:
    ```bash
    uv pip install httpx pydantic pydantic-settings
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `examples/openshift_cluster_manager` directory by copying `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file and replace `your_ocm_api_token_here` with your actual OCM API token. You can generate a token from [Red Hat Hybrid Cloud Console](https://console.redhat.com/openshift/token).

    ```ini
    # .env
    OCM_API_TOKEN="your_ocm_api_token_here"
    # OCM_API_URL="https://api.openshift.com" # Default, uncomment to override
    ```

## Running the Server

You can run the server using FastMCP's CLI or directly with Python.

**Using FastMCP CLI (recommended for development):**
```bash
fastmcp run ocm_server.py
```

## Resources
- ocm://clusters: Lists all accessible OpenShift clusters.
- ocm://cloud_providers: Lists available cloud providers.
- ocm://versions/{cloud_provider_id}: Lists OpenShift versions for a cloud provider (e.g., ocm://versions/aws).
- ocm://regions/{cloud_provider_id}: Lists regions for a cloud provider (e.g., ocm://regions/aws).

## Resource Templates
* ocm://clusters/{cluster_id}: Gets detailed information for a specific cluster. 
  - Example: ocm://clusters/your-cluster-id 
* ocm://addons/{addon_id}/versions: Lists available versions for a specific addon. 
  - Example: ocm://addons/cluster-logging-operator/versions

## Tools
* create_ocm_cluster: Creates a new OpenShift cluster.
  - Parameters: name (str), region (str), cloud_provider (Literal["aws", "gcp", "azure"], default "aws"), product (Literal["rosa", "osd"], default "rosa"), version (str | None), multi_az (bool, default False), compute_nodes (int, default 2), compute_machine_type (str, default "m5.xlarge" for AWS), properties (dict | None).
* delete_ocm_cluster: Deletes an OpenShift cluster.
  - Parameters: cluster_id (str).
* get_ocm_cluster_status: Retrieves the status of an OpenShift cluster.
  - Parameters: cluster_id (str).