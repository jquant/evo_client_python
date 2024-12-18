from typing import Optional, List, Annotated, Dict
import typer
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print as rich_print
import json
from pathlib import Path
from functools import wraps
from loguru import logger
from rich.tree import Tree
import sys

from ..api.gym_api import GymApi
from ..core.configuration import Configuration
from ..core.api_client import ApiClient
from ..models.gym_model import (
    GymKnowledgeBase,
)
from ..utils.decorators import handle_api_errors

# Configure loguru logger
logger.remove()  # Remove default handler
# Add file handler
logger.add(
    "logs/evo_client.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",  # Default level is INFO
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
# Add terminal handler
logger.add(sys.stderr, level="INFO")

# Common option types
DaysOption = Annotated[
    int,
    typer.Option(
        "--days",
        "-d",
        help="Number of days to look back",
        min=1,
        max=365,
        show_default=True,
    ),
]

MemberIdOption = Annotated[
    Optional[int], typer.Option("--member-id", "-m", help="Filter by member ID")
]

BranchOption = Annotated[
    Optional[List[int]],
    typer.Option(
        "--branch-ids",
        "-b",
        help="Branch IDs to filter by (comma-separated)",
        callback=lambda x: [int(i.strip()) for i in x.split(",")] if x else None,
    ),
]

# Create Typer apps for command groups
app = typer.Typer(
    help="Gym Management CLI",
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)
auth_app = typer.Typer(
    help="Authentication management commands", rich_markup_mode="rich"
)
contracts_app = typer.Typer(
    help="Contract management commands", rich_markup_mode="rich"
)
finance_app = typer.Typer(help="Financial management commands", rich_markup_mode="rich")
members_app = typer.Typer(help="Member management commands", rich_markup_mode="rich")
webhooks_app = typer.Typer(help="Webhook management commands", rich_markup_mode="rich")
kb_app = typer.Typer(help="Knowledge base commands", rich_markup_mode="rich")
app.add_typer(kb_app, name="kb", help="Access gym knowledge base")

# Add sub-commands to main app
app.add_typer(auth_app, name="auth", help="Manage authentication and credentials")
app.add_typer(contracts_app, name="contracts", help="Manage gym contracts")
app.add_typer(finance_app, name="finance", help="Manage financial operations")
app.add_typer(members_app, name="members", help="Manage gym members")
app.add_typer(webhooks_app, name="webhooks", help="Manage webhook subscriptions")
app.add_typer(kb_app, name="kb", help="Access gym knowledge base")

console = Console()


# Global state
class State:
    def __init__(self):
        self._gym_api: Optional[GymApi] = None
        self.verbose: bool = False

    def _get_filtered_branch_clients(
        self, branch_ids: Optional[List[int]] = None
    ) -> Dict[str, ApiClient]:
        """Get branch API clients filtered by branch IDs."""
        if not self._gym_api or not self._gym_api.branch_api_clients:
            return {}

        if not branch_ids:
            return self._gym_api.branch_api_clients

        return {
            str(bid): client
            for bid, client in self._gym_api.branch_api_clients.items()
            if int(bid) in branch_ids
        }

    def get_data_fetcher(
        self, fetcher_name: str, branch_ids: Optional[List[int]] = None
    ):
        """Get a data fetcher instance for specific branches."""
        if self._gym_api is None:
            self._gym_api = get_gym_api()

        # Return the appropriate data fetcher from GymApi
        if fetcher_name == "activity":
            return self._gym_api.activity_data_fetcher
        elif fetcher_name == "configuration":
            return self._gym_api.configuration_data_fetcher
        elif fetcher_name == "entries":
            return self._gym_api.entries_data_fetcher
        elif fetcher_name == "member":
            return self._gym_api.member_data_fetcher
        elif fetcher_name == "membership":
            return self._gym_api.membership_data_fetcher
        elif fetcher_name == "prospects":
            return self._gym_api.prospects_data_fetcher
        elif fetcher_name == "sales":
            return self._gym_api.sales_data_fetcher
        elif fetcher_name == "service":
            return self._gym_api.service_data_fetcher
        elif fetcher_name == "receivables":
            return self._gym_api.receivables_data_fetcher
        elif fetcher_name == "knowledge_base":
            return self._gym_api.knowledge_base_fetcher

        raise ValueError(f"Unknown fetcher: {fetcher_name}")

    @property
    def gym_api(self) -> GymApi:
        """Get the API client, initializing it if necessary."""
        if self._gym_api is None:
            self._gym_api = get_gym_api()
        return self._gym_api

    @gym_api.setter
    def gym_api(self, value: Optional[GymApi]):
        """Set the API client."""
        self._gym_api = value


state = State()


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from importlib.metadata import version

        try:
            v = version("evo-client")
            rich_print(f"[green]evo-client[/green] version: [blue]{v}[/blue]")
        except Exception:
            rich_print("[yellow]Version information not available[/yellow]")
        raise typer.Exit()


def verbose_callback(value: bool):
    """Set verbose mode."""
    state.verbose = value


def requires_auth(f):
    """Decorator to ensure authentication is set up."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # The api_client property will initialize the client if needed
        return f(*args, **kwargs)

    return wrapper


def get_gym_api() -> GymApi:
    """Get API client with credentials."""
    config_dir = Path(".config")
    config_dir.mkdir(exist_ok=True)
    logger.debug(f"Using config directory: {config_dir.absolute()}")

    # Find credential files
    cred_files = list(config_dir.glob("credentials.*.json"))
    logger.debug(f"Found credential files: {[f.name for f in cred_files]}")

    if not cred_files:
        console.print(
            "[red]No credentials found. Please run 'gym auth login' first.[/red]"
        )
        raise typer.Exit(1)

    # Use the most recently modified credential file
    latest_cred_file = max(cred_files, key=lambda f: f.stat().st_mtime)
    gym_name = latest_cred_file.stem.split(".")[1]
    config_file = config_dir / f"branch_configs.{gym_name}.json"

    logger.debug(
        f"Processing gym {gym_name}, config will be saved to: {config_file.absolute()}"
    )

    # Read credentials
    with open(latest_cred_file) as f:
        creds = json.load(f)
        logger.debug(f"Loaded credentials for {len(creds)} branches")

    if not creds:
        logger.warning(f"Empty credentials file for {gym_name}")
        raise typer.Exit(1)

    # Initialize branch API clients
    branch_api_clients = {}
    for branch_id, branch_creds in creds.items():
        config = Configuration()
        config.username = branch_creds["username"]
        config.password = branch_creds["password"]
        branch_api_clients[str(branch_id)] = ApiClient(configuration=config)

    # Create API client with first available client as default
    default_api_client = next(iter(branch_api_clients.values()))
    gym_api = GymApi(
        api_client=default_api_client, branch_api_clients=branch_api_clients
    )

    # Only validate/fetch configurations if cache doesn't exist
    if not config_file.exists():
        logger.debug("No cached configurations found, fetching from API...")
        try:
            configs = (
                gym_api.configuration_data_fetcher.validate_and_cache_configurations()
            )
            logger.debug(f"Retrieved {len(configs)} configurations from API")

            # Save configurations using same naming pattern as credentials
            for cred_file in cred_files:
                gym_name = cred_file.stem.split(".")[1]
                config_file = config_dir / f"branch_configs.{gym_name}.json"

                # Convert configurations to JSON-serializable format
                serializable_configs = []
                for config in configs:
                    config_dict = config.model_dump()
                    # Convert any datetime objects to ISO format strings
                    for key, value in config_dict.items():
                        if isinstance(value, datetime):
                            config_dict[key] = value.isoformat()
                    serializable_configs.append(config_dict)

                cache_data = {
                    "last_updated": datetime.now().isoformat(),
                    "configurations": serializable_configs,
                }

                with open(config_file, "w") as f:
                    json.dump(cache_data, f, indent=2)
                logger.debug(f"Saved configuration to: {config_file.absolute()}")

                # Verify file exists and has content
                if config_file.exists():
                    logger.debug(
                        f"Configuration file size: {config_file.stat().st_size} bytes"
                    )
                else:
                    logger.error(f"Configuration file was not created: {config_file}")

        except Exception as e:
            logger.error(f"Failed to validate configurations: {str(e)}")
            console.print(
                "[red]Error validating branch configurations. Please check credentials.[/red]"
            )
            raise typer.Exit(1)

    return gym_api


# Common option types
DaysOption = Annotated[
    int,
    typer.Option(
        "--days",
        "-d",
        help="Number of days to look back",
        min=1,
        max=365,
        show_default=True,
    ),
]

BranchOption = Annotated[
    Optional[List[int]],
    typer.Option(
        "--branch-ids",
        "-b",
        help="Branch IDs to filter by (comma-separated)",
        callback=lambda x: [int(i.strip()) for i in x.split(",")] if x else None,
    ),
]

BranchesOption = Annotated[
    Optional[List[str]],
    typer.Option("--branch-ids", "-b", help="List of branch IDs to filter by"),
]


# Auth commands
@auth_app.command("login")
def auth_login(
    username: Annotated[
        str, typer.Option("--username", "-u", help="API username", prompt=True)
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            help="API password",
            prompt=True,
            hide_input=True,
            confirmation_prompt=True,
        ),
    ],
    gym_name: Annotated[
        str,
        typer.Option(
            "--gym-name", "-g", help="Gym name for configuration", prompt=True
        ),
    ],
    branch_id: Annotated[
        Optional[str],
        typer.Option("--branch-id", "-b", help="Branch ID for multi-branch setup"),
    ] = None,
):
    """Login with username and password."""
    config_dir = Path.home() / ".config" / "evo-client"
    config_file = config_dir / f"credentials.{gym_name}.json"

    config_dir.mkdir(parents=True, exist_ok=True)

    config = {}
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)

    if branch_id:
        config[branch_id] = {"username": username, "password": password}
        rich_print(
            f"[green]✓[/green] Credentials saved for {gym_name} branch {branch_id}"
        )
    else:
        config["default"] = {"username": username, "password": password}
        rich_print(f"[green]✓[/green] Default credentials saved for {gym_name}")

    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    config_file.chmod(0o600)


@auth_app.command("login-file")
def auth_login_file(
    config_path: Annotated[
        Path,
        typer.Argument(
            help="Path to JSON config file",
            exists=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ],
):
    """Login using a JSON config file and fetch branch configurations."""
    try:
        # Read credentials file
        logger.debug(f"Reading credentials from: {config_path.absolute()}")
        with open(config_path) as f:
            creds = json.load(f)

        # Extract gym name from filename
        gym_name = config_path.stem.split(".")[1]
        logger.debug(f"Using gym name: {gym_name}")

        # Create .config directory in project root
        config_dir = Path(".config")
        config_dir.mkdir(parents=True, exist_ok=True)

        # Save credentials
        cred_file = config_dir / f"credentials.{gym_name}.json"
        with open(cred_file, "w") as f:
            json.dump(creds, f, indent=2)
        cred_file.chmod(0o600)
        rich_print(f"[green]✓[/green] Saved credentials for {len(creds)} branches")

        # Initialize API client and fetch configurations
        branch_api_clients = {}
        for branch_id, branch_creds in creds.items():
            config = Configuration()
            config.username = branch_creds["username"]
            config.password = branch_creds["password"]
            branch_api_clients[str(branch_id)] = ApiClient(configuration=config)

        # Create GymApi instance
        default_api_client = next(iter(branch_api_clients.values()))
        api_client = GymApi(
            api_client=default_api_client, branch_api_clients=branch_api_clients
        )

        # Fetch and save branch configurations
        logger.debug("Fetching branch configurations...")
        configs = (
            api_client.configuration_data_fetcher.validate_and_cache_configurations()
        )

        # Convert configurations to JSON-serializable format
        serializable_configs = []
        for config in configs:
            config_dict = config.model_dump()
            # Convert any datetime objects to ISO format strings
            for key, value in config_dict.items():
                if isinstance(value, datetime):
                    config_dict[key] = value.isoformat()
            serializable_configs.append(config_dict)

        # Save configurations
        config_file = config_dir / f"branch_configs.{gym_name}.json"
        cache_data = {
            "last_updated": datetime.now().isoformat(),
            "configurations": serializable_configs,
        }

        with open(config_file, "w") as f:
            json.dump(cache_data, f, indent=2)

        rich_print(
            f"[green]✓[/green] Fetched and saved configurations for {len(configs)} branches"
        )

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        rich_print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@auth_app.command("logout")
def auth_logout(
    gym_name: Annotated[
        Optional[str],
        typer.Option("--gym-name", "-g", help="Gym name to remove credentials for"),
    ] = None,
    branch_id: Annotated[
        Optional[str],
        typer.Option("--branch-id", "-b", help="Branch ID to remove credentials for"),
    ] = None,
    all: Annotated[
        bool, typer.Option("--all", help="Remove all credentials", is_flag=True)
    ] = False,
):
    """Remove saved credentials."""
    config_dir = Path.home() / ".config" / "evo-client"

    if all:
        # Remove all credential files
        for cred_file in config_dir.glob("credentials.*.json"):
            cred_file.unlink()
            rich_print(
                f"[green]✓[/green] Removed credentials for {cred_file.stem.split('.')[1]}"
            )
        return

    if not gym_name:
        rich_print("[yellow]Please specify a gym name or use --all[/yellow]")
        return

    config_file = config_dir / f"credentials.{gym_name}.json"
    config_cache = config_dir / f"branch_configs.{gym_name}.json"

    if not config_file.exists():
        rich_print(f"[yellow]No credentials found for {gym_name}[/yellow]")
        return

    with open(config_file) as f:
        config = json.load(f)

    if branch_id:
        if branch_id in config:
            del config[branch_id]
            rich_print(
                f"[green]✓[/green] Credentials removed for {gym_name} branch {branch_id}"
            )
        else:
            rich_print(f"[yellow]No credentials found for branch {branch_id}[/yellow]")
    else:
        config_file.unlink()
        if config_cache.exists():
            config_cache.unlink()
        rich_print(f"[green]✓[/green] All credentials removed for {gym_name}")
        return

    if config:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    else:
        config_file.unlink()
        if config_cache.exists():
            config_cache.unlink()


@auth_app.command("list")
def auth_list():
    """List configured credentials."""
    config_dir = Path.home() / ".config" / "evo-client"
    cred_files = list(config_dir.glob("credentials.*.json"))

    if not cred_files:
        rich_print("[yellow]No credentials configured[/yellow]")
        return

    table = Table(title="Configured Credentials")
    table.add_column("Gym", style="magenta")
    table.add_column("Branch ID", style="cyan")
    table.add_column("Username", style="green")
    table.add_column("Type", style="blue")

    for cred_file in cred_files:
        gym_name = cred_file.stem.split(".")[1]
        with open(cred_file) as f:
            config = json.load(f)

        for branch_id, creds in config.items():
            table.add_row(
                gym_name,
                branch_id,
                creds["username"],
                "Default" if branch_id == "default" else "Branch",
            )

    console.print(table)


@kb_app.command("info")
@handle_api_errors
def show_knowledge_base(
    format: Annotated[
        str,
        typer.Option(
            "--format", "-f", help="Output format (tree/table)", show_default=True
        ),
    ] = "tree",
):
    """Display gym knowledge base information."""
    try:
        kb = state.gym_api.knowledge_base_fetcher.build_knowledge_base()

        if format == "table":
            _display_kb_table(kb)
        else:
            _display_kb_tree(kb)

    except Exception as e:
        logger.error(f"Error displaying knowledge base: {str(e)}")
        raise typer.Exit(1)


def _display_kb_table(kb: GymKnowledgeBase):
    """Display knowledge base in table format."""
    table = Table(title=f"{kb.name} Gym Network")
    table.add_column("Branch ID", justify="right")
    table.add_column("Name")
    table.add_column("Location")
    table.add_column("Activities", justify="right")
    table.add_column("Services", justify="right")
    table.add_column("Plans", justify="right")

    for unit in kb.units:
        table.add_row(
            str(unit.unit_id),
            unit.name,
            f"{unit.address.city}, {unit.address.state}",
            str(len(unit.activities)),
            str(len(unit.available_services)),
            str(len(unit.plans)),
        )

    console.print(table)


def _display_kb_tree(kb: GymKnowledgeBase):
    """Display knowledge base in tree format."""
    tree = Tree(f"[bold magenta]{kb.name} Gym Network[/]")

    for unit in kb.units:
        unit_tree = tree.add(f"[bold cyan]Branch {unit.unit_id}: {unit.name}[/]")
        unit_tree.add(f"📍 {unit.address.city}, {unit.address.state}")
        unit_tree.add(f"🏃 Activities: {len(unit.activities)}")
        unit_tree.add(f"🛍️ Services: {len(unit.available_services)}")
        unit_tree.add(f"📋 Plans: {len(unit.plans)}")

    console.print(tree)


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="Show version and exit",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v", help="Enable verbose output", callback=verbose_callback
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
):
    """
    Gym Management CLI - A command-line interface for managing gym operations.

    Run 'gym auth login' to set up authentication before using other commands.
    """
    # Set logging level based on debug flag
    if debug:
        logger.remove()
        logger.add(
            "logs/evo_client.log",
            rotation="1 day",
            retention="7 days",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )
    pass


if __name__ == "__main__":
    app()
