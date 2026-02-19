# Telegram Instagram Downloader Bot

Bot de Telegram profesional para descargar contenido de Instagram (imágenes, videos, carousels) de manera automática.

## 🚀 Características

- **Descarga Automática**: Detecta enlaces de Instagram y descarga el contenido.
- **Soporte Multimedia**: Imágenes, videos y álbumes.
- **Seguro**: Autenticación de administrador y manejo seguro de credenciales.
- **Producción**: Listo para desplegar con Docker y Dokploy.
- **Rate Limiting**: Protección contra abuso (5 descargas/minuto por usuario).
- **Cuentas Privadas**: Soporte para descargar contenido de cuentas privadas (si el bot las sigue).

## 🛠️ Requisitos

- Python 3.11+
- Docker (opcional, recomendado)
- Cuenta de Instagram (para el bot)
- Token de Bot de Telegram (conseguido en @BotFather)

## ⚙️ Configuración

1.  **Clonar el repositorio**:
    ```bash
    git clone <repo_url>
    cd project
    ```

2.  **Configurar Variables de Entorno**:
    Copia el archivo de ejemplo y edítalo:
    ```bash
    cp .env.example .env
    ```
    
    Edita `.env` con tus datos:
    ```env
    TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    ADMIN_TELEGRAM_ID=123456789
    IG_USERNAME=mi_usuario_bot_ig
    IG_PASSWORD=mi_password_seguro
    DOMAIN=mi-dominio.com
    PORT=8080
    ```

## 🐳 Despliegue con Docker

### Construir y Correr
```bash
docker build -t insta-bot .
docker run -d --env-file .env -p 8080:8080 --name insta-bot insta-bot
```

### Usando Dokploy
1.  **Crear Proyecto**: En tu panel de Dokploy, crea una nueva aplicación (Application) o usa Docker Compose.
2.  **Repositorio**: Conecta este repositorio de GitHub.
3.  **Variables de Entorno (Environment)**:
    *   Ve a la pestaña **"Environment"** de tu aplicación en Dokploy.
    *   Copia el contenido de tu archivo `.env` local (o usa los valores de `.env.example`).
    *   Pégalos allí. Asegúrate de que `PORT` coincida con el puerto interno (8080).
4.  **Despliegue**: Haz clic en "Deploy".

## 💻 Ejecución Local (Sin Docker)

1.  Crear entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

2.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3.  Ejecutar:
    ```bash
    python -m app.main
    ```

## 📝 Comandos del Bot

- `/start`: Inicia el bot y muestra mensaje de bienvenida.
- `/help`: Muestra instrucciones de uso.
- `/status`: (Solo Admin) Muestra estado de la conexión con Instagram.

## ⚠️ Nota Legal y Responsabilidad

Este bot ha sido desarrollado con fines **únicamente educativos**. 
El usuario es responsable de respetar los derechos de autor y la privacidad de los contenidos descargados.
No utilices este software para descargar contenido sin autorización del propietario.

---
Generado con ❤️ por Antigravity
