from sanic import Sanic
from sanic.response import json
from sanic import Blueprint

bp = Blueprint('my_blueprint')

@bp.route('/')
async def bp_root(request):
    return json({"my":"blueprint"})


app = Sanic(__name__)
app.blueprint(bp)
app.run(host='0.0.0.0',port=8000,debug=True)