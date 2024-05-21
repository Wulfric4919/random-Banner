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
    return ("No contents in this page. §^ム^§")

@app.route("/banner.png", methods=['GET'])
def get_banner():
    "Returns random banner"
    banners = glob("./static/banners/*.png")
    banner = choice(banners)
    return redirect(url_for(os.path.basename(banner)))

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

# favicon: favicon.ico, favicon.png, site.webmanifest etc.
class Favicon(View):
    "dinamic dispatch class for favicon"
    methods = ['GET']
    def __init__(self, material, mime):
        self.material = material
        self.material_abspath = os.path.abspath(f"./static/{material}")
        self.mime = mime

    def dispatch_request(self):
        return send_file(self.material_abspath, mimetype=self.mime)

# favicons in this site
favicon_materials = {
    "android-chrome-192x192.png": "image/png",
    "android-chrome-512x512.png": "image/png",
    "apple-touch-icon.png": "image/png",
    "favicon-16x16.png": "image/png",
    "favicon-32x32.png": "image/png",
    "favicon.ico": "image/vnd.microsoft.icon",
    "favicon.png": "image/png",
    "site.webmanifest": "application/manifest+json"
}

# add url rule for favicons
for material, mime in favicon_materials.items():
    app.add_url_rule(
        f"/{material}",
        view_func=Favicon.as_view(material, material, mime)
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
