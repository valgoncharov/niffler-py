import json
import logging

import allure
from faker import Faker
from python_test.data_helpers.api_helpers import UserApiHelper
from python_test.model.db.user import UserName
from python_test.report_helper import Epic, Story


@allure.epic(Epic.app)
@allure.story(Story.kafka)
class TestKafka:

    @allure.title("Проверить что есть сообщение в кафке после успешной регистрации пользователя")
    def test_massage_should_be_produce_to_kafka_after_successful_registration(self, kafka, envs):
        username = Faker().user_name()
        password = Faker().password()

        topic_partitions = kafka.subscribe_listen_new_offsets("users")

        with allure.step('Зарегистрировать нового пользователя'):
            auth_client = UserApiHelper(envs)
            result = auth_client.create_user(username, password)
            assert result.status_code == 201

        event = kafka.log_msg_and_json(topic_partitions)

        with allure.step("Проверить что сообщение есть в кафке"):
            assert event != '' and event != b''

        with allure.step("Проверить что сообщение содержит правильные данные"):
            UserName.model_validate(json.loads(event.decode('utf8')))
            assert json.loads(event.decode('utf8'))['username'] == username

    @allure.title('Проверить что приложение забирает сообщение из топика Kafka')
    def test_app_should_consume_message_from_kafka(self, kafka, userdata_db):
        with allure.step('Отправить сообщение в Kafka'):
            user_name_for_msg = Faker().user_name()
            logging.info(
                f'Отправить сообщение по пользователю: {user_name_for_msg}')
            kafka.send_message("users", user_name_for_msg)
        with allure.step('Убедиться, что в таблице userdata есть запись о пользователе из сообщения'):
            user_from_db = userdata_db.get_user(username=user_name_for_msg)
            assert user_from_db.username == user_name_for_msg
