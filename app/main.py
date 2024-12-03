import tkinter as tk
from tkinter import messagebox
import pandas as pd 
from PIL import Image, ImageTk  
from db_connector import create_connection
from ventanausuarios import UserCRUDApp
from ventanaactividades import ActividadCRUDApp
from ventanacharlas import CharlasCRUDApp
from ventanacursos import CursosCRUDApp
from ventanaempleados import EmpleadosCRUDApp
from ventanajuegosdeportivos import JuegosdeportivosCRUDApp
from ventanatalleres import TalleresCRUDApp

class MainApp:
    def __init__(self, master, username):
        self.master = master
        self.username = username  # Guardar el nombre de usuario
        self.master.title("Menú")
        self.master.geometry("600x400")
        
        # Cambiar el fondo de la ventana
        self.master.configure(bg="#FFFFFF")

        # Crear la barra de menú
        self.menu_bar = tk.Menu(self.master)

        # Crear el menú "Archivo"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Cerrar", command=self.master.quit)
        self.file_menu.add_command(label="Minimizar", command=self.master.iconify)

        # Agregar el menú "Archivo" a la barra de menú
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)

        # Crear el menú "Información"
        self.info_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.info_menu.add_command(label="Estadísticas", command=self.show_statistics)
        self.info_menu.add_command(label="Desarrolladores", command=self.show_info)

        # Agregar el menú "Información" a la barra de menú
        self.menu_bar.add_cascade(label="Información", menu=self.info_menu)

        # Configurar la barra de menú en la ventana
        self.master.config(menu=self.menu_bar)

        # Establecer el ícono de la ventana
        self.master.iconbitmap('C:/Users/PC/Desktop/registrobasepazyvida/app/img/logo.ico')  # Cambia 'img/logo.ico' por la ruta correcta de tu ícono

        # Frame para los botones
        button_frame = tk.Frame(master, bg="#FFFFFF")
        button_frame.pack(pady=20)

        # Definir los botones
        self.user_button = tk.Button(button_frame, text="Registrar Usuarios", command=self.open_user_window, bg="#FF0000", fg="#FFFFFF", font=("Helvetica", 14, "bold"), height=2, width=20)
        self.user_button.grid(row=0, column=0, padx=10, pady=10)

        self.empleado_button = tk.Button(button_frame, text="Registrar Empleados", command=self.open_empleado_window, bg="#003366", fg="#FFFFFF", font=("Helvetica", 14, "bold"), height=2, width=20)
        self.empleado_button.grid(row=0, column=1, padx=10, pady=10)

        self.activity_button = tk.Button(button_frame, text="Registrar Actividades", command=self.open_activity_window, bg="#139A45", fg="#FFFFFF", font=("Helvetica", 12), height=2, width=20)
        self.activity_button.grid(row=1, column=0, padx=10, pady=5)

        self.charla_button = tk.Button(button_frame, text="Registrar Charlas", command=self.open_charla_window, bg="#139A45", fg="#FFFFFF", font=("Helvetica", 12), height=2, width=20)
        self.charla_button.grid(row=1, column=1, padx=10, pady=5)

        self.curso_button = tk.Button(button_frame, text="Registrar Cursos", command=self.open_curso_window, bg="#139A45", fg="#FFFFFF", font=("Helvetica", 12), height=2, width=20)
        self.curso_button.grid(row=2, column=0, padx=10, pady=5)

        self.juego_button = tk.Button(button_frame, text="Registrar Juegos", command=self.open_juego_window, bg="#139A45", fg="#FFFFFF", font=("Helvetica", 12), height=2, width=20)
        self.juego_button.grid(row=2, column=1, padx=10, pady=5)

        self.taller_button = tk.Button(button_frame, text="Registrar Talleres", command=self.open_taller_window, bg="#139A45", fg="#FFFFFF", font=("Helvetica", 12), height=2, width=20)
        self.taller_button.grid(row=3, column=0, padx=10, pady=5)

        # Llamar a la función de inicio de sesión con el nombre de usuario
        self.login_user(self.username)

        # Cargar y mostrar la imagen
        self.load_image()

    def load_image(self):
        # Cargar la imagen
        image_path = 'C:/Users/PC/Desktop/registrobasepazyvida/app/img/logo.png'
        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 100), Image.LANCZOS)  # Redimensionar la imagen
        self.photo = ImageTk.PhotoImage(self.image)

        # Crear etiqueta para la imagen
        self.image_label = tk.Label(self.master, image=self.photo, bg="#FFFFFF")
        self.image_label.pack(pady=(1, 0))

    def disable_buttons(self):
        # Deshabilitar todos los botones
        self.empleado_button.config(state=tk.DISABLED)
        self.activity_button.config(state=tk.DISABLED)
        self.charla_button.config(state=tk.DISABLED)
        self.curso_button.config(state=tk.DISABLED)
        self.juego_button.config(state=tk.DISABLED)
        self.taller_button.config(state=tk.DISABLED)

    def enable_buttons(self):
        # Habilitar todos los botones
        self.user_button.config(state=tk.NORMAL)
        self.empleado_button.config(state=tk.NORMAL)
        self.activity_button.config(state=tk.NORMAL)
        self.charla_button.config(state=tk.NORMAL)
        self.curso_button.config(state=tk.NORMAL)
        self.juego_button.config(state=tk.NORMAL)
        self.taller_button.config(state=tk.NORMAL)

    def login_user(self, username):
        if username == "admin":
            self.enable_buttons()  # Habilitar todos los botones para el administrador
            self.enable_menus()    # Habilitar todos los menús para el administrador
        elif username == "user":
            self.disable_buttons()  # Deshabilitar todos los botones para el usuario
            self.disable_menus()    # Deshabilitar todos los menús para el usuario
        else:
            self.disable_buttons()  # Deshabilitar todos los botones para otros usuarios
            self.disable_menus()    # Deshabilitar todos los menús para otros usuarios

    def enable_menus(self):
        # Habilitar el menú de estadísticas
        self.info_menu.entryconfig("Estadísticas", state=tk.NORMAL)

    def disable_menus(self):
        # Deshabilitar el menú de estadísticas
        self.info_menu.entryconfig("Estadísticas", state=tk.DISABLED)

    def show_statistics(self):
        # Crear una nueva ventana para mostrar las estadísticas
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Estadísticas")

        # Configurar la cuadrícula para que se expanda
        stats_window.grid_rowconfigure(0, weight=1)
        stats_window.grid_columnconfigure(0, weight=1)

        connection = None
        cursor = None
        result = ""  # Inicializar la variable result

        try:
            # Conectar a la base de datos y obtener estadísticas de la tabla auditoriausuarios
            connection = create_connection()  
            cursor = connection.cursor()

            # Leer los datos de la tabla
            query = "SELECT * FROM auditoriausuarios"
            df = pd.read_sql(query, connection)

            # Frecuencia de actividades
            actividades = ['Actividad', 'Taller', 'Juego', 'Charla', 'Curso']
            frecuencia_actividad = {act: df[act].notna().sum() for act in actividades}

            # Determinar la actividad más y menos frecuente
            mas_frecuente = max(frecuencia_actividad, key=frecuencia_actividad.get)
            menos_frecuente = min(frecuencia_actividad, key=frecuencia_actividad.get)

            # Determinar la asistencia por área, excluyendo "No aplica"
            df['Area'] = df.apply(lambda row: next((row[act] for act in ['Actividad', 'Taller', 'Juego', 'Charla', 'Curso'] if pd.notna(row[act])), None), axis=1)

            # Filtrar filas donde 'Area' no es None
            df = df[df['Area'].notna()]

            # Contar la asistencia por área
            asistencia_area = df['Area'].value_counts()
            area_mas_asistida = asistencia_area.idxmax()
            area_menos_asistida = asistencia_area.idxmin()

            # Construir el resultado
            result += f"Área más frecuente: {mas_frecuente} (Total: {frecuencia_actividad[mas_frecuente]})\n"
            result += f"Área menos frecuente: {menos_frecuente} (Total: {frecuencia_actividad[menos_frecuente]})\n"
            result += f"Actividad más asistida: {area_mas_asistida} (Total: {asistencia_area[area_mas_asistida]})\n"
            result += f"Actividad menos asistida: {area_menos_asistida} (Total: {asistencia_area[area_menos_asistida]})\n"

            results_label = tk.Label(stats_window, text=result, justify=tk.LEFT, font=("Helvetica", 12))
            results_label.grid(row=0, column=0, sticky='nsew', pady=20)

            # Botón para exportar a Excel
            export_button = tk.Button(stats_window, text="Exportar a Excel", command=lambda: self.export_to_excel(df))
            export_button.grid(row=1, column=0, sticky='nsew', pady=(10, 5))

            # Botón para cerrar la ventana de estadísticas
            close_button = tk.Button(stats_window, text=" Cerrar", command=stats_window.destroy)
            close_button.grid(row=2, column=0, sticky='nsew', pady=(5, 20))

            # Ajustar la ventana al contenido
            stats_window.update_idletasks()

        except Exception as e:
            error_label = tk.Label(stats_window, text=f"Ocurrió un error: {str(e)}", fg="red")
            error_label.pack(pady=20)

        finally:
            # Cerrar el cursor y la conexión si fueron creados
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
    def export_to_excel(self, df):
        """Exporta el DataFrame a un archivo Excel."""
        try:
            # Exportar a un archivo Excel
            df.to_excel("auditoria_usuarios.xlsx", index=False)
            messagebox.showinfo("Éxito", "Datos exportados a auditoria_usuarios.xlsx exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a Excel: {str(e)}")
                        
    def show_info(self):
        # Crear una nueva ventana para mostrar la información de los desarrolladores
        info_window = tk.Toplevel(self.master)
        info_window.title("Información de Desarrolladores")
        info_window.geometry("300x200")

        # Agregar un label con la información
        info_label = tk.Label(info_window, text="Desarrolladores:\n\n- Angely Gonzalez\n- Andreina Parra\n- Virginia Paz", justify=tk.LEFT)
        info_label.pack(pady=20)

        # Botón para cerrar la ventana de información
        close_button = tk.Button(info_window, text="Cerrar", command=info_window.destroy)
        close_button.pack(pady=(0, 20))

    def open_user_window(self):
        user_window = tk.Toplevel(self.master)
        UserCRUDApp(user_window)

    def open_empleado_window(self):
        empleado_window = tk.Toplevel(self.master)
        EmpleadosCRUDApp(empleado_window)

    def open_activity_window(self):
        activity_window = tk.Toplevel(self.master)
        ActividadCRUDApp(activity_window)

    def open_charla_window(self):
        charla_window = tk.Toplevel(self.master)
        CharlasCRUDApp(charla_window)

    def open_curso_window(self):
        curso_window = tk.Toplevel(self.master)
        CursosCRUDApp(curso_window)

    def open_juego_window(self):
        juego_window = tk.Toplevel(self.master)
        JuegosdeportivosCRUDApp(juego_window)

    def open_taller_window(self):
        taller_window = tk.Toplevel(self.master)
        TalleresCRUDApp(taller_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()