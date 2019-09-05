from flask import Blueprint, render_template, url_for

# movie_bp = Blueprint("movie", __name__, url_prefix='/movie',static_folder="my_static", template_folder="my_tem")
movie_bp = Blueprint("movie", __name__, url_prefix='/movie',static_folder="my_static")
@movie_bp.route("/list")
def list():
    return render_template('list_list.html')