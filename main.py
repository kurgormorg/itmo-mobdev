import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.uix.image import Image, AsyncImage

NEWS_API_KEY = 'cb60a28411d24f90b0500699df51db4f'
class NewsApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_screen = MainScreen(name='main')
        self.screen_manager.add_widget(self.main_screen)

        self.detail_screen = DetailScreen(name='detail')
        self.screen_manager.add_widget(self.detail_screen)

        return self.screen_manager
    
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_label = Label(text='News', size_hint_y = None, height=dp(10), font_size="16sp", bold=True)
        self.layout.add_widget(self.title_label)

        self.scroll_view = ScrollView(size_hint=(1,1))
        self.grid_layout = GridLayout(cols=1, spacing = 5, size_hint_y = None)

        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        self.scroll_view.add_widget(self.grid_layout)
        self.layout.add_widget(self.scroll_view)
        self.add_widget(self.layout)
        
        self.load_news()

    def load_news(self):
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        news_data= response.json()

        if news_data['status'] == 'ok':
            for article in news_data['articles']:
                news_item = NewsItem(article)
                self.grid_layout.add_widget(news_item)

class NewsItem(ButtonBehavior, BoxLayout):
    def __init__(self, article, **kwargs):
        super(NewsItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = [10, 10, 10, 10]
        self.spacing = 10
        self.article = article

        self.image = AsyncImage(
            source = article['urlToImage'] if article['urlToImage'] else 'Error downloading image',
            size_hint = (None, None),
            size = (dp(100), dp(100)), fit_mode = 'scale-down'
        )
        self.add_widget(self.image)

        self.text_layout = BoxLayout(orientation='vertical', spacing = 5, size_hint_x = 0.7)

        self.title_label = Label(
            text=article['title'] if article['title'] else "No title",
            size_hint_y = None,
            height = dp(40),
            text_size=(Window.width-dp(140), None),
            halign = 'left',
            valign = 'top',
            bold = True
        )
        self.source_label = Label(text=f"Source:{article['source']['name']}" if article['source']['name'] else "Source unknown",
            size_hint_y = None,
            height = dp(20),
            text_size = (Window.width-dp(140), None),
            halign = 'left',
            font_size = '14sp',
            bold = True)

        self.text_layout.add_widget(self.title_label)
        self.text_layout.add_widget(self.source_label)
        self.add_widget(self.text_layout)
        self.bind(on_press=self.show_detail)
    
    def show_detail(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'detail'

        app.detail_screen.show_article(self.article)

class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.add_widget(self.layout)

    def show_article(self, article):
            self.layout.clear_widgets()

            title_label = Label(text=article['title'] if article['title'] else "No title",
                                size_hint_y = None,
                                height = dp(500),
                                text_size = (Window.width-dp(20), None),
                                halign = 'left',
                                font_size = '24sp',
                                bold = True)
            
            self.layout.add_widget(title_label)

            source_label = Label(text=f"Source:{article['source']['name']}" if article['source']['name'] else "Unknown source",
                                size_hint_y = None,
                                height = dp(30),
                                text_size = (Window.width-dp(20), None),
                                halign = 'left',
                                font_size = '18sp')
            
            self.layout.add_widget(source_label)

            image = AsyncImage(source=article['urlToImage'] if article['urlToImage'] else "Error downloading image",
                                size_hint_y = None,
                                height = dp(200),
                                allow_stretch = True)
            
            self.layout.add_widget(image)

            content_text = article['content'] if article['content'] else "No further info"
            content_label = Label(text=content_text,
                                 size_hint_y = None,
                                 height = (Window.height-dp(350), None),
                                 text_size = (Window.width-dp(20), None),
                                 halign = 'left',
                                 valign = 'top',
                                 font_size = '16sp')
            
            self.layout.add_widget(content_label)

            back_button = Button(text='Back',
                                 size_hint_y = None,
                                 height = dp(50),
                                 background_color=(0.2, 0.6, 1, 1))
            
            back_button.bind(on_press=self.go_back)
            self.layout.add_widget(back_button)


    def go_back(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'main'


if __name__ == '__main__':
    NewsApp().run()