from typing import Optional, List, cast, Any, Annotated, Dict
import typer
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rich_print
import json
from pathlib import Path
from functools import wraps
from rich import box
from loguru import logger
import logging
from decimal import Decimal

from ..api.gym_api import GymApi
from ..core.configuration import Configuration
from ..core.api_client import ApiClient
from ..models.gym_model import (
    ReceivableStatus,
    OverdueMember,
)
from ..services.data_fetchers.activity_data_fetcher import ActivityDataFetcher
from ..services.data_fetchers.configuration_data_fetcher import ConfigurationDataFetcher
from ..services.data_fetchers.entries_data_fetcher import EntriesDataFetcher
from ..services.data_fetchers.member_data_fetcher import MemberDataFetcher
from ..services.data_fetchers.membership_data_fetcher import MembershipDataFetcher
from ..services.data_fetchers.prospects_data_fetcher import ProspectsDataFetcher
from ..services.data_fetchers.receivables_data_fetcher import ReceivablesDataFetcher
from ..services.data_fetchers.sales_data_fetcher import SalesDataFetcher
from ..services.data_fetchers.service_data_fetcher import ServiceDataFetcher
from ..utils.decorators import handle_api_errors

# Configure loguru logger
logger.add(
    "logs/evo_client.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Common option types
DaysOption = Annotated[int, typer.Option(
    "--days", "-d",
    help="Number of days to look back",
    min=1, max=365, show_default=True
)]

MemberIdOption = Annotated[Optional[int], typer.Option(
    "--member-id", "-m",
    help="Filter by member ID"
)]

BranchIdOption = Annotated[Optional[int], typer.Option(
    "--branch-id", "-b",
    help="Branch ID to filter by"
)]

# Create Typer apps for command groups
app = typer.Typer(
    help="Gym Management CLI",
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]}
)
auth_app = typer.Typer(help="Authentication management commands", rich_markup_mode="rich")
contracts_app = typer.Typer(help="Contract management commands", rich_markup_mode="rich")
finance_app = typer.Typer(help="Financial management commands", rich_markup_mode="rich")
members_app = typer.Typer(help="Member management commands", rich_markup_mode="rich")
webhooks_app = typer.Typer(help="Webhook management commands", rich_markup_mode="rich")

# Add sub-commands to main app
app.add_typer(auth_app, name="auth", help="Manage authentication and credentials")
app.add_typer(contracts_app, name="contracts", help="Manage gym contracts")
app.add_typer(finance_app, name="finance", help="Manage financial operations")
app.add_typer(members_app, name="members", help="Manage gym members")
app.add_typer(webhooks_app, name="webhooks", help="Manage webhook subscriptions")

console = Console()

# Global state
class State:
    def __init__(self):
        self._api_client: Optional[GymApi] = None
        self._data_fetchers = {}
        self.verbose: bool = False
    
    @property
    def api_client(self) -> GymApi:
        """Get the API client, initializing it if necessary."""
        if self._api_client is None:
            self._api_client = get_api_client()
            # Initialize data fetchers when API client is created
            self._data_fetchers = {
                'activity': ActivityDataFetcher(self._api_client.activities_api, self._api_client.branch_api_clients),
                'configuration': ConfigurationDataFetcher(self._api_client.configuration_api, self._api_client.branch_api_clients),
                'entries': EntriesDataFetcher(self._api_client.entries_api, self._api_client.branch_api_clients),
                'member': MemberDataFetcher(self._api_client.members_api, self._api_client.branch_api_clients),
                'membership': MembershipDataFetcher(self._api_client.membership_api, self._api_client.branch_api_clients),
                'prospects': ProspectsDataFetcher(self._api_client.prospects_api, self._api_client.branch_api_clients),
                'receivables': ReceivablesDataFetcher(
                    self._api_client.receivables_api,
                    self._api_client.branch_api_clients
                ),
                'sales': SalesDataFetcher(self._api_client.sales_api, self._api_client.branch_api_clients),
                'service': ServiceDataFetcher(self._api_client.service_api, self._api_client.branch_api_clients)
            }
        return self._api_client
    
    @property
    def data_fetchers(self):
        """Get data fetchers, ensuring API client is initialized."""
        if not self._data_fetchers:
            _ = self.api_client  # This will initialize data fetchers
        return self._data_fetchers
    
    @api_client.setter
    def api_client(self, value: Optional[GymApi]):
        """Set the API client."""
        self._api_client = value

