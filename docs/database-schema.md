# Database Schema

## Overview

This document outlines the database schema for the StokTok API. The schema is designed to support a scalable, real-time stock watchlist system capable of handling the millions of users it will surely have.

## Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Watchlist : has
    Watchlist ||--o{ WatchlistItem : contains
    WatchlistItem }o--|| Security : references
    
    User {
        int id PK
        string username UK
        string email
        string password
        string first_name
        string last_name
    }
    
    Watchlist {
        int id PK
        int user_id FK
        string name
        datetime created_at
        datetime updated_at
    }
    
    WatchlistItem {
        int id PK
        int watchlist_id FK
        int security_id FK
        datetime added_at
    }
    
    Security {
        int id PK
        string ticker UK
        string name
        decimal last_price
        string currency
        string exchange
        datetime last_updated
    }
```

## Table Descriptions

### User

This `User` table is provided by Django's built-in authentication system.

| Column     | Type         | Constraints           |
|------------|--------------|------------------------|
| id         | INTEGER      | PRIMARY KEY            |
| username   | VARCHAR(150) | UNIQUE, NOT NULL       |
| email      | VARCHAR(254) | NOT NULL               |
| password   | VARCHAR(128) | NOT NULL               |
| first_name | VARCHAR(150) |                        |
| last_name  | VARCHAR(150) |                        |

### Security

Stores information about individual stocks and ETFs.

| Column       | Type           | Constraints                |
|--------------|----------------|----------------------------|
| id           | INTEGER        | PRIMARY KEY                |
| ticker       | VARCHAR(20)    | UNIQUE, NOT NULL           |
| name         | VARCHAR(255)   | NOT NULL                   |
| last_price   | DECIMAL(11, 2) |                            |
| currency     | CHAR(3)        | DEFAULT 'USD'              |
| exchange     | VARCHAR(50)    |                            |
| last_updated | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP  |

Indexes:

- `ticker_idx` on (`ticker`)

### Watchlist

Represents a user's watchlist.

| Column     | Type         | Constraints                               |
|------------|--------------|-------------------------------------------|
| id         | INTEGER      | PRIMARY KEY                               |
| user_id    | INTEGER      | FOREIGN KEY (User.id), NOT NULL           |
| name       | VARCHAR(100) | DEFAULT 'Default'                         |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                 |
| updated_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE       |

Indexes:

- `user_id_idx` on (`user_id`)

Constraints:

- UNIQUE (`user_id`, `name`)

### WatchlistItem

Represents the many-to-many relationship between Watchlist and Security.

| Column       | Type      | Constraints                          |
|--------------|-----------|--------------------------------------|
| id           | INTEGER   | PRIMARY KEY                          |
| watchlist_id | INTEGER   | FOREIGN KEY (Watchlist.id), NOT NULL |
| security_id  | INTEGER   | FOREIGN KEY (Security.id), NOT NULL  |
| added_at     | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP            |

Indexes:

- `watchlist_id_idx` on (`watchlist_id`)
- `security_id_idx` on (`security_id`)

Constraints:

- UNIQUE (`watchlist_id`, `security_id`)

## Design Considerations

1. **Scalability**: The schema is designed to handle millions of users, each with multiple watchlists.
2. **Performance**:
   - Appropriate indexes are added to optimize common query patterns.
   - `CharField` is used instead of `TextField` for fixed-length fields to improve database performance.
3. **Data Integrity**:
   - Unique constraints prevent duplicate entries in watchlists and securities.
   - Foreign key constraints ensure referential integrity.
4. **Flexibility**: The design allows users to have multiple named watchlists.
5. **Real-time Updates**: The `last_updated` field in the Security table facilitates efficient price updates without affecting the watchlist structure.
