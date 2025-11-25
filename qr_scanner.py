#!/usr/bin/env python3
"""
Professional QR Code Scanner
A comprehensive tool for scanning QR codes from webcam, images, and files.
"""

import cv2
import numpy as np
from pyzbar import pyzbar
import argparse
import sys
import json
import os
from datetime import datetime
from pathlib import Path
import logging
from typing import List, Dict, Optional, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qr_scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class QRCodeScanner:
    """Main QR Code Scanner class with multiple scanning capabilities."""
    
    def __init__(self, output_file: Optional[str] = None):
        self.output_file = output_file
        self.results = []
        self.camera = None
        
    def scan_image(self, image_path: str) -> List[Dict]:
        """
        Scan QR codes from an image file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of detected QR codes with their data
        """
        try:
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return []
            
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return []
            
            return self._decode_qr_codes(image, source=image_path)
        except Exception as e:
            logger.error(f"Error scanning image {image_path}: {str(e)}")
            return []
    
    def scan_webcam(self, duration: int = 30, show_preview: bool = True) -> List[Dict]:
        """
        Scan QR codes from webcam feed.
        
        Args:
            duration: Duration in seconds to scan (0 for infinite)
            show_preview: Whether to show camera preview
            
        Returns:
            List of detected QR codes with their data
        """
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                logger.error("Failed to open camera")
                return []
            
            logger.info("Starting webcam scan... Press 'q' to quit")
            start_time = datetime.now()
            detected_codes = set()  # To avoid duplicates
            
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                # Check duration limit
                if duration > 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    if elapsed >= duration:
                        break
                
                # Decode QR codes
                codes = self._decode_qr_codes(frame, source="webcam")
                for code in codes:
                    code_str = code.get('data', '')
                    if code_str and code_str not in detected_codes:
                        detected_codes.add(code_str)
                        self.results.append(code)
                        logger.info(f"QR Code detected: {code_str[:50]}...")
                
                if show_preview:
                    # Draw bounding boxes
                    frame = self._draw_bounding_boxes(frame, codes)
                    cv2.imshow('QR Code Scanner - Press Q to quit', frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
            if show_preview:
                cv2.destroyAllWindows()
            
            self._release_camera()
            return list(self.results)
            
        except Exception as e:
            logger.error(f"Error during webcam scan: {str(e)}")
            self._release_camera()
            return []
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        """
        Scan QR codes from all images in a directory.
        
        Args:
            directory: Directory path to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of detected QR codes with their data
        """
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
        results = []
        
        try:
            path = Path(directory)
            if not path.exists():
                logger.error(f"Directory not found: {directory}")
                return []
            
            pattern = '**/*' if recursive else '*'
            image_files = [f for f in path.glob(pattern) 
                          if f.suffix.lower() in supported_formats]
            
            logger.info(f"Found {len(image_files)} image files to scan")
            
            for image_file in image_files:
                logger.info(f"Scanning: {image_file}")
                codes = self.scan_image(str(image_file))
                results.extend(codes)
                
        except Exception as e:
            logger.error(f"Error scanning directory: {str(e)}")
        
        return results
    
    def _decode_qr_codes(self, image: np.ndarray, source: str = "unknown") -> List[Dict]:
        """Internal method to decode QR codes from image array."""
        codes = pyzbar.decode(image)
        results = []
        
        for code in codes:
            result = {
                'data': code.data.decode('utf-8'),
                'type': code.type,
                'rect': {
                    'left': code.rect.left,
                    'top': code.rect.top,
                    'width': code.rect.width,
                    'height': code.rect.height
                },
                'polygon': [(p.x, p.y) for p in code.polygon],
                'source': source,
                'timestamp': datetime.now().isoformat()
            }
            results.append(result)
        
        return results
    
    def _draw_bounding_boxes(self, image: np.ndarray, codes: List[Dict]) -> np.ndarray:
        """Draw bounding boxes around detected QR codes."""
        for code in codes:
            polygon = code.get('polygon', [])
            if polygon:
                points = np.array(polygon, dtype=np.int32)
                cv2.polylines(image, [points], True, (0, 255, 0), 2)
                
                # Add text label
                rect = code.get('rect', {})
                cv2.putText(image, 'QR Code', 
                           (rect.get('left', 0), rect.get('top', 0) - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image
    
    def _release_camera(self):
        """Release camera resources."""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """
        Save scan results to JSON file.
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = self.output_file or f"qr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output = {
            'scan_date': datetime.now().isoformat(),
            'total_codes': len(self.results),
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename}")
        return filename
    
    def export_to_text(self, filename: Optional[str] = None) -> str:
        """
        Export results to plain text file.
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"qr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"QR Code Scan Results\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Codes Found: {len(self.results)}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, result in enumerate(self.results, 1):
                f.write(f"Code #{i}\n")
                f.write(f"Data: {result['data']}\n")
                f.write(f"Type: {result['type']}\n")
                f.write(f"Source: {result['source']}\n")
                f.write(f"Timestamp: {result['timestamp']}\n")
                f.write("-" * 50 + "\n\n")
        
        logger.info(f"Results exported to {filename}")
        return filename


class QRScannerGUI:
    """GUI application for QR Code Scanner."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Professional QR Code Scanner")
        self.root.geometry("800x600")
        self.scanner = QRCodeScanner()
        self.scanning = False
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create GUI widgets."""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Scan Image...", command=self.scan_image_file)
        file_menu.add_command(label="Scan Directory...", command=self.scan_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results...", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="Scan from Webcam", 
                 command=self.scan_webcam, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Scan Image File", 
                 command=self.scan_image_file, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Scan Directory", 
                 command=self.scan_directory, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Results", 
                 command=self.clear_results, width=15).pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_label = tk.Label(main_frame, text="Scan Results:", font=("Arial", 12, "bold"))
        results_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(main_frame, height=20, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = tk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(5, 0))
    
    def scan_webcam(self):
        """Start webcam scanning in a separate thread."""
        if self.scanning:
            messagebox.showwarning("Warning", "Scanning already in progress")
            return
        
        def scan_thread():
            self.scanning = True
            self.update_status("Scanning from webcam... Press 'q' in camera window to stop")
            codes = self.scanner.scan_webcam(duration=0, show_preview=True)
            self.scanning = False
            self.update_results()
            self.update_status(f"Scan complete. Found {len(codes)} QR code(s)")
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def scan_image_file(self):
        """Open file dialog and scan selected image."""
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.update_status(f"Scanning {os.path.basename(filename)}...")
            codes = self.scanner.scan_image(filename)
            self.scanner.results.extend(codes)
            self.update_results()
            self.update_status(f"Found {len(codes)} QR code(s) in image")
    
    def scan_directory(self):
        """Open directory dialog and scan all images."""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        
        if directory:
            self.update_status(f"Scanning directory: {directory}...")
            codes = self.scanner.scan_directory(directory, recursive=True)
            self.scanner.results.extend(codes)
            self.update_results()
            self.update_status(f"Found {len(codes)} QR code(s) in directory")
    
    def clear_results(self):
        """Clear all scan results."""
        self.scanner.results = []
        self.update_results()
        self.update_status("Results cleared")
    
    def export_results(self):
        """Export results to file."""
        if not self.scanner.results:
            messagebox.showinfo("Info", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            if filename.endswith('.txt'):
                self.scanner.export_to_text(filename)
            else:
                self.scanner.save_results(filename)
            messagebox.showinfo("Success", f"Results saved to {filename}")
    
    def update_results(self):
        """Update results display."""
        self.results_text.delete(1.0, tk.END)
        
        if not self.scanner.results:
            self.results_text.insert(tk.END, "No QR codes detected yet.\n")
            return
        
        self.results_text.insert(tk.END, f"Total QR Codes Found: {len(self.scanner.results)}\n\n")
        
        for i, result in enumerate(self.scanner.results, 1):
            self.results_text.insert(tk.END, f"Code #{i}\n")
            self.results_text.insert(tk.END, f"Data: {result['data']}\n")
            self.results_text.insert(tk.END, f"Type: {result['type']}\n")
            self.results_text.insert(tk.END, f"Source: {result['source']}\n")
            self.results_text.insert(tk.END, f"Timestamp: {result['timestamp']}\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n\n")
    
    def update_status(self, message: str):
        """Update status bar."""
        self.status_label.config(text=message)
        self.root.update_idletasks()


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Professional QR Code Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --webcam                    # Scan from webcam
  %(prog)s --image photo.jpg           # Scan from image file
  %(prog)s --directory ./images        # Scan all images in directory
  %(prog)s --gui                       # Launch GUI application
        """
    )
    
    parser.add_argument('--webcam', action='store_true',
                       help='Scan QR codes from webcam')
    parser.add_argument('--image', type=str,
                       help='Path to image file to scan')
    parser.add_argument('--directory', type=str,
                       help='Directory containing images to scan')
    parser.add_argument('--recursive', action='store_true', default=True,
                       help='Recursively scan subdirectories (default: True)')
    parser.add_argument('--output', type=str,
                       help='Output file for results (JSON or TXT)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Webcam scan duration in seconds (0 for infinite)')
    parser.add_argument('--no-preview', action='store_true',
                       help='Disable camera preview window')
    parser.add_argument('--gui', action='store_true',
                       help='Launch GUI application')
    
    args = parser.parse_args()
    
    # Launch GUI if requested
    if args.gui or (not args.webcam and not args.image and not args.directory):
        root = tk.Tk()
        app = QRScannerGUI(root)
        root.mainloop()
        return
    
    # CLI mode
    scanner = QRCodeScanner(output_file=args.output)
    
    try:
        if args.webcam:
            codes = scanner.scan_webcam(duration=args.duration, 
                                       show_preview=not args.no_preview)
            print(f"\nDetected {len(codes)} QR code(s)")
            
        elif args.image:
            codes = scanner.scan_image(args.image)
            print(f"\nDetected {len(codes)} QR code(s) in {args.image}")
            
        elif args.directory:
            codes = scanner.scan_directory(args.directory, recursive=args.recursive)
            print(f"\nDetected {len(codes)} QR code(s) in directory")
        
        # Display results
        for i, code in enumerate(scanner.results, 1):
            print(f"\nCode #{i}:")
            print(f"  Data: {code['data']}")
            print(f"  Type: {code['type']}")
            print(f"  Source: {code['source']}")
        
        # Save results if output specified
        if args.output:
            if args.output.endswith('.txt'):
                scanner.export_to_text(args.output)
            else:
                scanner.save_results(args.output)
        elif scanner.results:
            scanner.save_results()
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        scanner._release_camera()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

