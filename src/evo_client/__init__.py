# coding: utf-8

# flake8: noqa

"""
EVO Client Python SDK

🎊 **FULLY REFACTORED: BUNDLER PROBLEM ELIMINATED!** 🎊

This library now provides clean, separate sync and async implementations:

✅ **Clean Async** (Real async/await):
    from evo_client.aio import AsyncApiClient
    from evo_client.aio.api import AsyncMembersApi

    async with AsyncApiClient() as client:
        members_api = AsyncMembersApi(client)
        members = await members_api.get_members()

✅ **Clean Sync** (Simple and direct):
    from evo_client.sync import SyncApiClient
    from evo_client.sync.api import SyncMembersApi

    with SyncApiClient() as client:
        members_api = SyncMembersApi(client)
        members = members_api.get_members()

🔄 **Backward Compatibility**: Existing code continues to work

OpenAPI spec version: v1
Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# Clean module imports
# Configuration helpers
from . import aio, config, sync
from .aio.core.api_client import AsyncApiClient

# Configuration
from .core.configuration import Configuration

# Main clients - clean import
from .sync.core.api_client import SyncApiClient

# ==============================================================================
# 🚀 NEW CLEAN INTERFACES (Recommended)
# ==============================================================================


# ==============================================================================
# 🔄 BACKWARD COMPATIBILITY (Existing users) - DEPRECATED
# ==============================================================================

# For backward compatibility, map old ApiClient to SyncApiClient
ApiClient = SyncApiClient

# ==============================================================================
# 📦 MODEL IMPORTS (Shared across sync/async)
# ==============================================================================

# import models into sdk package
from .models.atividade_agenda_api_view_model import AtividadeAgendaApiViewModel
from .models.atividade_basico_api_view_model import AtividadeBasicoApiViewModel
from .models.atividade_list_api_view_model import AtividadeListApiViewModel
from .models.atividade_lugar_reserva_api_view_model import (
    AtividadeLugarReservaApiViewModel,
)
from .models.atividade_lugar_reserva_view_model import AtividadeLugarReservaViewModel
from .models.atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from .models.bandeiras_basico_view_model import BandeirasBasicoViewModel
from .models.bank_accounts_view_model import BankAccountsViewModel
from .models.basic_freeze_view_model import BasicFreezeViewModel
from .models.basic_member_membership_api_view_model import (
    BasicMemberMembershipApiViewModel,
)
from .models.bonus_session_view_model import BonusSessionViewModel
from .models.business_hours_view_model import BusinessHoursViewModel
from .models.card_data_view_model import CardDataViewModel
from .models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from .models.cliente_enotas_retorno import ClienteEnotasRetorno
from .models.cliente_transferencia_view_model import ClienteTransferenciaViewModel
from .models.clientes_ativos_view_model import ClientesAtivosViewModel
from .models.configuracao_api_view_model import ConfiguracaoApiViewModel
from .models.contrato_entradas_api_view_model import ContratoEntradasApiViewModel
from .models.contrato_filiais_resumo_api_view_model import (
    ContratoFiliaisResumoApiViewModel,
)
from .models.contrato_nao_renovados_view_model import ContratoNaoRenovadosViewModel
from .models.contratos_cancelados_parcelas_api_view_model import (
    ContratosCanceladosParcelasApiViewModel,
)
from .models.contratos_cancelados_resumo_api_view_model import (
    ContratosCanceladosResumoApiViewModel,
)
from .models.contratos_resumo_api_view_model import ContratosResumoApiViewModel
from .models.contratos_resumo_pagina_venda_view_model import (
    ContratosResumoPaginaVendaViewModel,
)
from .models.convenios_api_view_model import ConveniosApiViewModel
from .models.cost_center_api_view_model import CostCenterApiViewModel
from .models.dados_contrato_trasnferencia_api_view_model import (
    DadosContratoTrasnferenciaApiViewModel,
)
from .models.dados_troca_contrato_api_view_model import DadosTrocaContratoApiViewModel
from .models.diferenciais_api_view_model import DiferenciaisApiViewModel
from .models.differentials_view_model import DifferentialsViewModel
from .models.e_forma_contato import EFormaContato
from .models.e_forma_pagamento_totem import EFormaPagamentoTotem
from .models.e_origem_agendamento import EOrigemAgendamento
from .models.e_status_atividade import EStatusAtividade
from .models.e_status_atividade_sessao import EStatusAtividadeSessao
from .models.e_tipo_contrato import ETipoContrato
from .models.e_tipo_gateway import ETipoGateway
from .models.employee_api_integracao_atualizacao_view_model import (
    EmployeeApiIntegracaoAtualizacaoViewModel,
)
from .models.employee_api_integracao_view_model import EmployeeApiIntegracaoViewModel
from .models.empresas_convenios_api_view_model import EmpresasConveniosApiViewModel
from .models.empresas_filiais_gateway_view_model import EmpresasFiliaisGatewayViewModel
from .models.empresas_filiais_ocupacao_view_model import (
    EmpresasFiliaisOcupacaoViewModel,
)
from .models.endereco_enotas_retorno import EnderecoEnotasRetorno
from .models.enotas_retorno import EnotasRetorno
from .models.entradas_resumo_api_view_model import EntradasResumoApiViewModel
from .models.freeze_view_model import FreezeViewModel
from .models.funcionarios_resumo_api_view_model import FuncionariosResumoApiViewModel
from .models.http_response_error import HttpResponseError
from .models.installment_view_model import InstallmentViewModel
from .models.log_tef_api_view_model import LogTefApiViewModel
from .models.member_authenticate_view_model import MemberAuthenticateViewModel
from .models.member_basic_responsible_view_model import MemberBasicResponsibleViewModel
from .models.member_data_view_model import MemberDataViewModel
from .models.member_membership_api_view_model import MemberMembershipApiViewModel
from .models.member_new_sale_view_model import MemberNewSaleViewModel
from .models.member_responsible_view_model import MemberResponsibleViewModel
from .models.member_service_view_model import MemberServiceViewModel
from .models.members_api_view_model import MembersApiViewModel
from .models.members_basic_api_view_model import MembersBasicApiViewModel
from .models.metadados_enotas_retorno import MetadadosEnotasRetorno
from .models.month_discount_view_model import MonthDiscountViewModel
from .models.new_sale_view_model import NewSaleViewModel
from .models.notification_api_view_model import NotificationApiViewModel
from .models.payables_api_sub_types_view_model import PayablesApiSubTypesViewModel
from .models.payables_api_view_model import PayablesApiViewModel
from .models.periodizacao_api_view_model import PeriodizacaoApiViewModel
from .models.pix_payment_details_view_model import PixPaymentDetailsViewModel
from .models.prospect_api_integracao_atualizacao_view_model import (
    ProspectApiIntegracaoAtualizacaoViewModel,
)
from .models.prospect_api_integracao_view_model import ProspectApiIntegracaoViewModel
from .models.prospect_id_view_model import ProspectIdViewModel
from .models.prospect_responsavel_resumo_api_view_model import (
    ProspectResponsavelResumoApiViewModel,
)
from .models.prospect_transferencia_view_model import ProspectTransferenciaViewModel
from .models.prospects_resumo_api_view_model import ProspectsResumoApiViewModel
from .models.publico_atividade_view_model import PublicoAtividadeViewModel
from .models.receivables_api_sub_types_view_model import ReceivablesApiSubTypesViewModel
from .models.receivables_api_view_model import ReceivablesApiViewModel
from .models.receivables_credit_details import ReceivablesCreditDetails
from .models.receivables_invoice_api_view_model import ReceivablesInvoiceApiViewModel
from .models.receivables_mask_received_view_model import (
    ReceivablesMaskReceivedViewModel,
)
from .models.revenue_center_api_view_model import RevenueCenterApiViewModel
from .models.sale_itens_view_model import SaleItensViewModel
from .models.sales_item_view_model import SalesItemViewModel
from .models.sales_items_view_model import SalesItemsViewModel
from .models.sales_view_model import SalesViewModel
from .models.service_discount_view_model import ServiceDiscountViewModel
from .models.servico_adicional_api_view_model import ServicoAdicionalApiViewModel
from .models.servico_anual_api_view_model import ServicoAnualApiViewModel
from .models.servico_enotas_retorno import ServicoEnotasRetorno
from .models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from .models.sps_rel_prospects_cadastrados_convertidos import (
    SpsRelProspectsCadastradosConvertidos,
)
from .models.tax_data_view_model import TaxDataViewModel
from .models.telefone_api_view_model import TelefoneApiViewModel
from .models.vouchers_resumo_api_view_model import VouchersResumoApiViewModel
from .models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)
from .models.w12_utils_webhook_filter_view_model import W12UtilsWebhookFilterViewModel
from .models.w12_utils_webhook_header_view_model import W12UtilsWebhookHeaderViewModel
from .models.w12_utils_webhook_view_model import W12UtilsWebhookViewModel
from .models.year_discount_view_model import YearDiscountViewModel

# ==============================================================================
# 📋 PUBLIC API EXPORTS
# ==============================================================================

__all__ = [
    # ✅ Clean interfaces (recommended for new code)
    "SyncApiClient",
    "AsyncApiClient",
    "sync",
    "aio",
    "config",
    # 🔄 Shared components
    "Configuration",
    # ⚠️  DEPRECATED - Backward compatibility only (use sync/aio versions instead)
    "ApiClient",  # -> SyncApiClient (DEPRECATED)
    # All model classes available (these remain the same)
    # (Full list maintained for compatibility)
]

# ==============================================================================
# 🎊 USAGE EXAMPLES
# ==============================================================================

"""
🎯 **RECOMMENDED USAGE PATTERNS:**

