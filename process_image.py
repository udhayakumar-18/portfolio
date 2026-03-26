import sys
try:
    from PIL import Image
    from rembg import remove
except ImportError:
    print("Please install required packages first by running: pip install rembg pillow")
    sys.exit(1)

input_path = 'photo.jpg'
output_path = 'profile.png'

print(f"Reading {input_path}...")
try:
    with open(input_path, 'rb') as i:
        input_data = i.read()
    
    print("Removing background...")
    output_data = remove(input_data)
    
    # We can just load the output data into PIL
    import io
    img = Image.open(io.BytesIO(output_data))
    
    print("Cropping and centering image...")
    
    # Find bounding box (left, upper, right, lower)
    bbox = img.getbbox()
    if bbox:
        left, upper, right, lower = bbox
        person_height = lower - upper
        # Crop just below the watch, which is about 55% down the person's body
        new_lower = upper + int(person_height * 0.55)
        
        # Crop the image to this new tight bounding box
        img = img.crop((left, upper, right, new_lower))
        
    # We want a square output so it fits perfectly in the circular CSS
    width, height = img.size
    max_dim = max(width, height)
    
    # Create a new square transparent image
    square_img = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
    
    # Paste the cropped image centered horizontally, and aligned to the BOTTOM vertically
    # This ensures the hard cut from the crop aligns perfectly at the bottom of the circle
    offset_x = (max_dim - width) // 2
    offset_y = max_dim - height
    
    square_img.paste(img, (offset_x, offset_y))
    
    # Save the final image
    square_img.save(output_path)
    print(f"Successfully processed! Saved to {output_path}")
    
except Exception as e:
    print(f"An error occurred: {e}")
