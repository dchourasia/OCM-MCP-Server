import httpx
from typing import Any, Literal

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError
from .settings import settings

# Create FastMCP server instance
mcp = FastMCP(
    name="OpenShiftClusterManagerServer",
    instructions="A server to manage OpenShift clusters using the OCM API.",
    dependencies=["httpx", "fastmcp"],  # Add other specific dependencies if any
)


async def _ocm_request(
        method: str, endpoint: str, ctx: Context | None = None, **kwargs: Any
) -> httpx.Response:
    """Helper function to make authenticated API requests to OCM."""
    headers = {
        "Authorization": f"Bearer {settings.api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if "headers" in kwargs:
        headers.update(kwargs.pop("headers"))

    full_url = f"{str(settings.api_url).rstrip('/')}{endpoint}"

    async with httpx.AsyncClient() as client:
        if ctx:
            await ctx.debug(
                f"Making OCM API request: {method} {full_url} with data:"
                f" {kwargs.get('params') or kwargs.get('json')}"
            )
        try:
            response = await client.request(
                method, full_url, headers=headers, **kwargs
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text
            if ctx:
                await ctx.error(
                    f"OCM API Error: {e.response.status_code} - {error_detail}"
                )
            raise ToolError(
                f"OCM API Error: {e.response.status_code} - {error_detail}"
            ) from e
        except httpx.RequestError as e:
            if ctx:
                await ctx.error(f"OCM Request Error: {e}")
            raise ToolError(f"OCM Request Error: {e!s}") from e
        return response


# --- Resources ---


@mcp.resource(uri="ocm://clusters", description="List all OpenShift clusters.")
async def list_all_clusters(ctx: Context) -> list[dict[str, Any]]:
    """Retrieves a list of all OpenShift clusters accessible by the API token."""
    response = await _ocm_request("GET", "/api/clusters_mgmt/v1/clusters", ctx=ctx)
    return response.json().get("items", [])


@mcp.resource(
    uri="ocm://cloud_providers", description="List available cloud providers."
)
async def list_cloud_providers(ctx: Context) -> list[dict[str, Any]]:
    """Retrieves a list of supported cloud providers."""
    response = await _ocm_request("GET", "/api/clusters_mgmt/v1/cloud_providers", ctx=ctx)
    return response.json().get("items", [])


@mcp.resource(
    uri="ocm://versions/{cloud_provider_id}",
    description="List available OpenShift versions for a specific cloud provider.",
)
async def list_ocm_versions(cloud_provider_id: str, ctx: Context) -> list[dict[str, Any]]:
    """Retrieves available OpenShift versions for the given cloud provider ID (e.g., 'aws', 'gcp')."""
    params = {"order": "version desc"}  # Show newest versions first
    response = await _ocm_request(
        "GET", f"/api/clusters_mgmt/v1/versions", params=params, ctx=ctx
    )
    # Filter by cloud provider client-side if API doesn't support it directly for versions
    # OCM API for versions doesn't seem to directly filter by cloud_provider_id in the path in the same way regions do.
    # It returns all versions, often with a `cloud_provider` field within each version object or channel.
    # Here, we assume a more general listing and the LLM/user might need to infer or filter further.
    # A more specific tool might be needed if granular filtering is available.
    return response.json().get("items", [])


@mcp.resource(
    uri="ocm://regions/{cloud_provider_id}",
    description="List available regions for a specific cloud provider.",
)
async def list_available_regions(
        cloud_provider_id: str, ctx: Context
) -> list[dict[str, Any]]:
    """Retrieves a list of regions for the specified cloud provider ID (e.g., 'aws', 'gcp')."""
    response = await _ocm_request(
        "GET", f"/api/clusters_mgmt/v1/cloud_providers/{cloud_provider_id}/regions", ctx=ctx
    )
    return response.json().get("items", [])


# --- Resource Templates ---


@mcp.resource(
    uri="ocm://clusters/{cluster_id}",
    description="Get detailed information for a specific OpenShift cluster.",
)
async def get_ocm_cluster_details(cluster_id: str, ctx: Context) -> dict[str, Any]:
    """Retrieves detailed information for the cluster with the given ID."""
    response = await _ocm_request(
        "GET", f"/api/clusters_mgmt/v1/clusters/{cluster_id}", ctx=ctx
    )
    return response.json()


@mcp.resource(
    uri="ocm://addons/{addon_id}/versions",
    description="List available versions for a specific addon.",
)
async def list_ocm_addon_versions(addon_id: str, ctx: Context) -> list[dict[str, Any]]:
    """Retrieves available versions for the addon with the given ID."""
    response = await _ocm_request(
        "GET", f"/api/clusters_mgmt/v1/addons/{addon_id}/versions", ctx=ctx
    )
    return response.json().get("items", [])


# --- Tools ---


@mcp.tool(description="Create a new OpenShift cluster (e.g., ROSA or OSD).")
async def create_ocm_cluster(
        ctx: Context,
        name: str,
        region: str = 'us-east-1',
        cloud_provider: Literal["aws", "gcp", "azure"] = "aws",
        product: Literal["rosa", "osd"] = "rosa",
        version: str | None = None,  # e.g., "openshift-v4.14.0"
        multi_az: bool = False,
        compute_nodes: int = 2,
        compute_machine_type: str = "m5.2xlarge",  # e.g. m5.xlarge for AWS, n1-standard-4 for GCP
        properties: dict[str, Any] | None = None,  # For additional provider-specific properties
) -> dict[str, Any]:
    """
    Creates a new OpenShift cluster.
    Provide a unique name, region, cloud provider, and product type (rosa or osd).
    Optionally specify the OpenShift version, multi-AZ, number of compute nodes, and compute machine type.
    Use 'properties' for any other provider-specific settings.
    Example version: 'openshift-v4.14.0'. It's best to list available versions first.
    """
    payload: dict[str, Any] = {
        "name": name,
        "region": {"id": region},
        "cloud_provider": {"id": cloud_provider},
        "product": {"id": product},
        "multi_az": multi_az,
        "nodes": {
            "compute": compute_nodes,
            "compute_machine_type": {"id": compute_machine_type},
        },
    }
    if version:
        payload["version"] = {"id": version}

    # For ROSA (AWS), ccs.enabled is usually required.
    if product == "rosa" and cloud_provider == "aws":
        payload["ccs"] = {"enabled": True}  # Assume STS cluster for simplicity

    if properties:
        payload["properties"] = properties

    response = await _ocm_request(
        "POST", "/api/clusters_mgmt/v1/clusters", json=payload, ctx=ctx
    )
    return response.json()


# @mcp.tool(description="Delete an OpenShift cluster.")
# async def delete_ocm_cluster(cluster_id: str, ctx: Context) -> dict[str, Any]:
#     """Deletes the OpenShift cluster with the specified ID."""
#     await _ocm_request("DELETE", f"/api/clusters_mgmt/v1/clusters/{cluster_id}", ctx=ctx)
#     return {"cluster_id": cluster_id, "status": "deletion_initiated"}


@mcp.tool(description="Get the status of an OpenShift cluster.")
async def get_ocm_cluster_status(cluster_id: str, ctx: Context) -> dict[str, Any]:
    """Retrieves the current status of the cluster with the given ID."""
    response = await _ocm_request(
        "GET", f"/api/clusters_mgmt/v1/clusters/{cluster_id}/status", ctx=ctx
    )
    return response.json()


# --- Prompts (Optional) ---
@mcp.prompt(description="Generate a request to list clusters in a specific region and provider.")
def list_clusters_in_region_prompt(region: str, cloud_provider: str) -> str:
    """Generates a user message to list clusters in a specific region and cloud provider."""
    return f"Can you list all OpenShift clusters in the '{region}' region on '{cloud_provider}'?"


if __name__ == "__main__":
    mcp.run()