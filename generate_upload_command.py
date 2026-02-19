import base64
import os
import glob

def generate_command():
    # Buscar archivos de sesión
    session_files = glob.glob("session-*")
    if not session_files:
        print("Error: No se encontró ningún archivo 'session-usuario' en esta carpeta.")
        print("Por favor, asegura que ya ejecutaste 'generate_session.py' y el archivo existe.")
        return

    # Usar el primero que encuentre o preguntar si hay varios
    session_file = session_files[0]
    print(f"Generando comando para el archivo: {session_file}")

    try:
        with open(session_file, "rb") as f:
            content = f.read()
            b64_content = base64.b64encode(content).decode("utf-8")

        # Comando para Linux (Dokploy/Docker container)
        # Usamos python para decodificar porque a veces 'base64' CLI no está o tiene opciones distintas
        cmd = (
            f"mkdir -p /app/session && "
            f"echo \"{b64_content}\" | base64 -d > /app/session/{session_file}"
        )

        print("\n=== COPIA EL SIGUIENTE COMANDO ===")
        print("Ve a la pestaña 'Console', 'Terminal' o 'Shell' de tu aplicación en Dokploy y pega esto:")
        print("-" * 20)
        print(cmd)
        print("-" * 20)
        print("\nDespués de pegarlo y dar Enter, reinicia la aplicación.")

    except Exception as e:
        print(f"Error leyendo el archivo: {e}")

if __name__ == "__main__":
    generate_command()
