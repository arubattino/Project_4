from unittest import result
import utils
import os
import middleware
from middleware import model_predict
import settings



from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify, 
    current_app
)

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """
    return render_template("index.html")


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):                  

        file_hash = utils.get_file_hash(file)
        dst_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_hash)
        if not os.path.exists(dst_filepath):
            file.save(dst_filepath)
        flash("Image successfully uploaded and displayed below")
        prediction, score = model_predict(file_hash)
        context = {
            "prediction": prediction,
            "score": score,
            "filename": file.filename,
        }

        # Update `render_template()` parameters as needed
        return render_template("index.html", filename=file_hash, context=context)

    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    )


@router.route("/predict", methods=["POST"])
def predict():
    
    
    rpse = {"success": False, "prediction": None, "score": None}

    if "file" in request.files and utils.allowed_file(request.files["file"].filename):

        file = request.files["file"]
        file_hash=utils.get_file_hash(file)
        dst_filepath=os.path.join(current_app.config["UPLOAD_FOLDER"], file_hash)

        if not os.path.exists(dst_filepath):
            file.save(dst_filepath)

        prediction, score = model_predict(file_hash)
        rpse["success"] = True
        rpse["prediction"] = prediction
        rpse["score"] = score

        return jsonify(rpse), 200
    
    return jsonify(rpse), 400



@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    
    # Get reported predictions from `report` key
    report = request.form.get("report")

    # Store the reported data to a file on the corresponding path
    # already provided in settings.py module
    
    if report:
        with open(settings.FEEDBACK_FILEPATH, "a+") as f:
            f.write(report + "\n")

    return render_template("index.html")
