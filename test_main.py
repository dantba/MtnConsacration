import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_form():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Consagração a Jesus por Maria" in response.text

@pytest.mark.asyncio
async def test_generate_pdf():
    data = {
        "name": "Daniel Araújo",
        "pdf_template": "nsa_sra_aparecida.pdf"
    }
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/generate_consacration_file/", data=data)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert response.headers["Content-Disposition"].startswith("attachment")
    assert "daniel_consagracao_nsa_sra_aparecida.pdf" in response.headers["Content-Disposition"]
