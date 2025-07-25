"""
Main file for launching the Flask backend
"""

import logging
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

from bson import json_util, ObjectId
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from pynpm import NPMPackage

import configs
from assessment import Assessment, get_all_assessments
from configs import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIMETYPES,
    FRONTEND_BASE,
    FRONTEND_BUILD,
    MONGO_URI,
    UPLOADS_BASE,
)
from userinput import UserInput
from exceptions import DBError, OutputFormatError, UserInputError


def _get_last_modified_time(path: Path):
    """
    Recursive function to get last modified time of a path in nanoseconds.
    If a directory is passed, returns the last modified time of the whole tree
    under the directory.
    """
    ret = path.stat().st_mtime_ns
    if path.is_dir():
        for child in path.iterdir():
            ret = max(ret, _get_last_modified_time(child))

    return ret


def _get_directory_newest_member(path: Path):
    """
    Helper function to get path to last modified child of the directory passed
    """
    times_and_paths = [(_get_last_modified_time(i), i) for i in path.iterdir()]
    return max(times_and_paths)[1]


def rebuild_frontend():
    """
    Function to rebuild frontend (if it is outdated)
    """
    # This block of code is needed to ensure that this function is running only
    # once, even when there are multiple processes
    lock_file = Path("temp.lock")
    try:
        lock_file.touch(exist_ok=False)
    except FileExistsError:
        return

    try:
        if _get_directory_newest_member(FRONTEND_BASE) != FRONTEND_BUILD:
            print("Rebuilding frontend build...")
            pkg = NPMPackage(str(FRONTEND_BASE / "package.json"))
            if ret := pkg.run_script("build", "--report"):
                if isinstance(ret, int):
                    sys.exit(ret)
    finally:
        lock_file.unlink()


rebuild_frontend()

app = Flask(__name__, static_folder=FRONTEND_BUILD)
CORS(app)
app.logger.setLevel(logging.INFO)

configs.pymongo = PyMongo(app, MONGO_URI)


@app.errorhandler(UserInputError)
@app.errorhandler(OutputFormatError)
@app.errorhandler(DBError)
def handle_exception(err: UserInputError | OutputFormatError | DBError):
    """
    Return JSON instead of HTML for UserInputError errors.
    """

    response: dict[str, Any] = {"error": err.description}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        if len(err.args) > 1:
            response["extra_messages"] = err.args[1:]

    return jsonify(response), err.code


def _make_filename_unique(file: Path):
    """
    Helper function to return a file name that is unique.
    It does this by first appending the current time to the file, and if there
    are still conflicts, they are resolved by appending a copy index.
    """
    ret = file = file.with_stem(
        file.stem + datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
    )
    num = 0
    while ret.exists():
        ret = ret.with_stem(f"{file.stem}_copy{num}")

    return ret


@app.route("/api/v1/upload_file", methods=["POST"])
def upload_file():
    """
    Implements /api/v1/upload_file endpoint.

    This endpoint only accepts one file, and this file is checked to be a PDF
    file. It is stored in the predefined uploads folder with a unique name, and
    this new name is returned as a response.
    """
    if len(request.files) != 1 and "file" not in request.files:
        raise UserInputError("Got an invalid amount of file uploads")

    file = request.files["file"]
    if file.mimetype not in ALLOWED_MIMETYPES:
        raise UserInputError("Uploaded file has unsupported mimetype")

    if not UPLOADS_BASE.is_dir():
        UPLOADS_BASE.mkdir()

    uploaded_path = UPLOADS_BASE / ("file.pdf" if not file.filename else file.filename)
    if uploaded_path.suffix not in ALLOWED_EXTENSIONS:
        raise UserInputError(
            f"Uploaded file has unsupported extension: {uploaded_path.suffix}"
        )

    uploaded_path = _make_filename_unique(uploaded_path)
    file.save(uploaded_path)
    return uploaded_path.name


def bsonify(obj: Any):
    """
    Just like jsonify but handles bson stuff like ObjectId
    """
    return app.response_class(
        response=json_util.dumps(obj),
        status=200,
        mimetype="application/json",
    )


@app.route("/api/v1/generate_assessment", methods=["POST"])
def generate_assessment():
    """
    Implements /api/v1/generate_assessment endpoint.

    Expects all attributes as needed by UserInput.from_request_form to be set
    """

    user_inp = UserInput.from_request_form(request.form)
    assessment = Assessment.from_user_input(user_inp)
    assessment.save()
    return bsonify(assessment.to_dict())


@app.route("/api/v1/save_assessment", methods=["POST"])
def save_assessment():
    """
    Implements /api/v1/save_assessment endpoint to save assessment data to MongoDB.

    This endpoint can handle both 'save as copy' and 'save as overwrite'. If the
    request has an '_id' attribute this endpoint does 'save as overwrite' on the
    document with that ID, otherwise this endpoint creates a new copy document.
    """
    assessment = Assessment.from_request_json(request.json)
    assessment.save()
    return bsonify(
        {"_id": assessment.get_id(), "last_modified": assessment.last_modified}
    )


@app.route("/api/v1/get_history", methods=["GET"])
def get_history():
    """
    Implements /api/v1/get_history endpoint.

    The response is just a list of all assessment dictionaries.
    """
    return bsonify(get_all_assessments())


@app.route("/api/v1/get_assessment/<ObjectId:assessment_id>", methods=["GET"])
def get_assessment(assessment_id: ObjectId):
    """
    Implements /api/v1/get_assessment endpoint.

    Given the assessment_id attribute (allocated by MongoDB) this endpoint
    returns the assessment dictionary.
    """
    return bsonify(Assessment.from_db(assessment_id).to_dict())


@app.route("/api/v1/delete_assessment/<ObjectId:assessment_id>", methods=["DELETE"])
def delete_assessment(assessment_id: ObjectId):
    """
    Implements /api/v1/delete_assessment endpoint

    Given the assessment_id attribute (allocated by MongoDB) this endpoint
    deletes the assessment dictionary.
    """
    # Delete the assessment from the database
    Assessment.delete_from_db(assessment_id)
    return jsonify({"message": "Assessment deleted successfully."})


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_static(path: str):
    """
    Serves any static file that are generated by react build.
    """
    if app.static_folder is None:
        raise RuntimeError("app.static_folder is unset")

    return send_from_directory(app.static_folder, path)


@app.errorhandler(404)
def handle_404(_):
    """
    Generic 404 error handler.
    If any URL that is client-side routed is requested, the server cannot handle
    it. So send index.html and let client side router handle it.
    """
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
