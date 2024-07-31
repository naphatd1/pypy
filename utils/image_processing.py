from PIL import Image, ImageDraw, ImageFont
import io

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it."""
    buf = io.BytesIO()
    fig.savefig(buf, transparent=True)
    buf.seek(0)
    img = Image.open(buf).convert('RGBA')
    return img

def resize_image(image, max_width, max_height):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    if original_width > original_height:
        new_width = min(max_width, original_width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(max_height, original_height)
        new_width = int(new_height * aspect_ratio)

    return image.resize((new_width, new_height), Image.LANCZOS)

def draw_text(image, position, text, font="fonts/THSarabunNew Bold.ttf", font_size=40, anchor="la"):
  """Draws text on an image with options for font, size, alignment, and fill color.

  Args:
      image: The PIL image object to draw on.
      position: A tuple (x, y) representing the top-left corner of the text.
      text: The text string to draw.
      font: Path to the font file (optional, default: THSarabunNew Bold.ttf).
      font_size: Size of the text in pixels (optional, default: 20).
      anchor: Alignment of drawn text relative to the xy parameter (optional, default: la).

  Raises:
      ValueError: If the alignment is not one of "left", "center", or "right".
  """
  # Check and adjust fill color based on image mode
  image_mode = image.mode
  if image_mode == "L":
      fill = 0  # Use 0 for black or a value between 0-255 for shades of gray
  else:
      fill = (0, 0, 0)  # Black for RGB/RGBA images

  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype(font, font_size)
  draw.multiline_text(position, text, font=font, fill=fill, anchor=anchor)
