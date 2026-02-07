# Health Checks Skill

Pre-deployment system health checks for self-hosted infrastructure.

## Disk Space Checks

```bash
# Check root filesystem
df -h / | awk 'NR==2 {print $5}'

# Check Docker data directory
df -h /var/lib/docker | awk 'NR==2 {print $5}'

# Docker-specific disk usage
docker system df
```

| Threshold | Status |
|-----------|--------|
| <70% used | OK |
| 70-85% used | Warning - consider pruning |
| >85% used | Critical - prune before deploying |

Pruning commands:
```bash
docker system prune -f           # Remove stopped containers, unused networks
docker image prune -a -f         # Remove unused images
docker volume prune -f           # Remove unused volumes (CAUTION: data loss)
```

## Memory Checks

```bash
free -m | awk 'NR==2 {printf "Total: %sMB, Used: %sMB, Available: %sMB\n", $2, $3, $7}'
```

| Available Memory | Status |
|-----------------|--------|
| >512MB | OK |
| 256-512MB | Warning - may be tight |
| <256MB | Critical - deployment may OOM |

## Port Availability

```bash
# Check if a specific port is in use
ss -tlnp | grep :<PORT>

# List all listening ports
ss -tlnp
```

If a port is occupied:
1. Identify the process: `ss -tlnp | grep :<port>` shows PID
2. Check if it is the same service being updated (expected)
3. If it is a different service, flag as Critical conflict

## DNS Resolution

```bash
# Check if subdomain resolves
nslookup <subdomain>.<hostname>

# Check /etc/hosts for local resolution
grep <subdomain> /etc/hosts
```

For `.hotport` subdomains, DNS is resolved via router hosts file or `/etc/hosts`.

## Docker Daemon Status

```bash
# Check Docker is running
docker info > /dev/null 2>&1 && echo "OK" || echo "FAIL"

# Check Docker version
docker version --format '{{.Server.Version}}'

# Check Docker Compose
docker compose version
```

## Image Pull Verification

```bash
# Check if image exists for target architecture
docker manifest inspect <image>:<tag> 2>/dev/null

# Check available architectures
docker manifest inspect <image>:<tag> | grep architecture
```

For Raspberry Pi, required architecture is `arm64` or `arm/v8`.

## SSL Certificate Checks

```bash
# Check certificate expiry (for HTTPS services)
echo | openssl s_client -servername <domain> -connect <domain>:443 2>/dev/null | openssl x509 -noout -dates
```

## Temperature (Raspberry Pi)

```bash
vcgencmd measure_temp
# or
cat /sys/class/thermal/thermal_zone0/temp  # Divide by 1000 for Celsius
```

| Temperature | Status |
|-------------|--------|
| <60C | OK |
| 60-70C | Warning - fan should be active |
| >70C | Critical - may throttle |
