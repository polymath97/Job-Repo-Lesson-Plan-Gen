import json
import pytest
import requests

def test_generate_response_output_is_valid_json():
    '''
    test if the container generate a valid json object format
    '''
    
    url = "http://localhost:5000/generate-response"

    # provide mock data to test the generate response function
    data = {
        "topic": "heat transfer simulation",
        "subject": "Science",
        "grade": "middle",
        "student_profile": "",
        "tech_domain": ""
    }

    # Make a POST request to your API
    response = requests.post(url, json=data, timeout=120)
    
    # Check if the response has a 200 status code
    assert response.status_code == 200

    # Check if the response is a valid JSON
    try:
        json.loads(response.text)
    except json.JSONDecodeError:
        pytest.fail("Output is not a valid JSON object")


