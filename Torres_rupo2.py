import flet as ft
import time
import threading

# Función para mover discos en las Torres de Hanoi
def hanoi(n, source, target, auxiliary, move_callback):
    if n > 0:
        hanoi(n - 1, source, auxiliary, target, move_callback)
        move_callback(source, target)
        hanoi(n - 1, auxiliary, target, source, move_callback)

# Clase que representa el estado del juego y la interfaz gráfica
class HanoiApp:
    def __init__(self):
        self.disks = 4  # Número de discos
        self.rods = {'A': [], 'B': [], 'C': []}
        self.tower_a = None
        self.tower_b = None
        self.tower_c = None

    def build(self, page):
        self.page = page
        self.page.title = "Torres de Hanoi"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 20

        self.reset_rods()

        self.tower_a = self.create_tower('A', 'Torre 1')  # Cambiar el texto aquí
        self.tower_b = self.create_tower('B', 'Torre 2')  # Cambiar el texto aquí
        self.tower_c = self.create_tower('C', 'Torre 3')  # Cambiar el texto aquí

        self.start_button = ft.ElevatedButton(
            text="INICIAR",
            on_click=self.start_hanoi
        )

        self.page.add(
            ft.Row([self.tower_a, self.tower_b, self.tower_c], alignment=ft.MainAxisAlignment.CENTER),
            self.start_button
        )

    def reset_rods(self):
        self.rods['A'] = list(range(self.disks, 0, -1))
        self.rods['B'] = []
        self.rods['C'] = []
        if self.tower_a and self.tower_b and self.tower_c:
            self.update_towers()

    def create_tower(self, rod_name, display_name):
        tower = ft.Column([], alignment=ft.MainAxisAlignment.END, spacing=5)
        title = ft.Text(f"{display_name}", weight=ft.FontWeight.BOLD)  # Usar el nombre de visualización personalizado
        tower_container = ft.Container(
            width=200,  # Ancho fijo para todas las columnas
            content=ft.Column([title, tower], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        )
        return tower_container

    def move_disk(self, source, target):
        disk = self.rods[source].pop()
        self.rods[target].append(disk)
        self.update_towers()

    def update_towers(self):
        for name, tower_container in zip(['A', 'B', 'C'], [self.tower_a, self.tower_b, self.tower_c]):
            tower = tower_container.content.controls[1]
            tower.controls.clear()
            for disk in reversed(self.rods[name]):  # Reversed para apilar de mayor a menor
                tower.controls.append(self.create_disk(disk))
        self.page.update()
        time.sleep(0.9)  # Pausa para visualizar el movimiento

    def create_disk(self, size):
        colors = ["#84FF08", "#FF3508", "#08BFFF", "#E908FF"]
        return ft.Container(
            width=size * 40 + 40,
            height=30,
            bgcolor=colors[size % len(colors)],
            alignment=ft.alignment.center
        )

    def start_hanoi(self, e):
        self.reset_rods()
        threading.Thread(target=hanoi, args=(self.disks, 'A', 'C', 'B', self.move_disk)).start()

# Ejecuta la aplicación
if __name__ == "__main__":
    ft.app(target=HanoiApp().build)