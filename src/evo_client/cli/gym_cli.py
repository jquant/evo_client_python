import json
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Annotated, List, Optional

import typer
from loguru import logger
from rich import print as rich_print
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from ..sync.core.api_client import SyncApiClient
from ..core.configuration import Configuration
from ..models.gym_model import GymKnowledgeBase
from ..models.webhook_model import WebhookEventType
from ..services.data_fetchers import BranchApiClientManager
from ..services.data_fetchers.gym_metrics_data_fetcher import GymMetricsDataFetcher
from ..services.data_fetchers.overdue_members_data_fetcher import (
    OverdueMembersDataFetcher,
)
from ..services.gym_api import GymApi
from ..services.gym_knowledge_base.gym_kb_data_fetcher import GymKnowledgeBaseService
from ..services.member_files.member_files_data_fetcher import MemberFilesDataFetcher
from ..services.operating_data.operating_data_fetcher import OperatingDataFetcher
from ..services.webhook_management.webhook_management import WebhookManagementService

console = Console()

app = typer.Typer(
    help="Gym Management CLI", no_args_is_help=True, rich_markup_mode="rich"
)
auth_app = typer.Typer(
    help="Authentication management commands. Handles credential files in .config/credentials.<gymname>.json",
    rich_markup_mode="rich",
)
contracts_app = typer.Typer(
    help="Contract management commands", rich_markup_mode="rich"
)
finance_app = typer.Typer(help="Financial management commands", rich_markup_mode="rich")
members_app = typer.Typer(help="Member management commands", rich_markup_mode="rich")
webhooks_app = typer.Typer(help="Webhook management commands", rich_markup_mode="rich")
kb_app = typer.Typer(help="Knowledge base commands", rich_markup_mode="rich")
operating_data_app = typer.Typer(
    help="Operating data commands", rich_markup_mode="rich"
)

app.add_typer(auth_app, name="auth", help="Manage authentication and credentials")
app.add_typer(contracts_app, name="contracts", help="Manage gym contracts")
app.add_typer(finance_app, name="finance", help="Manage financial operations")
app.add_typer(members_app, name="members", help="Manage gym members")
app.add_typer(webhooks_app, name="webhooks", help="Manage webhook subscriptions")
app.add_typer(kb_app, name="kb", help="Access gym knowledge base")
app.add_typer(
    operating_data_app, name="operating-data", help="Get operating data metrics"
)

# New subcommands
overdue_app = typer.Typer(help="Retrieve overdue members for campaigns")
metrics_app = typer.Typer(help="Retrieve advanced metrics like MRR, LTV, NRR, etc.")

app.add_typer(overdue_app, name="overdue", help="Overdue members retrieval")
app.add_typer(metrics_app, name="metrics", help="Advanced KPI metrics")


class State:
    def __init__(self):
        self._gym_api = None
        self.verbose = False
        self._client_manager = None

    @property
    def gym_api(self):
        if self._gym_api is None:
            self._gym_api = get_gym_api()
        return self._gym_api

    def get_client_manager(self):
        if self._client_manager is None:
            config_dir = Path(".config")

            # Check for active credentials first
            cred_file: Optional[Path] = None
            active_cred_file = config_dir / "active_credentials"
            if active_cred_file.exists():
                cred_file = Path(active_cred_file.read_text().strip())
                if cred_file.exists():
                    console.print(
                        f"[green]Using selected credentials:[/green] {cred_file}"
                    )
                else:
                    console.print(
                        "[yellow]Selected credentials file not found, falling back to latest[/yellow]"
                    )
                    active_cred_file.unlink()
                    cred_file = None

            if not cred_file:
                # Fall back to finding credentials files
                cred_files = list(config_dir.glob("credentials.*.json"))
                if not cred_files:
                    console.print(
                        "[red]No credentials found. Please create a credentials file using:[/red]"
                    )
                    console.print(
                        "[yellow]evo auth setup --gym-name <name> --branch-id <id> --username <user>[/yellow]"
                    )
                    console.print(
                        "\nOr select an existing one using: [yellow]evo auth select[/yellow]"
                    )
                    raise typer.Exit(1)

                cred_file = max(cred_files, key=lambda f: f.stat().st_mtime)
                console.print(f"[green]Using latest credentials:[/green] {cred_file}")

            try:
                with open(cred_file) as f:
                    creds = json.load(f)
            except json.JSONDecodeError:
                console.print("[red]Invalid JSON format in credentials file[/red]")
                raise typer.Exit(1)
            except Exception as e:
                console.print(f"[red]Error reading credentials file: {str(e)}[/red]")
                raise typer.Exit(1)

            branch_api_clients = {}
            for branch_id, branch_creds in creds.items():
                configuration = Configuration()
                configuration.username = branch_creds["username"]
                configuration.password = branch_creds["password"]
                branch_api_clients[str(branch_id)] = SyncApiClient(
                    configuration=configuration
                )
            self._client_manager = BranchApiClientManager(
                branch_api_clients=branch_api_clients
            )
        return self._client_manager


