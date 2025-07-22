import flet as ft
from pages.home import HomePage
from pages.check_lists import CheckListsPage
from pages.webscrap import WebScrapPage
from pages.confrontas import ConfrontasPage

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Web App IMSS v2"
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_resizable = False
        
        # Estado actual de la página
        self.current_page = "home"
        
        # Mostrar página inicial
        self.show_home()
    
    def navigate_to_checklist(self, e=None):
        """Navegar a la página de checklist"""
        if self.current_page != "checklist":
            self.show_checklist()
    
    def navigate_to_webscrap(self, e=None):
        """Navegar a la página de webscraping"""
        if self.current_page != "webscrap":
            self.show_webscrap()
    
    def navigate_to_confrontas(self, e=None):
        """Navegar a la página de confrontas"""
        if self.current_page != "confrontas":
            self.show_confrontas()
    
    def navigate_to_home(self, e=None):
        """Navegar a la página de inicio"""
        if self.current_page != "home":
            self.show_home()
    
    def show_home(self):
        """Mostrar la página de inicio"""
        self.current_page = "home"
        # Limpiar la página antes de mostrar el home
        self.page.controls.clear()
        home_page = HomePage(self.page, self.navigate_to_checklist, self.navigate_to_webscrap, self.navigate_to_confrontas)
        self.page.update()
    
    def show_checklist(self):
        """Mostrar la página de checklist"""
        self.current_page = "checklist"
        # Limpiar la página antes de mostrar checklist
        self.page.controls.clear()
        checklist_page = CheckListsPage(self.page, self.navigate_to_home, self.navigate_to_webscrap, self.navigate_to_confrontas)
        self.page.add(checklist_page)
        self.page.update()

    def show_confrontas(self):
        """Mostrar la página de confrontas"""
        self.current_page = "confrontas"
        # Limpiar la página antes de mostrar confrontas
        self.page.controls.clear()
        confrontas_page = ConfrontasPage(self.page, self.navigate_to_home, self.navigate_to_checklist, self.navigate_to_webscrap)
        self.page.add(confrontas_page)
        self.page.update()

    def show_webscrap(self):
        """Mostrar la página de webscraping"""
        self.current_page = "webscrap"
        # Limpiar la página antes de mostrar webscrap
        self.page.controls.clear()
        webscrap_page = WebScrapPage(self.page, self.navigate_to_home, self.navigate_to_checklist, self.navigate_to_confrontas)
        self.page.add(webscrap_page)
        self.page.update()

def main(page: ft.Page):
    MainApp(page)

if __name__ == "__main__":
    ft.app(target=main)