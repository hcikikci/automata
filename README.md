# Automata - Modern Python Eel Application

A clean, manageable, and beautiful Python Eel application with modern architecture and UI design.

## 🚀 Features

- **Modern Architecture**: Clean separation of concerns with service-oriented design
- **Beautiful UI**: Modern, responsive design with light/dark theme support
- **System Information**: Real-time system monitoring and information display
- **Data Management**: JSON-based user data persistence
- **Notifications**: Toast notifications and notification panel
- **Responsive Design**: Works on desktop and mobile devices
- **Modular Structure**: Well-organized codebase for easy maintenance

## 🏗️ Project Structure

```
automata/
├── src/
│   ├── main.py                 # Application entry point
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── app_config.py   # Application configuration
│   │   │   └── app_controller.py # Main application controller
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── system_service.py # System information service
│   │       ├── data_service.py   # Data persistence service
│   │       └── ui_service.py     # UI notification service
│   └── frontend/
│       ├── pages/
│       │   └── index.html      # Main application page
│       └── assets/
│           ├── css/
│           │   ├── styles.css      # Main styles
│           │   ├── themes.css      # Theme definitions
│           │   └── components.css  # UI component styles
│           └── js/
│               ├── eel.js          # Eel communication
│               ├── app.js          # Main application logic
│               └── components.js   # UI components
├── requirements.txt
└── README.md
```

## 🛠️ Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   cd src
   python main.py
   ```

## 📦 Dependencies

- **eel**: Python-JavaScript bridge for desktop applications
- **psutil**: System and process utilities
- **gevent**: Asynchronous networking library
- **bottle**: Lightweight WSGI micro web-framework
- **websockets**: WebSocket implementation
- **whichcraft**: Cross-platform executable finder

## 🎨 Features Overview

### Dashboard
- Application statistics and quick stats
- Real-time uptime counter
- Quick action buttons
- System overview

### System Information
- Platform details (OS, processor, architecture)
- Memory usage and statistics
- CPU information and usage
- Disk space and usage
- Real-time refresh capability

### Data Management
- JSON-based user data editor
- Load and save user preferences
- Data export functionality
- Persistent settings storage

### Settings
- Light/Dark theme toggle
- Notification preferences
- Application configuration

### UI Components
- Toast notifications
- Notification panel
- Progress bars
- Loading spinners
- Responsive navigation
- Modal dialogs

## 🎯 Architecture

### Backend Services

1. **SystemService**: Handles system information gathering and monitoring
2. **DataService**: Manages user data persistence and settings
3. **UIService**: Handles notifications and UI-related operations

### Frontend Components

1. **App Module**: Main application logic and state management
2. **Components Module**: Reusable UI components
3. **Eel Module**: Python-JavaScript communication bridge

### Configuration

The application uses a centralized configuration system through `AppConfig` class:
- Window settings (size, position)
- Development settings (cache, debug)
- Server settings (host, port, mode)
- Application metadata

## 🎨 Theming

The application supports light and dark themes with:
- CSS custom properties for easy customization
- Automatic theme persistence
- Smooth theme transitions
- Consistent design tokens

## 📱 Responsive Design

- Mobile-friendly navigation
- Adaptive card layouts
- Responsive typography
- Touch-friendly interactions

## 🔧 Development

### Adding New Services

1. Create a new service class in `src/backend/services/`
2. Initialize it in `AppController`
3. Register any Eel functions in `_register_eel_functions`

### Adding New UI Components

1. Add HTML structure to `index.html`
2. Add styles to appropriate CSS files
3. Add JavaScript logic to `app.js` or `components.js`

### Customizing Themes

Edit `src/frontend/assets/css/themes.css` to modify:
- Color schemes
- Typography
- Spacing
- Shadows and effects

## 🚀 Building for Production

For production deployment:

1. Set `DEBUG = False` in `AppConfig`
2. Set `DISABLE_CACHE = False`
3. Choose appropriate `MODE` (e.g., 'chrome-app')
4. Consider using PyInstaller for executable generation

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

## 📞 Support

For questions or support, please open an issue in the project repository.

---

Built with ❤️ using Python Eel and modern web technologies. 