state = State()

def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from importlib.metadata import version
        try:
            v = version("evo-client")
            rich_print(f"[green]evo-client[/green] version: [blue]{v}[/blue]")
        except:
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

def get_api_client() -> GymApi:
    """Get API client with credentials."""
    config_file = Path.home() / ".config" / "evo-client" / "credentials.json"
    
    if not config_file.exists():
        console.print("[red]No credentials found. Please run 'auth login' first.[/red]")
        raise typer.Exit(1)
    
    with open(config_file) as f:
        config = json.load(f)
    
    if not config:
        console.print("[red]Credentials file is empty or invalid.[/red]")
        raise typer.Exit(1)
    
    # Multi-branch setup
    if any(k != "default" for k in config.keys()):
        logger.debug("Using multi-branch configuration")
        branch_api_clients = {}
        configured_branches = set()
        
        for branch_id, creds in config.items():
            if branch_id == "default":
                continue
            try:
                branch_id_int = int(branch_id)
                configured_branches.add(branch_id_int)
                logger.debug(f"Adding credentials for branch {branch_id}")
                
                branch_config = Configuration()
                branch_config.username = creds["username"]
                branch_config.password = creds["password"]
                
                branch_api_clients[str(branch_id)] = ApiClient(configuration=branch_config)
            except (ValueError, KeyError):
                logger.warning(f"Invalid or incomplete branch credentials in {branch_id}")
        
        default_api_client = next(iter(branch_api_clients.values())) if branch_api_clients else None
        api_client = GymApi(
            api_client=default_api_client,
            branch_api_clients=branch_api_clients
        )
        
        # Validate branch IDs (synchronously)
        try:
            logger.debug("Fetching branch configurations for validation...")
            branch_configs = api_client.configuration_data_fetcher.fetch_branch_configurations()
            logger.debug(f"Raw branch configs: {branch_configs}")

            flattened_configs = []
            for c in branch_configs:
                if isinstance(c, list):
                    logger.debug(f"Found list of configs: {c}")
                    flattened_configs.extend(c)
                else:
                    logger.debug(f"Found single config: {c}")
                    flattened_configs.append(c)
            
            if flattened_configs:
                valid_branches = {str(b.id_branch) for b in flattened_configs if b.id_branch}
                invalid_branches = configured_branches - {int(b) for b in valid_branches}
                if invalid_branches:
                    logger.warning(f"Invalid branch IDs found in credentials: {invalid_branches}")
                    logger.warning(f"Valid branch IDs: {valid_branches}")
        except Exception as e:
            logger.warning(f"Failed to validate branch IDs: {e}")
        
        return api_client
    
    # Single branch setup
    default_creds = config.get("default")
    if not default_creds:
        console.print("[red]Default credentials not found. Please run 'auth login' first.[/red]")
        raise typer.Exit(1)
    
    configuration = Configuration()
    configuration.username = default_creds["username"]
    configuration.password = default_creds["password"]
    
    single_api_client = ApiClient(configuration=configuration)
    return GymApi(api_client=single_api_client, branch_api_clients={})

# Common option types
DaysOption = Annotated[int, typer.Option(
    "--days", "-d",
    help="Number of days to look back",
    min=1, max=365, show_default=True
)]

BranchOption = Annotated[Optional[int], typer.Option(
    "--branch-id", "-b",
    help="Branch ID to filter by"
)]

