from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.claims import service as claims_service
from app.modules.evidence.schemas import (
    UploadedEvidenceResponse,
)
from app.modules.evidence.service import (
    create_uploaded_evidence,
)
from app.services.uploads.service import extract_uploaded_text


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)


@router.post(
    "/document",
    status_code=status.HTTP_200_OK,
)
async def upload_document(
    file: UploadFile = File(...),
):
    try:
        text = await extract_uploaded_text(
            file,
            "document",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text": text,
        "message": "Document processed successfully",
    }


@router.post(
    "/image",
    status_code=status.HTTP_200_OK,
)
async def upload_image(
    file: UploadFile = File(...),
):
    try:
        text = await extract_uploaded_text(
            file,
            "image",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text": text,
        "message": "Image processed successfully",
    }


async def process_claim_upload(
    claim_id: UUID,
    file: UploadFile,
    upload_type: str,
    db: Session,
    current_user,
):
    claim = claims_service.get_claim(
        db=db,
        claim_id=str(claim_id),
        user_id=current_user.id,
    )

    try:
        text = await extract_uploaded_text(
            file,
            upload_type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    source_type = (
        "DOCUMENT"
        if upload_type == "document"
        else "IMAGE"
    )

    source, chunks = create_uploaded_evidence(
        db=db,
        claim_id=claim.id,
        filename=file.filename or "unknown",
        content_type=file.content_type or "",
        source_type=source_type,
        content=text,
    )

    return {
        "source": source,
        "chunks": chunks,
    }


@router.post(
    "/{claim_id}/document",
   response_model=UploadedEvidenceResponse,
    status_code=status.HTTP_200_OK,
)
async def upload_document_for_claim(
    claim_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await process_claim_upload(
        claim_id=claim_id,
        file=file,
        upload_type="document",
        db=db,
        current_user=current_user,
    )


@router.post(
    "/{claim_id}/image",
    response_model=UploadedEvidenceResponse,
    status_code=status.HTTP_200_OK,
)
async def upload_image_for_claim(
    claim_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await process_claim_upload(
        claim_id=claim_id,
        file=file,
        upload_type="image",
        db=db,
        current_user=current_user,
    )