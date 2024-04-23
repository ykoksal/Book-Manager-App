from flask import Flask, jsonify, request, render_template, redirect, url_for
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# # Set a secret key for sessions
# app.config["SECRET_KEY"] = "8a14GodB2hKSVCenA-l-zA"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# app.config['DEBUG_TB_FORCE_ENABLE'] = True
# toolbar = DebugToolbarExtension(app)

books = [
    {"id": 1, "title": "Godfather", "author": "Mario Puzo", "price": 25.99},
    {
        "id": 2,
        "title": "Humans of New York",
        "author": "Brandon Stanton",
        "price": 19.99,
    },
]

@app.route("/home")
def home():
    return "<html><body><h1>Home Page</h1></body></html>"


# curl http://localhost:5000
@app.route("/", methods=["GET", "POST"])
def index():
    print(books)
    return render_template("index.html", books=books)


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


# curl http://localhost:5000/add_book --request POST --data '{"id":3,"author":"aaa","title":"bbb","price":99.99}' --header "Content-Type: application/json"
@app.post("/add_book")
def add_book():
    data = request.form
    new_book = {
        "id": len(books) + 1,
        "author": data["author"],
        "title": data["title"],
        "price": data["price"],
    }
    books.append(new_book)
    return redirect(url_for("index"))


# curl http://localhost:5000/update_book/2 --request POST --data '{"id":3,"author":"aaa","title":"bbb","price":99.99}' --header "Content-Type: application/json"
@app.route("/update_book/<int:id>", methods=["GET", "POST"])
def update_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if not book:
        return f"Book with id {id} not found", 404

    if request.method == "POST":
        book["title"] = request.form["title"]
        book["author"] = request.form["author"]
        book["price"] = request.form["price"]
        return redirect(url_for("index"))
    return render_template("update_book.html", book=book)


# curl http://localhost:5000/delete_book/2 --request DELETE
@app.route("/delete_book/<int:id>", methods=["GET"])
def delete_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if not book:
        return f"Book with id {id} not found", 404

    books.remove(book)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
