# Define color scheme
COLORS = {
    "primary": "#2196f3",     # Blue
    "success": "#4caf50",     # Green
    "danger": "#f44336",      # Red
    "warning": "#ff9800",     # Orange
    "light": "#ffffff",       # White
    "dark": "#2c3e50",        # Dark Blue
    "gray": "#95a5a6",        # Gray
    "text_gray": "#666666",   # Text Gray
    "hover_light": "#f8f9fa", # Light Gray for hover effects
    "bg_light": "#f0f2f5"     # Background Light Gray
}

# Define common styles
STYLES = {
    "main_container": {
        "bg": COLORS["light"],
        "padx": 40,
        "pady": 20
    },
    
    "title_label": {
        "font": ("Helvetica", 24, "bold"),
        "fg": COLORS["dark"],
        "bg": COLORS["light"]
    },
    
    "label": {
        "font": ("Helvetica", 12),
        "fg": COLORS["dark"],
        "bg": COLORS["light"]
    },
    
    "entry": {
        "font": ("Helvetica", 12),
        "bg": COLORS["hover_light"],
        "relief": "solid",
        "borderwidth": 1
    },
    
    "button": {
        "font": ("Helvetica", 12),
        "padx": 20,
        "pady": 8,
        "relief": "flat"
    }
} 