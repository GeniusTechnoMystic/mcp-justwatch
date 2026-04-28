# Example NixOS 25.11 configuration snippet for mcp-justwatch

{ config, pkgs, ... }:

let
  appDir = "/srv/mcp-justwatch";
in {
  security.acme.acceptTerms = true;
  security.acme.defaults.email = "you@example.com";

  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 80 443 ];
  };

  users.users.mcp-justwatch = {
    isSystemUser = true;
    group = "mcp-justwatch";
    home = appDir;
    createHome = false;
  };

  users.groups.mcp-justwatch = { };

  systemd.services.mcp-justwatch = {
    description = "mcp-justwatch FastMCP HTTP service";
    after = [ "network.target" ];
    wantedBy = [ "multi-user.target" ];

    serviceConfig = {
      Type = "simple";
      User = "mcp-justwatch";
      Group = "mcp-justwatch";
      WorkingDirectory = appDir;
      Restart = "on-failure";
      RestartSec = 5;
      ExecStart = "${pkgs.python312}/bin/python -m mcp_justwatch.server";
    };

    environment = {
      MCP_JUSTWATCH_TRANSPORT = "http";
      MCP_JUSTWATCH_HOST = "127.0.0.1";
      MCP_JUSTWATCH_PORT = "8000";
      MCP_JUSTWATCH_LOG_LEVEL = "INFO";
      MCP_JUSTWATCH_LOG_FILE = "";
      PYTHONPATH = "${appDir}/src";
    };
  };

  services.nginx = {
    enable = true;
    recommendedProxySettings = true;
    recommendedTlsSettings = true;
    virtualHosts."justwatch-mcp.example.com" = {
      enableACME = true;
      forceSSL = true;
      locations."/mcp".proxyPass = "http://127.0.0.1:8000/mcp";
      locations."/health".proxyPass = "http://127.0.0.1:8000/health";
    };
  };
}
