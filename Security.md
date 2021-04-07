# Возможные уязвимости и варианты их предотвращения
## 1. SQL-уязвимости.
 	1.1 В форме логина, регистрации;
 	1.2 В форме создания объявления;
 	1.3 Поиске объявления.
 ### Решение:
 Использование проверенного фреймворк Django, который предоставляет свой интерфейс для работы с БД MySQL, и сами мы напрямую с БД не взаимодействуем, исключает возникновение SQL-уязвимостей ввиду неправильного обращения с БД.

## 2. XSS-уязвимости. 
	2.1 В форме создания объявления(вредоносный JS-код, которы будет сохранен и отображен другим пользователям).
 ### Решение:
 Экранирование вводимых пользователем данных. Необходимо проверять, что содержимое является простым текстом, а не исполняемым кодом.

## 3. Раскрытие конфиденциальных данных.
    3.1 Логины/пароли пользователей;
    3.2 Содержимое директорий и файлов на сервере с веб-приложением.
 ### Решение:
 Закрыть доступ ко внутренним ресурсам.
 [Пример:](https://stackoverflow.com/questions/43271275/django-restrict-static-folder-access-to-non-logged-in-users)
 ```python
 from django.http import HttpResponseForbidden
  from whitenoise.middleware import WhiteNoiseMiddleware
  class ProtectedStaticFileMiddleware(WhiteNoiseMiddleware):
        def process_request(self, request):
             check user authentication
            if condition_met(request):
               return super(WhiteNoiseMiddleware, self).process_request(request)
            # condition false
            return HttpResponseForbidden("you are not authorized")
 ```
 
## 4. Переход в личные кабинеты пользователей в обход аутентификации, простая аутентификация.
 ### Решение:
 Использование модуля HTTPS в Django.
 Хранение хэшей от паролей в БД, а при аутентификации считать хэш от введённого пользователем пароля и сравнивать с имеющимся хэшем
