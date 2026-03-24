"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CODEDOCK IMAGE GENERATION PIPELINE v11.0.0                 ║
║                                                                               ║
║  Multi-Provider Image Generation System                                       ║
║  - OpenAI gpt-image-1                                                         ║
║  - Gemini Nano Banana                                                         ║
║  - Grok Imagine API                                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import uuid
import base64
import asyncio
import os

# Load environment
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

router = APIRouter(prefix="/imagine", tags=["Image Generation"])

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# ============================================================================
# REQUEST MODELS
# ============================================================================

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=4000, description="Image description")
    provider: Literal["auto", "openai", "gemini", "grok"] = "auto"
    style: Optional[str] = Field(None, description="Art style (realistic, cartoon, anime, etc.)")
    size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024"
    quality: Literal["standard", "hd"] = "standard"
    count: int = Field(1, ge=1, le=4, description="Number of images to generate")
    negative_prompt: Optional[str] = Field(None, description="What to avoid in the image")

class ImageVariationRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded source image")
    prompt: Optional[str] = Field(None, description="Variation guidance")
    provider: Literal["openai", "gemini"] = "openai"
    count: int = Field(1, ge=1, le=4)

class ImageEditRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded source image")
    mask_base64: Optional[str] = Field(None, description="Base64 encoded mask (transparent areas will be edited)")
    prompt: str = Field(..., description="What to add/change")
    provider: Literal["openai", "gemini"] = "openai"

# ============================================================================
# PROVIDER IMPLEMENTATIONS
# ============================================================================

async def generate_with_openai(prompt: str, size: str, quality: str, count: int) -> dict:
    """Generate images using OpenAI gpt-image-1"""
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=EMERGENT_LLM_KEY)
        
        response = await client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            quality=quality,
            n=count,
            response_format="b64_json"
        )
        
        images = []
        for img_data in response.data:
            images.append({
                "data": img_data.b64_json,
                "format": "base64_png",
                "revised_prompt": getattr(img_data, 'revised_prompt', prompt)
            })
        
        return {
            "provider": "openai",
            "model": "gpt-image-1",
            "images": images,
            "status": "success"
        }
    except Exception as e:
        return {"provider": "openai", "error": str(e), "status": "failed"}

async def generate_with_gemini(prompt: str, style: Optional[str] = None) -> dict:
    """Generate images using Gemini Nano Banana"""
    try:
        # Gemini Nano Banana integration via emergent
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        # Enhance prompt for better image generation
        enhanced_prompt = f"""Generate a highly detailed image description for:
{prompt}
{f'Style: {style}' if style else ''}

Provide a vivid, detailed visual description including:
- Main subject and composition
- Colors and lighting
- Background and environment  
- Mood and atmosphere
- Fine details and textures

Make it specific enough for image generation."""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"nano-banana-{uuid.uuid4().hex[:8]}",
            system_message="You are an expert at creating vivid image descriptions for AI image generators."
        ).with_model("google", "gemini-2.0-flash")
        
        response = await chat.send_message(UserMessage(text=enhanced_prompt))
        enhanced_description = response.content if hasattr(response, 'content') else str(response)
        
        # Try actual image generation with Imagen via Gemini
        try:
            import google.generativeai as genai
            genai.configure(api_key=EMERGENT_LLM_KEY)
            
            # Use Imagen model if available
            imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
            result = await asyncio.to_thread(
                imagen.generate_images,
                prompt=enhanced_description,
                number_of_images=1
            )
            
            if result.images:
                return {
                    "provider": "gemini",
                    "model": "nano-banana/imagen-3",
                    "images": [{
                        "data": base64.b64encode(result.images[0]._pil_image.tobytes()).decode(),
                        "format": "base64_png",
                        "enhanced_prompt": enhanced_description
                    }],
                    "status": "success"
                }
        except Exception:
            pass  # Fallback to description-only mode
        
        return {
            "provider": "gemini",
            "model": "nano-banana",
            "images": [{
                "enhanced_prompt": enhanced_description,
                "format": "text_description",
                "note": "Use this enhanced prompt with any image generator"
            }],
            "status": "success",
            "mode": "prompt_enhancement"
        }
    except Exception as e:
        return {"provider": "gemini", "error": str(e), "status": "failed"}