1️⃣ **Super Easy Configuration** (New in Phase 4.2!):
    ```python
    from evo_client.config import ConfigBuilder
    from evo_client import SyncApiClient, AsyncApiClient
    
    # Environment-based config (recommended)
    config = ConfigBuilder.from_env()  # Reads EVO_* env vars
    
    # Or quick gym setup
    config = ConfigBuilder.basic_auth(
        host="https://api.evo.com", 
        username="your_gym_dns",
        password="your_secret_key"
    )
    
    # Works with both sync and async!
    with SyncApiClient(config) as client:
        # Use sync client
        pass
        
    async with AsyncApiClient(config) as client:
        # Use async client  
        pass
    ```

2️⃣ **Configuration Presets** (Instant setup):
    ```python
    from evo_client.config import ConfigPresets
    
    # Development setup
    config = ConfigPresets.gym_development()
    
    # Production setup  
    config = ConfigPresets.gym_production()
    config.username = "your_gym_dns"
    config.password = "your_secret_key"
    
    # High-performance setup
    config = ConfigPresets.high_performance()
    ```

3️⃣ **Clean Async** (Modern, efficient):
    ```python
    from evo_client.aio import AsyncApiClient
    from evo_client.aio.api import AsyncMembersApi
    from evo_client.config import ConfigBuilder
    
    config = ConfigBuilder.from_env()
    async with AsyncApiClient(config) as client:
        members_api = AsyncMembersApi(client)
        members = await members_api.get_members()
    ```

4️⃣ **Clean Sync** (Simple, direct):
    ```python
    from evo_client.sync import SyncApiClient
    from evo_client.sync.api import SyncMembersApi
    from evo_client.config import QuickConfig
    
    config = QuickConfig.gym_basic("your_gym_dns", "secret_key")
    with SyncApiClient(config) as client:
        members_api = SyncMembersApi(client)
        members = members_api.get_members()
    ```

5️⃣ **Configuration Validation** (Catch issues early):
    ```python
    from evo_client.config import ConfigValidator
    
    is_valid, errors, warnings = ConfigValidator.validate_config(config)
    if not is_valid:
        print(f"Config errors: {errors}")
    
    # Get full report
    report = ConfigValidator.get_validation_report(config)
    print(report)
    ```

🔄 **Backward Compatible** (Existing code):
    ```python
    from evo_client import ApiClient, MembersApi
    # Works exactly as before
    ```
"""
