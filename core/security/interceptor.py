from typing import TypeVar, Any
from core.security.pipeline import CipherPipe, DecryptPipe

TEntity = TypeVar("TEntity")

class PersistenceInterceptor:
    def __init__(self, cipher_pipe: CipherPipe, decrypt_pipe: DecryptPipe):
        self._cipher_pipe = cipher_pipe
        self._decrypt_pipe = decrypt_pipe

    def _get_encrypted_fields(self, entity: TEntity) -> list[str]:
        # Extraemos la configuración de campos cifrables de la entidad
        return getattr(entity.__class__, "__encrypted_fields__", [])

    def prepare_for_write(self, entity: TEntity) -> TEntity:
        fields = self._get_encrypted_fields(entity)
        if not fields:
            return entity

        for field in fields:
            val = getattr(entity, field, None)
            if val is not None:
                # Ciframos el valor y actualizamos la entidad
                encrypted_val = self._cipher_pipe.execute(val)
                setattr(entity, field, encrypted_val)
        return entity

    def materialize_from_read(self, entity: TEntity) -> TEntity:
        fields = self._get_encrypted_fields(entity)
        if not fields:
            return entity

        for field in fields:
            val = getattr(entity, field, None)
            if val is not None:
                # Desciframos el valor y actualizamos la entidad
                decrypted_val = self._decrypt_pipe.execute(val)
                setattr(entity, field, decrypted_val)
        return entity
