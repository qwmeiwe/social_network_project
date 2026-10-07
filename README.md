# Микросервисная социальная сеть (Микроблогинг)

## Сфера приложения
Проект представляет собой минималистичную социальную сеть для молодежи и локальных комьюнити. Главная ценность — строго хронологическая лента без алгоритмов, возможность вступления в неформальные "кланы" по выбранному эмодзи-аватару при регистрации, и удобная система дискуссий (по умолчанию отображается только один самый популярный комментарий).

## Архитектурная схема взаимодействия

```mermaid
graph TD
    Client(Клиент / Frontend)

    subgraph Микросервисы
        IdentityAPI[Identity Service]
        ContentAPI[Content Service]
    end

    subgraph Базы_данных [Базы данных]
        DB1[(Identity DB: Users, Clans)]
        DB2[(Content DB: Posts, Likes)]
    end

    Client -->|Публичная сеть: Авторизация| IdentityAPI
    Client -->|Публичная сеть: Лента и посты| ContentAPI

    IdentityAPI -.->|Внутренняя сеть: Проверка профиля| ContentAPI

    IdentityAPI -->|Внутреннее подключение| DB1
    ContentAPI -->|Внутреннее подключение| DB2
```

## ER-диаграмма базы данных (Content Service)

```mermaid
erDiagram
    POSTS {
        uuid id PK
        varchar(50) author_id
        varchar(10) clan_emoji "Эмодзи клана автора"
        text content
        timestamp created_at
    }
    
    COMMENTS {
        uuid id PK
        uuid post_id FK
        varchar(50) author_id
        text content
        int likes_count "Для вывода топ-комментария"
        timestamp created_at
    }
    
    LIKES {
        uuid id PK
        uuid post_id FK
        varchar(50) user_id
        varchar(10) clan_emoji "Эмодзи клана лайкнувшего"
        timestamp created_at
    }
    
    BOOKMARKS {
        uuid id PK
        uuid post_id FK
        varchar(50) user_id "Кто сохранил"
        timestamp created_at
    }

    POSTS ||--o{ COMMENTS : "содержит"
    POSTS ||--o{ LIKES : "получает"
    POSTS ||--o{ BOOKMARKS : "сохраняется в"
```