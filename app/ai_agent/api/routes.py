# app/ai_agent/api/routes.py
# API endpoints for /agent/generate, /agent/upload_doc, /agent/upload_sop
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.ai_agent.api.schemas import GenerateRequest
from app.ai_agent.agents.help_qa import HelpQAAgent
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/agent/generate")
async def generate_response(request: GenerateRequest):
    # This acts as our simplistic intent detection layer for now
    if request.mode == "help":
        logger.info(f"Routing request to HelpQAAgent for project: {request.project_id}")
        agent = HelpQAAgent(project_id=request.project_id)
        try:
            response = agent.generate(request.user_input)
            return {"response": response, "intent": "help_qa", "project_id": request.project_id}
        except Exception as e:
            logger.error(f"Error during help generation: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # Fallback or other modes not yet implemented
        logger.warning(f"Unimplemented mode requested: {request.mode}")
        raise HTTPException(status_code=400, detail=f"Only 'help' mode is currently fully implemented. Received: {request.mode}")

@router.post("/agent/upload_sop")
async def upload_sop(
    file: UploadFile = File(...),
    project_id: str = Form("freightship")
):
    logger.info(f"Received SOP upload: {file.filename} for project: {project_id}")
    try:
        content = await file.read()
        # Assume it's a Markdown or text file based on the prompt instructions
        text_content = content.decode("utf-8")
        
        agent = HelpQAAgent(project_id=project_id)
        agent.index_document(text_content, file.filename)
        
        return {
            "status": "indexed", 
            "filename": file.filename, 
            "project_id": project_id,
            "message": "SOP successfully indexed into FAISS."
        }
    except UnicodeDecodeError:
        logger.error(f"Failed to decode {file.filename} as UTF-8.")
        raise HTTPException(status_code=400, detail="Only UTF-8 encoded text/markdown files are supported for SOP upload currently.")
    except Exception as e:
        logger.error(f"Error during SOP indexing: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to index SOP: {str(e)}")
