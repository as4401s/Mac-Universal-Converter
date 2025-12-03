# Mac Universal Converter

A modern, native macOS application for converting images, videos, and audio files between various formats. Built with Python and CustomTkinter, featuring a beautiful dark-themed interface that follows macOS design principles.

![Mac Universal Converter Screenshot](https://github.com/as4401s/Mac-Universal-Converter/raw/main/App-image.png)

## ✨ Features

- **Multi-Format Support**: Convert between 30+ file formats
- **Batch Processing**: Convert multiple files at once
- **Modern UI**: Beautiful dark-themed interface with macOS-native feel
- **Three Conversion Modes**:
  - **Image Mode**: PNG, JPEG, WEBP, ICNS, PDF, TIFF, BMP, ICO, HEIC, SVG
  - **Video Mode**: MP4, MOV, AVI, MKV, WEBM, WMV, FLV, MPEG, GIF
  - **Audio Mode**: MP3, WAV, FLAC, AAC, M4A, OGG, WMA, AIFF
- **HEIC Support**: Native support for Apple's HEIC image format
- **Progress Tracking**: Real-time progress bar and file status indicators
- **Error Handling**: Clear error messages and success indicators

## 🎨 Screenshots

The app features a sleek sidebar with:
- File management controls (Add Files, Add Folder, Clear Queue)
- Format selection with categorized options (Image/Audio/Video)
- Large, prominent conversion button

The main area displays:
- File queue with visual file type indicators
- Progress tracking
- Status updates

## 📋 Requirements

- **macOS**: 10.15 (Catalina) or later
- **Python**: 3.12 or later (for development)
- **ffmpeg**: Required for video/audio conversion (install via Homebrew)
- **Cairo**: Required for SVG format support (install via Homebrew)

### Installing Dependencies

```bash
# Required for video/audio conversion
brew install ffmpeg

# Required for SVG format support
brew install cairo
```

## 🚀 Installation

### Option 1: Build from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/as4401s/Mac-Universal-Converter.git
   cd Mac-Universal-Converter
   ```

2. Install dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```

3. Build the application:
   ```bash
   uv run python build_app.py
   ```

4. Find the built app in the `dist` folder: `dist/MacConverter.app`

## 💻 Usage

1. **Launch the app**: Double-click `MacConverter.app`

2. **Add files**:
   - Click "Add Files" to select individual files
   - Click "Add Folder" to add all supported files from a folder

3. **Select output format**:
   - Choose the conversion mode (Image/Audio/Video) using the segmented button
   - Select your desired output format from the dropdown

4. **Convert**:
   - Click "START CONVERSION"
   - Choose the output directory
   - Wait for the conversion to complete

5. **View results**: Check the status indicators:
   - 🟢 Green border = Success
   - 🔴 Red border = Error
   - 🟡 Yellow border = Skipped (incompatible format)

## 📁 Supported Formats

### Image Formats
- **Input**: JPG, JPEG, PNG, HEIC, WEBP, BMP, TIFF, ICO, PDF, SVG
- **Output**: PNG, JPEG, JPG, WEBP, ICNS, PDF, TIFF, BMP, ICO, HEIC, SVG

### Video Formats
- **Input**: MP4, MOV, AVI, MKV, WEBM, WMV, FLV, MPEG, GIF
- **Output**: MP4, MOV, AVI, MKV, WEBM, WMV, FLV, MPEG, GIF

### Audio Formats
- **Input**: MP3, WAV, FLAC, M4A, OGG, WMA, AIFF, AAC (also extracts from video)
- **Output**: MP3, WAV, FLAC, AAC, M4A, OGG, WMA, AIFF

## 🛠️ Development

### Project Structure

```
Mac-Universal-Converter/
├── converter.py          # Main application code
├── build_app.py          # PyInstaller build script
├── pyproject.toml        # Project dependencies
├── AppIcon.icns          # Application icon
├── README.md             # This file
└── dist/                 # Built application (after build)
```

### Dependencies

- **customtkinter**: Modern, customizable Tkinter widgets
- **Pillow**: Image processing
- **pillow-heif**: HEIC format support
- **cairosvg**: SVG format support
- **moviepy**: Video and audio processing
- **PyInstaller**: Application bundling

### Running in Development

```bash
uv run python converter.py
```

### Building the App

The build script (`build_app.py`) handles:
- Collecting all dependencies
- Including package metadata (fixes import errors)
- Bundling CustomTkinter assets
- Creating a macOS .app bundle
- Setting the application icon

```bash
uv run python build_app.py
```

## 🐛 Troubleshooting

### App won't open
- Ensure ffmpeg is installed: `brew install ffmpeg`
- Check Console.app for error messages
- Try running from terminal: `dist/MacConverter.app/Contents/MacOS/MacConverter`

### Video/Audio conversion fails
- Verify ffmpeg installation: `ffmpeg -version`
- Check file permissions
- Ensure sufficient disk space

### HEIC files not opening
- The app includes pillow-heif, but may require system libraries
- Try converting HEIC files using the Image mode

### SVG conversion not working
- Ensure Cairo is installed: `brew install cairo`
- SVG support requires the Cairo library to be available on your system
- The app will work without Cairo, but SVG conversion features will be disabled

## 📝 Notes

- **ICNS Format**: When converting to ICNS, images are automatically resized to 1024x1024 for optimal quality
- **SVG Format**: SVG conversion requires Cairo library (`brew install cairo`). SVG to raster conversion uses cairosvg, while raster to SVG embeds the image as base64-encoded PNG
- **Video Codecs**: Uses libx264 for most video formats, libvpx for WebM
- **Audio Extraction**: Can extract audio from video files
- **Batch Processing**: All files in the queue are processed sequentially

## 👤 Author

**Arjun Sarkar**

Built with ❤️ for macOS users

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/as4401s/Mac-Universal-Converter/issues).

## 🙏 Acknowledgments

- CustomTkinter for the beautiful UI framework
- Pillow and MoviePy for media processing capabilities
- The open-source community for amazing tools and libraries

---

**Made for macOS** 🍎
