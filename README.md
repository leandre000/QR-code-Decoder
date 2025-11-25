# Professional QR Code Scanner

A comprehensive, professional-grade QR code scanner application built with Python. This tool supports scanning QR codes from webcam feeds, image files, and entire directories with both command-line and graphical user interfaces.

## Features

- 🎥 **Webcam Scanning**: Real-time QR code detection from webcam feed
- 📷 **Image File Scanning**: Scan QR codes from various image formats (JPG, PNG, BMP, TIFF, GIF)
- 📁 **Directory Scanning**: Batch scan all images in a directory (with recursive option)
- 🖥️ **GUI Application**: User-friendly graphical interface built with Tkinter
- 💻 **CLI Tool**: Command-line interface for automation and scripting
- 📊 **Export Results**: Save results in JSON or plain text format
- 🔍 **Multiple Code Detection**: Detect and decode multiple QR codes in a single image
- 📝 **Detailed Logging**: Comprehensive logging for debugging and audit trails
- ⚡ **Real-time Preview**: Visual feedback with bounding boxes around detected codes

## Installation

### Prerequisites

- Python 3.7 or higher
- Webcam (for webcam scanning feature)
- System dependencies for pyzbar:
  - **Windows**: No additional dependencies needed
  - **Linux**: `sudo apt-get install libzbar0`
  - **macOS**: `brew install zbar`

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode (Recommended for beginners)

Launch the graphical interface:

```bash
python qr_scanner.py --gui
```

Or simply:

```bash
python qr_scanner.py
```

The GUI provides:
- Easy file selection dialogs
- Real-time webcam scanning
- Visual results display
- Export functionality

### Command-Line Mode

#### Scan from Webcam

```bash
# Scan for 30 seconds (default)
python qr_scanner.py --webcam

# Scan indefinitely (until 'q' is pressed)
python qr_scanner.py --webcam --duration 0

# Scan without preview window
python qr_scanner.py --webcam --no-preview
```

#### Scan from Image File

```bash
python qr_scanner.py --image path/to/image.jpg
```

#### Scan Directory

```bash
# Scan all images in directory (recursive by default)
python qr_scanner.py --directory ./images

# Non-recursive scan
python qr_scanner.py --directory ./images --no-recursive
```

#### Export Results

```bash
# Export to JSON
python qr_scanner.py --image photo.jpg --output results.json

# Export to text file
python qr_scanner.py --image photo.jpg --output results.txt
```

## Output Format

### JSON Output

```json
{
  "scan_date": "2025-01-27T10:30:00",
  "total_codes": 2,
  "results": [
    {
      "data": "https://example.com",
      "type": "QRCODE",
      "rect": {
        "left": 100,
        "top": 150,
        "width": 200,
        "height": 200
      },
      "polygon": [[100, 150], [300, 150], [300, 350], [100, 350]],
      "source": "webcam",
      "timestamp": "2025-01-27T10:30:15.123456"
    }
  ]
}
```

### Text Output

```
QR Code Scan Results
Date: 2025-01-27 10:30:00
Total Codes Found: 2
==================================================

Code #1
Data: https://example.com
Type: QRCODE
Source: webcam
Timestamp: 2025-01-27T10:30:15.123456
--------------------------------------------------
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- GIF (.gif)

## Examples

### Example 1: Quick Webcam Scan

```bash
python qr_scanner.py --webcam --duration 10
```

### Example 2: Batch Process Images

```bash
python qr_scanner.py --directory ./qr_images --output batch_results.json
```

### Example 3: Single Image with Export

```bash
python qr_scanner.py --image qr_code.png --output result.txt
```

## Project Structure

```
qr-code-scanner/
├── qr_scanner.py          # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── qr_scanner.log         # Application logs (generated)
```

## Logging

The application creates detailed logs in `qr_scanner.log` with timestamps, log levels, and messages for debugging and audit purposes.

## Error Handling

The scanner includes comprehensive error handling for:
- Missing or invalid image files
- Camera access issues
- Corrupted images
- Unsupported formats
- Network issues (for URL-based QR codes)

## Performance

- Real-time webcam processing at 30 FPS
- Fast batch processing of image directories
- Efficient memory usage for large images
- Multi-threaded GUI operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created with ❤️ for professional QR code scanning needs.

## Troubleshooting

### Camera not working
- Ensure your webcam is connected and not being used by another application
- Check camera permissions in your operating system settings

### No QR codes detected
- Ensure the QR code is clearly visible and not damaged
- Try adjusting lighting conditions
- Make sure the QR code is in focus

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.7 or higher: `python --version`

## Future Enhancements

- [ ] Support for barcode scanning (Code128, EAN, etc.)
- [ ] QR code generation capabilities
- [ ] Cloud storage integration
- [ ] API server mode
- [ ] Mobile app integration
- [ ] Advanced filtering and search
- [ ] Batch export to multiple formats
- [ ] QR code validation and verification
