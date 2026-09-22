"""
Paris Group Copilot — API

Backend do copiloto de venture studio. Expõe as duas entidades centrais do
enquadramento: Projeto (um MVP do studio) e Hipótese (uma hipótese de valor
testável ligada a um projeto).

O contrato OpenAPI é gerado automaticamente pelo FastAPI e fica em /docs.
"""

import os
from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://copilot:copilot@db:5432/copilot"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


# --------------------------------------------------------------------------
# Modelos de banco
# --------------------------------------------------------------------------


class Projeto(Base):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    contexto: Mapped[str] = mapped_column(Text, nullable=False)
    dor_usuario: Mapped[str] = mapped_column(Text, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Hipotese(Base):
    __tablename__ = "hipoteses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projeto_id: Mapped[int] = mapped_column(
        ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False
    )
    enunciado: Mapped[str] = mapped_column(Text, nullable=False)
    metrica: Mapped[str] = mapped_column(String(240), nullable=False)
    criterio_aceite: Mapped[str] = mapped_column(String(240), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="nao_testada")
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# --------------------------------------------------------------------------
# Schemas de request / response (contrato OpenAPI)
# --------------------------------------------------------------------------


class ProjetoCreate(BaseModel):
    nome: str = Field(..., max_length=120, examples=["Paris Group Copilot"])
    contexto: str = Field(..., examples=["PM de venture studio iniciando um novo MVP"])
    dor_usuario: str = Field(
        ...,
        examples=[
            "Marina gasta ~8h por produto novo remontando enquadramento do zero"
        ],
    )


class ProjetoOut(BaseModel):
    id: int
    nome: str
    contexto: str
    dor_usuario: str
    criado_em: datetime

    model_config = {"from_attributes": True}


class HipoteseCreate(BaseModel):
    projeto_id: int = Field(..., examples=[1])
    enunciado: str = Field(
        ...,
        examples=[
            "Se o copiloto sugerir enquadramentos a partir do histórico de MVPs, "
            "então o enquadramento inicial cai de 8h para 2h"
        ],
    )
    metrica: str = Field(
        ..., max_length=240, examples=["Tempo até enquadramento concluído"]
    )
    criterio_aceite: str = Field(
        ..., max_length=240, examples=["4 de 5 produtos em <= 2h"]
    )


class HipoteseOut(BaseModel):
    id: int
    projeto_id: int
    enunciado: str
    metrica: str
    criterio_aceite: str
    status: str
    criado_em: datetime

    model_config = {"from_attributes": True}


# --------------------------------------------------------------------------
# App
# --------------------------------------------------------------------------

app = FastAPI(
    title="Paris Group Copilot API",
    description=(
        "Backend do copiloto de venture studio. Entidades: Projeto e Hipótese. "
        "O histórico de hipóteses é o ativo que permite ao studio reaproveitar "
        "aprendizado entre MVPs."
    ),
    version="0.1.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def criar_tabelas() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["infra"])
def health() -> dict:
    return {"status": "ok"}


@app.post("/projetos", response_model=ProjetoOut, status_code=201, tags=["projetos"])
def criar_projeto(payload: ProjetoCreate, db: Session = Depends(get_db)) -> Projeto:
    projeto = Projeto(**payload.model_dump())
    db.add(projeto)
    db.commit()
    db.refresh(projeto)
    return projeto


@app.get("/projetos", response_model=list[ProjetoOut], tags=["projetos"])
def listar_projetos(db: Session = Depends(get_db)) -> list[Projeto]:
    return db.query(Projeto).order_by(Projeto.criado_em.desc()).all()


@app.post("/hipoteses", response_model=HipoteseOut, status_code=201, tags=["hipoteses"])
def criar_hipotese(payload: HipoteseCreate, db: Session = Depends(get_db)) -> Hipotese:
    if not db.get(Projeto, payload.projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    hipotese = Hipotese(**payload.model_dump())
    db.add(hipotese)
    db.commit()
    db.refresh(hipotese)
    return hipotese


@app.get("/hipoteses", response_model=list[HipoteseOut], tags=["hipoteses"])
def listar_hipoteses(
    projeto_id: Optional[int] = None, db: Session = Depends(get_db)
) -> list[Hipotese]:
    query = db.query(Hipotese)
    if projeto_id is not None:
        query = query.filter(Hipotese.projeto_id == projeto_id)
    return query.order_by(Hipotese.criado_em.desc()).all()
