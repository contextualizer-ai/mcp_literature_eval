"""CLI interface for mcp_literature_eval."""

import typer
from typing_extensions import Annotated

app = typer.Typer(help="mcp_literature_eval: Eval of MCPs that retrieve stuff to do with scientific literature")


@app.command()
def run(
    name: Annotated[str, typer.Option(help="Name of the person to greet")],
):
    typer.echo(f"Hello, {name}!")

def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
