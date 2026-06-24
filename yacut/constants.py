# Константы для валидации custom_id
CUSTOM_ID_MAX_LENGTH = 16
CUSTOM_ID_PATTERN = r'^[a-zA-Z0-9]+$'

# Ключи в JSON-запросах
URL_KEY = 'url'
CUSTOM_ID_KEY = 'custom_id'

# Зарезервированные short_id
RESERVED_SHORT_IDS = ('files',)

# Константы для модели URLMap
ORIGINAL_URL_MAX_LENGTH = 256
SHORT_ID_MAX_LENGTH = 16

# Константы для генерации short_id
SHORT_ID_LENGTH = 6