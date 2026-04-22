import pytest
from app import app

@pytest.fixture
def client():
    """Configura o client de testes do Flask."""
    app.config['TESTING'] = True

    # Cria o client de testes
    with app.test_client() as client:
        # Precisamos de um contexto de aplicação para rodar url_for, etc.
        with app.app_context():
            yield client
