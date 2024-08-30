Tests
=====

Описание тестов
---------------

В проекте используются тесты для проверки основных функций. Тесты включают:

1. Тесты для успешного GET запроса.
2. Тесты для неудачного GET запроса.
3. Тесты для успешного POST запроса.
4. Тесты для неудачного POST запроса.

Примеры тестов
--------------

### Пример 1: Тест успешного GET запроса

.. code-block:: python

   @patch('undisk.views.requests.get')
   def test_get_request_success(self, mock_get):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"_embedded": {"items": []}}'
        mock_get.return_value = mock_response

        response = self.client.get(self.url, {'public_key': 'test_key'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'undisk/index.html')
        self.assertContains(response, 'Un<span class="highlight">Disk</span>', html=True)
        self.assertContains(response, 'Public key:', html=True)


### Пример 2: Тест неудачного GET запроса

.. code-block:: python

   @patch('undisk.views.requests.get')
   def test_get_request_failure(self, mock_get):
       mock_response = requests.Response()
       mock_response.status_code = 500
       mock_get.return_value = mock_response

       response = self.client.get(self.url, {'public_key': 'test_key'})
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'undisk/index.html')
       self.assertContains(response, 'Произошла ошибка при запросе к Yandex Disk API.', html=True)


Запуск тестов
-------------

Для запуска тестов используйте следующую команду:

.. code-block:: sh

   python manage.py test


Эта команда выполнит все тесты, определенные в вашем проекте, и выведет результаты в консоль.