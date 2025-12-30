import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
from app.config import settings


class FileStorageService:
    def __init__(self):
        self.media_root = Path(settings.MEDIA_ROOT)
        self.media_root.mkdir(parents=True, exist_ok=True)

    def _get_product_folder(self, category_slug: str, product_uuid: str, stage_name: Optional[str] = None) -> Path:
        """Generate the folder path for a product's images."""
        folder = self.media_root / "categories" / category_slug / "products" / product_uuid
        
        if stage_name:
            folder = folder / f"stage-{stage_name}"
        
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def validate_image(self, file: UploadFile) -> Tuple[bool, Optional[str]]:
        """Validate image file type and size."""
        # Check file type
        if file.content_type not in settings.allowed_image_types_list:
            return False, f"Invalid file type. Allowed types: {', '.join(settings.allowed_image_types_list)}"
        
        # Check file size (read file to check size)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.max_image_size_bytes:
            return False, f"File too large. Max size: {settings.MAX_IMAGE_SIZE_MB}MB"
        
        return True, None

    def save_image(
        self,
        file: UploadFile,
        category_slug: str,
        product_uuid: str,
        stage_name: Optional[str] = None
    ) -> Tuple[str, int, int, int]:
        """
        Save an image file and return its relative path, width, height, and size.
        
        Returns:
            Tuple of (relative_path, width, height, size_in_bytes)
        """
        # Validate image
        is_valid, error_msg = self.validate_image(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate unique filename
        file_uuid = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        new_filename = f"{file_uuid}_{file.filename}"
        
        # Get folder path
        folder = self._get_product_folder(category_slug, product_uuid, stage_name)
        file_path = folder / new_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        # Get image dimensions
        try:
            with Image.open(file_path) as img:
                width, height = img.size
        except Exception:
            width, height = None, None
        
        # Calculate relative path
        relative_path = str(file_path.relative_to(self.media_root))
        
        # Get file size
        file_size = file_path.stat().st_size
        
        return relative_path, width, height, file_size

    def delete_image(self, relative_path: str) -> bool:
        """Delete an image file from the filesystem."""
        try:
            file_path = self.media_root / relative_path
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def get_full_path(self, relative_path: str) -> Path:
        """Get the full filesystem path from a relative path."""
        return self.media_root / relative_path

    def file_exists(self, relative_path: str) -> bool:
        """Check if a file exists."""
        return (self.media_root / relative_path).exists()


# Singleton instance
file_storage = FileStorageService()
