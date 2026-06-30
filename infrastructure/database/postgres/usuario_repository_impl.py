from sqlalchemy.orm import Session
from typing import List, Optional
from domain.port.usuario_repository import UsuarioRepository
from domain.model.usuario import UsuarioUpdate
from infrastructure.database.postgres.models import Usuario
from core.security import persistence_interceptor

class UsuarioRepositoryImpl(UsuarioRepository):
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self, rol: Optional[str] = None) -> List[Usuario]:
        query = self.db.query(Usuario)
        if rol:
            query = query.filter(Usuario.rol == rol)
        usuarios = query.all()
        return [persistence_interceptor.materialize_from_read(u) for u in usuarios]
        
    def get_by_id(self, id_usuario: str) -> Optional[Usuario]:
        usuario = self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            return persistence_interceptor.materialize_from_read(usuario)
        return None
        
    def update(self, id_usuario: str, update_data: UsuarioUpdate) -> Optional[Usuario]:
        usuario = self.get_by_id(id_usuario)
        if not usuario:
            return None
            
        if update_data.rol is not None:
            usuario.rol = update_data.rol
        if update_data.activo is not None:
            usuario.activo = update_data.activo
            
        usuario = persistence_interceptor.prepare_for_write(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return persistence_interceptor.materialize_from_read(usuario)
        
    def delete(self, id_usuario: str) -> bool:
        usuario = self.get_by_id(id_usuario)
        if not usuario:
            return False
            
        self.db.delete(usuario)
        self.db.commit()
        return True
