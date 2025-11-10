import json
import os

class ThemeManager:
    
    # Light theme colors (matching web app)
    LIGHT_THEME = {
        'background': '#FFFFFF',
        'foreground': '#0A0A0A',
        'card': '#FFFFFF',
        'card_foreground': '#0A0A0A',
        'primary': '#E74C3C',
        'primary_foreground': '#F8E8E6',
        'secondary': '#F5F5F5',
        'secondary_foreground': '#171717',
        'muted': '#F5F5F5',
        'muted_foreground': '#737373',
        'accent': '#F5F5F5',
        'accent_foreground': '#171717',
        'border': '#E5E5E5',
        'input': '#E5E5E5',
        'chart_1': '#3B82F6',
        'chart_2': '#10B981',
        'chart_3': '#F59E0B',
        'chart_4': '#EF4444',
        'chart_5': '#8B5CF6',
        'chart_6': '#EC4899',
    }
    
    # Dark theme colors (matching web app)
    DARK_THEME = {
        'background': '#0A0A0A',
        'foreground': '#FAFAFA',
        'card': '#171717',
        'card_foreground': '#FAFAFA',
        'primary': '#E67E73',
        'primary_foreground': '#F8E8E6',
        'secondary': '#262626',
        'secondary_foreground': '#FAFAFA',
        'muted': '#262626',
        'muted_foreground': '#A3A3A3',
        'accent': '#262626',
        'accent_foreground': '#FAFAFA',
        'border': '#262626',
        'input': '#333333',
        'chart_1': '#3B82F6',
        'chart_2': '#10B981',
        'chart_3': '#F59E0B',
        'chart_4': '#EF4444',
        'chart_5': '#8B5CF6',
        'chart_6': '#EC4899',
    }
    
    def __init__(self):
        self.config_file = 'theme_config.json'
        self.current_theme = self.load_theme()
    
    def load_theme(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('theme', 'light')
            except:
                return 'light'
        return 'light'
    
    def save_theme(self, theme):
        with open(self.config_file, 'w') as f:
            json.dump({'theme': theme}, f)
        self.current_theme = theme
    
    def toggle_theme(self):
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_theme(new_theme)
        return new_theme
    
    def get_colors(self):
        return self.LIGHT_THEME if self.current_theme == 'light' else self.DARK_THEME
    
    def get_stylesheet(self):
        colors = self.get_colors()
        
        return f"""
            QMainWindow, QWidget {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
            
            QPushButton {{
                padding: 8px 16px;
                background-color: {colors['primary']};
                color: {colors['primary_foreground']};
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {colors['primary']};
                opacity: 0.9;
            }}
            
            QPushButton:disabled {{
                background-color: {colors['muted']};
                color: {colors['muted_foreground']};
            }}
            
            QLineEdit {{
                padding: 8px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['input']};
                color: {colors['foreground']};
            }}
            
            QComboBox {{
                padding: 8px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['input']};
                color: {colors['foreground']};
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {colors['card']};
                color: {colors['card_foreground']};
                selection-background-color: {colors['accent']};
                border: 1px solid {colors['border']};
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {colors['border']};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: {colors['foreground']};
                background-color: {colors['card']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            
            QLabel {{
                color: {colors['foreground']};
                background-color: transparent;
            }}
            
            QTableWidget {{
                background-color: {colors['card']};
                color: {colors['card_foreground']};
                border: 1px solid {colors['border']};
                gridline-color: {colors['border']};
            }}
            
            QTableWidget::item {{
                padding: 5px;
            }}
            
            QTableWidget::item:selected {{
                background-color: {colors['accent']};
                color: {colors['accent_foreground']};
            }}
            
            QHeaderView::section {{
                background-color: {colors['secondary']};
                color: {colors['secondary_foreground']};
                padding: 5px;
                border: 1px solid {colors['border']};
                font-weight: bold;
            }}
            
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                background-color: {colors['card']};
            }}
            
            QTabBar::tab {{
                background-color: {colors['secondary']};
                color: {colors['secondary_foreground']};
                padding: 8px 16px;
                border: 1px solid {colors['border']};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {colors['card']};
                color: {colors['card_foreground']};
            }}
            
            QMessageBox {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
        """
    
    def get_chart_colors(self):
        """Get chart colors for matplotlib"""
        colors = self.get_colors()
        return [
            colors['chart_1'],
            colors['chart_2'],
            colors['chart_3'],
            colors['chart_4'],
            colors['chart_5'],
            colors['chart_6'],
        ]
