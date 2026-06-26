from typing import List, Optional
from domain.port.usuario_repository import UsuarioRepository
from domain.model.usuario import UsuarioUpdate
from infrastructure.database.postgres.models import Usuario

class UsuarioUseCase:
    """
    Capa de Aplicación: Orquesta la lógica de negocio usando el Puerto (Interfaz).
    """
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository
        
    def obtener_todos_los_usuarios(self, rol: Optional[str] = None) -> List[Usuario]:
        return self.repository.get_all(rol)
        
    def modificar_usuario(self, id_usuario: str, update_data: UsuarioUpdate) -> Optional[Usuario]:
        # Aquí se podrían añadir validaciones de negocio complejas antes de guardar
        return self.repository.update(id_usuario, update_data)
        
    def eliminar_usuario(self, id_usuario: str, id_admin_actual: str) -> bool:
        # Regla de negocio: Un admin no puede borrarse a sí mismo
        if id_usuario == id_admin_actual:
            raise ValueError("No puedes eliminar tu propia cuenta de administrador")
            
        return self.repository.delete(id_usuario)
