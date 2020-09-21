Артем Терехов – «Бот ВКонтакте «Напоминания»»

Пользовательские сценарии

Группа 10И4

Электронная почта
[terehov2004year@yandex.ru](mailto:terehov2004year@yandex.ru)

VK [vk.com/aterehov2015](http://vk.com/aterehov2015)

# Сценарий 1 - Регистрация
1.      Пользователь открывает диалог с ботом и пишет ему любое сообщение.
2.      Бот проверяет, зарегистрирован ли пользователь; если нет, то приветствует пользователя и предлагает ему написать «Начать» для регистрации.
3.      Пользователь отправляет «Начать».
4.      Если пользователь написал «Начать», то бот выводит список часовых поясов и просит пользователя выбрать часовой пояс под нужным номером; если нет, то бот снова отправляет приветствие.
5.      Пользователь отправляет номер часового пояса.
6.      Если пользователь отправил верный номер часового пояса, то бот сохраняет регистрационные данные пользователя; если нет, то бот предупреждает пользователя об этом и просит его выбрать часовой пояс еще раз.
7.      Бот сообщает пользователю о завершении регистрации и переходит к сценарию «Отображение главного меню».

# Сценарий 2 – Отображение главного меню
1.      Пользователь пишет боту любое сообщение.
2.      Бот проверяет, зарегистрирован ли пользователь.
3.      Если пользователь зарегистрирован, бот предлагает ему выбрать действие из списка: изменить часовой пояс, добавить напоминание, просмотреть список напоминаний.
4.      Пользователь выбирает нужное действие.
5.      Бот проверяет наличие введенного действия.
6.      Если пользователь выбрал существующее действие, бот переходит к соответствующему сценарию. 
7.      Если такого действия нет, бот сообщает ему об этом и предлагает заново выбрать пункт меню.

# Сценарий 3 - Изменение часового пояса
1.      Бот выводит список часовых поясов и вариант для отмены изменений.
2.      Пользователь выбирает нужный вариант.
3.      Если пользователь выбрал неверный вариант, бот сообщает ему об этом и просит выбрать заново.
4.      Если пользователь выбрал вариант отмены, бот переходит к сценарию «Отображение главного меню».
5.      Если пользователь выбрал часовой пояс, бот изменяет часовой пояс пользователя и время отправки всех установленных напоминаний в соответствии с выбором пользователя.
6.      Бот уведомляет пользователя об изменении часового пояса и просит написать сообщение.
7.      Бот переходит к сценарию «Отображение главное меню».
# Сценарий 4 - Добавление напоминания
1.      Бот запрашивает у пользователя текст напоминания или предлагает ему отменить действие и сообщает условия, которым должен удовлетворять текст.
2.      Пользователь вводит текст напоминания.
3.      Бот проверяет, удовлетворяет ли текст условиям. Если нет, бот сообщает пользователю об этом и просит выбрать другой текст.
4.      Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
5.      Бот просит ввести время отправки первого напоминания и сообщает условия, которым должно удовлетворять время. Также сообщается вариант для отмены.
6.      Пользователь вводит время отправки первого напоминания.
7.      Бот проверяет время на соответствие условиям. Если условия не выполнены, бот сообщает пользователю об этом и просит ввести время еще раз.
8.      Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
9.      Бот просит ввести частоту повторения напоминания и сообщает условия, которым она должна удовлетворять, или предлагает отменить действие.
10.  Пользователь вводит частоту повторения напоминания.
11.  Бот проверяет частоту на соответствие условиям. Если нет, бот сообщает пользователю об этом и просит ввести частоту еще раз.
12.  Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
13.  Бот сохраняет введенные пользователем данные с учетом его часового пояса и добавляет его в список напоминаний для отправки, затем переходит к сценарию «Отображение главного меню».
# Сценарий 5 - Просмотр списка напоминаний
1.      Бот выводит список напоминаний пользователя и предлагает выбрать напоминание для изменения либо отменить действие.
2.      Пользователь вводит номер напоминания для изменения.
3.      Если пользователь выбрал отмену действия, бот переходит к сценарию «Отображение главного меню».
4.      Бот спрашивает, хочет ли пользователь изменить или удалить напоминание или отменить действие.
5.      Пользователь вводит желаемое действие.
6.      Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
7.      Запускается сценарий «Изменение и удаление напоминания».
# Сценарий 6 - Изменение и удаление напоминания
1.      Если выбрано удаление напоминания: бот спрашивает, уверен ли пользователь, что ему нужно удалить напоминание.
2.      Пользователь подтверждает действие или отменяет его.
3.      Если пользователь подтверждает удаление, бот удаляет напоминание.
4.      Если пользователь выбрал другой вариант, бот уведомляет его об этом и предлагает ввести свой выбор заново.
5.      Бот возвращается к сценарию «Отображение главного меню».
6.      Если выбрано изменение напоминания: бот просит ввести новый текст напоминания или оставить его без изменений, либо отменить действие.
7.      Пользователь вводит новый текст напоминания.
8.      Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
9.      Если пользователь ввел неверный текст, бот сообщает об этом и просит ввести текст заново.
10.  Бот просит пользователя ввести новое время первого напоминания или оставить его без изменений, либо отменить действие.
11.  Пользователь вводит новое время первого напоминания.
12.  Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
13.  Если пользователь ввел неверное время, бот сообщает об этом и просит ввести другое время.
14.  Бот просит ввести новую частоту повторения напоминания или оставить ее без изменения, либо отменить действие.
15.  Пользователь вводит новую частоту повторения напоминания.
16.  Если пользователь выбрал отмену, бот переходит к сценарию «Отображение главного меню».
17.  Если пользователь ввел неверную частоту, бот уведомляет его об этом и просит ввести другую частоту.
18.  Бот сохраняет изменения с учетом часового пояса пользователя и возвращается к сценарию «Отображение главного меню».
# Сценарий 7 - Отправка уведомления о напоминании (выполняется без участия пользователя)
1.      Бот ждет, когда наступит время отправки первого напоминания.
2.      Бот отправляет напоминание нужному пользователю.
3.      Бот проверяет, нужно ли повторять напоминание.
4.      Если да, бот планирует повтор этого напоминания.
5.      Если нет, бот удаляет его.
6.      Бот ищет следующее напоминание в списке напоминаний.
7.      Бот повторяет данный сценарий для следующего напоминания.

Взаимодействие с пользователем с помощью личных сообщений осуществляется во
всех сценариях
