import pytest
from income.handlers import get_object
from income.models import Income


class TestIncomeHandlersMethods:
    """Класс тестирования функционала, связанного с объектом Income."""
    def test_get_ok(self, mocker):
        """Тестируем получения объекта объекта."""
        rigth_name = 'test'
        mock_value = 1

        request_mock = mocker.Mock()
        request_mock.method = 'GET'
        request_mock.GET.get.return_value = mock_value

        income_objects_mock = mocker.patch('income.handlers.Income')
        income_objects_item_mock = mocker.Mock()
        income_objects_item_mock.name = rigth_name
        income_objects_mock.objects.get.return_value = income_objects_item_mock

        result = get_object(request_mock)

        # проверяем, что атрибут name не мутировал
        assert result.name == rigth_name
        # проверяем, что метод Income.objects.get был вызван с нужными параметрами
        income_objects_mock.objects.get.assert_called_once_with(pk=mock_value, user_id=mock_value)

    def test_get_error(self, mocker):
        """Тестируем возбуждения исключени при получении объекта объекта."""
        request_mock = mocker.Mock()
        request_mock.method = 'GET'
        request_mock.GET.get('id').return_value = 1
        request_mock.GET.get('user_id').return_value = 1

        income_objects_mock = mocker.patch('income.handlers.Income')
        income_objects_item_mock = mocker.Mock()
        income_objects_item_mock.name = 'test'
        income_objects_mock.objects.get.side_effect = Income.DoesNotExist()

        with pytest.raises(Income.DoesNotExist):
            result = get_object(request_mock)
