import os
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

# Import project-specific modules
from .db.database import get_db, engine, Base
from .db.models import ModerationRequest, ModerationResult
from .tasks.image_moderation import moderate_image_task
from .services.llm import moderate_text_content
from .services.notifications import send_email_notification

# Create FastAPI app instance
app = FastAPI()

# Pydantic models for API requests
class ModerateTextRequest(BaseModel):
    email: EmailStr
    text: str

class ModerateImageRequest(BaseModel):
    email: EmailStr
    image_url: str

# Database initialization function
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Startup event to create database tables
@app.on_event("startup")
async def on_startup():
    await init_db()

# Main API Endpoints
# ----------------------------------------------------------------------
@app.post("/api/v1/moderate/text")
async def moderate_text(request: ModerateTextRequest, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to moderate a text submission using an LLM.
    """
    # Create and save a new moderation request to the database
    new_request = ModerationRequest(
        content_type="text",
        status="pending",
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)

    # Call the LLM service to moderate the content
    try:
        llm_response_text = moderate_text_content(request.text)
        # Parse the LLM's response (this is a placeholder)
        classification = "safe"  # Assume safe for now
        confidence = 100
        reasoning = "Placeholder reasoning"
        
        # Save the result to the database
        new_result = ModerationResult(
            request_id=new_request.id,
            classification=classification,
            confidence=confidence,
            reasoning=reasoning,
            llm_response=llm_response_text,
        )
        db.add(new_result)
        
        # Update the request status
        new_request.status = "completed"
        await db.commit()

        # Trigger notification if content is inappropriate
        if classification != "safe":
            send_email_notification(request.email, classification, llm_response_text)

        return {"message": "Text moderation request processed successfully.", "request_id": new_request.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/moderate/image")
async def moderate_image(request: ModerateImageRequest):
    """
    Endpoint to moderate an image submission asynchronously.
    """
    # Enqueue the task for Celery to handle in the background
    moderate_image_task.delay(request.email, request.image_url)
    
    return {"message": "Image moderation is being processed in the background.", "status": 202}

@app.get("/api/v1/analytics/summary")
async def get_summary(user: EmailStr, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to retrieve a moderation summary for a given user.
    """
    # Query the database for all moderation requests by the user
    result = await db.execute(select(ModerationRequest).where(ModerationRequest.email == user))
    requests = result.scalars().all()
    
    if not requests:
        return {"message": "No moderation requests found for this user."}

    summary = {
        "user": user,
        "total_requests": len(requests),
        "requests": [{"id": r.id, "content_type": r.content_type, "status": r.status} for r in requests]
    }
    
    return summary
