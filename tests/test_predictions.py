import pytest
from fastapi import HTTPException
from backend.app.services.ml_service import predict
from backend.app.api.predictions import run_prediction 


def test_prediction(mocker):
    mock_db = mocker.Mock()
    mock_campaign = mocker.Mock(id="8000")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_campaign

    mocker.patch("backend.app.api.predictions.predict", 
                 return_value={"prediction": 1, "probability": 0.88})

    mock_data = mocker.Mock()
    mock_data.campaign_id = "8000"
    mock_data.model_dump.return_value = {
        "Age": 56, "Income": 136000, "AdSpend": 5000,
        "Gender": "Male", "CampaignChannel": "Email", "CampaignType": "Awareness"
    }

    from backend.app.api.predictions import run_prediction
    response = run_prediction(data=mock_data, db=mock_db, user={"sub": "nouhayla"})

    assert response["prediction"] == 1
    assert response["success"] is True