# Оксана Арсенова, 41-я когорта - финальный проект. Инженер по тестированию расширенный
import pytest
import data
import sender_stand_request

class TestOrderCreation:
    """
    Тест-сьют для проверки создания заказа и получения его по треку
    """
    
    def test_create_and_get_order_by_track(self):
        """
        Тест проверяет сценарий:
        1. Создание заказа
        2. Сохранение номера трека
        3. Получение заказа по треку
        4. Проверка кода ответа 200
        """
        # Шаг 1: Выполнить запрос на создание заказа
        create_response = sender_stand_request.create_order(data.order_body)
        
        # Проверяем, что заказ успешно создан (код 201 или 200)
        assert create_response.status_code in [200, 201], \
            f"Ожидался код 200 или 201, получен {create_response.status_code}"
        
        # Шаг 2: Сохранить номер трека заказа
        track_id = create_response.json().get("track")
        assert track_id is not None, "Трек заказа не получен в ответе"
        
        # Шаг 3: Выполнить запрос на получение заказа по треку
        get_response = sender_stand_request.get_order_by_track(track_id)
        
        # Шаг 4: Проверить, что код ответа равен 200
        assert get_response.status_code == 200, \
            f"Ожидался код 200, получен {get_response.status_code}"
        
        # Дополнительная проверка: убедимся, что получен корректный заказ
        order_data = get_response.json()
        assert order_data.get("order") is not None, "Данные заказа не получены"
        
        # Проверяем, что данные заказа соответствуют созданному
        order_info = order_data.get("order")
        assert order_info.get("firstName") == data.order_body["firstName"], \
            "Имя заказчика не совпадает"
        assert order_info.get("phone") == data.order_body["phone"], \
            "Телефон заказчика не совпадает"

    def test_get_order_with_invalid_track(self):
        """
        Негативный тест: попытка получения заказа с несуществующим треком
        """
        invalid_track = 999999999
        response = sender_stand_request.get_order_by_track(invalid_track)
        
        # Ожидаем код 404 (Not Found) для несуществующего заказа
        assert response.status_code == 404, \
            f"Для несуществующего трека ожидался код 404, получен {response.status_code}"

# Дополнительно можно добавить параметризованный тест
@pytest.mark.parametrize("color", [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
])
def test_create_order_with_different_colors(color):
    """Тест создания заказа с разными цветами самоката"""
    # Создаем копию тела заказа и изменяем цвет
    order_with_color = data.order_body.copy()
    order_with_color["color"] = color
    
    response = sender_stand_request.create_order(order_with_color)
    
    assert response.status_code in [200, 201], \
        f"Не удалось создать заказ с цветом {color}"
    
    track_id = response.json().get("track")
    assert track_id is not None, "Трек не получен"

if __name__ == "__main__":
    pytest.main(["-v", "create_order_test.py"])