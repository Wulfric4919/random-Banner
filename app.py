""" Random banner app
"""

from glob import glob
import os
from random import choice

from flask import Flask, make_response, redirect, render_template, send_file, url_for
from flask.views import View

# app instance
app = Flask(__name__)

@app.route("/")
def root_text():
    "Root page"
    return ("No contents in this page.")

@app.route("/banne.png", methods=['GET'])
def get_banner():
    "Returns random banner"
    banners = glob("./static/banners/*.png")
    banner = choice(banners)
    return redirect(url_for(os.path.basename(banner)))

@app.route("/banner.png", methods=['GET'])
def get_jinja():
    "Returns random banner"
    jinjas = glob("./static/jinjas/*.png")
    jinja = choice(jinjas)
    return redirect(url_for(os.path.basename(jinja)))

@app.route("/jinja.gif", methods=['GET'])
def get_jinja2():
    "Returns random banner"
    jinja2s = glob("./static/jinjas/*.gif")
    jinja2 = choice(jinja2s)
    return redirect(url_for(os.path.basename(jinja2)))

@app.route("/place.png.", methods=['GET'])
def get_place():
    "Returns random banner"
    places = glob("./static/placeholders/*.png")
    place = choice(places)
    return redirect(url_for(os.path.basename(place)))

@app.route("/gallery", methods=['GET'])
def gallery():
    "return gallery"
    banners = glob("./static/banners/*.png")
    return render_template("gallery.html", banners=banners)

class StaticBanner(View):
    "dinamic dispatch class for banner (direct access)"
    methods = ['GET']
    def __init__(self, material, mime):
        self.material = material
        self.material_abspath = os.path.abspath(material)
        self.mime = mime
    
    def dispatch_request(self):
        resp = make_response(send_file(self.material_abspath, mimetype=self.mime))
        resp.headers['Cache-Control'] = "max-age=604800"
        return resp

for banner in glob("./static/banners/*.png"):
    app.add_url_rule(
        f"/{os.path.basename(banner)}",
        view_func=StaticBanner.as_view(os.path.basename(banner), banner, "image/png")
        )
for jinja in glob("./static/jinjas/*.png"):
    app.add_url_rule(
        f"/{os.path.basename(jinja)}",
        view_func=StaticBanner.as_view(os.path.basename(jinja), jinja, "image/png")
    )

for jinja2 in glob("./static/jinjas/*.gif"):
    app.add_url_rule(
        f"/{os.path.basename(jinja2)}",
        view_func=StaticBanner.as_view(os.path.basename(jinja2), jinja2, "image/gif")
    )
for placeholder in glob("./static/placeholders/*.png"):
    app.add_url_rule(
        f"/{os.path.basename(place)}",
        view_func=StaticBanner.as_view(os.path.basename(place), place, "image/png")
    )
# responce headers
# see https://www.kosh.dev/article/10/#2-security-considerations
headers = {
    'Content-Security-Policy':"default-src 'self'; style-src https://cdn.jsdelivr.net",
    'X-Content-Type-Options':'nosniff',
    'X-Frame-Options':'SAMEORIGIN',
    'X-XSS-Protection':'1; mode=block'
}

@app.after_request
def after_request(responce):
    "modify responce header"
    responce.headers.update(headers)
    return responce

app.run(debug=True, host='0.0.0.0', port=8000)
