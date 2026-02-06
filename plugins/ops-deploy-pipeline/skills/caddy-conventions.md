# Caddy Conventions Skill

Caddyfile patterns for reverse proxy configuration in self-hosted environments.

## Subdomain Routing

Each service gets a subdomain of the server hostname:

```caddyfile
myapp.hotport {
    reverse_proxy app:8080
}
```

For services on non-standard ports:
```caddyfile
myapp.hotport {
    reverse_proxy app:3000
}
```

## Reverse Proxy Directives

### Basic Reverse Proxy

```caddyfile
subdomain.hostname {
    reverse_proxy container_name:port
}
```

### With Health Checks

```caddyfile
subdomain.hostname {
    reverse_proxy container_name:port {
        health_uri /health
        health_interval 30s
        health_timeout 10s
    }
}
```

### Load Balancing (Multiple Instances)

```caddyfile
subdomain.hostname {
    reverse_proxy app1:8080 app2:8080 {
        lb_policy round_robin
    }
}
```

## Security Headers

Apply to all sites:

```caddyfile
(security_headers) {
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options SAMEORIGIN
        Referrer-Policy strict-origin-when-cross-origin
        -Server
    }
}
```

Import in site blocks: `import security_headers`

## Rate Limiting

For API endpoints:

```caddyfile
subdomain.hostname {
    rate_limit {
        zone api_zone {
            key {remote_host}
            events 100
            window 1m
        }
    }
    reverse_proxy app:8080
}
```

## Docker Network Integration

Caddy must be on the same Docker network as the target service to use container DNS names. The Caddy container needs:

```yaml
networks:
  - caddy-network
  - app-network  # Join each app's network
```

## CORS Configuration

```caddyfile
subdomain.hostname {
    header Access-Control-Allow-Origin "*"
    header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
    header Access-Control-Allow-Headers "Content-Type, Authorization"

    @options method OPTIONS
    respond @options 204

    reverse_proxy app:8080
}
```

## Automatic HTTPS

- Caddy provides automatic HTTPS for public domains
- For local `.hotport` subdomains, use HTTP only (no valid TLS cert)
- For Tailscale access, consider `tls internal` for self-signed certs

## File Server (Static Assets)

```caddyfile
files.hotport {
    root * /srv/files
    file_server browse
}
```