state = State()


def version_callback(value: bool):
    if value:
        rich_print("[green]evo-client[/green] version: [blue]1.0.1[/blue]")
        raise typer.Exit()


def verbose_callback(value: bool):
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
        configuration = Configuration()
        configuration.username = branch_creds["username"]
        configuration.password = branch_creds["password"]
        branch_api_clients[str(branch_id)] = SyncApiClient(configuration=configuration)

    client_manager = BranchApiClientManager(branch_api_clients=branch_api_clients)
    gym_api = GymApi(client_manager=client_manager)

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
            configuration = Configuration()
            configuration.username = branch_creds["username"]
            configuration.password = branch_creds["password"]
            branch_api_clients[str(branch_id)] = SyncApiClient(
                configuration=configuration
            )

        client_manager = BranchApiClientManager(branch_api_clients=branch_api_clients)
        api_client = GymApi(client_manager=client_manager)

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


@members_app.command("list")
def members_list():
    """List members."""
    members = state.gym_api.member_data_fetcher.fetch_members()
    console.print(members)


@members_app.command("member")
def members_files(
    member_id: Annotated[str, typer.Argument(help="Member ID")],
    branch_id: Annotated[
        Optional[int],
        typer.Option("--branch-id", "-b", help="Branch ID to filter by"),
    ] = None,
):
    """List members files."""
    members_files = state.gym_api.member_data_fetcher.fetch_member_by_id(
        member_id=member_id, branch_id=branch_id
    )
    console.print(members_files)


@contracts_app.command("list")
def contracts_list():
    """List contracts."""
    contracts = state.gym_api.membership_data_fetcher.fetch_memberships()
    console.print(contracts)


@contracts_app.command("categories")
def contracts_categories():
    """List contracts."""
    contracts = state.gym_api.membership_data_fetcher.fetch_membership_categories()
    console.print(contracts)


@finance_app.command("list")
def finance_list():
    """List receivables."""
    receivables = state.gym_api.receivables_data_fetcher.fetch_receivables()
    console.print(receivables)


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
            str(unit.branch_id),
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
        unit_tree = tree.add(f"[bold cyan]Branch {unit.branch_id}: {unit.name}[/]")
        unit_tree.add(f"📍 {unit.address.city}, {unit.address.state}")
        unit_tree.add(f"🏃 Activities: {len(unit.activities)}")
        unit_tree.add(f"🛍️ Services: {len(unit.available_services)}")
        unit_tree.add(f"📋 Plans: {len(unit.plans)}")

    console.print(tree)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
        callback=verbose_callback,
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
):
    if debug:
        logger.remove()
        logger.add(
            "logs/evo_client.log",
            rotation="1 day",
            retention="7 days",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )


