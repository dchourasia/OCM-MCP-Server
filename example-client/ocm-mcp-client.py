import asyncio
from fastmcp import Client
from ..src.ocm_server import mcp  # Assuming you run this from project root


async def main():
    # Ensure your .env file is in examples/openshift_cluster_manager/
    # or OCM_API_TOKEN is set in your environment.

    # For in-memory testing (if .env is loaded correctly by ocm_server.py):
    async with Client(mcp) as client:
        print("Listing clusters (in-memory)...")
        try:
            clusters = await client.read_resource("ocm://clusters")
            print(f"Found {len(clusters[0].text.splitlines()) - 2} clusters (approx, from JSON string).")  # rough count
            # print(clusters[0].text) # This will be a JSON string
        except Exception as e:
            print(f"Error listing clusters: {e}")

        print("\\nGetting cluster details for a dummy ID (expect error if ID doesn't exist)...")
        try:
            details = await client.read_resource("ocm://clusters/dummy-id")
            # print(details[0].text)
        except Exception as e:
            print(f"Error getting cluster details: {e}")

        print("\\nAttempting to create a cluster (will fail without real parameters/auth)...")
        try:
            # This will likely fail due to insufficient/mock parameters or auth issues
            # but demonstrates the tool call structure.
            new_cluster = await client.call_tool(
                "create_ocm_cluster",
                {
                    "name": "test-mcp-cluster",
                    "region": "us-east-1",  # Replace with a valid region for your provider
                    "cloud_provider": "aws",
                    "product": "rosa",
                    "version": "openshift-v4.14.0",  # Replace with a valid version
                    "compute_nodes": 2,
                    "compute_machine_type": "m5.xlarge"
                }
            )
            # print(new_cluster[0].text)
        except Exception as e:
            print(f"Error creating cluster: {e}")


if __name__ == "__main__":
    # Ensure you are in the `examples/openshift_cluster_manager` directory
    # or adjust paths if running from project root.
    # This example script assumes it can import `ocm_server` if run directly.
    # More practically, you would run ocm_server.py and connect with a separate client script.
    asyncio.run(main())