BranchesOption = Annotated[Optional[List[str]], typer.Option(
    "--branch-ids", "-b",
    help="List of branch IDs to filter by"
)]

# Auth commands
@auth_app.command("login")
def auth_login(
    username: Annotated[str, typer.Option("--username", "-u", help="API username", prompt=True)],
    password: Annotated[str, typer.Option(
        "--password", "-p",
        help="API password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True
    )],
    branch_id: Annotated[Optional[str], typer.Option(
        "--branch-id", "-b",
        help="Branch ID for multi-branch setup"
    )] = None,
):
    """Login with username and password."""
    config_dir = Path.home() / ".config" / "evo-client"
    config_file = config_dir / "credentials.json"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config = {}
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
    
    if branch_id:
        config[branch_id] = {"username": username, "password": password}
        rich_print(f"[green]✓[/green] Credentials saved for branch {branch_id}")
    else:
        config["default"] = {"username": username, "password": password}
        rich_print("[green]✓[/green] Default credentials saved")
    
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    config_file.chmod(0o600)

@auth_app.command("login-file")
def auth_login_file(
    config_path: Annotated[Path, typer.Argument(
        help="Path to JSON config file",
        exists=True,
        dir_okay=False,
        resolve_path=True
    )]
):
    """Login using a JSON configuration file."""
    try:
        with open(config_path) as f:
            source_config = json.load(f)
        
        config_dir = Path.home() / ".config" / "evo-client"
        config_file = config_dir / "credentials.json"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine if it's a single branch or multi-branch config
        if isinstance(source_config, dict) and all(isinstance(v, str) for v in source_config.values()):
            # Single branch config
            target_config = {"default": source_config}
            rich_print("[green]✓[/green] Loaded default credentials")
        else:
            # Multi-branch config
            target_config = source_config
            rich_print(f"[green]✓[/green] Loaded credentials for {len(target_config)} branches")
        
        with open(config_file, "w") as f:
            json.dump(target_config, f, indent=2)
        config_file.chmod(0o600)
        
        rich_print("[green]✓[/green] Configuration saved successfully")
        
    except json.JSONDecodeError:
        rich_print("[red]Error:[/red] Invalid JSON file format")
        raise typer.Exit(1)
    except KeyError as e:
        rich_print(f"[red]Error:[/red] Missing required field: {e}")
        raise typer.Exit(1)
    except Exception as e:
        rich_print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@auth_app.command("logout")
def auth_logout(
    branch_id: Annotated[Optional[str], typer.Option(
        "--branch-id", "-b",
        help="Branch ID to remove credentials for"
    )] = None,
    all: Annotated[bool, typer.Option(
        "--all",
        help="Remove all credentials",
        is_flag=True
    )] = False,
):
    """Remove saved credentials."""
    config_file = Path.home() / ".config" / "evo-client" / "credentials.json"
    
    if not config_file.exists():
        rich_print("[yellow]No credentials found[/yellow]")
        return
    
    if all:
        config_file.unlink()
        rich_print("[green]✓[/green] All credentials removed")
        return
    
    with open(config_file) as f:
        config = json.load(f)
    
    if branch_id:
        if branch_id in config:
            del config[branch_id]
            rich_print(f"[green]✓[/green] Credentials removed for branch {branch_id}")
        else:
            rich_print(f"[yellow]No credentials found for branch {branch_id}[/yellow]")
    else:
        if "default" in config:
            del config["default"]
            rich_print("[green]✓[/green] Default credentials removed")
        else:
            rich_print("[yellow]No default credentials found[/yellow]")
    
    if config:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    else:
        config_file.unlink()

