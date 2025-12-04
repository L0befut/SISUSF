# =============================================================================
# controllers/relatorio_controller.py
# =============================================================================
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.paciente import Paciente
from models.consulta import Consulta
from models.auditoria import LogAuditoria
from db.connection import db_manager
from controllers.auth_controller import auth
from datetime import date, datetime

class RelatorioController:

    def get_dashboard_data(self) -> dict:
        if not auth.has_permission('read'):
            return {"success": False, "message": "Sem permissão"}

        session = db_manager.get_session()
        try:
            hoje = date.today()
            inicio_mes = hoje.replace(day=1)

            total_pacientes = session.query(func.count(Paciente.id)).filter(Paciente.ativo == True).scalar()
            pacientes_mes = session.query(func.count(Paciente.id)).filter(
                and_(
                    Paciente.ativo == True,
                    func.date(Paciente.created_at) >= inicio_mes
                )
            ).scalar()
            consultas_hoje = session.query(func.count(Consulta.id)).filter(func.date(Consulta.data_hora) == hoje).scalar()
            consultas_mes = session.query(func.count(Consulta.id)).filter(
                and_(
                    func.date(Consulta.data_hora) >= inicio_mes,
                    func.date(Consulta.data_hora) <= hoje
                )
            ).scalar()

            return {
                "success": True,
                "data": {
                    "total_pacientes": total_pacientes,
                    "pacientes_mes": pacientes_mes,
                    "consultas_hoje": consultas_hoje,
                    "consultas_mes": consultas_mes,
                    "data_atualizacao": datetime.now().isoformat()
                }
            }
        finally:
            session.close()

    def get_consultas_por_tipo(self, inicio: date, fim: date) -> dict:
        if not auth.has_permission('report'):
            return {"success": False, "message": "Sem permissão"}

        session = db_manager.get_session()
        try:
            resultado = session.query(
                Consulta.tipo,
                func.count(Consulta.id).label('total')
            ).filter(
                and_(
                    func.date(Consulta.data_hora) >= inicio,
                    func.date(Consulta.data_hora) <= fim
                )
            ).group_by(Consulta.tipo).all()

            dados = [{"tipo": r.tipo.value, "total": r.total} for r in resultado]
            return {"success": True, "dados": dados}
        finally:
            session.close()

    def get_pacientes_por_faixa_etaria(self) -> dict:
        session = db_manager.get_session()
        try:
            pacientes = session.query(Paciente).filter(Paciente.ativo == True).all()
            faixas = {'0-17': 0, '18-39': 0, '40-59': 0, '60+': 0}

            for p in pacientes:
                idade = p.idade
                if idade < 18:
                    faixas['0-17'] += 1
                elif idade < 40:
                    faixas['18-39'] += 1
                elif idade < 60:
                    faixas['40-59'] += 1
                else:
                    faixas['60+'] += 1

            dados = [{"faixa": k, "total": v} for k, v in faixas.items()]
            return {"success": True, "dados": dados}
        finally:
            session.close()

# Instância global
relatorio_controller = RelatorioController()
