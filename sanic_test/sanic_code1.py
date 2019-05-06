from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)

@app.route("/")
async def test(request):
    print(request)
    return text('Hello world!')


def index():
    """Main"""
    return app.run(host="0.0.0.0", port=8000, debug=True)



if __name__ == '__main__':
    index()