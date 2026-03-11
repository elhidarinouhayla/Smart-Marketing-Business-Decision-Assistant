from google import genai
from pathlib import Path
import sys

# Standard absolute imports assuming the root is in PYTHONPATH
try:
    from backend.app.config import GEMINI_API_KEY
    from backend.app.schemas.gemini_schema import output_gemini
except ImportError:
    # Fallback for local testing if running from within backend/app
    try:
        from app.config import GEMINI_API_KEY
        from app.schemas.gemini_schema import output_gemini
    except ImportError:
        from ..config import GEMINI_API_KEY
        from ..schemas.gemini_schema import output_gemini


def retention_gemini(probability, prediction):

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Contexte :
    Un modèle de Machine Learning a prédit la probabilité de succès d'une campagne marketing
    pour un client donné.

    Probabilité de conversion : {probability}
    Prédiction du modèle : {prediction}

    Interprétation :
    - Si la probabilité est faible (<0.4) → la campagne a peu de chance de réussir.
    - Si la probabilité est moyenne (0.4 - 0.7) → la campagne peut être améliorée.
    - Si la probabilité est élevée (>0.7) → la campagne est efficace mais peut être optimisée.

    Tâche :
    Propose 6 décisions marketing concrètes pour :
    - améliorer la campagne si la probabilité est faible
    - optimiser la campagne si elle est moyenne
    - maximiser la conversion si elle est élevée

    Les décisions doivent être simples et directement applicables par une équipe marketing.

    Format de réponse attendu :

    "retention_plan": [
        "- action marketing 1",
        "- action marketing 2",
        "- action marketing 3",
        "- action marketing 4",
        "- action marketing 5",
        "- action marketing 6"
    ]
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": output_gemini.model_json_schema()
        }
    )

    output = output_gemini.model_validate_json(response.text)

    return output


# # Test
# probability = 0.25
# prediction = 0

# result = retention_gemini(probability, prediction)

# print(result)