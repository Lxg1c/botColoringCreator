# 🎨 Coloring Book Bot

Telegram-бот, который по текстовому описанию или загруженному изображению генерирует раскраску с помощью нейросети **Stable Diffusion**.
Подходит как для детей, так и для взрослых — создавайте уникальные раскраски в один клик!

> ⚠️ **Важно:** бот — не полностью автономное решение. Для работы требуется запустить отдельный сервис с моделью генерации изображений.

---

## 📦 Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Lxg1c/botColoringCreator.git
cd coloring-book-bot
```

---

### 2. Установка зависимостей (если запускаете локально)

> Рекомендуемый способ — через Poetry

Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate  # или .\venv\Scripts\activate для Windows
```

Установите Poetry:

```bash
pip install poetry
```

Установите зависимости:

```bash
poetry install
```

---

### 3. Создайте файл `.env`

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
BOT_TOKEN=ваш_токен_от_BotFather
```

> 🔐 **Никогда не публикуйте `.env` в открытом доступе!**

---

### 4. 🚀 Запуск с помощью Docker Compose

#### Архитектура для запуска
```bash
coloring-book-bot/
├── apiColoringCreator/        # Backend-сервис генерации изображений
│   └── Dockerfile             # Dockerfile для backend
│
├── botColoringCreator/        # Telegram-бот на aiogram
│   └── Dockerfile             # Dockerfile для бота
│   └── .env                   # Переменные окружения для бота
│
├── .env                       # Конфигурация для kafka и zookeeper
│
├── docker-compose.yml         # Описание сервисов и сетей Docker
```
#### 1. Убедитесь, что установлен [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

#### 2. В корне проекта создайте `.env`, содержащий конфигурацию kafka и zookeeper:

```env
# Kafka
KAFKA_BROKER_ID=1
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-task:9092
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT
KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
KAFKA_MESSAGE_MAX_BYTES=36700160
KAFKA_REPLICA_FETCH_MAX_BYTES=36700160
KAFKA_MAX_REQUEST_SIZE=36700160
KAFKA_DEFAULT_TOPIC_MAX_MESSAGE_BYTES=36700160

# Zookeeper
ZOOKEEPER_CLIENT_PORT=2181

# Kafdrop
KAFKA_BROKERCONNECT=kafka-task:9092
```

#### 3. Так же в корне проекта создайте docker-compose.yml, содержащий конфигурацию сервисов

```docker-compose.yml
services:
  zookeeper:
    image: wurstmeister/zookeeper:latest
    container_name: zookeeper
    ports:
      - "2181:2181"
    env_file:
      - .env
    networks:
      - coloring-network

  kafka:
    image: wurstmeister/kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
    env_file:
      - .env
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_MESSAGE_MAX_BYTES: 36700160
      KAFKA_REPLICA_FETCH_MAX_BYTES: 36700160
      KAFKA_MAX_REQUEST_SIZE: 36700160
      KAFKA_DEFAULT_TOPIC_MAX_MESSAGE_BYTES: 36700160
    healthcheck:
      test: ["CMD-SHELL", "kafka-broker-api-versions.sh --bootstrap-server localhost:9092"]
      interval: 30s
      timeout: 10s
      retries: 5
    depends_on:
      - zookeeper
    networks:
      - coloring-network

  kafdrop:
    image: obsidiandynamics/kafdrop
    container_name: kafdrop
    ports:
      - "9000:9000"
    environment:
      KAFKA_BROKERCONNECT: kafka:9092
    depends_on:
      - kafka
    networks:
      - coloring-network

  bot:
    build:
      context: ./botColoringCreator
      dockerfile: Dockerfile
    container_name: tg-bot
    env_file:
      - .env
    depends_on:
      - kafka
    networks:
      - coloring-network

  backend:
    build:
      context: ./apiColoringCreator
      dockerfile: Dockerfile
    container_name: coloring-backend
    env_file:
      - .env
    depends_on:
      - kafka
    networks:
      - coloring-network


networks:
  coloring-network:
    name: coloring-network
```

#### 4. Запустите контейнеры:

```bash
docker-compose up -d --build
```

Контейнеры, которые будут запущены:

* 🧠 `backend` — сервис генерации изображений
* 🤖 `bot` — Telegram-бот
* 🐘 `kafka` и `zookeeper` — брокер сообщений
* 📊 `kafdrop` — интерфейс для просмотра Kafka (по адресу [http://localhost:9000](http://localhost:9000))

> ⚠️ Убедитесь, что порт `9092` (Kafka) и `9000` (Kafdrop) не заняты другими процессами.

---

## 🧠 Как работает бот

1. Пользователь отправляет **описание** или **изображение**.
2. Бот показывает введённые данные и предлагает подтвердить, изменить или отменить.
3. После подтверждения:

   * Бот отправляет описание или изображение в Kafka.
   * Backend-сервис принимает сообщение, генерирует раскраску и отправляет результат обратно в Kafka.
   * Бот получает готовое изображение и отправляет его пользователю.
4. Пользователь получает готовую раскраску.

---

## ⚙️ Используемые технологии

* 🤖 [`aiogram 3`](https://docs.aiogram.dev)
* 🧵 Kafka — для обмена сообщениями между ботом и backend-сервисом
* 🐳 Docker + Docker Compose — для удобного развёртывания
* 📦 Poetry — для управления зависимостями и окружением

---