@auth_app.command("list")
def auth_list():
    """List configured credentials."""
    config_file = Path.home() / ".config" / "evo-client" / "credentials.json"
    
    if not config_file.exists():
        rich_print("[yellow]No credentials configured[/yellow]")
        return
    
    with open(config_file) as f:
        config = json.load(f)
    
    table = Table(title="Configured Credentials")
    table.add_column("Branch ID", style="cyan")
    table.add_column("Username", style="green")
    table.add_column("Type", style="blue")
    
    for branch_id, creds in config.items():
        table.add_row(
            branch_id,
            creds["username"],
            "Default" if branch_id == "default" else "Branch"
        )
    
    console.print(table)

# Contract commands
@contracts_app.command("list")
@handle_api_errors
def list_plans():
    """List available membership contracts."""
    try:
        api_client = get_api_client()
        
        # Get contracts synchronously
        logger.debug("Fetching contracts...")
        contracts = api_client.membership_data_fetcher.fetch_memberships(
            active=True
        )
        
        # Process contracts
        active_contracts = []
        
        if isinstance(contracts, dict):
            contract_list = contracts.values()
        else:
            contract_list = contracts
            
        flattened_contracts = []
        for item in contract_list:
            if isinstance(item, list):
                flattened_contracts.extend(item)
            else:
                flattened_contracts.append(item)
        
        for contract in flattened_contracts:
            logger.debug(f"Found individual plan: {contract.name_membership} (Branch: {contract.id_branch})")
            
            # Skip inactive
            if contract.inactive:
                logger.debug(f"Plan {contract.name_membership} (ID: {contract.id_membership}, Branch: {contract.id_branch}): inactive=True")
                continue
            
            if contract.access_branches:
                logger.debug(f"  Branches: {[(b.id_branch, b.name) for b in contract.access_branches]}")
            
            active_contracts.append(contract)
        
        logger.debug(f"Found {len(active_contracts)} active plans")
        
        # Create and display table
        table = Table(title="Membership Contracts")
        table.add_column("ID", justify="right")
        table.add_column("Plan")
        table.add_column("Value", justify="right")
        table.add_column("Duration", justify="right")
        table.add_column("Multi", justify="center")
        table.add_column("Branch ID", justify="right", style="yellow")
        table.add_column("Branches")
        
        active_contracts.sort(key=lambda x: x.name_membership)
        
        for contract in active_contracts:
            if contract.duration_type == "Days":
                duration = f"{contract.duration}d"
            elif contract.duration_type == "Months":
                duration = f"{contract.duration}m"
            else:
                duration = "N/A"
            
            value = f"${contract.value:.2f}" if contract.value is not None else "N/A"
            
            branch_ids = []
            branch_names = []
            if contract.access_branches:
                for branch in contract.access_branches:
                    if branch.id_branch:
                        branch_ids.append(str(branch.id_branch))
                        branch_names.append(branch.name)
            
            branch_id_str = ", ".join(branch_ids) if branch_ids else "N/A"
            branch_names_str = ", ".join(branch_names) if branch_names else "N/A"
            
            is_multi = "Yes" if len(branch_ids) > 1 else "No"
            
            table.add_row(
                str(contract.id_membership),
                contract.name_membership,
                value,
                duration,
                is_multi,
                branch_id_str,
                branch_names_str
            )
        
        console.print(table)
        
    except Exception as e:
        logger.error(f"Error listing contracts: {str(e)}")
        console.print(Panel(f"Error listing contracts: {str(e)}", style="red"))

