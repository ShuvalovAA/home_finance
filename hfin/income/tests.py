import pytest


class TestIncome:
    """Класс тестирования функционала, связанного с объектом Income."""
    @pytest.mark.asyncio
    def test_get_ok(self, mocker):
        """Тестируем получения объекта объекта."""
        request_mock = mocker.Mock()
        request_mock.method = 'GET'
        request_mock.GET.get('id').return_value = 1
        request_mock.GET.get('user_id').return_value = 1
        
        income_objects_mock = mocker.patch('income.views.Income')
        income_objects_mock.get.return_value = mocker.Mock()
        
        model_to_dict_mock = mocker.patch('income.views.model_to_dict')
        model_to_dict_mock.return_value = {'test': 'test'}
        
        get_mock = mocker.patch('income.views.get')
        
        result = get_mock(request_mock)
        
        import pdb
        pdb.set_trace()
        