@kb_app.command("info")
def show_knowledge_base(
    format: str = typer.Option(
        "tree", "--format", "-f", help="Output format (tree/table)"
    ),
):
    client_manager = state.get_client_manager()
    kb_service = GymKnowledgeBaseService(client_manager)
    kb = kb_service.build_knowledge_base()

    if format == "table":
        table = Table(title=f"{kb.name} Gym Network")
        table.add_column("Branch ID", justify="right")
        table.add_column("Name")
        table.add_column("Location")
        table.add_column("Activities", justify="right")
        table.add_column("Services", justify="right")
        table.add_column("Plans", justify="right")

        for unit in kb.units:
            table.add_row(
                str(unit.branch_id),
                unit.name,
                f"{unit.address.city}, {unit.address.state}",
                str(len(unit.activities)),
                str(len(unit.available_services)),
                str(len(unit.plans)),
            )

        console.print(table)
    else:
        tree = Tree(f"[bold magenta]{kb.name} Gym Network[/]")
        for unit in kb.units:
            unit_tree = tree.add(f"[bold cyan]Branch {unit.branch_id}: {unit.name}[/]")
            unit_tree.add(f"📍 {unit.address.city}, {unit.address.state}")
            unit_tree.add(f"🏃 Activities: {len(unit.activities)}")
            unit_tree.add(f"🛍️ Services: {len(unit.available_services)}")
            unit_tree.add(f"📋 Plans: {len(unit.plans)}")

        console.print(tree)


@operating_data_app.command("fetch")
def fetch_operating_data(
    branch_ids: str = typer.Option(
        "", "--branch-ids", help="Comma-separated list of branch IDs"
    ),
    start_date: str = typer.Option(None, "--start-date", help="Start date YYYY-MM-DD"),
    end_date: str = typer.Option(None, "--end-date", help="End date YYYY-MM-DD"),
):
    client_manager = state.get_client_manager()
    od_fetcher = OperatingDataFetcher(client_manager)

    branches = None
    if branch_ids.strip():
        branches = [
            int(b.strip()) for b in branch_ids.split(",") if b.strip().isdigit()
        ]

    from_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    to_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    data = od_fetcher.fetch_operating_data(
        from_date=from_date, to_date=to_date, branch_ids=branches
    )

    if isinstance(data, list):
        for d in data:
            console.print(f"Branch: {d.branch_id}")
            console.print(d.to_dict())
    else:
        console.print(data.to_dict())


@members_app.command("files")
def member_files_cmd(
    member_ids: str = typer.Option(
        ..., "--member-ids", "-m", help="Comma-separated list of member IDs"
    ),
    branch_ids: str = typer.Option(
        "", "--branch-ids", help="Comma-separated list of branch IDs"
    ),
    start_date: str = typer.Option(None, "--start-date", help="Start date YYYY-MM-DD"),
    end_date: str = typer.Option(None, "--end-date", help="End date YYYY-MM-DD"),
):
    client_manager = state.get_client_manager()
    mf_fetcher = MemberFilesDataFetcher(client_manager)

    m_ids = [int(m.strip()) for m in member_ids.split(",") if m.strip().isdigit()]
    branches = None
    if branch_ids.strip():
        branches = [
            int(b.strip()) for b in branch_ids.split(",") if b.strip().isdigit()
        ]

    from_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    to_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    members_files = mf_fetcher.get_members_files(
        member_ids=m_ids, branch_ids=branches, from_date=from_date, to_date=to_date
    )
    if isinstance(members_files, list):
        for mf in members_files:
            console.print(mf.model_dump(mode="json"))
    else:
        console.print(members_files.model_dump(mode="json"))


# New commands


@overdue_app.command("list")
def overdue_list(
    branch_ids: str = typer.Option(
        "", "--branch-ids", help="Comma-separated branch IDs"
    ),
    due_date_end: str = typer.Option(
        None, "--due-date-end", help="Fetch receivables due before this date YYYY-MM-DD"
    ),
):
    client_manager = state.get_client_manager()
    od_fetcher = OverdueMembersDataFetcher(client_manager)

    branches = None
    if branch_ids.strip():
        branches = [
            int(b.strip()) for b in branch_ids.split(",") if b.strip().isdigit()
        ]

    dte = datetime.strptime(due_date_end, "%Y-%m-%d") if due_date_end else None
    overdue = od_fetcher.fetch_overdue_members(due_date_end=dte, branch_ids=branches)

    table = Table(title="Overdue Members")
    table.add_column("Member ID", justify="right")
    table.add_column("Name")
    table.add_column("Total Overdue")
    table.add_column("Overdue Since")

    for om in overdue:
        table.add_row(
            str(om.member_id),
            om.name,
            f"{om.total_overdue:.2f}",
            om.overdue_since.strftime("%Y-%m-%d"),
        )
    console.print(table)