@finance_app.command("receivables")
@requires_auth
def list_receivables(
    member_id: MemberIdOption = None,
    branch_id: BranchIdOption = None,
    status: Optional[str] = typer.Option(
        None,
        "--status", "-s",
        help="Filter by status (PAID, PENDING, OVERDUE)"
    ),
    days: Optional[int] = 30
):
    """List payment receivables."""
    try:
        logger.info("Fetching receivables [member_id={}, branch_id={}, status={}, days={}]",
                    member_id, branch_id, status, days)
        days_value = days if days else 30
        from_date = datetime.now() - timedelta(days=days_value)
        to_date = datetime.now()
        
        account_status = None
        if status:
            try:
                status_enum = ReceivableStatus(status.lower())
                status_map = {
                    ReceivableStatus.PENDING: "1",
                    ReceivableStatus.PAID: "2",
                    ReceivableStatus.CANCELLED: "3",
                    ReceivableStatus.OVERDUE: "4",
                }
                account_status = status_map.get(status_enum)
            except ValueError:
                typer.echo(f"Invalid status: {status}. Must be one of: PAID, PENDING, OVERDUE", err=True)
                raise typer.Exit(1)
        
        logger.debug("Requesting receivables from API...")
        receivables_data = state.data_fetchers['receivables'].fetch_receivables(
            registration_date_start=from_date,
            registration_date_end=to_date,
            account_status=account_status,
            member_id=member_id
        )
        
        receivables = []
        for r in receivables_data:
            try:
                status_id = str(r.status.id) if r.status and r.status.id else "1"
                status_map = {
                    "1": ReceivableStatus.PENDING,
                    "2": ReceivableStatus.PAID,
                    "3": ReceivableStatus.CANCELLED,
                    "4": ReceivableStatus.OVERDUE,
                }
                receivable_status = status_map.get(status_id, ReceivableStatus.PENDING)
                
                # If you need to filter by branch and the receivable object has a branch attribute:
                # if branch_id and r.id_branch != branch_id:
                #     continue
                
                receivables.append({
                    'id': r.id_receivable,
                    'member_id': r.id_member_payer,
                    'member_name': r.payer_name,
                    'description': r.description,
                    'amount': r.ammount,
                    'amount_paid': r.ammount_paid,
                    'due_date': r.due_date,
                    'status': receivable_status,
                    'status_name': r.status.name if r.status else None
                })
            except AttributeError as e:
                logger.warning("Skipping malformed receivable: %s", str(e))
                continue
        
        if not receivables:
            logger.info("No receivables found matching the given criteria.")
            typer.echo("No receivables found for the given criteria.")
            return
        
        table = Table(show_header=True, box=box.ROUNDED)
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Member", style="blue")
        table.add_column("Description", style="green")
        table.add_column("Amount", style="magenta", justify="right")
        table.add_column("Paid", style="green", justify="right")
        table.add_column("Due Date", style="yellow")
        table.add_column("Status", style="bold")
        
        for receivable in receivables:
            status_style_map = {
                ReceivableStatus.PAID: "green",
                ReceivableStatus.PENDING: "yellow",
                ReceivableStatus.OVERDUE: "red",
                ReceivableStatus.CANCELLED: "dim"
            }
            amount_paid_str = f"${receivable['amount_paid']:.2f}" if receivable['amount_paid'] else "N/A"
            due_date_str = receivable['due_date'].strftime("%Y-%m-%d") if receivable['due_date'] else "N/A"
            status_style = status_style_map.get(receivable['status'], "white")
            
            table.add_row(
                str(receivable['id']),
                receivable['member_name'] or "N/A",
                receivable['description'] or "N/A",
                f"${receivable['amount']:.2f}",
                amount_paid_str,
                due_date_str,
                f"[{status_style}]{receivable['status'].value.upper()}[/]"
            )
        
        console.print(Panel(table, title=f"Receivables (Last {days} days)"))
        
    except Exception as e:
        logger.error("Error fetching receivables: {}", str(e))
        typer.echo(f"Error fetching receivables: {str(e)}", err=True)
        if state.verbose:
            import traceback
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())
        raise typer.Exit(1)

