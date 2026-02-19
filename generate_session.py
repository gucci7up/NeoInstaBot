import instaloader
import getpass
import os

def generate_session():
    print("=== Generador de Sesión de Instagram para NeoInstaBot ===")
    username = input("Ingresa tu usuario de Instagram: ")
    password = getpass.getpass("Ingresa tu contraseña de Instagram: ")

    L = instaloader.Instaloader()
    
    try:
        print(f"Intentando iniciar sesión como {username}...")
        L.login(username, password)
        print("¡Login exitoso!")
        
        filename = f"session-{username}"
        L.save_session_to_file(filename=filename)
        
        full_path = os.path.abspath(filename)
        print(f"\nArchivo de sesión guardado en: {full_path}")
        print("\nPASOS SIGUIENTES:")
        print(f"1. Ve a tu panel de Dokploy -> Volúmenes (o File Manager).")
        print(f"2. Navega a la carpeta '/app/session/'.")
        print(f"3. Sube este archivo '{filename}' a esa carpeta.")
        print(f"4. Reinicia el bot.")
        
    except Exception as e:
        print(f"\nError durante el login: {e}")
        print("Asegúrate de no tener 2FA activado o revisa si Instagram te pidió verificación en tu celular.")

if __name__ == "__main__":
    generate_session()
