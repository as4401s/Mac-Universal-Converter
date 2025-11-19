import PyInstaller.__main__
import customtkinter
import os
import shutil
import sys

def build():
    print("--- 🚀 Starting Build Process ---")

    # 1. Get the path to customtkinter library
    # We need this to include the theme files (json/images) in the app
    ctk_path = os.path.dirname(customtkinter.__file__)
    print(f"Found CustomTkinter at: {ctk_path}")

    # 2. Check for Icon
    icon_option = []
    if os.path.exists("AppIcon.icns"):
        print("✅ Using AppIcon.icns")
        icon_option = ['--icon=AppIcon.icns']
    else:
        print("⚠️ Warning: AppIcon.icns not found. Using default Python icon.")

    # 3. Collect all hidden imports needed
    hidden_imports = [
        # Core dependencies
        'pillow_heif',
        'PIL._tkinter_finder',  # PIL tkinter support
        'PIL._webp',  # WebP support
        
        # MoviePy and all its submodules
        'moviepy',
        'moviepy.editor',
        'moviepy.video',
        'moviepy.video.io',
        'moviepy.video.fx',
        'moviepy.video.fx.all',
        'moviepy.audio',
        'moviepy.audio.io',
        'moviepy.audio.fx',
        'moviepy.audio.fx.all',
        'moviepy.config',
        'moviepy.tools',
        
        # MoviePy dependencies
        'proglog',
        'decorator',
        'imageio',
        'imageio_ffmpeg',
        'numpy',
        'requests',
        'tqdm',
        
        # Additional moviepy submodules that might be needed
        'moviepy.video.tools',
        'moviepy.audio.tools',
        'moviepy.video.compositing',
        'moviepy.audio.AudioClip',
        'moviepy.video.VideoClip',
    ]

    # 4. Collect package metadata (needed for imageio and other packages)
    # This fixes the "No package metadata was found" error
    collect_metadata = [
        '--copy-metadata=imageio',
        '--copy-metadata=imageio_ffmpeg',
        '--copy-metadata=moviepy',
        '--copy-metadata=proglog',
        '--copy-metadata=numpy',
        '--copy-metadata=Pillow',
        '--copy-metadata=pillow-heif',
    ]

    # 5. Build PyInstaller command
    # Using --onedir for better macOS compatibility and reliability
    # PyInstaller will automatically create .app bundle on macOS
    params = [
        'converter.py',                   # Your main script
        '--name=MacConverter',            # Name of the App
        '--noconsole',                    # Don't show terminal window
        '--clean',                        # Clean build cache
        '--onedir',                       # Create directory bundle (better for macOS)
        '--windowed',                     # macOS windowed app
        
        # CustomTkinter Data
        f'--add-data={ctk_path}{os.pathsep}customtkinter',
        
        # Collect metadata
    ] + collect_metadata + [f'--hidden-import={imp}' for imp in hidden_imports] + icon_option

    # 6. Add macOS-specific options for universal compatibility
    if sys.platform == 'darwin':
        # Note: --target-arch might not be available in all PyInstaller versions
        # It will build for the current architecture, which is fine for distribution
        params.append('--osx-bundle-identifier=com.arjunsarkar.macconverter')

    print("\n--- Building with PyInstaller ---")
    print(f"Parameters: {' '.join(params[:5])}... (and {len(params)-5} more)")
    
    # 7. Run PyInstaller
    PyInstaller.__main__.run(params)

    print("\n--- ✅ Build Complete! ---")
    print("Look in the 'dist' folder for 'MacConverter.app'")
    print("\n⚠️  Note: MoviePy requires ffmpeg to be installed on the target Mac.")
    print("   Users will need to install ffmpeg via Homebrew: brew install ffmpeg")

if __name__ == "__main__":
    build()