async def generate_with_grok(prompt: str, style: Optional[str] = None) -> dict:
    """Generate images using Grok Imagine API"""
    try:
        from openai import AsyncOpenAI
        
        # Grok via xAI API
        client = AsyncOpenAI(
            api_key=EMERGENT_LLM_KEY,
            base_url="https://api.x.ai/v1"
        )
        
        full_prompt = f"{prompt}\n\nStyle: {style}" if style else prompt
        
        # Grok Imagine endpoint
        response = await client.images.generate(
            model="grok-2-vision-1212",  # Grok's image model
            prompt=full_prompt,
            n=1,
            response_format="b64_json"
        )
        
        images = []
        for img_data in response.data:
            images.append({
                "data": img_data.b64_json,
                "format": "base64_png"
            })
        
        return {
            "provider": "grok",
            "model": "grok-imagine",
            "images": images,
            "status": "success"
        }
    except Exception as e:
        # Fallback: Use Grok for prompt enhancement, then OpenAI for generation
        try:
            from openai import AsyncOpenAI
            xai_client = AsyncOpenAI(
                api_key=EMERGENT_LLM_KEY,
                base_url="https://api.x.ai/v1"
            )
            
            # Get Grok to enhance the prompt
            chat_response = await xai_client.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": "You are Grok. Create vivid, detailed image prompts."},
                    {"role": "user", "content": f"Create a detailed image generation prompt for: {prompt}"}
                ]
            )
            enhanced = chat_response.choices[0].message.content
            
            # Generate with OpenAI using Grok's enhanced prompt
            openai_result = await generate_with_openai(enhanced, "1024x1024", "standard", 1)
            if openai_result.get("status") == "success":
                openai_result["provider"] = "grok+openai"
                openai_result["grok_enhanced_prompt"] = enhanced
                return openai_result
                
        except Exception:
            pass
            
        return {"provider": "grok", "error": str(e), "status": "failed"}

# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/info")
async def get_imagine_info():
    """Get image generation pipeline information"""
    return {
        "name": "CodeDock Imagine Pipeline",
        "version": "11.0.0",
        "providers": [
            {
                "id": "openai",
                "name": "OpenAI gpt-image-1",
                "capabilities": ["generation", "variation", "editing"],
                "sizes": ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"],
                "quality": ["standard", "hd"],
                "status": "active"
            },
            {
                "id": "gemini",
                "name": "Gemini Nano Banana",
                "capabilities": ["generation", "prompt_enhancement"],
                "sizes": ["1024x1024"],
                "status": "active"
            },
            {
                "id": "grok",
                "name": "Grok Imagine",
                "capabilities": ["generation", "prompt_enhancement"],
                "sizes": ["1024x1024"],
                "status": "active"
            }
        ],
        "styles": [
            "realistic", "photorealistic", "cartoon", "anime", "watercolor",
            "oil_painting", "digital_art", "3d_render", "pixel_art", "sketch",
            "cyberpunk", "fantasy", "sci-fi", "minimalist", "abstract"
        ],
        "max_prompt_length": 4000,
        "max_images_per_request": 4
    }

