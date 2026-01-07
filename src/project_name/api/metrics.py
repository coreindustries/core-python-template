"""Prometheus metrics endpoint.

Exposes application metrics in Prometheus format.
"""

from fastapi import APIRouter, Response

from project_name.metrics.config import get_metrics_settings


router = APIRouter(tags=["monitoring"])


@router.get(
    "/metrics",
    include_in_schema=get_metrics_settings().include_in_schema,
    response_class=Response,
)
async def metrics() -> Response:
    """Expose Prometheus metrics endpoint.

    Returns metrics in Prometheus text format for scraping.

    Returns:
        Prometheus metrics in text/plain format.
    """
    try:
        from prometheus_client import (
            CONTENT_TYPE_LATEST,
            generate_latest,
        )
    except ImportError:
        return Response(
            content="prometheus-client not installed",
            status_code=500,
            media_type="text/plain",
        )

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
