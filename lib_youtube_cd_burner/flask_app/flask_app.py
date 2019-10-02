from flask import Flask, render_template, url_for, flash, redirect
from .forms import URLForm
from ..lib_youtube_cd_burner import main

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = URLForm()
    if form.validate_on_submit():
        flash("Completed", "success")
        # Method call here to burn CDs!
        path = None if form.save_path.data == "" else form.save_path.data
        main(form.url.data, save_path=path)
        return render_template('home.html', form=form)
    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
