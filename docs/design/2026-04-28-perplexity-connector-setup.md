# Perplexity Remote Connector Setup Notes

**Date:** 2026-04-28

## Target connector shape
- remote MCP server URL must use HTTPS
- transport should be `Streamable HTTP`
- the exposed endpoint should be `/mcp`
- initial auth recommendation is `API Key`

## Expected runtime path
- local FastMCP server runs with HTTP transport
- reverse proxy publishes `https://<domain>/mcp`
- health check is available at `https://<domain>/health`

## Setup sequence
1. deploy the service locally behind Nginx
2. confirm HTTPS and proxy routing work
3. configure Perplexity custom remote connector
4. choose `Streamable HTTP`
5. set auth to `API Key` if proxy protection is enabled
6. validate the connector

## Common failure points
- using a non-HTTPS URL
- exposing the raw application port instead of the reverse proxy URL
- forgetting to route `/mcp`
- binding the app publicly instead of to loopback
- failing ACME issuance because router or DNS is incorrect
