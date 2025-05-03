# app.py
#To run your app - python app.py

from flask import Flask, render_template, request, send_file
import processor
import os
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    selected_color = "Blue"

    if request.method == "POST":
        selected_color = request.form["color"]
        output_path = f"static/output_{selected_color.lower()}.jpg"

        # Check if the file already exists
        if not os.path.exists(output_path):
            processor.save_recolored_image(selected_color, output_path)

        return render_template(
            "index.html",
            image=f"/{output_path}",
            colors=processor.get_color_options(),
            selected=selected_color
        )

    # GET request - initial load with default color
    output_path = f"static/output_{selected_color.lower()}.jpg"
    if not os.path.exists(output_path):
        processor.save_recolored_image(selected_color, output_path)

    return render_template(
        "index.html",
        image=f"/{output_path}",
        colors=processor.get_color_options(),
        selected=selected_color
    )

if __name__ == "__main__":
    app.run(debug=True)
