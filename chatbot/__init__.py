

from .config_chroma import CHROMA_SETTINGS  
from .preprocess import (
	PDFIngestion,
	ingest,
	find_pdf_paths,
	load_documents,
	split_documents,
	create_vector_store,
)

__all__ = [
	"CHROMA_SETTINGS",
	"PDFIngestion",
	"ingest",
	"find_pdf_paths",
	"load_documents",
	"split_documents",
	"create_vector_store",
]

__version__ = "0.1.0"