import io
from main import app
from flask import render_template, request, url_for, redirect, send_file, send_from_directory
import model


@app.route('/')
def index():
    contributions = model.Contribution.select().order_by(model.Contribution.id)
    return render_template('index.html', contributions=contributions)


@app.route('/assets/<path:path>')
def asset(path):
    return send_from_directory('static', path)


@app.route('/admin', methods=['GET'])
def admin():
    return redirect(url_for('contribution_new'))


@app.route('/admin/contribution/new', methods=['GET', 'POST'])
def contribution_new():
    if request.method == 'GET':
        return render_template('admin/contribution_form.html',
                               endpoint=url_for('contribution_new'),
                               map_countries=model.COUNTRIES,
                               contributions=model.Contribution.select().order_by(model.Contribution.id)
                               )

    contribution = model.Contribution(
        title=request.form.get('title'),
        description=request.form.get('description'),
        map_location=request.form.get('map_location'),
        shown_location=request.form.get('shown_location'),
        contributor=request.form.get('contributor'),
    )
    contribution.save()

    return redirect(url_for('contribution_edit', contr_id=contribution.id))


@app.route('/admin/contribution/<contr_id>', methods=['GET', 'POST'])
def contribution_edit(contr_id):
    contribution = model.Contribution.get_by_id(contr_id)

    if request.method == 'GET':
        return render_template('admin/contribution_form.html',
                               endpoint=url_for('contribution_edit', contr_id=contr_id),
                               map_countries=model.COUNTRIES,
                               contribution=contribution,
                               contributions=model.Contribution.select().order_by(model.Contribution.id)
                               )
    for attrib in request.form:
        setattr(contribution, attrib, request.form.get(attrib))
    contribution.save()

    return redirect(url_for('contribution_edit', contr_id=contribution.id))


@app.route('/admin/contribution/<contr_id>/delete', methods=['POST'])
def contribution_delete(contr_id):
    model.Contribution.delete_by_id(contr_id)

    return redirect(url_for('admin'))


@app.route('/image/<img_id>', methods=['GET'])
def image(img_id):
    image = model.Image.get_by_id(img_id)

    if not image:
        return 404
    return send_file(io.BytesIO(image.file), mimetype='image/png')


@app.route('/admin/contribution/<contr_id>/image/new', methods=['POST'])
def image_new(contr_id):
    image = model.Image(
        title=request.form.get('title'),
        description=request.form.get('description'),
        mimetype=request.files['file'].mimetype,
        file=request.files['file'].read(),
        contribution=contr_id
    )
    image.save()
    return redirect(url_for('contribution_edit', contr_id=contr_id))


@app.route('/admin/image/<img_id>', methods=['POST'])
def image_edit(img_id):
    img = model.Image.get_by_id(img_id)
    contribution = img.contribution
    for attrib in request.form:
        print(request.form.get(attrib))
        setattr(img, attrib, request.form.get(attrib))
    img.save()

    return redirect(url_for('contribution_edit', contr_id=contribution.id))


@app.route('/admin/image/<img_id>/delete', methods=['POST'])
def image_delete(img_id):
    img = model.Image.get_by_id(img_id)
    contribution = img.contribution
    model.Image.delete_by_id(img_id)

    return redirect(url_for('contribution_edit', contr_id=contribution.id))
