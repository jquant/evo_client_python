# EVO API
Use the DNS of your gym as the User and the Secret Key as the password. The authentication method used in the integration is Basic Authentication.

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: v1
- Package version: 1.0.0
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen

## Requirements

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/jquant/evo_client_python
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/jquant/evo_client_python`)

Then import the package:
```python
import evo_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import evo_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import evo_client
from evo_client.exceptions.api_exceptions import ApiException
from pprint import pprint
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
search = '' # str | Filter by activity name, group name or tags (optional)
branch_id = 56 # int | Filber by membership IdBranch (Only available when using a multilocation key, ignored otherwise) (optional)
take = 10 # int | Total number of records to return. (optional) (default to 10)
skip = 0 # int | Total number of records to skip. (optional) (default to 0)

try:
    # Get activities
    api_response = api_instance.get_activities(search=search, branch_id=branch_id, take=take, skip=skip)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_activities: %s\n" % e)
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
config_id = 56 # int | Activity IdConfiguration (Must be use combined with activityDate) (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (Must be use combined with idConfiguration) (optional)
session_id = 56 # int | Activity idActivitySession (This is mandatory if IdConfiguration and activityDate are null) (optional)

try:
    # Get activities schedule details
    api_response = api_instance.get_activities_schedule_detail(config_id=config_id, activity_date=activity_date, session_id=session_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_activities_schedule_detail: %s\n" % e)
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
config_id = 56 # int | Activity IdConfiguration (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (optional)
slot_number = 0 # int | Slot number (only available in activites that allow spot booking) (optional) (default to 0)
member_id = 0 # int | Id Member (this is required if IdProspect is null) (optional) (default to 0)
prospect_id = 0 # int | Id Member (this is required if IdMember is null) (optional) (default to 0)
origin = evo_client.EOrigemAgendamento() # EOrigemAgendamento |  (optional)

try:
    # Enroll member in activity schedule
    api_instance.enroll(config_id=config_id, activity_date=activity_date, slot_number=slot_number, member_id=member_id, prospect_id=prospect_id, origin=origin)
except ApiException as e:
    print("Exception when calling ActivitiesApi->enroll: %s\n" % e)
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
member_id = 0 # int | Filter by a member (optional) (default to 0)
take = 56 # int | Limit the ammount of itens returned (optional)
only_availables = false # bool | Filter by activities that are available (optional) (default to false)
_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by a specific date (optional)
show_full_week = false # bool | Show all activities in the week (Sunday to Saturday) (optional) (default to false)
branch_id = 56 # int | Filter by a different branch than the current one (optional)
activity_ids = 'id_activities_example' # str | Filter by a activities ids. Inform a comma separated list Ex.: \"1,2,3\" (optional)
audience_ids = 'id_audiences_example' # str | Filter by a audiences ids. Inform a comma separated list Ex.: \"1,2,3\" (optional)
id_branch_token = 'id_branch_token_example' # str | Filter by a different branch than the current one (optional)

try:
    # Get activities schedule
    api_response = api_instance.get_schedule(member_id=member_id, take=take, only_availables=only_availables, _date=_date, show_full_week=show_full_week, branch_id=branch_id, activity_ids=activity_ids, audience_ids=audience_ids, branch_token=branch_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_schedule: %s\n" % e)
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
prospect_id = 56 # int | IdProspect of who will participate from class (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date and time (yyyy-MM-dd HH:mm) (optional)
activity = 'activity_example' # str | Activity name (optional)
service = 'service_example' # str | Service that will be sold to allow the trial class (optional)
activity_exists = false # bool |  (optional) (default to false)
branch_id = 56 # int |  (optional)

try:
    # Create a new experimental class and enroll the member on it
    api_instance.create_experimental_class(prospect_id=prospect_id, activity_date=activity_date, activity=activity, service=service, activity_exists=activity_exists, branch_id=branch_id)
except ApiException as e:
    print("Exception when calling ActivitiesApi->create_experimental_class: %s\n" % e)
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
status = evo_client.EStatusAtividadeSessao() # EStatusAtividadeSessao | New status to be setted (Types: Attending = 0, Absent = 1, Justified absence = 2) (optional)
member_id = 56 # int | Id Member (optional)
prospect_id = 56 # int | Id Prospect (optional)
config_id = 56 # int | Activity IdConfiguration - only used when idActivitySession is null) (optional)
activity_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) - only used when idActivitySession is null) (optional)
session_id = 56 # int | IdActivity Session (optional)

