import os
import json
from app.utils.groq_client import groq_client
from app.schema.ai_schema import SummaryResult
from dotenv import load_dotenv
from typing import Optional, cast
from app.core.logger import logger

load_dotenv()

model = cast(str, os.getenv("SUMMARIZATION_MODEL"))
prompt = cast(str, os.getenv("SUMMARIZATION_PROMPT"))

def summarize_audio_service(text: str) -> Optional[SummaryResult]:
    try:
        response = groq_client.chat.completions.create(
        model=model,
        reasoning_effort="low",
        messages=[
            {"role": "system", "content": prompt.replace("\\n", "\n")},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        )
        raw_content = response.choices[0].message.content
        if raw_content is None:
            logger.error(f"AI response is null.")
            return None

    except Exception as e:
        logger.error(f"failed to generate summary and action items: {e}")
        return None

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError as e:
        logger.error(f"Groq returned invalid JSON: {e} | raw: {raw_content}")
        return None

    if "summary" not in parsed or "action_items" not in parsed:
        logger.error(f"Groq JSON missing expected keys | raw: {raw_content}")
        return None

    logger.info(f"summary from {model}: {parsed}")

    return SummaryResult(
        summary=parsed["summary"],
        action_items=parsed["action_items"],
    )