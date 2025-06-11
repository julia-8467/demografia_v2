import os

APP_ENV = os.getenv('APP_ENV', 'development')

# Dane produkcyjne
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'julia')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'Owieczka003')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'demografia.postgres.database.azure.com')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')

# Dane testowe (osobna baza na testy)
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'postgres_test')
