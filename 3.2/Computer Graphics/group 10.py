import numpy as np
from PIL import Image

def apply_color_lut(image_path, lut_path, output_path):
    """
    Apply a 2D color lookup table to an image.
    
    Args:
        image_path (str): Path to input image
        lut_path (str): Path to LUT image (e.g., 512x512 texture)
        output_path (str): Path to save processed image
    """
    
    # Load the input image and LUT
    input_img = Image.open(image_path).convert('RGB')
    lut_img = Image.open(lut_path).convert('RGB')
    
    # Convert images to numpy arrays for processing
    img_array = np.array(input_img).astype(float) / 255.0  # Normalize to [0,1]
    lut_array = np.array(lut_img).astype(float) / 255.0
    
    # Get dimensions
    img_height, img_width = img_array.shape[:2]
    lut_height, lut_width = lut_array.shape[:2]
    
    # Typically, LUT is square (e.g., 512x512) with 64x8 grid of 8x8 cells
    # Each cell represents a blue value, rows are green, columns are red
    cell_size = lut_width // 8  # Assuming 8x8 grid (64 cells total)
    
    # Create output array
    output_array = np.zeros_like(img_array)
    
    # Process each pixel
    for y in range(img_height):
        for x in range(img_width):
            # Get original RGB values
            r, g, b = img_array[y, x]
            
            # Calculate LUT coordinates
            # Blue determines which 8x8 cell to use (0-7)
            blue_idx = int(b * 7)  # 0-7 range
            cell_y = blue_idx * cell_size
            
            # Red and Green determine position within the cell
            red_idx = int(r * (cell_size - 1))    # 0-63 range within cell
            green_idx = int(g * (cell_size - 1))  # 0-63 range within cell
            
            # Calculate final LUT coordinates
            lut_x = blue_idx * cell_size + red_idx
            lut_y = green_idx
            
            # Ensure coordinates are within bounds
            lut_x = min(max(lut_x, 0), lut_width - 1)
            lut_y = min(max(lut_y, 0), lut_height - 1)
            
            # Get the color from LUT
            output_array[y, x] = lut_array[lut_y, lut_x]
    
    # Convert back to 0-255 range and save
    output_img = Image.fromarray((output_array * 255).astype(np.uint8))
    output_img.save(output_path)
    return output_img

# Example usage
def main():
    # Example file paths (you'd replace these with actual paths)
    input_image = "input.jpg"
    lut_image = "trial1.png"  # Should be a 512x512 LUT texture
    output_image = "output.png"
    
    try:
        result = apply_color_lut(input_image, lut_image, output_image)
        print(f"Image processed successfully. Saved to {output_image}")
    except Exception as e:
        print(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()