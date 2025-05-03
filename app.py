from flask import Flask, render_template, request
import processor
import os
from processor import hex_to_bgr


app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    selected_color = "#0000ff"  # Default color blue
    color_bgr = (255, 0, 0)     # Default BGR for blue
    error_message = None

    if request.method == "POST":
        color_input = request.form.get("color_text") or request.form.get("color") or "#0000ff"
        selected_color = color_input

        try:
            # Convert hex color to BGR
            color_bgr = hex_to_bgr(color_input)
        except ValueError as e:
            # Show error message if invalid color format
            error_message = str(e)
            return render_template(
                "index.html",
                image=None,
                selected=selected_color,
                error=error_message
            )

        output_path = f"static/output_{color_input.strip('#').lower()}.jpg"

        if not os.path.exists(output_path):
            processor.save_custom_color_image(color_bgr, output_path)

        return render_template(
            "index.html",
            image=f"/{output_path}",
            selected=selected_color,
            error=error_message
        )

    # If GET request or page reload, render with default image
    output_path = f"static/output_{selected_color.strip('#').lower()}.jpg"
    if not os.path.exists(output_path):
        processor.save_custom_color_image(color_bgr, output_path)

    return render_template(
        "index.html",
        image=f"/{output_path}",
        selected=selected_color,
        error=error_message
    )

if __name__ == "__main__":
    app.run(debug=True)