@finance_app.command("overdue")
@requires_auth
def list_overdue_members(
    branch_id: BranchOption = None,
    min_days: Annotated[int, typer.Option(
        "--min-days", "-d",
        help="Minimum days overdue",
        min=1,
        show_default=True
    )] = 1,
):
    """List members with overdue payments."""
    try:
        # Get overdue members for specific branch or all branches
        overdue = state.data_fetchers['receivables'].fetch_receivables(
            due_date_start=datetime.now() - timedelta(days=min_days),
            due_date_end=datetime.now(),
            payment_types="0"
        )
        
        # Filter by branch_id if specified
        if branch_id is not None:
            overdue = [r for r in overdue if 
                      (hasattr(r, 'id_branch') and r.id_branch == branch_id) or
                      (hasattr(r, 'branch') and r.branch and getattr(r.branch, 'id', None) == branch_id)]
            if not overdue:
                rich_print(f"[yellow]No overdue members found for branch {branch_id}[/yellow]")
                return
        
        if not overdue:
            rich_print("[yellow]No overdue members found[/yellow]")
            return
        
        table = Table(title=f"Overdue Members (Min {min_days} days)")
        table.add_column("Member ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Total Overdue", style="red")
        table.add_column("Overdue Since", style="yellow")
        table.add_column("# of Receivables", style="magenta")
        
        # Group receivables by member
        member_receivables = {}
        processed_receivables = set()  # Track processed receivable IDs

        for r in overdue:
            # Skip if no member ID or if receivable was already processed
            if not r.id_member_payer or r.id_receivable in processed_receivables:
                continue
            
            processed_receivables.add(r.id_receivable)
            
            if r.id_member_payer not in member_receivables:
                member_receivables[r.id_member_payer] = {
                    'member_id': r.id_member_payer,
                    'name': r.payer_name,
                    'total_overdue': Decimal('0'),
                    'overdue_since': None,
                    'receivables': set()  # Store unique receivable IDs
                }
            
            # Calculate remaining amount for this receivable
            amount = Decimal(str(r.ammount)) if r.ammount else Decimal('0')
            amount_paid = Decimal(str(r.ammount_paid)) if r.ammount_paid else Decimal('0')
            remaining_amount = amount - amount_paid
            
            # Only count if there's still an amount remaining
            if remaining_amount > Decimal('0'):
                member_receivables[r.id_member_payer]['total_overdue'] += remaining_amount
                member_receivables[r.id_member_payer]['receivables'].add(r.id_receivable)
                
                due_date = r.due_date
                if due_date and (not member_receivables[r.id_member_payer]['overdue_since'] or 
                               due_date < member_receivables[r.id_member_payer]['overdue_since']):
                    member_receivables[r.id_member_payer]['overdue_since'] = due_date

        # Add rows to table
        for member_data in member_receivables.values():
            if member_data['total_overdue'] > Decimal('0'):  # Only show members with actual overdue amounts
                table.add_row(
                    str(member_data['member_id']),
                    member_data['name'] or 'N/A',
                    f"${member_data['total_overdue']:.2f}",
                    member_data['overdue_since'].strftime("%Y-%m-%d") if member_data['overdue_since'] else 'N/A',
                    str(len(member_data['receivables']))
                )
        
        console.print(table)
        
        total_overdue = sum(m['total_overdue'] for m in member_receivables.values())
        console.print(f"\nTotal overdue amount: [red]${total_overdue:.2f}[/red]")
        console.print(f"Total members overdue: [yellow]{len(member_receivables)}[/yellow]")

    except Exception as e:
        logger.error("Error listing overdue members: {}", str(e))
        console.print(Panel.fit(
            f"[red]Error listing overdue members: {str(e)}[/]",
            border_style="red"
        ))
        if state.verbose:
            import traceback
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())

@app.callback()
def main(
    version: Annotated[Optional[bool], typer.Option(
        "--version",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True
    )] = None,
    verbose: Annotated[bool, typer.Option(
        "--verbose", "-v",
        help="Enable verbose output",
        callback=verbose_callback
    )] = False,
):
    """
    Gym Management CLI - A command-line interface for managing gym operations.
    
    Run 'gym auth login' to set up authentication before using other commands.
    """
    pass

if __name__ == "__main__":
    app()