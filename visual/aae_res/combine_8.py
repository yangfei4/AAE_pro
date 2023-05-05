from PIL import Image
import os

def combine_images_horizontally(image_dir):
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')][:8]
    images = [Image.open(os.path.join(image_dir, f)) for f in image_files]

    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]

    return new_image

def combine_images_vertically(image_dir):
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')][:10]
    images = [Image.open(os.path.join(image_dir, f)) for f in image_files]

    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    new_image = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for image in images:
        new_image.paste(image, (0, y_offset))
        y_offset += image.size[1]

    return new_image

def main():
    # nums = {'2','5','12','14','15','16','18','27','29'}

    # for num in nums:
    #     image_dir = f"{num}_combined"
    #     combined_image = combine_images_horizontally(image_dir)
    #     combined_image.save(f"{num}_combined.png")
    image_dir = './'
    combined_image = combine_images_vertically(image_dir)
    combined_image.save('combined_image_vertical.png')

if __name__ == '__main__':
    main()
