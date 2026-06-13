"""
ARKHEIA-CPS — File Extraction Utilities
Stubs for PDF/DOCX upload and text extraction.
OCR integration point for future full-document analysis.
"""
from __future__ import annotations
from typing import Optional


async def upload_file(file_bytes: bytes, filename: str, contract_id: str) -> str:
    """
    TODO: Upload file to S3 or local storage.
    Returns the stored file path.

    Future implementation:
        - boto3 for AWS S3
        - Google Cloud Storage client
        - Local filesystem with UUID-based paths

    For now, returns a placeholder path.
    """
    return f"/uploads/{contract_id}/{filename}"


def extract_text_from_pdf(file_path: str) -> str:
    """
    TODO: Extract raw text from a PDF file.

    Future implementation options:
        - pdfminer.six for text extraction
        - PyMuPDF (fitz) for layout-aware extraction
        - AWS Textract for scanned documents (OCR)
        - Google Document AI

    Returns extracted text string.
    """
    raise NotImplementedError(
        "PDF text extraction not yet implemented. "
        "Use JSON payload input for now. "
        "Integrate pdfminer.six or AWS Textract here."
    )


def extract_text_from_docx(file_path: str) -> str:
    """
    TODO: Extract raw text from a DOCX file.

    Future implementation:
        - python-docx library
        - mammoth for clean HTML extraction

    Returns extracted text string.
    """
    raise NotImplementedError(
        "DOCX text extraction not yet implemented. "
        "Use JSON payload input for now. "
        "Integrate python-docx here."
    )


def map_text_to_fia_auto(raw_text: str) -> dict:
    """
    TODO: Map extracted document text to AUTO FIA JSON structure.

    Future implementation:
        - Named Entity Recognition (NER) with spaCy
        - LLM extraction (Claude / GPT-4) with structured output
        - Regex patterns for VIN, APR, dates, amounts
        - Template matching for common dealer contract formats

    Returns dict matching AutoContractIn schema.
    """
    raise NotImplementedError(
        "Auto FIA text mapping not yet implemented. "
        "Use structured JSON payload for now. "
        "Integrate LLM extraction or NER pipeline here."
    )


def map_text_to_fia_housing(raw_text: str) -> dict:
    """
    TODO: Map extracted document text to HOUSING FIA JSON structure.

    Future implementation:
        - LLM extraction for lease clause identification
        - Pattern matching for rent amounts, dates, fee schedules
        - Clause classifier for illegal/predatory clause detection

    Returns dict matching HousingContractIn schema.
    """
    raise NotImplementedError(
        "Housing FIA text mapping not yet implemented. "
        "Use structured JSON payload for now. "
        "Integrate LLM lease extraction pipeline here."
    )


def detect_vertical(raw_text: str) -> Optional[str]:
    """
    TODO: Detect whether a document is an AUTO or HOUSING contract.

    Heuristics:
        - VIN pattern → AUTO
        - 'Lease Agreement' / 'Rental Agreement' → HOUSING
        - Presence of APR, monthly payment → AUTO
        - Presence of monthly rent, security deposit → HOUSING
    """
    text_lower = raw_text.lower()
    if any(kw in text_lower for kw in ["vehicle identification number", "vin", "retail installment"]):
        return "AUTO"
    if any(kw in text_lower for kw in ["lease agreement", "monthly rent", "security deposit", "landlord"]):
        return "HOUSING"
    return None