@metrics_app.command("advanced")
def metrics_advanced(
    branch_ids: str = typer.Option(
        "", "--branch-ids", help="Comma-separated branch IDs"
    ),
    start_date: str = typer.Option(None, "--start-date", help="Start date YYYY-MM-DD"),
    end_date: str = typer.Option(None, "--end-date", help="End date YYYY-MM-DD"),
):
    client_manager = state.get_client_manager()
    gm_fetcher = GymMetricsDataFetcher(client_manager)

    branches = None
    if branch_ids.strip():
        branches = [
            int(b.strip()) for b in branch_ids.split(",") if b.strip().isdigit()
        ]

    from_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    to_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    data = gm_fetcher.fetch_advanced_metrics(
        from_date=from_date, to_date=to_date, branch_ids=branches
    )
    # print metrics
    console.print("[bold magenta]Advanced Metrics[/bold magenta]")
    console.print(f"Churn Rate: {data.churn_rate}%")
    console.print(f"MRR: ${data.mrr}")
    console.print(f"LTV: ${data.lifetime_value}")
    console.print(f"ARR: ${data.arr}")
    grr = getattr(data, "grr", None)
    nrr = getattr(data, "nrr", None)
    if grr is not None:
        console.print(f"GRR: {grr}%")
    if nrr is not None:
        console.print(f"NRR: {nrr}%")
    discount_effect = getattr(data, "discount_effectiveness", None)
    campaign_effect = getattr(data, "campaign_effectiveness", None)
    if discount_effect:
        console.print(f"Discount Effectiveness: {discount_effect}")
    if campaign_effect:
        console.print(f"Campaign Effectiveness: {campaign_effect}")


