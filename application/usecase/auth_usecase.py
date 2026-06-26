from domain.port.usuario_repository import UsuarioRepository
from core.middleware.auth import verify_password, get_password_hash, create_access_token
from domain.model.usuario import UsuarioCreate
from infrastructure.database.postgres.models import Usuario

class AuthUseCase:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def autenticar_usuario(self, email, password):
        usuario = next((u for u in self.usuario_repo.get_all() if u.email == email), None)
        if not usuario or not verify_password(password, usuario.password_hash):
            return None
        if not usuario.activo:
            return "INACTIVO"
        return create_access_token(data={"sub": str(usuario.id_usuario)})

    def registrar_usuario(self, usuario_in: UsuarioCreate):
        existente = next((u for u in self.usuario_repo.get_all() if u.email == usuario_in.email), None)
        if existente:
            return None
            
        nuevo_usuario = Usuario(
            nombre=usuario_in.nombre,
            email=usuario_in.email,
            password_hash=get_password_hash(usuario_in.password),
            rol=usuario_in.rol
        )
        self.usuario_repo.db.add(nuevo_usuario)
        self.usuario_repo.db.commit()
        self.usuario_repo.db.refresh(nuevo_usuario)
        return nuevo_usuario
