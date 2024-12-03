import tkinter as tk
from tkinter import messagebox, ttk, font
from db_connector import create_connection
from tkcalendar import DateEntry
import time
from datetime import datetime  # Asegúrate de importar datetime

class UserCRUDApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Registro de Usuarios")
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.create_widgets()  # Crea los widgets
        self.update_time()  # Inicia la actualización del reloj
        self.master.state('zoomed')  # Maximiza la ventana (solo en Windows)
        self.read_users()  # Cargar los usuarios al iniciar la aplicación

       # Establecer el ícono de la ventana
        self.master.iconbitmap('C:/Users/PC/Desktop/registrobasepazyvida/app/img/logo.ico') 

    def validate_length(self, input_value, max_length):
        """Validar la longitud de la entrada."""
        try:
            max_length = int(max_length)  # Asegúrate de que max_length sea un entero
        except ValueError:
            return False  # Si no se puede convertir a entero, retorna False

        return len(input_value) <= max_length

    def validate_entries(self):
        """Verifica si solo el campo de CI está lleno para habilitar el botón de registrar."""
        ci = self.ci_entry.get()

        # Habilitar el botón de registrar solo si el campo de CI no está vacío
        if ci:
            self.create_button.config(state=tk.NORMAL)  # Habilitar el botón de registrar
        else:
            self.create_button.config(state=tk.DISABLED)  # Deshabilitar el botón de registrar

    def validate_email(self, input_value):
        """Validar el correo electrónico."""
        if input_value == "":
            return True
        return "@" in input_value and len(input_value) <= 70

    def validate_datetime(self, fecha, hora):
        try:
            # Intenta combinar y parsear la fecha y la hora
            datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
        
    def get_sexo_options(self):
        """Devuelve las opciones de sexo desde el ENUM de la base de datos."""
        return ["Masculino", "Femenino", "No Especificado"]

    def get_estado_civil_options(self):
        """Devuelve las opciones de estado civil desde el ENUM de la base de datos."""
        return ["Soltero", "Casado", "Viudo", "Divorciado"]

    def get_visitante_options(self):
        """Devuelve las opciones de visitante desde el ENUM de la base de datos."""
        return ["Si", "No"]

    def get_actividad_options(self):
        """Devuelve las opciones de actividad desde la base de datos."""
        try:
            self.cursor.execute("SELECT Nombre FROM actividades")
            return [row[0] for row in self.cursor.fetchall()]  # Suponiendo que 'Nombre' es la columna que deseas
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener actividades: {e}")
            return []

    def get_taller_options(self):
        """Devuelve las opciones de taller desde la base de datos."""
        try:
            self.cursor.execute("SELECT Nombre FROM talleres")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener talleres: {e}")
            return []

    def get_juego_options(self):
        """Devuelve las opciones de juego desde la base de datos."""
        try:
            self.cursor.execute("SELECT Nombre FROM juegosdeportivos")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener juegos: {e}")
            return []

    def get_charla_options(self):
        """Devuelve las opciones de charla desde la base de datos."""
        try:
            self.cursor.execute("SELECT Nombre FROM charlas")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener charlas: {e}")
            return []

    def get_curso_options(self):
        """Devuelve las opciones de curso desde la base de datos."""
        try:
            self.cursor.execute("SELECT Nombre FROM cursos")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener cursos: {e}")
            return []

    def on_double_click(self, event):
        """Maneja el evento de doble clic en el Treeview."""
        # Obtener la fila seleccionada
        item = self.tree.selection()[0]  # Obtiene el ID del elemento seleccionado
        user_data = self.tree.item(item, 'values')  # Obtiene los valores de la fila seleccionada

        # Llenar los campos de entrada con los datos del usuario
        self.ci_entry.delete(0, tk.END)
        self.ci_entry.insert(0, user_data[0])  # CI
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, user_data[1])  # Nombre
        self.fecha_nac_entry.delete(0, tk.END)
        self.fecha_nac_entry.insert(0, user_data[2])  # Fecha de nacimiento
        self.sexo_combo.set(user_data[3])  # Sexo
        self.estado_civil_combo.set(user_data[4])  # Estado Civil
        self.direccion_entry.delete(0, tk.END)
        self.direccion_entry.insert(0, user_data[5])  # Dirección
        self.telefono_entry.delete(0, tk.END)
        self.telefono_entry.insert(0, user_data[6])  # Teléfono
        self.correo_entry.delete(0, tk.END)
        self.correo_entry.insert(0, user_data[7])  # Correo
        self.visitante_combo.set(user_data[9])  # Visitante

        # Aquí se deben agregar los valores de actividad, taller, juego, charla y curso
        self.actividad_combo.set(user_data[10] if user_data[10] is not None else 'No aplica')  # Actividad
        self.taller_combo.set(user_data[11] if user_data[11] is not None else 'No aplica')  # Taller
        self.juego_combo.set(user_data[12] if user_data[12] is not None else 'No aplica')  # Juego
        self.charla_combo.set(user_data[13] if user_data[13] is not None else 'No aplica')  # Charla
        self.curso_combo.set(user_data[14] if user_data[14] is not None else 'No aplica')  # Curso

                # Limpiar el campo de búsqueda
        self.buscar_ci_entry.delete(0, tk.END)

        # Actualizar la lista de usuarios
        self.read_users()

        # Habilitar el botón de eliminar
        self.delete_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.NORMAL)

    def create_widgets(self):
        # Crear un marco para los datos del usuario
        self.data_frame = tk.Frame(self.master)
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Entradas para los datos del usuario
        self.ci_label = tk.Label(self.data_frame, text="CI Usuario:")
        self.ci_label.grid(row=0, column=0, sticky='w')
        self.ci_entry = tk.Entry(self.data_frame, validate="key")
        self.ci_entry['validatecommand'] = (self.ci_entry.register(self.validate_length), '%P', 10)
        self.ci_entry.grid(row=0, column=1)
        self.ci_entry.bind("<KeyRelease>", lambda event: self.validate_entries())  # Vincular evento

        self.nombre_label = tk.Label(self.data_frame, text="Nombre y Apellido:")
        self.nombre_label.grid(row=1, column=0, sticky='w')
        self.nombre_entry = tk.Entry(self.data_frame, validate="key")
        self.nombre_entry['validatecommand'] = (self.nombre_entry.register(self.validate_length), '%P', 150)
        self.nombre_entry.grid(row=1, column=1)

        self.fecha_nac_label = tk.Label(self.data_frame, text="Fecha de Nacimiento:")
        self.fecha_nac_label.grid(row=2, column=0, sticky='w')
        self.fecha_nac_entry = DateEntry(self.data_frame, date_pattern='yyyy-mm-dd')  # Asegúrate de usar el formato yyyy-mm-dd
        self.fecha_nac_entry.grid(row=2, column=1)

        # Sexo
        self.sexo_label = tk.Label(self.data_frame, text="Sexo:")
        self.sexo_label.grid(row=3, column=0, sticky='w')
        self.sexo_combo = ttk.Combobox(self.data_frame)
        self.sexo_combo['values'] = self.get_sexo_options()
        self.sexo_combo.set(self.get_sexo_options()[0])  # Establecer la primera opción como predeterminada
        self.sexo_combo.grid(row=3, column=1)

        # Estado Civil
        self.estado_civil_label = tk.Label(self.data_frame, text="Estado Civil:")
        self.estado_civil_label.grid(row=4, column=0, sticky='w')
        self.estado_civil_combo = ttk.Combobox(self.data_frame)
        self.estado_civil_combo['values'] = self.get_estado_civil_options()
        self.estado_civil_combo.set(self.get_estado_civil_options()[0])  # Establecer la primera opción como predeterminada
        self.estado_civil_combo.grid(row=4, column=1)

        self.direccion_label = tk.Label(self.data_frame, text="Dirección:")
        self.direccion_label.grid(row=5, column=0, sticky='w')
        self.direccion_entry = tk.Entry(self.data_frame, validate="key")
        self.direccion_entry['validatecommand'] = (self.direccion_entry.register(self.validate_length), '%P', 200)
        self.direccion_entry.grid(row=5, column=1)

        self.telefono_label = tk.Label(self.data_frame, text="Teléfono:")
        self.telefono_label.grid(row=6, column=0, sticky='w')
        self.telefono_entry = tk.Entry(self.data_frame, validate="key")
        self.telefono_entry['validatecommand'] = (self.telefono_entry.register(self.validate_length), '%P', 14)
        self.telefono_entry.grid(row=6, column=1)

        self.correo_label = tk.Label(self.data_frame, text="Correo:")
        self.correo_label.grid(row=7, column=0, sticky='w')
        self.correo_entry = tk.Entry(self.data_frame, validate="key")
        self.correo_entry['validatecommand'] = (self.correo_entry.register(self.validate_email), '%P')
        self.correo_entry.grid(row=7, column=1)

        # Configurar el evento de enfoque para completar automáticamente el correo
        self.correo_entry.bind("<FocusIn>", self.auto_complete_email)

        self.fecha_entrada_label = tk.Label(self.data_frame, text="Fecha de Entrada:")
        self.fecha_entrada_label.grid(row=8, column=0, sticky='w')
        self.fecha_entrada_entry = DateEntry(self.data_frame, date_pattern='yyyy-mm-dd')
        self.fecha_entrada_entry.grid(row=8, column=1)

        self.hora_label = tk.Label(self.data_frame, text="Hora de Entrada:") 
        self.hora_label.grid(row=8, column=2, sticky='w') 
        self.hora_entry = tk.Entry(self.data_frame) 
        self.hora_entry.grid(row=8, column=3)

        # Label para mostrar la hora actual 
        self.current_time_label = tk.Label(self.data_frame, text="", font=("Helvetica", 12)) 
        self.current_time_label.grid(row=8, column=4, padx=5)  # Asegúrate de que esta línea esté presente

        # Visitante
        self.visitante_label = tk.Label(self.data_frame, text="Visitante:")
        self.visitante_label.grid(row=9, column=0, sticky='w')
        self.visitante_combo = ttk.Combobox(self.data_frame)
        self.visitante_combo['values'] = self.get_visitante_options()
        self.visitante_combo.set(self.get_visitante_options()[0])  # Establecer la primera opción como predeterminada
        self.visitante_combo.grid(row=9, column=1)

        # Actividad
        self.actividad_label = tk.Label(self.data_frame, text="Actividad:")
        self.actividad_label.grid(row=10, column=0, sticky='w')
        self.actividad_combo = ttk.Combobox(self.data_frame)
        self.actividad_combo['values'] = self.get_actividad_options() + ['No aplica']  # Añadir 'No aplica'
        self.actividad_combo.set('No aplica')  # Establecer 'No aplica' como opción predeterminada
        self.actividad_combo.grid(row=10, column=1)

        # Taller
        self.taller_label = tk.Label(self.data_frame, text="Taller:")
        self.taller_label.grid(row=11, column=0, sticky='w')
        self.taller_combo = ttk.Combobox(self.data_frame)
        self.taller_combo['values'] = self.get_taller_options() + ['No aplica']  # Añadir 'No aplica'
        self.taller_combo.set('No aplica')  # Establecer 'No aplica' como opción predeterminada
        self.taller_combo.grid(row=11, column=1)

        # Juego
        self.juego_label = tk.Label(self.data_frame, text="Juego:")
        self.juego_label.grid(row=12, column=0, sticky='w')
        self.juego_combo = ttk.Combobox(self.data_frame)
        self.juego_combo['values'] = self.get_juego_options() + ['No aplica']  # Añadir 'No aplica'
        self.juego_combo.set('No aplica')  # Establecer 'No aplica' como opción predeterminada
        self.juego_combo.grid(row=12, column=1)

        # Charla
        self.charla_label = tk.Label(self.data_frame, text="Charla:")
        self.charla_label.grid(row=13, column=0, sticky='w')
        self.charla_combo = ttk.Combobox(self.data_frame)
        self.charla_combo['values'] = self.get_charla_options() + ['No aplica']  # Añadir 'No aplica'
        self.charla_combo.set('No aplica')  # Establecer 'No aplica' como opción predeterminada
        self.charla_combo.grid(row=13, column=1)

        # Curso
        self.curso_label = tk.Label(self.data_frame, text="Curso:")
        self.curso_label.grid(row=14, column=0, sticky='w')
        self.curso_combo = ttk.Combobox(self.data_frame)
        self.curso_combo['values'] = self.get_curso_options() + ['No aplica']  # Añadir 'No aplica'
        self.curso_combo.set('No aplica')  # Establecer 'No aplica' como opción predeterminada
        self.curso_combo.grid(row=14, column=1)

        self.buscar_ci_label = tk.Label(self.data_frame, text="Buscar por CI:")
        self.buscar_ci_label.grid(row=17, column=0, sticky='w')
        self.buscar_ci_entry = tk.Entry(self.data_frame)
        self.buscar_ci_entry.grid(row=17, column=1)

        # Botón de buscar
        self.buscar_button = tk.Button(self.data_frame, text="Buscar", command=self.buscar_usuario)
        self.buscar_button.grid(row=17, column=2, pady=5)

        # Botones para CRUD
        self.create_button = tk.Button(self.data_frame, text="Registrar", command=self.confirm_create_user)
        self.create_button.grid(row=15, column=0, pady=5)
        self.create_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de registrar

        self.read_button = tk.Button(self.data_frame, text="Actualizar lista", command=self.read_users)
        self.read_button.grid(row=15, column=1, pady=5)

        self.update_button = tk.Button(self.data_frame, text="Modificar", command=self.confirm_update_user)
        self.update_button.grid(row=16, column=0, pady=5)
        self.update_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de modificar

        self.delete_button = tk.Button(self.data_frame, text="Eliminar", command=self.confirm_delete_user)
        self.delete_button.grid(row=16, column=1, pady=5)
 
        # Inicialmente deshabilitar el botón de eliminar
        self.delete_button.config(state=tk.DISABLED)

        # Crear un marco para el Treeview y la barra de desplazamiento
        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Crear el Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=("CI", "Nombre", "Nacimiento", "Sexo", "Estado Civil", "Dirección", "Teléfono", "Correo", "Fecha Entrada", "Visitante", "Actividad", "Taller", "Juego", "Charla", "Curso"), show='headings')

        # Definir el encabezado de las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Configurar el Treeview para que se expanda
        self.tree.grid(row=0, column=0, sticky='nsew')  # Asegúrate de que el Treeview se expanda

        # Vincular el evento de doble clic
        self.tree.bind("<Double-1>", self.on_double_click)

        # Crear la barra de desplazamiento vertical
        self.scrollbar_y = tk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')  # Coloca la barra de desplazamiento a la derecha
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)  # Vincular la barra de desplazamiento vertical al Treeview

        # Crear la barra de desplazamiento horizontal
        self.scrollbar_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky='ew', columnspan=2)  # Coloca la barra de desplazamiento en la parte inferior
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)  # Vincular la barra de desplazamiento horizontal al Treeview

        # Configurar el grid para expandir
        self.tree_frame.grid_rowconfigure(0, weight=1)  # Permitir que la fila 0 se expanda
        self.tree_frame.grid_columnconfigure(0, weight=1)  # Permitir que la columna 0 se expanda

        # Configurar la ventana principal para que se expanda
        self.master.grid_rowconfigure(0, weight=1)  # Permitir que la fila 0 se expanda
        self.master.grid_columnconfigure(0, weight=1)  # Permitir que la columna 0 se expanda

    def buscar_usuario(self):
        ci_busqueda = self.buscar_ci_entry.get()
        
        # Limpiar el Treeview antes de cargar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            self.cursor.execute("SELECT * FROM usuarios WHERE CIusuario = %s", (ci_busqueda,))
            row = self.cursor.fetchone()

            if row:
                # Reemplazar None con "Nulo"
                row_with_nulo = [value if value is not None else "No aplica" for value in row]
                self.tree.insert("", "end", values=row_with_nulo)
            else:
                messagebox.showinfo("Resultado", "No se encontró ningún usuario con ese CI.")
        except Exception as e:

            messagebox.showerror("Error", f"Error al buscar el usuario: {e}")

    def auto_complete_email(self, event):
        # Completar automáticamente el campo de correo con "example@"
        if self.correo_entry.get() == "":
            self.correo_entry.insert(0, "example@")

    def update_time(self):
        """Actualiza la etiqueta con la hora actual."""
        current_time = datetime.now().strftime("%H:%M:%S")  # Obtiene la hora actual en formato HH:MM:SS
        self.current_time_label.config(text=current_time)  # Actualiza la etiqueta con la hora
        self.master.after(1000, self.update_time)  # Llama a este método nuevamente después de 1000 ms (1 segundo)
        
    def clear_entries(self):
        """Limpia todos los campos de entrada."""
        self.ci_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.fecha_nac_entry.delete(0, tk.END)
        self.sexo_combo.set('')  # O puedes usar un valor por defecto
        self.estado_civil_combo.set('')  # O puedes usar un valor por defecto
        self.direccion_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.correo_entry.delete(0, tk.END)
        self.fecha_entrada_entry.delete(0, tk.END)
        self.visitante_combo.set('')  # O puedes usar un valor por defecto
        self.actividad_combo.set('No aplica')  # O puedes usar un valor por defecto
        self.taller_combo.set('No aplica')  # O puedes usar un valor por defecto
        self.juego_combo.set('No aplica')  # O puedes usar un valor por defecto
        self.charla_combo.set('No aplica')  # O puedes usar un valor por defecto
        self.curso_combo.set('No aplica')  # O puedes usar un valor por defecto
        self.buscar_ci_entry.delete(0, tk.END)
    
    def adjust_column_widths(self):
        """Ajusta el ancho de las columnas del Treeview según el contenido."""
        for col in self.tree["columns"]:
            max_width = 0
            # Obtener el ancho del encabezado de la columna
            header_width = len(col) * 10  # Aproximar el ancho del encabezado
            max_width = max(max_width, header_width)

            # Iterar sobre las filas para encontrar el ancho máximo
            for row in self.tree.get_children():
                item = self.tree.item(row)
                value = item['values'][self.tree["columns"].index(col)]
                max_width = max(max_width, len(str(value)) * 10)  # Aproximar el ancho del contenido

            self.tree.column(col, width=max_width, anchor='w', minwidth=max_width)  # Ajustar el ancho

    def read_users(self):
        # Limpiar el Treeview antes de cargar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            self.cursor.execute("SELECT * FROM usuarios")
            rows = self.cursor.fetchall()

            for row in rows:
                # Reemplazar None con "Nulo"
                row_with_nulo = [value if value is not None else "No aplica" for value in row]
                self.tree.insert("", "end", values=row_with_nulo)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los usuarios: {e}")
        
        self.adjust_column_widths()  # Ajusta los anchos de las columnas          

    def confirm_create_user(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea registrar este usuario?"):
            self.create_user()  # Llama al método original para crear el usuario

    def confirm_update_user(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea modificar este usuario?"):
            self.update_user()  # Llama al método original para modificar el usuario

    def confirm_delete_user(self):
        if not self.tree.selection():
            messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este usuario?"):
            self.delete_user()  # Llama al método original para eliminar el usuario
      
    def create_user(self):
        ci = self.ci_entry.get()
        nombre = self.nombre_entry.get()
        fecha_nac = self.fecha_nac_entry.get()
        sexo = self.sexo_combo.get()
        estado_civil = self.estado_civil_combo.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        fecha_entrada = self.fecha_entrada_entry.get()
        visitante = self.visitante_combo.get()
        hora_entrada_str = self.hora_entry.get()  # Captura la hora de entrada

        # Combinar fecha y hora en un objeto datetime
        try:
            fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")  # Asegúrate de que la fecha esté en el formato correcto
            hora_entrada = datetime.strptime(hora_entrada_str, "%H:%M:%S").time()  # Asegúrate de que la hora esté en el formato correcto
            datetime_entrada = datetime.combine(fecha_entrada_dt, hora_entrada)  # Combina fecha y hora
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de fecha o hora incorrecto: {ve}")
            return

        # Verificar si cada campo es nulo
        actividad = self.actividad_combo.get() if self.actividad_combo.get() != 'No aplica' else None
        taller = self.taller_combo.get() if self.taller_combo.get() != 'No aplica' else None
        juego = self.juego_combo.get() if self.juego_combo.get() != 'No aplica' else None
        charla = self.charla_combo.get() if self.charla_combo.get() != 'No aplica' else None
        curso = self.curso_combo.get() if self.curso_combo.get() != 'No aplica' else None

        # Validar el correo electrónico
        if correo and "@" not in correo:
            messagebox.showerror("Error", "El correo electrónico debe contener el símbolo '@'.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO usuarios (CIusuario, Nombreyapellido, FechaNacimiento, Sexo, EstadoCivil, Direccion, Telefono, Correo, Fechaentrada, Visitante, Actividad, Taller, Juego, Charla, Curso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ci, nombre, fecha_nac, sexo, estado_civil, direccion, telefono, correo, datetime_entrada, visitante, actividad, taller, juego, charla, curso))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Usuario creado exitosamente.")

            # Limpiar los campos de entrada
            self.clear_entries()  # Llama al método para limpiar los campos
            self.read_users()  # Actualizar la lista de usuarios

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el usuario: {e}")

    def update_user(self):
        ci = self.ci_entry.get()  # CI del usuario a actualizar
        nombre = self.nombre_entry.get()
        fecha_nac = self.fecha_nac_entry.get()
        sexo = self.sexo_combo.get()
        estado_civil = self.estado_civil_combo.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        fecha_entrada = self.fecha_entrada_entry.get()
        hora_entrada_str = self.hora_entry.get()  # Captura la hora de entrada
        visitante = self.visitante_combo.get()

        # Combinar fecha y hora en un objeto datetime
        try:
            fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")  # Asegúrate de que la fecha esté en el formato correcto
            hora_entrada = datetime.strptime(hora_entrada_str, "%H:%M:%S").time()  # Asegúrate de que la hora esté en el formato correcto
            datetime_entrada = datetime.combine(fecha_entrada_dt, hora_entrada)  # Combina fecha y hora
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de fecha o hora incorrecto: {ve}")
            return

        # Manejar los valores que pueden ser nulos
        actividad = self.actividad_combo.get() if self.actividad_combo.get() != 'No aplica' else None
        taller = self.taller_combo.get() if self.taller_combo.get() != 'No aplica' else None
        juego = self.juego_combo.get() if self.juego_combo.get() != 'No aplica' else None
        charla = self.charla_combo.get() if self.charla_combo.get() != 'No aplica' else None
        curso = self.curso_combo.get() if self.curso_combo.get() != 'No aplica' else None


        # Actualizar el usuario
        try:
            self.cursor.execute("""
                UPDATE usuarios 
                SET Nombreyapellido = %s, FechaNacimiento = %s, Sexo = %s, EstadoCivil = %s, Direccion = %s, Telefono = %s, Correo = %s, Fechaentrada = %s, Visitante = %s, Actividad = %s, Taller = %s, Juego = %s, Charla = %s, Curso = %s
                WHERE CIusuario = %s
            """, (nombre, fecha_nac, sexo, estado_civil, direccion, telefono, correo, datetime_entrada, visitante, actividad, taller, juego, charla, curso, ci))
            
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el usuario: {e}")

        self.clear_entries()  # Llama al método para limpiar los campos
        self.read_users()  # Actualizar la lista de usuarios después de la eliminación
        
    def delete_user(self):
        ci = self.ci_entry.get()  # CI del usuario a eliminar
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE CIusuario = %s", (ci,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
            self.read_users()  # Volver a cargar los usuarios después de la eliminación
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el usuario: {e}")
        
        self.clear_entries()  # Llama al método para limpiar los campos
        self.read_users()  # Actualizar la lista de usuarios después de la eliminación

    def close_connection(self):
        """Cierra la conexión a la base de datos y destruye la ventana."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.master.destroy()  # Cierra la ventana

if __name__ == "__main__":
    root = tk.Tk()
    app = UserCRUDApp(root)
    app.read_users()  # Cargar los usuarios al iniciar la aplicación
    root.wm_minsize(800, 400)  # Establece el tamaño mínimo de la ventana
    root.protocol("WM_DELETE_WINDOW", app.close_connection)  # Asegúrate de cerrar la conexión al salir
    root.mainloop()