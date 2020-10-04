from app import app
from flask import Flask, render_template

@app.route('/')
def main():
    return render_template('index.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404