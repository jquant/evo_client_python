"""Workout-related Pydantic models based on API documentation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class WorkoutTag(BaseModel):
    """Workout tag model."""

    id_tag_treino: Optional[int] = Field(default=None, alias="idTagTreino")
    nome: Optional[str] = None
    id_filial: Optional[int] = Field(default=None, alias="idFilial")
    filial: Optional[str] = None
    evo_treino_tags: Optional[str] = Field(default=None, alias="evoTreinoTags")


class WorkoutSeriesItem(BaseModel):
    """Individual exercise item within a workout series."""

    id_item_serie: Optional[int] = Field(default=None, alias="idItemSerie")
    exercicio: Optional[str] = None
    codigo: Optional[str] = None
    repeticao: Optional[str] = None
    carga: Optional[str] = None
    intervalo: Optional[str] = None
    posicao: Optional[str] = None
    vezes: Optional[str] = None
    observacao: Optional[str] = None
    ordem: Optional[int] = None
    id_exercicio: Optional[int] = Field(default=None, alias="idExercicio")


class WorkoutSeries(BaseModel):
    """Workout series containing multiple exercises."""

    id_serie: Optional[int] = Field(default=None, alias="idSerie")
    nome: Optional[str] = None
    ordem: Optional[int] = None
    observacao: Optional[str] = None
    itens: Optional[List[WorkoutSeriesItem]] = None
    sessoes_concluidas: Optional[int] = Field(default=None, alias="sessoesConcluidas")


class WorkoutResponse(BaseModel):
    """Complete workout response model."""

    id_treino: Optional[int] = Field(default=None, alias="idTreino")
    id_treino_copiar_serie: Optional[int] = Field(
        default=None, alias="idTreinoCopiarSerie"
    )
    id_treino_importar_series: Optional[int] = Field(
        None, alias="idTreinoImportarSeries"
    )
    id_cliente: Optional[int] = Field(default=None, alias="idCliente")
    id_prospect: Optional[int] = Field(default=None, alias="idProspect")
    id_funcionario: Optional[int] = Field(default=None, alias="idFuncionario")
    nome_treino: Optional[str] = Field(default=None, alias="nomeTreino")
    treino_padrao: Optional[str] = Field(default=None, alias="treinoPadrao")
    data_criacao: Optional[datetime] = Field(default=None, alias="dataCriacao")
    data_inicio: Optional[datetime] = Field(default=None, alias="dataInicio")
    data_validade: Optional[datetime] = Field(default=None, alias="dataValidade")
    observacao: Optional[str] = None
    tags: Optional[List[WorkoutTag]] = None
    restricoes: Optional[str] = None
    series: Optional[List[WorkoutSeries]] = None
    nome_professor: Optional[str] = Field(default=None, alias="nomeProfessor")
    url_foto: Optional[str] = Field(default=None, alias="urlFoto")
    quantidade_sessoes: Optional[int] = Field(default=None, alias="quantidadeSessoes")
    quantidade_semanal: Optional[int] = Field(default=None, alias="quantidadeSemanal")
    frequencia_semana: Optional[int] = Field(default=None, alias="frequenciaSemana")
    sessoes_concluidas: Optional[int] = Field(default=None, alias="sessoesConcluidas")
    status_treino: Optional[int] = Field(default=None, alias="statusTreino")
    id_serie_atual: Optional[int] = Field(default=None, alias="idSerieAtual")
    permite_imprimir: Optional[bool] = Field(default=None, alias="permiteImprimir")
    origem_evo_app: Optional[bool] = Field(default=None, alias="origemEvoApp")


class WorkoutUpdateResponse(BaseModel):
    """Response model for workout update operations."""

    success: bool
    message: Optional[str] = None
    workout_id: Optional[int] = None
    errors: Optional[List[str]] = None
