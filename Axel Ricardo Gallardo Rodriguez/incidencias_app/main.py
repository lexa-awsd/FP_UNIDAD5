#Usar Python 3.10 (Recomendado)
"""& C:/Users/Axel/AppData/Local/Programs/Python/Python310/python.exe c:/Users/Axel/Documents/incidencias_app/main.py"""

# Importar las herramientas de Kivy que vamos a usar
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

# Esta pantalla es para que el usuario ingrese con su usuario y contraseña
class PantallaLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Crear un diseño vertical para organizar los elementos
        diseño = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Título de la pantalla
        diseño.add_widget(Label(text='INICIAR SESIÓN', font_size=24))
        
        # Campo para que el usuario escriba su nombre de usuario
        self.campo_usuario = TextInput(hint_text='Usuario', size_hint_y=None, height=40)
        
        # Campo para la contraseña (se ocultan los caracteres)
        self.campo_contraseña = TextInput(hint_text='Contraseña', password=True, size_hint_y=None, height=40)
        
        # Agregar los campos al diseño
        diseño.add_widget(self.campo_usuario)
        diseño.add_widget(self.campo_contraseña)
        
        # Botón para iniciar sesión
        boton_login = Button(text='ENTRAR', size_hint_y=None, height=50)
        boton_login.bind(on_press=self.verificar_login)
        diseño.add_widget(boton_login)
        
        self.add_widget(diseño)
    
    def verificar_login(self, instancia):
        # Verificar que ambos campos tengan texto
        # En una app real aquí iría la conexión con una base de datos
        if self.campo_usuario.text and self.campo_contraseña.text:
            self.manager.current = 'menu'

# Pantalla principal con el menú de opciones
class PantallaMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        diseño = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Lista de botones del menú principal
        opciones_menu = [
            ('MIS REPORTES', 'reportes'),
            ('NUEVO REPORTE', 'nuevo'),
            ('BUSCAR', 'buscar')
        ]
        
        # Crear un botón por cada opción del menú
        for texto_boton, nombre_pantalla in opciones_menu:
            boton = Button(text=texto_boton, size_hint_y=None, height=60)
            boton.bind(on_press=lambda x, pantalla=nombre_pantalla: self.ir_a_pantalla(pantalla))
            diseño.add_widget(boton)
        
        self.add_widget(diseño)
    
    def ir_a_pantalla(self, pantalla_destino):
        # Cambiar a la pantalla que se seleccionó
        self.manager.current = pantalla_destino

