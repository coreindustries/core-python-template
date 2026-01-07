"""CLI application using Typer.

This module provides command-line interface functionality.
"""

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from project_name import __version__
from project_name.config import settings


# Create CLI app
app = typer.Typer(
    name="project-name",  # TODO: Update project name
    help="Project Name CLI - A command-line interface for the application.",
    add_completion=True,
)

# Console for rich output
console = Console()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        is_eager=True,
    ),
) -> None:
    """Project Name CLI.

    A command-line interface for managing the application.
    """
    if version:
        rprint(f"[bold blue]Project Name[/bold blue] version: {__version__}")
        raise typer.Exit()


@app.command()
def info() -> None:
    """Display application configuration information."""
    table = Table(title="Application Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Environment", settings.environment)
    table.add_row("Debug Mode", str(settings.debug))
    table.add_row("Log Level", settings.log_level)
    table.add_row("API Host", settings.api_host)
    table.add_row("API Port", str(settings.api_port))
    table.add_row("Database URL", _mask_url(settings.database_url))
    table.add_row(
        "Redis URL",
        _mask_url(settings.redis_url) if settings.redis_url else "Not configured",
    )

    console.print(table)


@app.command()
def serve(
    host: str = typer.Option(
        settings.api_host,
        "--host",
        "-h",
        help="Host to bind to.",
    ),
    port: int = typer.Option(
        settings.api_port,
        "--port",
        "-p",
        help="Port to bind to.",
    ),
    reload: bool = typer.Option(
        settings.debug,
        "--reload",
        "-r",
        help="Enable auto-reload.",
    ),
) -> None:
    """Start the API server."""
    import uvicorn  # noqa: PLC0415  # Lazy import to avoid loading unless serving

    rprint(f"[bold green]Starting server on {host}:{port}[/bold green]")
    uvicorn.run(
        "project_name.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def db_migrate() -> None:
    """Run database migrations."""
    import subprocess  # noqa: PLC0415  # nosec B404  # CLI tool, lazy import

    rprint("[bold blue]Running database migrations...[/bold blue]")
    result = subprocess.run(  # nosec B603, B607  # shell=False is safe, command is hardcoded
        ["uv", "run", "prisma", "migrate", "deploy"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        rprint("[bold green]Migrations completed successfully![/bold green]")
    else:
        rprint(f"[bold red]Migration failed:[/bold red]\n{result.stderr}")
        raise typer.Exit(code=1)


@app.command()
def db_generate() -> None:
    """Generate Prisma client."""
    import subprocess  # noqa: PLC0415  # nosec B404  # CLI tool, lazy import

    rprint("[bold blue]Generating Prisma client...[/bold blue]")
    result = subprocess.run(  # nosec B603, B607  # shell=False is safe, command is hardcoded
        ["uv", "run", "prisma", "generate"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        rprint("[bold green]Prisma client generated successfully![/bold green]")
    else:
        rprint(f"[bold red]Generation failed:[/bold red]\n{result.stderr}")
        raise typer.Exit(code=1)


def _mask_url(url: str) -> str:
    """Mask sensitive parts of a URL.

    Args:
        url: URL string to mask.

    Returns:
        URL with password masked.
    """
    if "://" in url and "@" in url:
        # Mask password in URL
        protocol, rest = url.split("://", 1)
        if "@" in rest:
            credentials, host = rest.rsplit("@", 1)
            if ":" in credentials:
                user, _ = credentials.split(":", 1)
                return f"{protocol}://{user}:****@{host}"
    return url


if __name__ == "__main__":
    app()