try:
    # Change status of a member in activity schedule
    api_instance.change_status(status=status, member_id=member_id, prospect_id=prospect_id, config_id=config_id, activity_date=activity_date, session_id=session_id)
except ApiException as e:
    print("Exception when calling ActivitiesApi->change_status: %s\n" % e)
# Configure HTTP basic authorization: Basic
configuration = evo_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = evo_client.ActivitiesApi(evo_client.ApiClient(configuration))
config_id = 56 # int | Activity IdConfiguration (optional)
_date = '2013-10-20T19:20:30+01:00' # datetime | Activity schedule date (yyyy-MM-dd) (optional)

try:
    # List of spots that are already filled in the activity session
    api_instance.get_unavailable_spots(config_id=config_id, _date=_date)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_unavailable_spots: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://evo-integracao-api.w12app.com.br*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ActivitiesApi* | [**get_activities**](docs/ActivitiesApi.md#get_activities) | **GET** /api/v1/activities | Get activities
*ActivitiesApi* | [**get_schedule_detail**](docs/ActivitiesApi.md#get_schedule_detail) | **GET** /api/v1/activities/schedule/detail | Get activities schedule details
*ActivitiesApi* | [**enroll**](docs/ActivitiesApi.md#enroll) | **POST** /api/v1/activities/schedule/enroll | Enroll member in activity schedule
*ActivitiesApi* | [**get_schedule**](docs/ActivitiesApi.md#get_schedule) | **GET** /api/v1/activities/schedule | Get activities schedule
*ActivitiesApi* | [**create_experimental_class**](docs/ActivitiesApi.md#create_experimental_class) | **POST** /api/v1/activities/schedule/experimental-class | Create a new experimental class and enroll the member on it
*ActivitiesApi* | [**change_status**](docs/ActivitiesApi.md#change_status) | **POST** /api/v1/activities/schedule/enroll/change-status | Change status of a member in activity schedule
*ActivitiesApi* | [**get_unavailable_spots**](docs/ActivitiesApi.md#get_unavailable_spots) | **GET** /api/v1/activities/list-unavailable-spots | List of spots that are already filled in the activity session
*BankAccountsApi* | [**get_accounts**](docs/BankAccountsApi.md#get_accounts) | **GET** /api/v1/bank-accounts | Get bank accounts
*ConfigurationApi* | [**get_gateway_config**](docs/ConfigurationApi.md#get_gateway_config) | **GET** /api/v1/configuration/gateway | Get gateway configurations
*ConfigurationApi* | [**get_branch_config**](docs/ConfigurationApi.md#get_branch_config) | **GET** /api/v1/configuration | Get branch configurations
*ConfigurationApi* | [**get_occupations**](docs/ConfigurationApi.md#get_occupations) | **GET** /api/v1/configuration/occupation | Get Occupation
*ConfigurationApi* | [**get_card_flags**](docs/ConfigurationApi.md#get_card_flags) | **GET** /api/v1/configuration/card-flags | Get card flag
*ConfigurationApi* | [**get_translations**](docs/ConfigurationApi.md#get_translations) | **GET** /api/v1/configuration/card-translation | Get card translation
*EmployeesApi* | [**delete_employee**](docs/EmployeesApi.md#delete_employee) | **DELETE** /api/v1/employees | Delete Employees
*EmployeesApi* | [**get_employees**](docs/EmployeesApi.md#get_employees) | **GET** /api/v1/employees | Get Employees
*EmployeesApi* | [**update_employee**](docs/EmployeesApi.md#update_employee) | **POST** /api/v1/employees | Update Employees
*EmployeesApi* | [**create_employee**](docs/EmployeesApi.md#create_employee) | **PUT** /api/v1/employees | Add Employees
*EntriesApi* | [**get_entries**](docs/EntriesApi.md#get_entries) | **GET** /api/v1/entries | Get Entries
*InvoicesApi* | [**get_invoices**](docs/InvoicesApi.md#get_invoices) | **GET** /api/v1/invoices/get-invoices | Get invoices by date
*ManagmentApi* | [**get_active_clients**](docs/ManagmentApi.md#get_active_clients) | **GET** /api/v1/managment/activeclients | Get active Clients
*ManagmentApi* | [**get_prospects**](docs/ManagmentApi.md#get_prospects) | **GET** /api/v1/managment/prospects | Get Prospects
*ManagmentApi* | [**renewed_get**](docs/ManagmentApi.md#renewed_get) | **GET** /api/v1/managment/not-renewed | Get non-renewed Clients
*MemberMembershipApi* | [**cancel_membership**](docs/MemberMembershipApi.md#cancel_membership) | **POST** /api/v1/membermembership/cancellation | Cancel MemberMembership
*MemberMembershipApi* | [**get_membership**](docs/MemberMembershipApi.md#get_membership) | **GET** /api/v1/membermembership/{idMemberMembership} | Get summary of MemberMemberships by id
*MemberMembershipApi* | [**get_canceled_member_memberships**](docs/MemberMembershipApi.md#get_canceled_member_memberships) | **GET** /api/v2/membermembership | Get summary of canceled MemberMemberships
*MembersApi* | [**authenticate_member**](docs/MembersApi.md#authenticate_member) | **POST** /api/v1/members/auth | Authenticate member
*MembersApi* | [**get_basic_info**](docs/MembersApi.md#get_basic_info) | **GET** /api/v1/members/basic | Get basic member information. This endpoint does not return sensitive information. To return a member it is necessary to search by e-mail or document or phone or idsMembers.
*MembersApi* | [**get_fitcoins**](docs/MembersApi.md#get_fitcoins) | **GET** /api/v1/members/fitcoins | Get member fitcoins
*MembersApi* | [**update_fitcoins**](docs/MembersApi.md#update_fitcoins) | **PUT** /api/v1/members/fitcoins | Update a member fitcoins
*MembersApi* | [**get_members**](docs/MembersApi.md#get_members) | **GET** /api/v1/members | Get members
*MembersApi* | [**update_member_card**](docs/MembersApi.md#update_member_card) | **PUT** /api/v1/members/{idMember}/card | Update a member card number
*MembersApi* | [**get_member_profile**](docs/MembersApi.md#get_member_profile) | **GET** /api/v1/members/{idMember} | Get member profile
*MembersApi* | [**reset_password**](docs/MembersApi.md#reset_password) | **GET** /api/v1/members/resetPassword | Get link for reset password
*MembersApi* | [**get_member_services**](docs/MembersApi.md#get_member_services) | **GET** /api/v1/members/services | Get member services
*MembersApi* | [**transfer_member**](docs/MembersApi.md#transfer_member) | **POST** /api/v1/members/transfer | 
*MembersApi* | [**update_member_data**](docs/MembersApi.md#update_member_data) | **PATCH** /api/v1/members/update-member-data/{idMember} | Update basic member data
*MembershipApi* | [**get_categories**](docs/MembershipApi.md#get_categories) | **GET** /api/v1/membership/category | Get Memberships Categories
*MembershipApi* | [**get_memberships**](docs/MembershipApi.md#get_memberships) | **GET** /api/v1/membership | Get Memberships
*NotificationsApi* | [**create_notification**](docs/NotificationsApi.md#create_notification) | **POST** /api/v1/notifications | Insert a member notification
*PartnershipApi* | [**get_partnerships**](docs/PartnershipApi.md#get_partnerships) | **GET** /api/v1/partnership | Get partnerships
*PayablesApi* | [**get_cost_center**](docs/PayablesApi.md#get_cost_center) | **GET** /api/v1/costcenter | Get Cost Center
*PayablesApi* | [**get_payables**](docs/PayablesApi.md#get_payables) | **GET** /api/v1/payables | Get payables
*PixApi* | [**get_qr_code**](docs/PixApi.md#get_qr_code) | **GET** /api/v1/pix/qr-code | Get Qr-code
*ProspectsApi* | [**get_prospects**](docs/ProspectsApi.md#get_prospects) | **GET** /api/v1/prospects | Get prospects
*ProspectsApi* | [**create_prospect**](docs/ProspectsApi.md#create_prospect) | **POST** /api/v1/prospects | Add prospects
*ProspectsApi* | [**update_prospect**](docs/ProspectsApi.md#update_prospect) | **PUT** /api/v1/prospects | Update prospect
*ProspectsApi* | [**get_services**](docs/ProspectsApi.md#get_services) | **GET** /api/v1/prospects/services | Get prospect services
*ProspectsApi* | [**transfer_prospect**](docs/ProspectsApi.md#transfer_prospect) | **POST** /api/v1/prospects/transfer | 
*ReceivablesApi* | [**get_receivables**](docs/ReceivablesApi.md#get_receivables) | **GET** /api/v1/receivables | Get receivables
*ReceivablesApi* | [**get_revenue_center**](docs/ReceivablesApi.md#get_revenue_center) | **GET** /api/v1/revenuecenter | Get Cost Center
*ReceivablesApi* | [**mark_received**](docs/ReceivablesApi.md#mark_received) | **PUT** /api/v1/receivables/mark-received | 
*SalesApi* | [**get_sale_by_id**](docs/SalesApi.md#get_sale_by_id) | **GET** /api/v1/sales/{idSale} | Get sale by Id
*SalesApi* | [**create_sale**](docs/SalesApi.md#create_sale) | **POST** /api/v1/sales | Create a new sale
*SalesApi* | [**get_sales**](docs/SalesApi.md#get_sales) | **GET** /api/v2/sales | Get sales
*SalesApi* | [**get_sales_items**](docs/SalesApi.md#get_sales_items) | **GET** /api/v1/sales/sales-items | Return itens for sale -&gt; site/totem
*SalesApi* | [**get_sales_by_session_id**](docs/SalesApi.md#get_sales_by_session_id) | **GET** /api/v1/sales/by-session-id | Get sales
*ServiceApi* | [**get_services**](docs/ServiceApi.md#get_services) | **GET** /api/v1/service | Get Services
*StatesApi* | [**get_states**](docs/StatesApi.md#get_states) | **GET** /api/v1/states | 
*VoucherApi* | [**get_vouchers**](docs/VoucherApi.md#get_vouchers) | **GET** /api/v1/voucher | Get Vouchers
*WebhookApi* | [**delete_webhook**](docs/WebhookApi.md#delete_webhook) | **DELETE** /api/v1/webhook | Remove a specific webhook by id
*WebhookApi* | [**get_webhooks**](docs/WebhookApi.md#get_webhooks) | **GET** /api/v1/webhook | List all webhooks created
*WebhookApi* | [**create_webhook**](docs/WebhookApi.md#create_webhook) | **POST** /api/v1/webhook | Add new webhook
*WorkoutApi* | [**update_workout**](docs/WorkoutApi.md#update_workout) | **PUT** /api/v1/workout | Change data from a client&#x27;s prescribed workout
*WorkoutApi* | [**get_client_workouts**](docs/WorkoutApi.md#get_client_workouts) | **GET** /api/v1/workout/default-client-workout | Get All Client&#x27;s or Prospect&#x27;s or Employee&#x27;s workouts
*WorkoutApi* | [**get_workouts_by_month_year_professor**](docs/WorkoutApi.md#get_workouts_by_month_year_professor) | **GET** /api/v1/workout/workout-monthyear-professor | Get All Client&#x27;s or Prospect&#x27;s or Employee&#x27;s workouts by Month, Year or idProfessor
*WorkoutApi* | [**get_default_workouts**](docs/WorkoutApi.md#get_default_workouts) | **GET** /api/v1/workout/default-workout | Get All default Workouts
*WorkoutApi* | [**link_workout_to_client**](docs/WorkoutApi.md#link_workout_to_client) | **POST** /api/v1/workout/link-workout-to-client | Link Workout for Client


## Documentation For Models

 - [AtividadeAgendaApiViewModel](docs/AtividadeAgendaApiViewModel.md)
 - [AtividadeBasicoApiViewModel](docs/AtividadeBasicoApiViewModel.md)
 - [AtividadeListApiViewModel](docs/AtividadeListApiViewModel.md)
 - [AtividadeLugarReservaApiViewModel](docs/AtividadeLugarReservaApiViewModel.md)
 - [AtividadeLugarReservaViewModel](docs/AtividadeLugarReservaViewModel.md)
 - [AtividadeSessaoParticipanteApiViewModel](docs/AtividadeSessaoParticipanteApiViewModel.md)
 - [BandeirasBasicoViewModel](docs/BandeirasBasicoViewModel.md)
 - [BankAccountsViewModel](docs/BankAccountsViewModel.md)
 - [BasicFreezeViewModel](docs/BasicFreezeViewModel.md)
 - [BasicMemberMembershipApiViewModel](docs/BasicMemberMembershipApiViewModel.md)
 - [BonusSessionViewModel](docs/BonusSessionViewModel.md)
 - [BusinessHoursViewModel](docs/BusinessHoursViewModel.md)
 - [CardDataViewModel](docs/CardDataViewModel.md)
 - [ClienteDetalhesBasicosApiViewModel](docs/ClienteDetalhesBasicosApiViewModel.md)
 - [ClienteEnotasRetorno](docs/ClienteEnotasRetorno.md)
 - [ClienteTransferenciaViewModel](docs/ClienteTransferenciaViewModel.md)
 - [ClientesAtivosViewModel](docs/ClientesAtivosViewModel.md)
 - [ConfiguracaoApiViewModel](docs/ConfiguracaoApiViewModel.md)
 - [ContratoEntradasApiViewModel](docs/ContratoEntradasApiViewModel.md)
 - [ContratoFiliaisResumoApiViewModel](docs/ContratoFiliaisResumoApiViewModel.md)
 - [ContratoNaoRenovadosViewModel](docs/ContratoNaoRenovadosViewModel.md)
 - [ContratosCanceladosParcelasApiViewModel](docs/ContratosCanceladosParcelasApiViewModel.md)
 - [ContratosCanceladosResumoApiViewModel](docs/ContratosCanceladosResumoApiViewModel.md)
 - [ContratosResumoApiViewModel](docs/ContratosResumoApiViewModel.md)
 - [ContratosResumoPaginaVendaViewModel](docs/ContratosResumoPaginaVendaViewModel.md)
 - [ConveniosApiViewModel](docs/ConveniosApiViewModel.md)
 - [CostCenterApiViewModel](docs/CostCenterApiViewModel.md)
 - [DadosContratoTrasnferenciaApiViewModel](docs/DadosContratoTrasnferenciaApiViewModel.md)
 - [DadosTrocaContratoApiViewModel](docs/DadosTrocaContratoApiViewModel.md)
 - [DiferenciaisApiViewModel](docs/DiferenciaisApiViewModel.md)
 - [DifferentialsViewModel](docs/DifferentialsViewModel.md)
 - [EFormaContato](docs/EFormaContato.md)
 - [EFormaPagamentoTotem](docs/EFormaPagamentoTotem.md)
 - [EOrigemAgendamento](docs/EOrigemAgendamento.md)
 - [EStatusAtividade](docs/EStatusAtividade.md)
 - [EStatusAtividadeSessao](docs/EStatusAtividadeSessao.md)
 - [ETipoContrato](docs/ETipoContrato.md)
 - [ETipoGateway](docs/ETipoGateway.md)
 - [EmployeeApiIntegracaoAtualizacaoViewModel](docs/EmployeeApiIntegracaoAtualizacaoViewModel.md)
 - [EmployeeApiIntegracaoViewModel](docs/EmployeeApiIntegracaoViewModel.md)
 - [EmpresasConveniosApiViewModel](docs/EmpresasConveniosApiViewModel.md)
 - [EmpresasFiliaisGatewayViewModel](docs/EmpresasFiliaisGatewayViewModel.md)
 - [EmpresasFiliaisOcupacaoViewModel](docs/EmpresasFiliaisOcupacaoViewModel.md)
 - [EnderecoEnotasRetorno](docs/EnderecoEnotasRetorno.md)
 - [EnotasRetorno](docs/EnotasRetorno.md)
 - [EntradasResumoApiViewModel](docs/EntradasResumoApiViewModel.md)
 - [FreezeViewModel](docs/FreezeViewModel.md)
 - [FuncionariosResumoApiViewModel](docs/FuncionariosResumoApiViewModel.md)
 - [HttpResponseError](docs/HttpResponseError.md)
 - [InstallmentViewModel](docs/InstallmentViewModel.md)
 - [LogTefApiViewModel](docs/LogTefApiViewModel.md)
 - [MemberAuthenticateViewModel](docs/MemberAuthenticateViewModel.md)
 - [MemberBasicResponsibleViewModel](docs/MemberBasicResponsibleViewModel.md)
 - [MemberDataViewModel](docs/MemberDataViewModel.md)
 - [MemberMembershipApiViewModel](docs/MemberMembershipApiViewModel.md)
 - [MemberNewSaleViewModel](docs/MemberNewSaleViewModel.md)
 - [MemberResponsibleViewModel](docs/MemberResponsibleViewModel.md)
 - [MemberServiceViewModel](docs/MemberServiceViewModel.md)
 - [MemberTransferViewModel](docs/MemberTransferViewModel.md)
 - [MembersApiViewModel](docs/MembersApiViewModel.md)
 - [MembersBasicApiViewModel](docs/MembersBasicApiViewModel.md)
 - [MetadadosEnotasRetorno](docs/MetadadosEnotasRetorno.md)
 - [MonthDiscountViewModel](docs/MonthDiscountViewModel.md)
 - [NewSaleViewModel](docs/NewSaleViewModel.md)
 - [NotificationApiViewModel](docs/NotificationApiViewModel.md)
 - [PayablesApiSubTypesViewModel](docs/PayablesApiSubTypesViewModel.md)
 - [PayablesApiViewModel](docs/PayablesApiViewModel.md)
 - [PeriodizacaoApiViewModel](docs/PeriodizacaoApiViewModel.md)
 - [PixPaymentDetailsViewModel](docs/PixPaymentDetailsViewModel.md)
 - [ProspectApiIntegracaoAtualizacaoViewModel](docs/ProspectApiIntegracaoAtualizacaoViewModel.md)
 - [ProspectApiIntegracaoViewModel](docs/ProspectApiIntegracaoViewModel.md)
 - [ProspectIdViewModel](docs/ProspectIdViewModel.md)
 - [ProspectResponsavelResumoApiViewModel](docs/ProspectResponsavelResumoApiViewModel.md)
 - [ProspectTransferenciaViewModel](docs/ProspectTransferenciaViewModel.md)
 - [ProspectsResumoApiViewModel](docs/ProspectsResumoApiViewModel.md)
 - [PublicoAtividadeViewModel](docs/PublicoAtividadeViewModel.md)
 - [ReceivablesApiSubTypesViewModel](docs/ReceivablesApiSubTypesViewModel.md)
 - [ReceivablesApiViewModel](docs/ReceivablesApiViewModel.md)
 - [ReceivablesCreditDetails](docs/ReceivablesCreditDetails.md)
 - [ReceivablesInvoiceApiViewModel](docs/ReceivablesInvoiceApiViewModel.md)
 - [ReceivablesMaskReceivedViewModel](docs/ReceivablesMaskReceivedViewModel.md)
 - [RevenueCenterApiViewModel](docs/RevenueCenterApiViewModel.md)
 - [SaleItensViewModel](docs/SaleItensViewModel.md)
 - [SalesItemViewModel](docs/SalesItemViewModel.md)
 - [SalesItemsViewModel](docs/SalesItemsViewModel.md)
 - [SalesViewModel](docs/SalesViewModel.md)
 - [ServiceDiscountViewModel](docs/ServiceDiscountViewModel.md)
 - [ServicoAdicionalApiViewModel](docs/ServicoAdicionalApiViewModel.md)
 - [ServicoAnualApiViewModel](docs/ServicoAnualApiViewModel.md)
 - [ServicoEnotasRetorno](docs/ServicoEnotasRetorno.md)
 - [ServicosResumoApiViewModel](docs/ServicosResumoApiViewModel.md)
 - [SpsRelProspectsCadastradosConvertidos](docs/SpsRelProspectsCadastradosConvertidos.md)
 - [TaxDataViewModel](docs/TaxDataViewModel.md)
 - [TelefoneApiViewModel](docs/TelefoneApiViewModel.md)
 - [VouchersResumoApiViewModel](docs/VouchersResumoApiViewModel.md)
 - [W12UtilsCategoryMembershipViewModel](docs/W12UtilsCategoryMembershipViewModel.md)
 - [W12UtilsWebhookHeaderViewModel](docs/W12UtilsWebhookHeaderViewModel.md)
 - [W12UtilsWebhookViewModel](docs/W12UtilsWebhookViewModel.md)
 - [W12UtilzWebHookFilterViewModel](docs/W12UtilzWebHookFilterViewModel.md)
 - [YearDiscountViewModel](docs/YearDiscountViewModel.md)

## Documentation For Authorization


## Basic

- **Type**: HTTP basic authentication


## Author