@router.post("/generate")
async def generate_images(request: ImageGenerationRequest):
    """Generate images from text prompt"""
    request_id = str(uuid.uuid4())
    
    # Build full prompt with style
    full_prompt = request.prompt
    if request.style:
        full_prompt = f"{request.prompt}, {request.style} style"
    if request.negative_prompt:
        full_prompt += f". Avoid: {request.negative_prompt}"
    
    # Auto-select provider or use specified
    if request.provider == "auto":
        # Try OpenAI first (best quality), then fallback
        result = await generate_with_openai(full_prompt, request.size, request.quality, request.count)
        if result.get("status") == "failed":
            result = await generate_with_grok(full_prompt, request.style)
        if result.get("status") == "failed":
            result = await generate_with_gemini(full_prompt, request.style)
    elif request.provider == "openai":
        result = await generate_with_openai(full_prompt, request.size, request.quality, request.count)
    elif request.provider == "gemini":
        result = await generate_with_gemini(full_prompt, request.style)
    elif request.provider == "grok":
        result = await generate_with_grok(full_prompt, request.style)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {request.provider}")
    
    return {
        "id": request_id,
        "status": result.get("status", "unknown"),
        "provider": result.get("provider"),
        "model": result.get("model"),
        "images": result.get("images", []),
        "prompt": request.prompt,
        "full_prompt": full_prompt,
        "parameters": {
            "size": request.size,
            "quality": request.quality,
            "style": request.style
        },
        "error": result.get("error"),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/variation")
async def create_variation(request: ImageVariationRequest):
    """Create variations of an existing image"""
    request_id = str(uuid.uuid4())
    
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=EMERGENT_LLM_KEY)
        
        # Decode base64 image
        image_bytes = base64.b64decode(request.image_base64)
        
        response = await client.images.create_variation(
            image=image_bytes,
            n=request.count,
            size="1024x1024",
            response_format="b64_json"
        )
        
        variations = []
        for img_data in response.data:
            variations.append({
                "data": img_data.b64_json,
                "format": "base64_png"
            })
        
        return {
            "id": request_id,
            "status": "success",
            "provider": "openai",
            "variations": variations,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit")
async def edit_image(request: ImageEditRequest):
    """Edit an image with a mask and prompt"""
    request_id = str(uuid.uuid4())
    
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=EMERGENT_LLM_KEY)
        
        image_bytes = base64.b64decode(request.image_base64)
        mask_bytes = base64.b64decode(request.mask_base64) if request.mask_base64 else None
        
        kwargs = {
            "image": image_bytes,
            "prompt": request.prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }
        if mask_bytes:
            kwargs["mask"] = mask_bytes
        
        response = await client.images.edit(**kwargs)
        
        return {
            "id": request_id,
            "status": "success",
            "provider": "openai",
            "edited_image": {
                "data": response.data[0].b64_json,
                "format": "base64_png"
            },
            "prompt": request.prompt,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhance-prompt")
async def enhance_prompt(prompt: str, style: Optional[str] = None, provider: str = "grok"):
    """Enhance a prompt for better image generation"""
    request_id = str(uuid.uuid4())
    
    enhancement_prompt = f"""Create an enhanced, detailed image generation prompt based on:

Original: {prompt}
{f'Style: {style}' if style else ''}

Create a vivid, specific prompt that includes:
1. Main subject with precise details
2. Composition and framing
3. Lighting and atmosphere
4. Color palette
5. Background elements
6. Mood and emotion
7. Technical aspects (depth of field, angle, etc.)

Output only the enhanced prompt, no explanations."""

    try:
        if provider == "grok":
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=EMERGENT_LLM_KEY, base_url="https://api.x.ai/v1")
            response = await client.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": "You are an expert at creating detailed image prompts."},
                    {"role": "user", "content": enhancement_prompt}
                ]
            )
            enhanced = response.choices[0].message.content
        else:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"enhance-{uuid.uuid4().hex[:8]}",
                system_message="You are an expert at creating detailed image prompts."
            ).with_model("openai", "gpt-4o")
            response = await chat.send_message(UserMessage(text=enhancement_prompt))
            enhanced = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "id": request_id,
            "original_prompt": prompt,
            "enhanced_prompt": enhanced,
            "style": style,
            "provider": provider,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
