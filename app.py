from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    make_response,
    flash,
    session,
)
from functools import wraps
import jwt
from datetime import timedelta, timezone
from datetime import datetime

app = Flask(__name__)

# # Set a secret key for sessions
app.secret_key = "8a14GodB2hKSVCenA-l-zA"

books = [
    {"id": 1, "title": "Godfather", "author": "Mario Puzo", "price": 25.99},
    {
        "id": 2,
        "title": "Humans of New York",
        "author": "Brandon Stanton",
        "price": 19.99,
    },
]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return redirect(url_for("login"))
        try:
            payload = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "buukworm" and auth.password == "buuk2024":
            return f(*args, **kwargs)

        return make_response(
            "Could not verify your login!",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required"'},
        )

    return decorated


# Home
# curl http://localhost:5000
@app.route("/", methods=["GET", "POST"])
@token_required
def index():
    return render_template("index.html", books=books)


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form["username"] == "buukworm" and request.form["password"] == "buuk2024"):
            session["logged_in"] = True
            token = jwt.encode(
                {
                    "user": request.form["username"],
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
                },
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            resp = redirect(url_for('index'))
            resp.set_cookie('token', token, httponly=True)
            return resp
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))
    return render_template("login.html")


# curl http://localhost:5000/books
@app.get("/books")
def get_books():
    return jsonify(books)


@app.get("/book/<int:id>")
def get_book(id):
    for book in books:
        if book["id"] == id:
            return jsonify(book)
    return f"Book with id {id} not found", 404


@app.post("/add_book")
@token_required
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    price_string = request.form.get("price")

    if not title or not author or not price_string:
        flash("All fields are required.", "error")
        return redirect(url_for("index"))
    try:
        price = float(price_string)
    except ValueError:
        flash("Invalid price entered. Please enter a valid number.")
        return redirect(url_for("index"))

    new_book = {
        "id": len(books) + 1,
        "author": title,
        "title": author,
        "price": price,
    }
    books.append(new_book)

    return redirect(url_for("index"))


@app.route("/update_book/<int:id>", methods=["GET", "POST"])
@token_required
def update_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if not book:
        return f"Book with id {id} not found", 404

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        price_string = request.form.get("price")

        if not title or not author or not price_string:
            flash("All fields are required.", "error")
            return redirect(url_for("update_book", id=id))
        try:
            price = float(price_string)
        except ValueError:
            flash("Invalid price entered. Please enter a valid number.", "error")
            return redirect(url_for("update_book", id=id))

        book["title"] = title
        book["author"] = author
        book["price"] = price
        return redirect(url_for("index"))

    return render_template("update_book.html", book=book)


# curl http://localhost:5000/delete_book/2 --request DELETE
@app.route("/delete_book/<int:id>", methods=["GET"])
@token_required
def delete_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if not book:
        return f"Book with id {id} not found", 404

    books.remove(book)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