@webhooks_app.command("subscribe")
def webhook_subscribe(
    url: str = typer.Option(..., "--url", "-u", help="Webhook callback URL"),
    event_types: str = typer.Option(
        "", "--events", "-e", help="Comma-separated list of event types"
    ),
    branch_ids: str = typer.Option(
        "", "--branch-ids", "-b", help="Comma-separated list of branch IDs"
    ),
    headers: str = typer.Option(
        "",
        "--headers",
        "-h",
        help='JSON string of headers [{"nome": "name", "valor": "value"}]',
    ),
    filters: str = typer.Option(
        "",
        "--filters",
        "-f",
        help='JSON string of filters [{"filterType": "type", "value": "value"}]',
    ),
):
    """Subscribe to webhook events."""
    client_manager = state.get_client_manager()
    webhook_service = WebhookManagementService(client_manager)

    # Parse event types
    event_list = None
    if event_types.strip():
        event_list = [e.strip() for e in event_types.split(",")]
        # Validate event types
        valid_events = [e.value for e in WebhookEventType]
        invalid_events = [e for e in event_list if e not in valid_events]
        if invalid_events:
            console.print(
                f"[red]Invalid event types: {', '.join(invalid_events)}[/red]"
            )
            console.print(f"Valid event types: {', '.join(valid_events)}")
            raise typer.Exit(1)

    # Parse branch IDs
    branch_list = None
    if branch_ids.strip():
        branch_list = [b.strip() for b in branch_ids.split(",")]

    # Parse headers
    header_list = None
    if headers.strip():
        try:
            header_list = json.loads(headers)
        except json.JSONDecodeError:
            console.print("[red]Invalid headers JSON format[/red]")
            raise typer.Exit(1)

    # Parse filters
    filter_list = None
    if filters.strip():
        try:
            filter_list = json.loads(filters)
        except json.JSONDecodeError:
            console.print("[red]Invalid filters JSON format[/red]")
            raise typer.Exit(1)

    try:
        success = webhook_service.manage_webhooks(
            url_callback=url,
            branch_ids=[int(b) for b in branch_list] if branch_list else [],
            event_types=event_list,
            headers=header_list,
            filters=filter_list,
            unsubscribe=False,
        )
        if success:
            console.print("[green]Successfully subscribed to webhook events[/green]")
        else:
            console.print("[red]Failed to subscribe to webhook events[/red]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@webhooks_app.command("unsubscribe")
def webhook_unsubscribe(
    url: str = typer.Option(
        ..., "--url", "-u", help="Webhook callback URL to unsubscribe"
    ),
    event_types: str = typer.Option(
        "", "--events", "-e", help="Comma-separated list of event types to unsubscribe"
    ),
    branch_ids: str = typer.Option(
        "", "--branch-ids", "-b", help="Comma-separated list of branch IDs"
    ),
):
    """Unsubscribe from webhook events."""
    client_manager = state.get_client_manager()
    webhook_service = WebhookManagementService(client_manager)

    # Parse event types
    event_list = None
    if event_types.strip():
        event_list = [e.strip() for e in event_types.split(",")]
        # Validate event types
        valid_events = [e.value for e in WebhookEventType]
        invalid_events = [e for e in event_list if e not in valid_events]
        if invalid_events:
            console.print(
                f"[red]Invalid event types: {', '.join(invalid_events)}[/red]"
            )
            console.print(f"Valid event types: {', '.join(valid_events)}")
            raise typer.Exit(1)

    # Parse branch IDs
    branch_list = None
    if branch_ids.strip():
        branch_list = [b.strip() for b in branch_ids.split(",")]

    try:
        success = webhook_service.manage_webhooks(
            url_callback=url,
            branch_ids=[int(b) for b in branch_list] if branch_list else [],
            event_types=event_list,
            unsubscribe=True,
        )
        if success:
            console.print(
                "[green]Successfully unsubscribed from webhook events[/green]"
            )
        else:
            console.print("[red]Failed to unsubscribe from webhook events[/red]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@webhooks_app.command("list-events")
def list_event_types():
    """List all available webhook event types."""
    table = Table(title="Available Webhook Event Types")
    table.add_column("Event Type")
    table.add_column("Description")

    event_descriptions = {
        "NewSale": "Triggered when a new sale is made",
        "NewMember": "Triggered when a new member is registered",
        "CanceledMember": "Triggered when a member is canceled",
        "NewCheckin": "Triggered when a member checks in",
        "NewDebt": "Triggered when a new debt is registered",
        "NewPayment": "Triggered when a new payment is made",
    }

    for event in WebhookEventType:
        table.add_row(
            event.value, event_descriptions.get(event.value, "No description available")
        )

    console.print(table)


@auth_app.command("setup")
def setup_auth(
    gym_name: str = typer.Option(
        ..., "--gym-name", "-g", help="Name of the gym for the credentials file"
    ),
    branch_id: int = typer.Option(
        ..., "--branch-id", "-b", help="Branch ID for authentication"
    ),
    username: str = typer.Option(
        ..., "--username", "-u", help="Username for authentication"
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        help="Password for authentication",
        prompt=True,
        hide_input=True,
    ),
):
    """
    Set up authentication credentials for a gym branch.

    Creates or updates a credentials file at .config/credentials.<gymname>.json
    with the provided authentication information.

    Example:
        evo auth setup --gym-name mygym --branch-id 123 --username admin
    """
    config_dir = Path(".config")
    config_dir.mkdir(exist_ok=True)

    cred_file = config_dir / f"credentials.{gym_name}.json"

    # Load existing credentials if file exists
    creds = {}
    if cred_file.exists():
        try:
            with open(cred_file) as f:
                creds = json.load(f)
        except json.JSONDecodeError:
            console.print(
                "[yellow]Existing credentials file is invalid, creating new one[/yellow]"
            )

    # Update credentials
    creds[str(branch_id)] = {"username": username, "password": password}

    # Save credentials
    with open(cred_file, "w") as f:
        json.dump(creds, f, indent=4)

    console.print(f"[green]Successfully saved credentials to[/green] {cred_file}")


@auth_app.command("list")
def list_auth():
    """
    List all available credential files and their associated branches.

    Shows the credentials files present in .config/ directory
    and the branch IDs configured in each file.
    """
    config_dir = Path(".config")
    cred_files = list(config_dir.glob("credentials.*.json"))

    if not cred_files:
        console.print("[yellow]No credential files found.[/yellow]")
        console.print(
            "Create one using: [green]evo auth setup --gym-name <name> --branch-id <id> --username <user>[/green]"
        )
        return

    table = Table(title="Available Credential Files")
    table.add_column("Gym Name")
    table.add_column("File Path")
    table.add_column("Branch IDs")
    table.add_column("Last Modified")

    for cred_file in cred_files:
        try:
            with open(cred_file) as f:
                creds = json.load(f)
            gym_name = cred_file.stem.split(".")[1]
            branch_ids = ", ".join(creds.keys())
            mod_time = datetime.fromtimestamp(cred_file.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            table.add_row(gym_name, str(cred_file), branch_ids, mod_time)
        except Exception as e:
            table.add_row(
                cred_file.stem.split(".")[1],
                str(cred_file),
                f"[red]Error: {str(e)}[/red]",
                datetime.fromtimestamp(cred_file.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            )

    console.print(table)


@auth_app.command("select")
def select_auth():
    """
    Interactively select which credentials file to use.

    Lists all available credential files and allows the user to
    select one as the active credentials file.
    """
    config_dir = Path(".config")
    cred_files = list(config_dir.glob("credentials.*.json"))

    if not cred_files:
        console.print("[yellow]No credential files found.[/yellow]")
        console.print(
            "Create one using: [green]evo auth setup --gym-name <name> --branch-id <id> --username <user>[/green]"
        )
        return

    # Create list of choices
    choices = []
    for i, cred_file in enumerate(cred_files, 1):
        gym_name = cred_file.stem.split(".")[1]
        try:
            with open(cred_file) as f:
                creds = json.load(f)
            branch_ids = ", ".join(creds.keys())
            choices.append(f"{i}. {gym_name} (Branches: {branch_ids})")
        except Exception as e:
            choices.append(f"{i}. {gym_name} [red](Error: {str(e)})[/red]")

    # Print choices
    console.print("\n[bold]Available credential files:[/bold]")
    for choice in choices:
        console.print(choice)

    # Get user selection
    while True:
        try:
            selection = console.input("\nSelect a credentials file (enter number): ")
            idx = int(selection) - 1
            if 0 <= idx < len(cred_files):
                selected_file = cred_files[idx]
                # Create a symlink or marker file to indicate the selected credentials
                marker_file = config_dir / "active_credentials"
                if marker_file.exists():
                    marker_file.unlink()
                marker_file.write_text(str(selected_file))
                console.print(
                    f"\n[green]Successfully selected credentials:[/green] {selected_file}"
                )
                break
            else:
                console.print(
                    "[red]Invalid selection. Please enter a valid number.[/red]"
                )
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            raise typer.Exit(1)


@webhooks_app.command("list")
def list_webhooks():
    """List all configured webhooks."""
    client_manager = state.get_client_manager()
    webhook_service = WebhookManagementService(client_manager)

    try:
        webhooks = webhook_service.webhook_fetcher.fetch_webhooks()

        if not webhooks:
            console.print("[yellow]No webhooks configured.[/yellow]")
            return

        table = Table(title="Configured Webhooks")
        table.add_column("Branch ID")
        table.add_column("Event Type")
        table.add_column("URL")
        table.add_column("Headers", overflow="fold")
        table.add_column("Filters", overflow="fold")
        table.add_column("Created Date")

        for webhook in webhooks:
            # Convert header models to dicts before JSON serialization
            # headers_str = (
            #     json.dumps(
            #         [{"name": h.nome, "value": h.valor} for h in webhook.headers]
            #     )
            #     if webhook.headers
            #     else ""
            # )
            # filters_str = (
            #     json.dumps([f.model_dump() for f in webhook.filters])
            #     if webhook.filters
            #     else ""
            # )
            webhook.created_date if webhook.created_date else "N/A"

            table.add_row(
                str(webhook.IdBranch or "All"),
                webhook.eventType or "N/A",
                webhook.urlCallback or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing webhooks: {str(e)}[/red]")
        raise typer.Exit(1)
