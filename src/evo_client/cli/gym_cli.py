from typing import Optional, List, cast, Any, Annotated
import typer
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rich_print
from decimal import Decimal
from multiprocessing.pool import AsyncResult
import json
from pathlib import Path
from functools import wraps
import asyncio
from rich import box
from loguru import logger

from ..api.gym_api import GymApi, TypedAsyncResult
from ..api.receivables_api import ReceivablesApi
from ..core.configuration import Configuration
from ..core.api_client import ApiClient
from ..exceptions.api_exceptions import ApiException
from ..api.webhook_api import WebhookApi
from ..models.gym_model import (
    MembershipStatus,
    ReceivableStatus,
    OverdueMember,
    MembersFiles,
    MemberProfile,
)

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
        self.verbose: bool = False
    
    @property
    def api_client(self) -> GymApi:
        """Get the API client, initializing it if necessary."""
        if self._api_client is None:
            self._api_client = get_api_client()
        return self._api_client
    
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

def handle_async_result(result: Any) -> Any:
    """Handle potential async result."""
    if isinstance(result, (AsyncResult, TypedAsyncResult)):
        return result.get()
    return result

def requires_auth(f):
    """Decorator to ensure authentication is set up."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # The api_client property will initialize the client if needed
        return f(*args, **kwargs)
    return wrapper

def get_api_client() -> GymApi:
    """Get or initialize the API client."""
    config_dir = Path.home() / ".config" / "evo-client"
    config_file = config_dir / "credentials.json"
    
    if not config_file.exists():
        rich_print(Panel(
            "[red]No credentials found[/red]\nRun [green]gym auth login[/green] to set up authentication",
            title="Authentication Required"
        ))
        raise typer.Exit(1)
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        
        if "default" in config:
            # Single branch configuration
            creds = config["default"]
            configuration = Configuration()
            configuration.username = creds["username"]
            configuration.password = creds["password"]
            return GymApi(api_client=ApiClient(configuration=configuration))
        else:
            # Multi-branch configuration
            branch_credentials = []
            for branch_id, creds in config.items():
                branch_credentials.append({
                    "username": creds["username"],
                    "password": creds["password"],
                    "branch_id": branch_id
                })
            return GymApi(branch_credentials=branch_credentials)
    except Exception as e:
        rich_print(Panel(
            f"[red]Error loading credentials:[/red]\n{str(e)}",
            title="Authentication Error"
        ))
        raise typer.Exit(1)

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
    """Login using a JSON configuration file.
    
    The JSON file should have one of these formats:
    
    Single branch:
    {
        "username": "your-username",
        "password": "your-password"
    }
    
    Multi-branch:
    {
        "branch-id-1": {
            "username": "username-1",
            "password": "password-1"
        },
        "branch-id-2": {
            "username": "username-2",
            "password": "password-2"
        }
    }
    """
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
@requires_auth
def list_contracts(
    branch_id: BranchOption = None,
    member_id: Annotated[Optional[int], typer.Option(
        "--member-id", "-m",
        help="Filter by member ID"
    )] = None,
    active_only: Annotated[bool, typer.Option(
        "--active-only/--all",
        help="Show only active contracts",
        show_default=True
    )] = True,
):
    """List membership contracts."""
    try:
        contracts = state.api_client.get_contracts(
            member_id=member_id,
            branch_id=branch_id,
            active_only=active_only
        )

        console.print(Panel.fit("[bold blue]Membership Contracts[/]", border_style="blue"))
        
        table = Table(show_header=True, box=box.ROUNDED)
        table.add_column("Contract ID", style="cyan", justify="right")
        table.add_column("Member ID", style="blue", justify="right")
        table.add_column("Plan", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Monthly Value", style="magenta", justify="right")
        table.add_column("Duration", style="cyan", justify="right")
        table.add_column("Multi-Unit", style="blue")

        for contract in contracts:
            status_style = "green" if contract.status == MembershipStatus.ACTIVE else "red"
            multi_unit = "✓" if contract.plan.multi_unit_access else "✗"
            multi_unit_style = "green" if contract.plan.multi_unit_access else "red"
            
            table.add_row(
                str(contract.id),
                str(contract.member_id),
                contract.plan.name,
                f"[{status_style}]{contract.status.value if contract.status else 'N/A'}[/]",
                f"${contract.plan.price:.2f}",
                f"{contract.plan.minimum_commitment_months}m",
                f"[{multi_unit_style}]{multi_unit}[/]"
            )

        console.print(table)

    except Exception as e:
        console.print(Panel.fit(
            f"[red]Error listing contracts: {str(e)}[/]",
            border_style="red"
        ))

# Finance commands
@finance_app.command("operating-data")
@requires_auth
def get_operating_data(
    branch_id: BranchIdOption = None,
    days: Optional[int] = 30,
):
    """Get comprehensive operating data including metrics, receivables, and entries."""
    try:
        logger.info("Fetching operating data [branch_id={}, days={}]", branch_id, days)
        logger.debug("Using branch_ids: {}", [str(branch_id)] if branch_id else None)
        
        start_time = datetime.now()
        
        # Show progress message
        with console.status("[yellow]Fetching data...[/yellow]", spinner="dots") as status:
            try:
                # Get operating data in sync mode
                data = state.api_client.get_operating_data(
                    branch_ids=[str(branch_id)] if branch_id else None,
                    days=days,
                    async_req=False
                )
                
                elapsed_time = (datetime.now() - start_time).total_seconds()
                logger.debug("Data fetched in {:.2f}s", elapsed_time)
                
                console.print(f"Data fetched in {elapsed_time:.2f}s")
                
                # Show summary of data
                table = Table(title="Operating Data Summary", box=box.ROUNDED)
                table.add_column("Metric", style="blue")
                table.add_column("Value", style="green", justify="right")
                
                # Handle single branch or multi-branch response
                if isinstance(data, list):
                    # Multiple branches - aggregate data
                    metrics = {
                        'Active Clients': sum(len(d.active_members) for d in data),
                        'Active Contracts': sum(len(d.active_contracts) for d in data),
                        'Prospects': sum(len(d.prospects) for d in data),
                        'Non-renewed Clients': sum(len(d.non_renewed_members) for d in data),
                        'Total Receivables': sum(len(d.receivables) for d in data),
                        'Total Entries': sum(len(d.recent_entries) for d in data),
                        'Monthly Revenue': sum(d.mrr for d in data),
                        'Churn Rate': sum(d.churn_rate for d in data) / len(data) if data else 0,
                    }
                else:
                    # Single branch
                    metrics = {
                        'Active Clients': len(data.active_members),
                        'Active Contracts': len(data.active_contracts),
                        'Prospects': len(data.prospects),
                        'Non-renewed Clients': len(data.non_renewed_members),
                        'Total Receivables': len(data.receivables),
                        'Total Entries': len(data.recent_entries),
                        'Monthly Revenue': data.mrr,
                        'Churn Rate': data.churn_rate,
                    }
                
                # Add metrics to table with formatting
                for metric, value in metrics.items():
                    if metric in ['Monthly Revenue']:
                        formatted_value = f"${value:.2f}"
                    elif metric in ['Churn Rate']:
                        formatted_value = f"{value:.1f}%"
                    else:
                        formatted_value = str(value)
                    table.add_row(metric, formatted_value)
                
                console.print(table)
                
            except ApiException as e:
                if e.status == 404:
                    logger.warning("Branch not found or no data available")
                    console.print("[yellow]No data available for the specified branch[/yellow]")
                    
                    # Still show empty table
                    table = Table(title="Operating Data Summary", box=box.ROUNDED)
                    table.add_column("Metric", style="blue")
                    table.add_column("Value", style="green", justify="right")
                    
                    metrics = {
                        'Active Clients': 0,
                        'Active Contracts': 0,
                        'Prospects': 0,
                        'Non-renewed Clients': 0,
                        'Total Receivables': 0,
                        'Total Entries': 0,
                    }
                    
                    for metric, value in metrics.items():
                        table.add_row(metric, str(value))
                    
                    console.print(table)
                else:
                    raise e

    except Exception as e:
        logger.error("Error fetching operating data: {}", str(e))
        console.print(Panel.fit(
            f"[red]Error getting operating data: {str(e)}[/]",
            border_style="red"
        ))
        if state.verbose:
            import traceback
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())
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
        days_value = days if days is not None else 30
        from_date = datetime.now() - timedelta(days=days_value)
        to_date = datetime.now()
        
        # Convert status string to enum if provided
        status_enum = None
        account_status = None
        if status:
            try:
                status_enum = ReceivableStatus(status.lower())
                # Map status enum to API status codes
                status_map = {
                    ReceivableStatus.PENDING: "1",  # Opened
                    ReceivableStatus.PAID: "2",     # Received
                    ReceivableStatus.CANCELLED: "3", # Canceled
                    ReceivableStatus.OVERDUE: "4",   # Overdue
                }
                account_status = status_map.get(status_enum)
                logger.debug("Status converted: {} -> {} (API status: {})", 
                           status, status_enum, account_status)
            except ValueError:
                logger.error("Invalid status value provided: {}", status)
                typer.echo(f"Invalid status: {status}. Must be one of: PAID, PENDING, OVERDUE", err=True)
                raise typer.Exit(1)
        
        # Convert branch_id to string and create list if provided
        branch_ids: Optional[List[str]] = [str(branch_id)] if branch_id is not None else None
        logger.debug("Using branch_ids: {}", branch_ids)
        
        start_time = datetime.now()
        logger.debug("Starting API call to get_operating_data")
        
        # Get receivables directly using the receivables API
        receivables_api = ReceivablesApi(state.api_client.default_api_client)
        result = receivables_api.get_receivables(
            registration_date_start=from_date,
            registration_date_end=to_date,
            account_status=account_status,
            member_id=member_id,
            async_req=True
        )
        
        api_time = datetime.now()
        logger.debug("API call completed in {}s, handling async result", 
                    (api_time - start_time).total_seconds())
        
        receivables_data = handle_async_result(result)
        handle_time = datetime.now()
        logger.debug("Async result handled in {}s", 
                    (handle_time - api_time).total_seconds())
        
        # Convert API response to list of receivables
        receivables = []
        for r in receivables_data:
            try:
                # Map status ID to enum
                status_id = str(r.status.id) if r.status and r.status.id else "1"
                status_map = {
                    "1": ReceivableStatus.PENDING,  # Opened
                    "2": ReceivableStatus.PAID,     # Received
                    "3": ReceivableStatus.CANCELLED, # Canceled
                    "4": ReceivableStatus.OVERDUE,   # Overdue
                }
                status = status_map.get(status_id, ReceivableStatus.PENDING)
                
                receivables.append({
                    'id': r.id_receivable,
                    'member_id': r.id_member_payer,
                    'member_name': r.payer_name,
                    'description': r.description,
                    'amount': r.ammount,
                    'amount_paid': r.ammount_paid,
                    'due_date': r.due_date,
                    'status': status,
                    'status_name': r.status.name if r.status else None
                })
                logger.debug("Processed receivable: id={}, status={}, status_name={}", 
                           r.id_receivable, status, r.status.name if r.status else None)
            except AttributeError as e:
                logger.warning("Skipping malformed receivable {}: {}", 
                             getattr(r, 'id_receivable', 'unknown'), str(e))
                continue
        
        logger.debug("Found {} total receivables in {}s total", 
                    len(receivables), 
                    (datetime.now() - start_time).total_seconds())
            
        if not receivables:
            logger.info("No receivables found matching criteria")
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
            # Format status with color
            status_style = {
                ReceivableStatus.PAID: "green",
                ReceivableStatus.PENDING: "yellow",
                ReceivableStatus.OVERDUE: "red",
                ReceivableStatus.CANCELLED: "dim"
            }.get(receivable['status'], "white")
            
            # Format amount paid
            amount_paid = f"${receivable['amount_paid']:.2f}" if receivable['amount_paid'] else "N/A"
            
            # Format due date
            due_date = receivable['due_date'].strftime("%Y-%m-%d") if receivable['due_date'] else "N/A"
            
            table.add_row(
                str(receivable['id']),
                receivable['member_name'] or "N/A",
                receivable['description'] or "N/A",
                f"${receivable['amount']:.2f}",
                amount_paid,
                due_date,
                f"[{status_style}]{receivable['status'].value.upper()}[/]"
            )
        
        console.print(Panel(table, title=f"Receivables (Last {days} days)"))
        
    except Exception as e:
        typer.echo(f"Error fetching receivables: {str(e)}", err=True)
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
    result = state.api_client.get_overdue_members(
        branch_id=branch_id,
        min_days_overdue=min_days
    )
    overdue = cast(List[OverdueMember], handle_async_result(result))
    
    table = Table(title=f"Overdue Members (Min {min_days} days)")
    table.add_column("Member ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Total Overdue", style="red")
    table.add_column("Overdue Since", style="yellow")
    table.add_column("# of Receivables", style="blue")
    
    for member in overdue:
        table.add_row(
            str(getattr(member, 'member_id', 'N/A')),
            getattr(member, 'name', 'Unknown'),
            f"${getattr(member, 'total_overdue', Decimal('0')):.2f}",
            getattr(member, 'overdue_since', datetime.now()).strftime("%Y-%m-%d"),
            str(len(getattr(member, 'overdue_receivables', [])))
        )
    
    console.print(table)

# Member commands
@members_app.command("info")
@requires_auth
def get_member_files(
    member_ids: Annotated[List[int], typer.Argument(
        help="List of member IDs to fetch data for"
    )],
    branch_ids: BranchesOption = None,
    days: Optional[int] = 30,
):
    """Get detailed member information and history."""
    days_value = days if days is not None else 30
    from_date = datetime.now() - timedelta(days=days_value)
    result = state.api_client.get_members_files(
        member_ids=member_ids,
        branch_ids=branch_ids,
        from_date=from_date
    )
    members_files = cast(MembersFiles, handle_async_result(result))
    
    profiles = getattr(members_files, 'profiles', [])
    profiles = cast(List[MemberProfile], profiles)
    
    for profile in profiles:
        # Member info panel
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Field", style="blue")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("ID", str(getattr(profile, 'member_id', 'N/A')))
        info_table.add_row("Name", getattr(profile, 'name', 'Unknown'))
        info_table.add_row("Email", getattr(profile, 'email', 'N/A'))
        info_table.add_row("Phone", getattr(profile, 'phone', 'N/A'))
        
        console.print(Panel(info_table, title="Member Profile"))
        
        # Contract info
        current_contract = getattr(profile, 'current_contract', None)
        if current_contract:
            contract_table = Table(show_header=False, box=None)
            contract_table.add_column("Field", style="blue")
            contract_table.add_column("Value", style="green")
            
            plan_name = getattr(current_contract.plan, 'name', 'N/A') if current_contract.plan else 'N/A'
            contract_table.add_row("Plan", plan_name)
            contract_table.add_row("Value", f"${getattr(current_contract, 'value', Decimal('0')):.2f}")
            contract_table.add_row(
                "Status",
                current_contract.status.value if current_contract.status else 'N/A'
            )
            
            console.print(Panel(contract_table, title="Current Contract"))
        
        # Financial summary
        finance_table = Table(show_header=False, box=None)
        finance_table.add_column("Metric", style="blue")
        finance_table.add_column("Amount", style="green")
        
        finance_table.add_row(
            "Total Paid",
            f"${getattr(profile, 'total_paid', Decimal('0')):.2f}"
        )
        finance_table.add_row(
            "Pending Payments",
            f"${getattr(profile, 'pending_payments', Decimal('0')):.2f}"
        )
        finance_table.add_row(
            "Overdue Payments",
            f"${getattr(profile, 'overdue_payments', Decimal('0')):.2f}"
        )
        
        console.print(Panel(finance_table, title="Financial Summary"))
        
        # Activity summary
        activity_table = Table(show_header=False, box=None)
        activity_table.add_column("Metric", style="blue")
        activity_table.add_column("Value", style="green")
        
        activity_table.add_row(
            "Total Entries",
            str(getattr(profile, 'total_entries', 0))
        )
        activity_table.add_row(
            "Classes Attended",
            str(getattr(profile, 'total_classes_attended', 0))
        )
        
        favorite_activities = getattr(profile, 'favorite_activities', [])
        if favorite_activities:
            activity_table.add_row(
                "Favorite Activities",
                ", ".join(favorite_activities)
            )
        
        console.print(Panel(activity_table, title="Activity Summary"))
        console.print("─" * 80)  # Separator between members

# Webhook commands
def run_async(coro):
    """Run an async function in the event loop."""
    return asyncio.get_event_loop().run_until_complete(coro)

@webhooks_app.command("manage")
@requires_auth
def manage_webhooks(
    url: Annotated[str, typer.Argument(help="Webhook callback URL")],
    event_types: Annotated[Optional[List[str]], typer.Option(
        "--events", "-e",
        help="Event types to subscribe to (e.g. NewSale, CreateMember, etc.)"
    )] = None,
    branch_ids: BranchesOption = None,
    unsubscribe: Annotated[bool, typer.Option(
        "--unsubscribe",
        help="Unsubscribe from webhooks instead of subscribing",
        is_flag=True
    )] = False,
):
    """Manage webhook subscriptions."""
    result = run_async(state.api_client.manage_webhooks(
        url_callback=url,
        event_types=event_types,
        branch_ids=branch_ids,
        unsubscribe=unsubscribe
    ))
    
    if result:
        rich_print(f"[green]✓[/green] Successfully {'unsubscribed from' if unsubscribe else 'subscribed to'} webhooks")
    else:
        rich_print("[red]✗[/red] Failed to manage webhooks")
        raise typer.Exit(1)

@webhooks_app.command("list")
@requires_auth
def list_webhooks(
    branch_id: BranchOption = None,
):
    """List all webhook subscriptions."""
    try:
        # Get branch-specific API client if branch_id is provided
        if branch_id is not None:
            branch_id_str = str(branch_id)
            if branch_id_str in state.api_client.branch_api_clients:
                # Create a new configuration for the branch
                branch_config = Configuration()
                branch_config.host = state.api_client.branch_api_clients[branch_id_str].configuration.host
                branch_config.username = state.api_client.branch_api_clients[branch_id_str].configuration.username
                branch_config.password = state.api_client.branch_api_clients[branch_id_str].configuration.password
                branch_config.base_path = "/api/v1"  # Ensure we're using v1
                
                # Create a new API client with the branch configuration
                branch_api_client = ApiClient(configuration=branch_config)
                webhook_api = WebhookApi(branch_api_client)
                
                logger.debug(f"Using branch-specific client for branch {branch_id}")
                logger.debug(f"Host: {branch_config.host}")
                logger.debug(f"Username: {branch_config.username}")
                logger.debug(f"Base path: {branch_config.base_path}")
            else:
                rich_print(f"[yellow]Warning:[/yellow] No credentials found for branch {branch_id}, using default client")
                webhook_api = WebhookApi(state.api_client.default_api_client)
        else:
            webhook_api = WebhookApi(state.api_client.default_api_client)

        result = webhook_api.get_webhooks()
        webhooks = handle_async_result(result)
        
        if not webhooks:
            rich_print("[yellow]No webhooks found[/yellow]")
            return

        # Group webhooks by URL and event type for better organization
        webhooks_by_url = {}
        for webhook in webhooks:
            webhook_id = webhook.get('idWebhook') or webhook.get('id')
            webhook_branch_id = webhook.get('idFilial') or webhook.get('idBranch')
            webhook_event = webhook.get('tipoEvento') or webhook.get('eventType')
            webhook_url = webhook.get('urlCallback')
            webhook_deleted = webhook.get('flExcluido', False)
            webhook_date = webhook.get('dataCriacao')
            
            if not webhook_deleted and (branch_id is None or webhook_branch_id == branch_id):
                if webhook_url not in webhooks_by_url:
                    webhooks_by_url[webhook_url] = {}
                if webhook_event not in webhooks_by_url[webhook_url]:
                    webhooks_by_url[webhook_url][webhook_event] = []
                webhooks_by_url[webhook_url][webhook_event].append({
                    'id': webhook_id,
                    'branch': webhook_branch_id,
                    'date': webhook_date
                })

        # Display webhooks grouped by URL and event type
        for url, events in webhooks_by_url.items():
            console.print(f"\n[bold blue]URL:[/bold blue] {url}")
            
            table = Table(show_header=True)
            table.add_column("Event Type", style="green")
            table.add_column("Webhook IDs", style="cyan")
            table.add_column("Branch", style="blue")
            table.add_column("Created", style="yellow")
            
            for event_type, webhooks in sorted(events.items()):
                # Sort webhooks by ID
                webhooks.sort(key=lambda x: x['id'] if x['id'] is not None else 0)
                
                # Format webhook IDs as a comma-separated list
                webhook_ids = ", ".join(str(w['id']) for w in webhooks if w['id'] is not None)
                
                # Get branch ID
                branch = str(webhooks[0]['branch']) if webhooks[0]['branch'] is not None else 'N/A'
                
                # Get the most recent creation date
                latest_date = max((w['date'] for w in webhooks if w['date']), default=None)
                if latest_date:
                    try:
                        from datetime import datetime
                        date_obj = datetime.fromisoformat(latest_date.replace('Z', '+00:00'))
                        date_str = date_obj.strftime("%Y-%m-%d %H:%M")
                    except:
                        date_str = latest_date
                else:
                    date_str = "N/A"
                
                table.add_row(
                    event_type or 'N/A',
                    webhook_ids,
                    branch,
                    date_str
                )
            
            console.print(table)

    except Exception as e:
        rich_print(f"[red]Error listing webhooks:[/red] {str(e)}")
        if state.verbose:
            import traceback
            rich_print("[red]Traceback:[/red]")
            rich_print(traceback.format_exc())
        raise typer.Exit(1)

# Main app options
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