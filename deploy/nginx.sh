#!/bin/bash
set -euo pipefail

# Скрипт настраивает Nginx по IP (без домена), берёт переменные из .env, лежащего рядом.

# === Загрузка переменных из .env ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "${SCRIPT_DIR}/.env" ]]; then
  echo "Файл .env не найден рядом со скриптом: ${SCRIPT_DIR}/.env"
  exit 1
fi

set -a
source "${SCRIPT_DIR}/.env"
set +a

# Обязательные переменные в .env:
: "${IP:?Укажи IP в .env, напр. IP=93.189.228.24}"
: "${APP_PORT:?Укажи порт backend, напр. APP_PORT=8000}"
: "${NGINX_MEDIA_DIR:?Укажи путь к медиа, напр. NGINX_MEDIA_DIR=/opt/star-burger/media}"
: "${NGINX_STATIC_DIR:?Укажи путь к статике, напр. NGINX_STATIC_DIR=/opt/star-burger/static}"

# Необязательные с дефолтами
SITE_NAME="${SITE_NAME:-starburger}"
SITE_PATH="/etc/nginx/sites-available/${SITE_NAME}"
ENABLED_LINK="/etc/nginx/sites-enabled/${SITE_NAME}"

# === Установка Nginx ===
sudo apt update
sudo apt install -y nginx

# === Конфиг Nginx (HTTP по IP) ===
sudo tee "$SITE_PATH" >/dev/null <<EOF
server {
    listen ${IP}:80;
    server_name _;

    # Проксирование всего трафика к приложению
    location / {
        include /etc/nginx/proxy_params;
        proxy_pass http://127.0.0.1:${APP_PORT};
    }

    # Опционально: если API отделён путём
    location /api/ {
        include /etc/nginx/proxy_params;
        proxy_pass http://127.0.0.1:${APP_PORT}/api/;
    }

    # Отдача медиа/статики с диска
    location /media/ {
        alias ${NGINX_MEDIA_DIR}/;
        autoindex off;
    }

    location /static/ {
        alias ${NGINX_STATIC_DIR}/;
        autoindex off;
    }
}
EOF

# === Активация сайта ===
sudo ln -snf "$SITE_PATH" "$ENABLED_LINK"
sudo rm -f /etc/nginx/sites-enabled/default || true

# === Проверка и перезапуск ===
sudo nginx -t
sudo systemctl reload nginx

echo "✅ Готово: http://${IP} → 127.0.0.1:${APP_PORT}"
echo "   Конфиг: ${SITE_PATH}"