# Pantalla para crear un nuevo reporte de incidencia
class PantallaNuevoReporte(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        diseño = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos donde el usuario escribe la información del reporte
        self.campo_titulo = TextInput(hint_text='Título del problema', size_hint_y=None, height=40)
        self.campo_descripcion = TextInput(hint_text='Descripción', size_hint_y=0.4)
        
        diseño.add_widget(Label(text='NUEVO REPORTE'))
        diseño.add_widget(self.campo_titulo)
        diseño.add_widget(self.campo_descripcion)
        
        # Panel para los botones de acción
        panel_botones = BoxLayout(size_hint_y=None, height=50)
        
        boton_enviar = Button(text='ENVIAR')
        boton_enviar.bind(on_press=self.guardar_reporte)
        
        boton_volver = Button(text='VOLVER')
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        
        panel_botones.add_widget(boton_volver)
        panel_botones.add_widget(boton_enviar)
        
        diseño.add_widget(panel_botones)
        self.add_widget(diseño)
    
    def guardar_reporte(self, instancia):
        # Verificar que ambos campos tengan contenido
        if self.campo_titulo.text and self.campo_descripcion.text:
            # Obtener la aplicación principal para acceder a la lista de reportes
            aplicacion = App.get_running_app()
            aplicacion.reportes.append({
                'titulo': self.campo_titulo.text,
                'descripcion': self.campo_descripcion.text
            })
            
            # Limpiar los campos después de guardar
            self.campo_titulo.text = ''
            self.campo_descripcion.text = ''
            
            # Regresar al menú principal
            self.manager.current = 'menu'

# Pantalla para ver todos los reportes guardados
class PantallaReportes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        diseño = BoxLayout(orientation='vertical')
        
        # Título de la pantalla
        diseño.add_widget(Label(text='MIS REPORTES', size_hint_y=None, height=50))
        
        # Área desplazable para la lista de reportes
        self.area_desplazable = ScrollView()
        self.contenedor_reportes = BoxLayout(orientation='vertical', size_hint_y=None)
        self.contenedor_reportes.bind(minimum_height=self.contenedor_reportes.setter('height'))
        
        self.area_desplazable.add_widget(self.contenedor_reportes)
        diseño.add_widget(self.area_desplazable)
        
        # Botón para regresar al menú
        boton_volver = Button(text='VOLVER AL MENÚ', size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        diseño.add_widget(boton_volver)
        
        self.add_widget(diseño)
    
    def on_enter(self):
        # Este método se ejecuta automáticamente cuando se entra a la pantalla
        self.actualizar_lista_reportes()
    
    def actualizar_lista_reportes(self):
        # Limpiar la lista actual
        self.contenedor_reportes.clear_widgets()
        
        # Obtener la lista de reportes de la aplicación
        aplicacion = App.get_running_app()
        
        # Mostrar cada reporte como un botón en la lista
        for indice, reporte in enumerate(aplicacion.reportes):
            elemento_lista = Button(
                text=f"{reporte['titulo']}\n{reporte['descripcion'][:50]}...",
                size_hint_y=None,
                height=80
            )
            self.contenedor_reportes.add_widget(elemento_lista)

# Pantalla para buscar reportes por palabras clave
class PantallaBuscar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        diseño = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campo de texto para escribir lo que se quiere buscar
        self.campo_busqueda = TextInput(hint_text='Buscar...', size_hint_y=None, height=40)
        diseño.add_widget(self.campo_busqueda)
        
        # Botón para ejecutar la búsqueda
        boton_buscar = Button(text='BUSCAR', size_hint_y=None, height=50)
        boton_buscar.bind(on_press=self.ejecutar_busqueda)
        diseño.add_widget(boton_buscar)
        
        # Etiqueta donde se muestran los resultados
        self.etiqueta_resultados = Label(text='Ingrese término de búsqueda')
        diseño.add_widget(self.etiqueta_resultados)
        
        # Botón para volver al menú
        boton_volver = Button(text='VOLVER', size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        diseño.add_widget(boton_volver)
        
        self.add_widget(diseño)
    
    def ejecutar_busqueda(self, instancia):
        # Convertir el texto a minúsculas para búsqueda sin区分 mayúsculas/minúsculas
        texto_busqueda = self.campo_busqueda.text.lower()
        aplicacion = App.get_running_app()
        
        # Buscar en todos los reportes
        reportes_encontrados = []
        for reporte in aplicacion.reportes:
            if (texto_busqueda in reporte['titulo'].lower() or 
                texto_busqueda in reporte['descripcion'].lower()):
                reportes_encontrados.append(reporte['titulo'])
        
        # Mostrar resultados
        if reportes_encontrados:
            self.etiqueta_resultados.text = '\n'.join(reportes_encontrados)
        else:
            self.etiqueta_resultados.text = 'No se encontraron resultados'

# Esta es la aplicación principal que coordina todo
class AplicacionReportes(App):
    def build(self):
        # Aquí guardamos todos los reportes (en una app real sería una base de datos)
        self.reportes = [
            {'titulo': 'Error de login', 'descripcion': 'No puedo iniciar sesión en el sistema'},
            {'titulo': 'Sistema lento', 'descripcion': 'La aplicación va muy lenta hoy'}
        ]
        
        # El administrador de pantallas controla qué pantalla se muestra
        administrador_pantallas = ScreenManager()
        
        # Registrar todas las pantallas de la aplicación
        administrador_pantallas.add_widget(PantallaLogin(name='login'))
        administrador_pantallas.add_widget(PantallaMenu(name='menu'))
        administrador_pantallas.add_widget(PantallaNuevoReporte(name='nuevo'))
        administrador_pantallas.add_widget(PantallaReportes(name='reportes'))
        administrador_pantallas.add_widget(PantallaBuscar(name='buscar'))
        
        return administrador_pantallas

# Punto de entrada de la aplicación
if __name__ == '__main__':
    AplicacionReportes().run()