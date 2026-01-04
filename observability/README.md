# Observability Stack

Complete observability solution with metrics, logs, and traces.

## Services

| Service | Purpose | Port | URL |
|---------|---------|------|-----|
| **Prometheus** | Metrics collection & storage | 9090 | http://localhost:9090 |
| **Grafana** | Metrics & logs visualization | 3000 | http://localhost:3000 |
| **Loki** | Log aggregation | 3100 | http://localhost:3100 |
| **Promtail** | Log shipper to Loki | - | - |
| **Jaeger** | Distributed tracing | 16686 | http://localhost:16686 |

## Quick Start

### Start All Services

```bash
# Start the full observability stack
docker-compose up -d prometheus grafana loki promtail jaeger

# Or start everything including the app
docker-compose up -d
```

### Access Dashboards

**Grafana** (Primary Dashboard)
- URL: http://localhost:3000
- Default credentials: `admin` / `admin`
- Pre-configured datasources: Prometheus, Loki, Jaeger
- Pre-loaded dashboard: Application Overview

**Prometheus** (Metrics Explorer)
- URL: http://localhost:9090
- Query metrics directly
- Check targets: http://localhost:9090/targets

**Jaeger** (Trace Explorer)
- URL: http://localhost:16686
- View distributed traces
- Search by service, operation, tags

## Application Integration

### Metrics

The application exposes Prometheus metrics at `/metrics`:

```bash
curl http://localhost:8000/metrics
```

**Available metrics:**
- `http_requests_total` - Total HTTP requests by method, path, status
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_in_progress` - Current in-flight requests
- `app_info` - Application version and environment
- `ai_token_usage_total` - AI token consumption (if AI features enabled)
- `ai_request_duration_seconds` - AI request latency

### Logs

**File-based logging:**
```bash
# Application writes JSON logs to logs/ directory
mkdir -p logs
# Promtail reads logs and ships to Loki
```

**Direct Loki integration (optional):**
```python
# Install python-logging-loki
uv add python-logging-loki

# Configure in config.py
LOKI_URL = "http://localhost:3100"
```

### Tracing (Future Enhancement)

To enable distributed tracing:

```bash
# Install OpenTelemetry
uv add opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi

# Configure in main.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
```

## Configuration Files

```
observability/
├── prometheus/
│   └── prometheus.yml          # Prometheus scrape config
├── loki/
│   └── loki-config.yml         # Loki storage & retention
├── promtail/
│   └── promtail-config.yml     # Log collection config
└── grafana/
    ├── provisioning/
    │   ├── datasources/        # Auto-configured data sources
    │   └── dashboards/         # Dashboard auto-loading
    └── dashboards/
        └── app-overview.json   # Pre-built dashboard
```

## Customization

### Add Custom Metrics

```python
from project_name.metrics import get_metrics_collector

metrics = get_metrics_collector()

# Record custom metric
metrics.record_ai_request(
    model="gpt-4",
    operation="completion",
    duration=1.5,
    prompt_tokens=100,
    completion_tokens=50
)
```

### Add Prometheus Scrape Targets

Edit `observability/prometheus/prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'my-service'
    static_configs:
      - targets: ['my-service:8080']
```

### Create Custom Grafana Dashboards

1. Create dashboard in Grafana UI
2. Export as JSON
3. Save to `observability/grafana/dashboards/`
4. Restart Grafana: `docker-compose restart grafana`

## Troubleshooting

### Prometheus can't scrape metrics

```bash
# Check if app is exposing metrics
curl http://localhost:8000/metrics

# Check Prometheus targets
open http://localhost:9090/targets
```

### Loki not receiving logs

```bash
# Check Promtail is running
docker-compose logs promtail

# Verify log files exist
ls -la logs/

# Test Loki API
curl http://localhost:3100/ready
```

### Grafana can't connect to datasources

```bash
# Restart Grafana
docker-compose restart grafana

# Check datasource config
cat observability/grafana/provisioning/datasources/datasources.yml
```

## Production Considerations

### Resource Limits

Add resource limits in docker-compose.yml:

```yaml
prometheus:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '0.5'
```

### Data Retention

**Prometheus:** Default 15 days
```yaml
command:
  - '--storage.tsdb.retention.time=30d'
```

**Loki:** Configure in `loki-config.yml`:
```yaml
limits_config:
  retention_period: 744h  # 31 days
```

### Security

- Change Grafana admin password
- Use authentication for Prometheus/Loki
- Enable HTTPS with reverse proxy
- Restrict network access with firewall rules

### High Availability

For production HA setup:
- Run multiple Prometheus instances with Thanos
- Use Loki in distributed mode with object storage (S3/GCS)
- Deploy Jaeger with Elasticsearch backend
- Use managed Grafana or Grafana Cloud

## Useful Queries

### PromQL (Prometheus)

```promql
# Request rate per endpoint
sum(rate(http_requests_total[5m])) by (path)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### LogQL (Loki)

```logql
# Error logs in last hour
{job="app"} |= "ERROR" | json

# Logs for specific correlation ID
{job="app"} | json | correlation_id="abc-123"

# Count errors by logger
sum(count_over_time({job="app"} |= "ERROR" [1h])) by (logger)
```

## Further Reading

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
