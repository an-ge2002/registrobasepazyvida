import tkinter as tk
from tkinter import messagebox
import bcrypt
from db_connector import create_connection
import subprocess
import sys
import os
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado para manejar imágenes
from main import MainApp  # Importar MainApp para poder instanciarla

# Definir roles en el código
user_roles = {
    "admin": "admin",
    "user": "user",
    "user1": "user",
    # Agrega más usuarios y sus roles según sea necesario
}

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ingresar")
        self.master.geometry("400x500")  # Aumentar el tamaño para acomodar la imagen
        self.master.resizable(False, False)
        self.master.configure(bg="#FFFFFF")  # Color de fondo blanco

        # Establecer el ícono de la ventana
        self.master.iconbitmap('C:/Users/PC/Desktop/registrobasepazyvida/app/img/logo.ico')

        # Estilo de la ventana
        self.frame = tk.Frame(self.master, padx=10, pady=10, bg="#FFFFFF")  # Fondo blanco
        self.frame.pack(padx=10, pady=10)

        # Etiqueta de título
        self.title_label = tk.Label(self.frame, text="Iniciar Sesión", font=("Helvetica", 16), bg="#FFFFFF", fg="#003366")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Etiqueta y entrada para el nombre de usuario
        self.username_label = tk.Label(self.frame, text="Usuario:", bg="#FFFFFF", fg="#003366")
        self.username_label.grid(row=1, column=0, sticky='w')
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1)

        # Etiqueta y entrada para la contraseña
        self.password_label = tk.Label(self.frame, text="Contraseña:", bg="#FFFFFF", fg="#003366")
        self.password_label.grid(row=2, column=0, sticky='w')
        self.password_entry = tk.Entry(self.frame, show='*')
        self.password_entry.grid(row=2, column=1)

        # Botón de inicio de sesión
        self.login_button = tk.Button(self.frame, text="Iniciar Sesión", command=self.login, bg="#FF0000", fg="#FFFFFF")
        self.login_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        # Botón de salir
        self.exit_button = tk.Button(self.frame, text="Salir", command=self.master.quit, bg="#FF0000", fg="#FFFFFF")
        self.exit_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Vincular la tecla "Enter" al método de inicio de sesión
        self.master.bind('<Return>', lambda event: self.login())

        # Cargar y mostrar la imagen
        self.load_image()

    def load_image(self):
        # Cargar la imagen
        image_path = 'C:/Users/PC/Desktop/registrobasepazyvida/app/img/logo.png'  # Cambia esto por la ruta correcta de tu imagen
        self.image = Image.open(image_path)
        self.image = self.image.resize((250, 250), Image.LANCZOS)  # Redimensionar la imagen
        self.photo = ImageTk.PhotoImage(self.image)

        # Crear etiqueta para la imagen
        self.image_label = tk.Label(self.master, image=self.photo, bg="#FFFFFF")
        self.image_label.pack(pady=(10, 0))

        # Texto debajo de la imagen
        self.footer_label = tk.Label(self.master, text="Base Paz y Vida Ciudad el Sol", bg="#FFFFFF",  font=("Times New Roman", 16), fg="#003366")
        self.footer_label.pack()


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_user(username, password)

    def login_user(self, username, password):
        connection = create_connection()
        cursor = connection.cursor()

        # Consultar el hash de la contraseña en la base de datos
        sql = "SELECT password FROM login WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        if result:
            stored_hash = result[0].encode('utf-8')  # Obtener el hash de la contraseña y convertir a bytes
            # Verificar la contraseña
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                self.master.destroy()  # Cerrar la ventana de login
                self.open_main(username)  # Ejecuta main.py con el nombre de usuario
            else:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
        else:
            messagebox.showerror("Error", "Nombre de usuario no encontrado.")

        cursor.close()
        connection.close()

    def open_main(self, username):
        root = tk.Tk()
        app = MainApp(root, username)  # Pasa la nueva instancia de Tk y el nombre de usuario
        root.mainloop()  # Inicia el bucle principal de la nueva ventana
        
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()