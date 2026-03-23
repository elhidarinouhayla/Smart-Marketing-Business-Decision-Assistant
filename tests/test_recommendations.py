import pytest
from fastapi import HTTPException
from backend.app.api.recommendations import generate_recommendation
from backend.app.models.recommendation import Recommendation


def test_generate_recommendation(mocker):
    mock_db = mocker.Mock()

    mock_gemini_result = mocker.Mock()
    mock_gemini_result.retention_plan = [
        "Augmenter le budget",
        "Cibler une audience" 
    ]

    mocker.patch("backend.app.api.recommendations.retention_gemini", 
                 return_value=mock_gemini_result)

    from backend.app.api.recommendations import generate_recommendation
    mock_data = mocker.Mock(campaign_id="123", probability=0.3, prediction=0)
    response = generate_recommendation(data=mock_data, db=mock_db, user={"sub": "nouhayla"})

    assert "Augmenter le budget" in response.advice_text
    assert "Cibler une audience" in response.advice_text 