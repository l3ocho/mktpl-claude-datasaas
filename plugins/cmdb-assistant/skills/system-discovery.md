# System Discovery Skill

Bash commands for gathering system information from the current machine.

## Basic Device Information

```bash
# Hostname
hostname

# OS/Platform info
cat /etc/os-release 2>/dev/null || uname -a

# Hardware model - Raspberry Pi
cat /proc/device-tree/model 2>/dev/null || echo "Unknown"

# Hardware model - x86 systems
cat /sys/class/dmi/id/product_name 2>/dev/null || echo "Unknown"

# Serial number - Raspberry Pi
cat /proc/device-tree/serial-number 2>/dev/null || cat /proc/cpuinfo | grep Serial | cut -d: -f2 | tr -d ' ' 2>/dev/null

# Serial number - x86 systems
cat /sys/class/dmi/id/product_serial 2>/dev/null || echo "Unknown"

# CPU count
nproc

# Memory in MB
free -m | awk '/Mem:/ {print $2}'

# Disk size in GB (root filesystem)
df -BG / | awk 'NR==2 {print $2}' | tr -d 'G'
```

## Network Interfaces

```bash
# Get interfaces with IPs (JSON format)
ip -j addr show 2>/dev/null || ip addr show

# Get default gateway interface
ip route | grep default | awk '{print $5}' | head -1

# Get MAC addresses
ip -j link show 2>/dev/null || ip link show
```

## Running Applications

```bash
# Docker containers (JSON format)
docker ps --format '{"name":"{{.Names}}","image":"{{.Image}}","status":"{{.Status}}","ports":"{{.Ports}}"}' 2>/dev/null || echo "Docker not available"

# Docker Compose projects (find compose files)
find ~/apps /home/*/apps -name "docker-compose.yml" -o -name "docker-compose.yaml" 2>/dev/null | head -20

# Running systemd services
systemctl list-units --type=service --state=running --no-pager --plain 2>/dev/null | grep -v "^UNIT" | head -30
```

## Interface Type Mapping

| Interface Pattern | NetBox Type |
|-------------------|-------------|
| `eth*`, `enp*` | `1000base-t` |
| `wlan*` | `ieee802.11ax` |
| `tailscale*`, `docker*`, `br-*` | `virtual` |
| `lo` | Skip (loopback) |

## Platform Detection

Based on OS detected, determine platform name:

| OS Detection | Platform Name |
|--------------|---------------|
| Raspberry Pi OS | `Raspberry Pi OS (Bookworm)` |
| Ubuntu | `Ubuntu {version} LTS` |
| Debian | `Debian {version}` |
| Default | `{OS Name} {Version}` |

## Device Role Auto-Detection

Based on detected services:

| Detection | Suggested Role |
|-----------|----------------|
| Docker containers found | `Docker Host` |
| Only basic services | `Server` |
| Specific role specified | Use specified |

## Container Role Mapping

Map container names/images to roles:

| Container Pattern | Role |
|-------------------|------|
| `*caddy*`, `*nginx*`, `*traefik*` | Reverse Proxy |
| `*db*`, `*postgres*`, `*mysql*`, `*redis*` | Database |
| `*webui*`, `*frontend*` | Web Application |
| Others | Infer from image or use "Container" |
