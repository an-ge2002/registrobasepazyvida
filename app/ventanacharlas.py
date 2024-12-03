import tkinter as tk
from tkinter import messagebox, ttk, font
from db_connector import create_connection
from tkcalendar import DateEntry
import time
from datetime import datetime  # Asegúrate de importar datetime

class CharlasCRUDApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CRUD de Charlas")
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.create_widgets()
        self.load_areacomun_options()  # Cargar áreas comunes al iniciar
        self.read_charlas()  # Cargar charlas al iniciar
        self.master.state('zoomed')  # Maximiza la ventana (solo en Windows)

       # Establecer el ícono de la ventana
        self.master.iconbitmap('C:/Users/PC/Desktop/registrobasepazyvida/app/img/logo.ico')

    def validate_length(self, input_value, max_length):
        """Validar la longitud de la entrada."""
        try:
            max_length = int(max_length)  # Asegúrate de que max_length sea un entero
        except ValueError:
            return True  # Si no se puede convertir a entero, permite la entrada

        return len(input_value) <= max_length  # Retorna True si la longitud es válida
    
    def validate_entries(self, event=None):
        """Verifica si el campo de nombre está lleno para habilitar el botón de registrar."""
        nombre = self.nombre_entry.get()

        # Habilitar el botón de registrar solo si el campo de Nombre no está vacío
        if nombre:
            self.create_button.config(state=tk.NORMAL)  # Habilitar el botón de registrar
        else:
            self.create_button.config(state=tk.DISABLED)  # Deshabilitar el botón de registrar

    def validate_datetime(self, fecha_inicio, hora_inicio, fecha_fin, hora_fin):
        try:
            # Intenta combinar y parsear la fecha y la hora de inicio
            datetime.strptime(f"{fecha_inicio} {hora_inicio}", "%Y-%m-%d %H:%M:%S")
            # Intenta combinar y parsear la fecha y la hora de fin
            datetime.strptime(f"{fecha_fin} {hora_fin}", "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
     
    def create_widgets(self):
        # Crear un marco para los datos de la actividad
        self.data_frame = tk.Frame(self.master)
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Entradas para los datos de la actividad
        # Campo de entrada para Nombre
        self.nombre_label = tk.Label(self.data_frame, text="Nombre:")
        self.nombre_label.grid(row=0, column=0, sticky='w')
        self.nombre_entry = tk.Entry(self.data_frame, validate="key")
        self.nombre_entry['validatecommand'] = (self.nombre_entry.register(self.validate_length), '%P', 60)
        self.nombre_entry.grid(row=0, column=1)
        self.nombre_entry.bind("<KeyRelease>", self.validate_entries)  # Vincular evento

        self.tema_label = tk.Label(self.data_frame, text="Tema:")
        self.tema_label.grid(row=1, column=0, sticky='w')
        self.tema_entry = tk.Entry(self.data_frame, validate="key")
        self.tema_entry['validatecommand'] = (self.tema_entry.register(self.validate_length), '%P', 150)
        self.tema_entry.grid(row=1, column=1)

        self.descripcion_label = tk.Label(self.data_frame, text="Descripción:")
        self.descripcion_label.grid(row=2, column=0, sticky='w')
        self.descripcion_entry = tk.Entry(self.data_frame, validate="key")
        self.descripcion_entry['validatecommand'] = (self.descripcion_entry.register(self.validate_length), '%P', 150)
        self.descripcion_entry.grid(row=2, column=1)

        self.fechaini_label = tk.Label(self.data_frame, text="Fecha Inicio:")
        self.fechaini_label.grid(row=3, column=0, sticky='w')
        self.fechaini_entry = DateEntry(self.data_frame, date_pattern='yyyy-mm-dd')
        self.fechaini_entry.grid(row=3, column=1)

        self.hora_inicio_label = tk.Label(self.data_frame, text="Hora Inicio:")
        self.hora_inicio_label.grid(row=3, column=2, sticky='w')
        self.hora_inicio_entry = tk.Entry(self.data_frame)  # Aquí puedes usar un Entry para la hora
        self.hora_inicio_entry.grid(row=3, column=3)

        self.fechafin_label = tk.Label(self.data_frame, text="Fecha Fin:")
        self.fechafin_label.grid(row=4, column=0, sticky='w')
        self.fechafin_entry = DateEntry(self.data_frame, date_pattern='yyyy-mm-dd')
        self.fechafin_entry.grid(row=4, column=1)

        self.hora_fin_label = tk.Label(self.data_frame, text="Hora Fin:")
        self.hora_fin_label.grid(row=4, column=2, sticky='w')
        self.hora_fin_entry = tk.Entry(self.data_frame)  # Aquí puedes usar un Entry para la hora
        self.hora_fin_entry.grid(row=4, column=3)

        self.areacomun_label = tk.Label(self.data_frame, text="Área Común:")
        self.areacomun_label.grid(row=5, column=0, sticky='w')
        self.areacomun_combo = ttk.Combobox(self.data_frame)
        self.load_areacomun_options()  # Cargar las opciones de área común
        self.areacomun_combo.set('')  # Establecer un valor por defecto
        self.areacomun_combo.grid(row=5, column=1)

        self.duracion_label = tk.Label(self.data_frame, text="Duración:")
        self.duracion_label.grid(row=6, column=0, sticky='w')
        self.duracion_entry = tk.Entry(self.data_frame, validate="key")
        self.duracion_entry['validatecommand'] = (self.duracion_entry.register(self.validate_length), '%P', 13)        
        self.duracion_entry.grid(row=6, column=1)

        # Botones para CRUD
        # Botón de registrar
        self.create_button = tk.Button(self.data_frame, text="Registrar", command=self.confirm_create_charla)
        self.create_button.grid(row=10, column=0, pady=10)
        self.create_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de registrar

        self.update_button = tk.Button(self.data_frame, text="Modificar", command=self.confirm_update_charla)
        self.update_button.grid(row=10, column=1, pady=10)
        self.update_button.config(state=tk.DISABLED)  # Inicialmente deshabilitar el botón de modificar

        self.delete_button = tk.Button(self.data_frame, text="Eliminar", command=self.confirm_delete_charla)
        self.delete_button.grid(row=10, column=2, pady=10)
        # Inicialmente deshabilitar el botón de eliminar
        self.delete_button.config(state=tk.DISABLED)

        self.read_button = tk.Button(self.data_frame, text="Actualizar lista", command=self.read_charlas)
        self.read_button.grid(row=10, column=3, pady=10)

        self.selected_charla_id = None  # Inicializar la variable de instancia para el ID

        # Crear un marco para el Treeview y la barra de desplazamiento
        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Crear el Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=("Nombre", "Tema", "Descripción", "Fecha de inicio", "Fecha de Fin", "Área Común", "Duración"), show='headings')

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

        # Vincular el evento de doble clic
        self.tree.bind("<Double-1>", self.on_double_click)

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
                    
    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            # Debes obtener el ID de la fila seleccionada
            # Necesitas hacer una consulta para obtener el ID de la charla seleccionada
            self.cursor.execute("SELECT IDcharla FROM charlas WHERE Nombre = %s", (values[0],))
            self.selected_charla_id = self.cursor.fetchone()[0]  # Asigna el ID de la charla seleccionada
            print(f"Charla seleccionada ID: {self.selected_charla_id}")  # Verifica que sea el ID

            # Resto del código para llenar los campos
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, values[0])  # Nombre
            self.tema_entry.delete(0, tk.END)
            self.tema_entry.insert(0, values[1])  # Tipo
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, values[2])  # Descripción
            # Omitir fechas y horas
            self.areacomun_combo.set(values[5])  # Área común
            self.duracion_entry.delete(0, tk.END)
            self.duracion_entry.insert(0, values[6])  # Duración

            # Habilitar el botón de eliminar y modificar
            self.delete_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)

    def load_areacomun_options(self):
        try:
            # Cargar solo IDArea
            self.cursor.execute("SELECT IDArea FROM areascomunes")
            areas = self.cursor.fetchall()

            # Establecer los valores del combobox solo con IDArea
            self.areacomun_combo['values'] = [area[0] for area in areas]  # Solo mostrar IDArea
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar áreas comunes: {e}")
                 
    def clear_entries(self):
        """Limpia todos los campos de entrada."""
        self.nombre_entry.delete(0, tk.END)
        self.tema_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.areacomun_combo.set('')  # O puedes usar un valor por defecto
        self.duracion_entry.delete(0, tk.END)

    def confirm_create_charla(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea registrar esta charla?"):
            self.create_charla()  # Llama al método original para crear el usuario

    def confirm_update_charla(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea modificar esta charla?"):
            self.update_charla()  # Llama al método original para modificar el usuario

    def confirm_delete_charla(self):
        if not self.tree.selection():
            messagebox.showwarning("Advertencia", "Por favor, selecciona una charla para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar esta charla?"):
            self.delete_charla()  # Llama al método original para eliminar el usuario
     
    def create_charla(self):
        # Obtener datos de los campos de entrada
        nombre = self.nombre_entry.get()
        tema = self.tema_entry.get()
        descripcion = self.descripcion_entry.get()
        fechaini_date = self.fechaini_entry.get()  # Obtiene la fecha de inicio
        hora_inicio = self.hora_inicio_entry.get()  # Obtiene la hora de inicio
        fechafin_date = self.fechafin_entry.get()  # Obtiene la fecha de fin
        hora_fin = self.hora_fin_entry.get()  # Obtiene la hora de fin
        areacomun = self.areacomun_combo.get()
        duracion = self.duracion_entry.get()

        # Validar que todos los campos requeridos estén llenos
        if not nombre or not tema or not fechaini_date or not fechafin_date or not hora_inicio or not hora_fin:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos requeridos.")
            return

        # Asegúrate de que las horas tengan el formato correcto
        if len(hora_inicio) == 5:  # Si el formato es HH:MM
            hora_inicio += ":00"  # Añadir segundos
        if len(hora_fin) == 5:  # Si el formato es HH:MM
            hora_fin += ":00"  # Añadir segundos

        # Validar las fechas y horas
        if not self.validate_datetime(fechaini_date, hora_inicio, fechafin_date, hora_fin):
            messagebox.showerror("Error", "El formato de fecha y hora es incorrecto. Debe ser 'YYYY-MM-DD HH:MM:SS'.")
            return

        # Combinar fecha y hora en un objeto datetime
        try:
            fechaini = datetime.strptime(f"{fechaini_date} {hora_inicio}", "%Y-%m-%d %H:%M:%S")
            fechafin = datetime.strptime(f"{fechafin_date} {hora_fin}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "El formato de fecha y hora es incorrecto. Debe ser 'YYYY-MM-DD HH:MM:SS'.")
            return

        # Realizar la inserción en la base de datos
        try:
            self.cursor.execute("""INSERT INTO charlas (Nombre, Tema, Descripcion, Fechaini, Fechafin, Areacomun, Duracion) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                                (nombre, tema, descripcion, fechaini, fechafin, areacomun, duracion))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Charla registrada exitosamente.")
            self.clear_entries()  # Limpia los campos después de crear la actividad
            self.read_charlas()  # Actualiza la lista de actividades
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la charla: {e}")

    def read_charlas(self):
        # Limpiar el Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Leer actividades de la base de datos, incluyendo el ID
        try: 
            self.cursor.execute("SELECT IDcharla, Nombre, Tema, Descripcion, Fechaini, Fechafin, Areacomun, Duracion FROM charlas")
            rows = self.cursor.fetchall()

            for row in rows:
                # Aquí solo mostramos los valores que queremos en el Treeview
                self.tree.insert("", "end", values=row[1:])  # Excluye el ID (row[1:])
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer las charlas: {e}")

        self.adjust_column_widths()  # Ajusta los anchos de las columnas          

    def update_charla(self):
        if self.selected_charla_id is None:
            messagebox.showwarning("Advertencia", "Seleccione una charla para modificar")
            return

        # Obtener datos de las entradas
        nombre = self.nombre_entry.get()
        tema = self.tema_entry.get()  # Asegúrate de que este campo esté correctamente referenciado
        descripcion = self.descripcion_entry.get()

        # Obtener fecha y hora
        fechaini_date = self.fechaini_entry.get()
        hora_inicio = self.hora_inicio_entry.get()
        fechafin_date = self.fechafin_entry.get()
        hora_fin = self.hora_fin_entry.get()

        # Asegúrate de que las horas tengan el formato correcto
        if len(hora_inicio) == 5:  # Si el formato es HH:MM
            hora_inicio += ":00"  # Añadir segundos
        if len(hora_fin) == 5:  # Si el formato es HH:MM
            hora_fin += ":00"  # Añadir segundos

        # Validar las fechas y horas
        if not self.validate_datetime(fechaini_date, hora_inicio, fechafin_date, hora_fin):
            messagebox.showerror("Error", "El formato de fecha y hora es incorrecto. Debe ser 'YYYY-MM-DD HH:MM:SS'.")
            return

        # Combinar fecha y hora en un objeto datetime
        try:
            fechaini = datetime.strptime(f"{fechaini_date} {hora_inicio}", "%Y-%m-%d %H:%M:%S")
            fechafin = datetime.strptime(f"{fechafin_date} {hora_fin}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "El formato de fecha y hora es incorrecto. Debe ser 'YYYY-MM-DD HH:MM:SS'.")
            return

        areacomun = self.areacomun_combo.get()
        duracion = self.duracion_entry.get()

        # Realizar la actualización
        try:
            self.cursor.execute("""
                UPDATE charlas 
                SET Nombre = %s, Tema = %s, Descripcion = %s, Fechaini = %s, Fechafin = %s, Areacomun = %s, 
                    Duracion = %s 
                WHERE IDcharla = %s
            """, (nombre, tema, descripcion, fechaini, fechafin, areacomun, duracion, self.selected_charla_id))
            
            self.conn.commit()  # Asegúrate de hacer commit

            messagebox.showinfo("Éxito", "Charla actualizada correctamente")
            self.read_charlas()  # Actualizar la lista de actividades
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la charla: {e}")
                     
    def delete_charla(self):
        if self.selected_charla_id is None:
            messagebox.showwarning("Advertencia", "Seleccione una charla para eliminar")
            return

        # Confirmar la eliminación
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta charla?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM charlas WHERE IDcharla = %s", (self.selected_charla_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Charla eliminado correctamente")
                self.read_charlas()  # Actualizar la lista de actividades
                self.selected_charla_id = None  # Reiniciar la variable de ID
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la charla: {e}")

    def close_connection(self):
        """Cierra la conexión a la base de datos y destruye la ventana."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.master.destroy()  # Cierra la ventana

if __name__ == "__main__":
    root = tk.Tk()
    app = CharlasCRUDApp(root)
    root.wm_minsize(800, 400)  # Establece el tamaño mínimo de la ventana
    root.mainloop()