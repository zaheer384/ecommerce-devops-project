# 🛒 E-commerce Product API

A RESTful API for managing products in an e-commerce system, built with Flask and PostgreSQL.

## 📋 Features

- ✅ Create, Read, Update, Delete (CRUD) products
- ✅ RESTful API endpoints
- ✅ PostgreSQL database
- ✅ Docker containerized
- ✅ Health check endpoint
- ✅ Web UI for product management

## 🛠️ Technologies Used

- **Backend**: Python 3.9, Flask
- **Database**: PostgreSQL 14
- **Containerization**: Docker, Docker Compose
- **Web Server**: Gunicorn
- **Database Driver**: psycopg2

## 📁 Project Structure

```
ecommerce-devops-project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Multi-container setup
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed
- Docker Compose installed
- Git installed

### Installation & Running

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ecommerce-devops-project
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Web UI: http://localhost:5001
   - API: http://localhost:5001/api/products
   - Health Check: http://localhost:5001/health

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

## 📡 API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products |
| GET | `/api/products/:id` | Get product by ID |
| POST | `/api/products` | Create new product |
| PUT | `/api/products/:id` | Update product |
| DELETE | `/api/products/:id` | Delete product |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check application and database health |

### Example API Requests

**Create a product:**
```bash
curl -X POST http://localhost:5001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "price": 999.99,
    "description": "Latest Apple smartphone",
    "stock": 50
  }'
```

**Get all products:**
```bash
curl http://localhost:5001/api/products
```

**Get product by ID:**
```bash
curl http://localhost:5001/api/products/1
```

**Update a product:**
```bash
curl -X PUT http://localhost:5001/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "price": 1099.99,
    "description": "Pro version with better camera",
    "stock": 30
  }'
```

**Delete a product:**
```bash
curl -X DELETE http://localhost:5001/api/products/1
```

## 🗄️ Database Schema

### Products Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key (auto-increment) |
| name | VARCHAR(100) | Product name |
| price | DECIMAL(10,2) | Product price |
| description | TEXT | Product description |
| stock | INTEGER | Available stock quantity |

## 🔧 Development

### View logs:
```bash
docker-compose logs -f app
```

### Access database:
```bash
docker exec -it product-database psql -U postgres productsdb
```

### Rebuild after code changes:
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## 🌐 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_HOST | localhost | Database hostname |
| DB_PORT | 5432 | Database port |
| DB_NAME | productsdb | Database name |
| DB_USER | postgres | Database user |
| DB_PASS | password | Database password |

## 📝 License

This project is for educational purposes.

## 👥 Author

DevOps Team

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request