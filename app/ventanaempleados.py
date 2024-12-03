import tkinter as tk
from tkinter import messagebox, ttk, font
from db_connector import create_connection
from tkcalendar import DateEntry
import time
from datetime import datetime  # Asegúrate de importar datetime

class EmpleadosCRUDApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CRUD de Empleados")
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.create_widgets()  # Crea los widgets
        self.update_time()  # Inicia la actualización del reloj
        self.master.state('zoomed')  # Maximiza la ventana (solo en Windows)
        self.read_empleados()  # Cargar los empleados al iniciar la aplicación

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
        return "@" in input_value and len(input_value) <= 80

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

    def on_double_click(self, event):
        """Maneja el evento de doble clic en el Treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            return  # No hay selección, salir de la función

        item = selected_item[0]  # Obtiene el ID del elemento seleccionado
        empleado_data = self.tree.item(item, 'values')  # Obtiene los valores de la fila seleccionada

        # Asegúrate de que los índices sean correctos
        self.ci_entry.delete(0, tk.END)
        self.ci_entry.insert(0, empleado_data[0])  # CI
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, empleado_data[1])  # Nombre
        self.fecha_nac_entry.delete(0, tk.END)
        self.fecha_nac_entry.insert(0, empleado_data[2])  # Fecha de nacimiento
        self.sexo_combo.set(empleado_data[3])  # Sexo
        self.direccion_entry.delete(0, tk.END)
        self.direccion_entry.insert(0, empleado_data[4])  # Dirección
        self.telefono_entry.delete(0, tk.END)
        self.telefono_entry.insert(0, empleado_data[5])  # Teléfono
        self.correo_entry.delete(0, tk.END)
        self.correo_entry.insert(0, empleado_data[6])  # Correo
        self.cargo_entry.delete(0, tk.END)
        self.cargo_entry.insert(0, empleado_data[7])  # Cargo (verifica este índice)

        # Habilitar el botón de eliminar
        self.delete_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.NORMAL)

    def create_widgets(self):
        # Crear un marco para los datos del empleado
        self.data_frame = tk.Frame(self.master)
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Entradas para los datos del empleado
        self.ci_label = tk.Label(self.data_frame, text="CI Empleado:")
        self.ci_label.grid(row=0, column=0, sticky='w')
        self.ci_entry = tk.Entry(self.data_frame, validate="key")
        self.ci_entry['validatecommand'] = (self.ci_entry.register(self.validate_length), '%P', 11)
        self.ci_entry.grid(row=0, column=1)
        self.ci_entry.bind("<KeyRelease>", lambda event: self.validate_entries())  # Vincular evento

        self.nombre_label = tk.Label(self.data_frame, text="Nombre y Apellido:")
        self.nombre_label.grid(row=1, column=0, sticky='w')
        self.nombre_entry = tk.Entry(self.data_frame, validate="key")
        self.nombre_entry['validatecommand'] = (self.nombre_entry.register(self.validate_length), '%P', 60)
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

        self.direccion_label = tk.Label(self.data_frame, text="Dirección:")
        self.direccion_label.grid(row=4, column=0, sticky='w')
        self.direccion_entry = tk.Entry(self.data_frame, validate="key")
        self.direccion_entry['validatecommand'] = (self.direccion_entry.register(self.validate_length), '%P', 200)
        self.direccion_entry.grid(row=4, column=1)

        self.telefono_label = tk.Label(self.data_frame, text="Teléfono:")
        self.telefono_label.grid(row=5, column=0, sticky='w')
        self.telefono_entry = tk.Entry(self.data_frame, validate="key")
        self.telefono_entry['validatecommand'] = (self.telefono_entry.register(self.validate_length), '%P', 14)
        self.telefono_entry.grid(row=5, column=1)

        self.correo_label = tk.Label(self.data_frame, text="Correo:")
        self.correo_label.grid(row=6, column=0, sticky='w')
        self.correo_entry = tk.Entry(self.data_frame, validate="key")
        self.correo_entry['validatecommand'] = (self.correo_entry.register(self.validate_email), '%P', 80)
        self.correo_entry.grid(row=6, column=1)

        self.cargo_label = tk.Label(self.data_frame, text="Cargo:")
        self.cargo_label.grid(row=7, column=0, sticky='w')
        self.cargo_entry = tk.Entry(self.data_frame, validate="key")
        self.cargo_entry['validatecommand'] = (self.telefono_entry.register(self.validate_length), '%P', 150)
        self.cargo_entry.grid(row=7, column=1)

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

        self.hora_salida_label = tk.Label(self.data_frame, text="Hora de Salida:")
        self.hora_salida_label.grid(row=9, column=0, sticky='w')
        self.hora_salida_entry = tk.Entry(self.data_frame)
        self.hora_salida_entry.grid(row=9, column=1)

        # Label para mostrar la hora actual 
        self.current_time_label = tk.Label(self.data_frame, text="", font=("Helvetica", 12)) 
        self.current_time_label.grid(row=8, column=4, padx=5)  # Asegúrate de que esta línea esté presente

        # Botones para CRUD
        self.create_button = tk.Button(self.data_frame, text="Registrar", command=self.confirm_create_empleado)
        self.create_button.grid(row=10, column=0, pady=5)
        self.create_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de registrar

        self.read_button = tk.Button(self.data_frame, text="Actualizar lista", command=self.read_empleados)
        self.read_button.grid(row=10, column=1, pady=5)

        self.update_button = tk.Button(self.data_frame, text="Modificar", command=self.confirm_update_empleado)
        self.update_button.grid(row=11, column=0, pady=5)
        self.update_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de modificar

        self.delete_button = tk.Button(self.data_frame, text="Eliminar", command=self.confirm_delete_empleado)
        self.delete_button.grid(row=11, column=1, pady=5)
 
        # Inicialmente deshabilitar el botón de eliminar
        self.delete_button.config(state=tk.DISABLED)

        # Crear un marco para el Treeview y la barra de desplazamiento
        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Crear el Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=("CI Empleado", "Nombre y Apellido", "Fecha de Nacimiento", "Sexo", "Dirección", "Teléfono", "Correo", "Cargo", "Entrada", "Salida"), show='headings')
        # Definir el encabezado de las columnas y establecer un ancho mínimo
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Configurar el Treeview para que no se expanda
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.grid_propagate(False)  # Evitar que el Treeview se expanda

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
        self.tree_frame.grid_columnconfigure(1, weight=0)  # La columna de la barra de desplazamiento no se expande

        # Configurar la ventana principal para que se expanda
        self.master.grid_rowconfigure(0, weight=1)  # Permitir que la fila 0 se expanda
        self.master.grid_columnconfigure(0, weight=1)  # Permitir que la columna 0 se expanda

        self.tree.bind("<Double-1>", self.on_double_click)

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
        self.direccion_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.correo_entry.delete(0, tk.END)
        self.cargo_entry.delete(0, tk.END)
        self.fecha_entrada_entry.delete(0, tk.END)
        self.hora_salida_entry.delete(0, tk.END)

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
               
    def read_empleados(self):
        # Limpiar el Treeview antes de cargar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute("SELECT * FROM empleados")
            rows = self.cursor.fetchall()
            
            # Insertar cada fila directamente en el Treeview
            for values in rows:
                self.tree.insert("", "end", values=values)  # Inserta los valores directamente

        except Exception as e:
            messagebox.showerror("Error", f"Error al leer los empleados: {e}")

        self.adjust_column_widths()  # Ajusta los anchos de las columnas
        
    def confirm_create_empleado(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea registrar este empleado?"):
            self.create_empleado()  # Llama al método original para crear el empleado

    def confirm_update_empleado(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea modificar este empleado?"):
            self.update_empleado()  # Llama al método original para modificar el empleado

    def confirm_delete_empleado(self):
        if not self.tree.selection():
            messagebox.showwarning("Advertencia", "Por favor, selecciona un empleado para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este empleado?"):
            self.delete_empleado()  # Llama al método original para eliminar el empleado
      
    def create_empleado(self):
        ci = self.ci_entry.get()
        nombre = self.nombre_entry.get()
        fecha_nac = self.fecha_nac_entry.get()
        sexo = self.sexo_combo.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        cargo = self.cargo_entry.get()
        fecha_entrada = self.fecha_entrada_entry.get()
        hora_entrada_str = self.hora_entry.get()  # Captura la hora de entrada
        hora_salida_str = self.hora_salida_entry.get()  # Captura la hora de salida

        # Combinar fecha y hora en un objeto datetime
        try:
            fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")  # Asegúrate de que la fecha esté en el formato correcto
            hora_entrada = datetime.strptime(hora_entrada_str, "%H:%M:%S").time()  # Asegúrate de que la hora esté en el formato correcto
            hora_salida = datetime.strptime(hora_salida_str, "%H:%M:%S").time()  # Asegúrate de que la hora de salida esté en el formato correcto
            datetime_entrada = datetime.combine(fecha_entrada_dt, hora_entrada)  # Combina fecha y hora
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de fecha o hora incorrecto: {ve}")
            return

        # Validar el correo electrónico
        if correo and "@" not in correo:
            messagebox.showerror("Error", "El correo electrónico debe contener el símbolo '@'.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO empleados (CIempleado, Nombreyapellido, Fechanacimiento, Sexo, Direccion, Telefono, Correo, Cargo, Entrada, Salida)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ci, nombre, fecha_nac, sexo, direccion, telefono, correo, cargo, datetime_entrada, hora_salida))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Empleado creado exitosamente.")

            # Limpiar los campos de entrada
            self.clear_entries()  # Llama al método para limpiar los campos
            self.read_empleados()  # Actualizar la lista de empleados

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el empleado: {e}")
                        
    def update_empleado(self):
        ci = self.ci_entry.get()  # CI del empleado a actualizar
        nombre = self.nombre_entry.get()
        fecha_nac = self.fecha_nac_entry.get()
        sexo = self.sexo_combo.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        cargo = self.cargo_entry.get()
        fecha_entrada = self.fecha_entrada_entry.get()
        hora_entrada_str = self.hora_entry.get()  # Captura la hora de entrada
        hora_salida_str = self.hora_salida_entry.get()  # Captura la hora de salida

        # Combinar fecha y hora en un objeto datetime
        try:
            fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")  # Asegúrate de que la fecha esté en el formato correcto
            hora_entrada = datetime.strptime(hora_entrada_str, "%H:%M:%S").time()  # Asegúrate de que la hora esté en el formato correcto
            hora_salida = datetime.strptime(hora_salida_str, "%H:%M:%S").time()  # Asegúrate de que la hora de salida esté en el formato correcto
            datetime_entrada = datetime.combine(fecha_entrada_dt, hora_entrada)  # Combina fecha y hora
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de fecha o hora incorrecto: {ve}")
            return

        # Actualizar el empleado
        try:
            self .cursor.execute("""
                UPDATE empleados
                SET Nombreyapellido = %s, Fechanacimiento = %s, Sexo = %s, Direccion = %s, Telefono = %s, Correo = %s, Cargo = %s, Entrada = %s, Salida = %s
                WHERE CIempleado = %s
            """, (nombre, fecha_nac, sexo, direccion, telefono, correo, cargo, datetime_entrada, hora_salida, ci))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Empleado actualizado exitosamente.")

            # Limpiar los campos de entrada
            self.clear_entries()  # Llama al método para limpiar los campos
            self.read_empleados()  # Actualizar la lista de empleados

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el empleado: {e}")
            
    def delete_empleado(self):
        ci = self.ci_entry.get()  # Obtener el CI del empleado a eliminar
        if not ci:  # Verificar que se haya ingresado un CI
            messagebox.showwarning("Advertencia", "Por favor, ingresa el CI del empleado a eliminar.")
            return

        try:
            # Ejecutar la consulta para eliminar el empleado
            self.cursor.execute("DELETE FROM empleados WHERE CIempleado = %s", (ci,))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Empleado eliminado exitosamente.")
            
            self.clear_entries()  # Limpiar los campos de entrada
            self.read_empleados()  # Volver a cargar los empleados después de la eliminación

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el empleado: {e}")
            
    def close_connection(self):
        """Cierra la conexión a la base de datos y destruye la ventana."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.master.destroy()  # Cierra la ventana

if __name__ == "__main__":
    root = tk.Tk()
    app = EmpleadosCRUDApp(root)
    app.read_empleados()  # Cargar los empleados al iniciar la aplicación
    root.wm_minsize(800, 400)  # Establece el tamaño mínimo de la ventana
    root.protocol("WM_DELETE_WINDOW", app.close_connection)  # Asegúrate de cerrar la conexión al salir
    root.mainloop()