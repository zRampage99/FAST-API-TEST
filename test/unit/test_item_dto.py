import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from dto.item_dto import ItemCreate, ItemRead
from service.item_service import create_item
from entity.item import Item

def test_create_item_success():
    # Arrange
    session = MagicMock()
    item_data = ItemCreate(name="Pistola", description="Bellissima pistola", price=Decimal("1000.00"))
    expected_item = Item(id=1, name="Pistola", description="Bellissima pistola", price=Decimal("1000.00"), is_active=True)
    
    # Simula il comportamento di session.refresh per impostare l'id
    def refresh_side_effect(item):
        item.id = expected_item.id
    session.refresh.side_effect = refresh_side_effect
    print(session.refresh.side_effect)
    # Act
    result = create_item(session, item_data)

    # Assert
    assert isinstance(result, ItemRead)
    assert result.id == expected_item.id
    assert result.name == expected_item.name
    assert result.description == expected_item.description
    assert result.price == float(expected_item.price)
    assert result.is_active == expected_item.is_active

    # Verifica che i metodi della sessione siano stati chiamati correttamente
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
