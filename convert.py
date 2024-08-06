"""
Converts a video file to H.265 format using ffmpeg.
Replaces the original file if the new file is smaller in size.
"""

import os
import sys
import logging
import ffmpeg

from pydantic import BaseModel

# Set up logging to add timestamps to the output
# Set up logging to add timestamps to the output
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessor(BaseModel):
    input_file: str
    input_size: int = 0
    output_file: str = ""
    output_size: int = 0

    def __init__(self, input_file: str):
        """Post-initialization to set up additional attributes."""
        super().__init__(input_file=input_file)
        file_without_ext, _ = os.path.splitext(input_file)
        self.output_file = f"{file_without_ext}.temp.mkv"
        logger.info(f"Setup Processor for: {input_file} => {self.output_file}")

    def convert_to_h265(self):
        """Converts the input video file to H.265 format using ffmpeg.
        """
        try:
            ffmpeg.input(
                self.input_file
            ).output(
                self.output_file, vcodec='libx265', crf=28
            ).run(overwrite_output=True)
            return True
        except ffmpeg.Error as e:
            logger.info(f"Error occurred: {e}")
            return False

    def compare_and_replace(self):
        """Compares the size of the input and output files.
        Replaces the input file with the output file if the output file is smaller.

        Args:
            input_file (str): Path to the input file.
            output_file (str): Path to the output file.
        """
        self.input_size = os.path.getsize(self.input_file)
        self.output_size = os.path.getsize(self.output_file)

        if self.output_size < self.input_size:
            os.replace(self.output_file, self.input_file)
            print(f"Replaced {self.input_file} with the smaller {self.output_file}")
        else:
            os.remove(self.output_file)
            print(f"Retained original {self.input_file}, new file {self.output_file} is not smaller")
            
        input_size_gb = self.input_size / (1024 * 1024 * 1024)
        output_size_gb = self.output_size / (1024 * 1024 * 1024)
        print(f"-- Original size: {input_size_gb}gb, New size: {output_size_gb}gb")

    def process(self):
        """Converts the video file to H.265 format and replaces the original file if the new file is smaller.

        Args:
            file_path (str): Path to the video file.
        """
        if self.convert_to_h265():
            self.compare_and_replace()
        else:
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
            print(f"Failed to convert {self.input_file}")

    def to_dict(self):
        return {
            "input_file": self.input_file,
            "input_size": self.input_size,
            "output_file": self.output_file,
            "output_size": self.output_size
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <video_file>")
    else:
        video_file = sys.argv[1]
        processor = VideoProcessor(input_file=video_file)
        processor.process()
        logger.info(f"Processed: {processor.to_dict()}")
