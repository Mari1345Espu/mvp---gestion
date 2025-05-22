from fastapi import UploadFile, HTTPException, status
from typing import List, Optional
import magic
import os
from ..middleware.security import ALLOWED_FILE_TYPES

# Tamaños máximos en bytes
MAX_FILE_SIZES = {
    "image": 5 * 1024 * 1024,  # 5MB
    "document": 10 * 1024 * 1024,  # 10MB
    "spreadsheet": 10 * 1024 * 1024,  # 10MB
    "presentation": 20 * 1024 * 1024,  # 20MB
}

async def validate_file(
    file: UploadFile,
    allowed_types: List[str],
    max_size: Optional[int] = None
) -> None:
    """
    Valida un archivo subido.
    
    Args:
        file: El archivo a validar
        allowed_types: Lista de tipos MIME permitidos
        max_size: Tamaño máximo en bytes (opcional)
    """
    # Verificar tamaño
    if max_size:
        file_size = 0
        chunk_size = 8192  # 8KB
        
        while chunk := await file.read(chunk_size):
            file_size += len(chunk)
            if file_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"El archivo excede el tamaño máximo permitido de {max_size/1024/1024}MB"
                )
        
        # Resetear el archivo para su posterior uso
        await file.seek(0)
    
    # Verificar tipo MIME
    content = await file.read(2048)  # Leer los primeros 2KB para detectar el tipo
    mime_type = magic.from_buffer(content, mime=True)
    
    if mime_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Tipo de archivo no permitido. Tipos permitidos: {', '.join(allowed_types)}"
        )
    
    # Resetear el archivo para su posterior uso
    await file.seek(0)

def get_file_type_category(mime_type: str) -> Optional[str]:
    """
    Obtiene la categoría de un tipo MIME.
    """
    for category, types in ALLOWED_FILE_TYPES.items():
        if mime_type in types:
            return category
    return None

async def validate_upload_file(
    file: UploadFile,
    file_type: str
) -> None:
    """
    Valida un archivo subido según su tipo.
    
    Args:
        file: El archivo a validar
        file_type: Tipo de archivo ('image', 'document', 'spreadsheet', 'presentation')
    """
    if file_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no válido: {file_type}"
        )
    
    allowed_types = ALLOWED_FILE_TYPES[file_type]
    max_size = MAX_FILE_SIZES.get(file_type)
    
    await validate_file(file, allowed_types, max_size)

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo para prevenir path traversal y otros problemas.
    """
    # Eliminar caracteres no seguros
    filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
    
    # Eliminar espacios al inicio y final
    filename = filename.strip()
    
    # Reemplazar espacios por guiones bajos
    filename = filename.replace(" ", "_")
    
    # Limitar longitud
    filename = filename[:255]
    
    return filename 