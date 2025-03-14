from flask import Flask, request, jsonify, render_template, Blueprint

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/')
def professores():
    return render_template('professores.html')