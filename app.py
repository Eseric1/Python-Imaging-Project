from flask import Flask, request, render_template, make_response, send_file
from PIL import Image
from wand.image import Image
import base64

app = Flask(__name__, template_folder='template')

@app.route("/")
def index():
    # render the index.html template
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # get the photo from the request form data
    photo = request.files["photo"]
    # open the photo using PIL
    image = Image.open(photo)
    # get the image format and size
    format = image.format
    size = image.size
    # return a message with the image details
    return f"You uploaded a {format} image with size {size}"

@app.route("/edit", methods=["POST"])
def edit():
    # get the photo and the sliders values from the request
    photo = request.files["photo"]
    slider1 = request.form["slider1"]
    slider2 = request.form["slider2"]
    # open the photo using wand
    with Image(file=photo) as image:
        # apply some imagemagick commands based on the sliders values
        # for example, flip the image if slider1 is 1
        if slider1 == "1":
            image.flip()
        # for example, resize the image by slider2 percent
        width = int(image.width * int(slider2) / 100)
        height = int(image.height * int(slider2) / 100)
        image.resize(width, height)
        # save the edited image to a temporary file
        image.save(filename="temp.jpg")
    # return the edited image as a file
    return send_file("temp.jpg", mimetype="image/jpeg")
    # alternatively, return the edited image as a base64 encoded string
    # with open("temp.jpg", "rb") as f:
    #     encoded = base64.b64encode(f.read()).decode()
    # return {"image": encoded}

if __name__ == "__main__":
    app.run(debug=True)