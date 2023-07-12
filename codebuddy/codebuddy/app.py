from flask import Flask, request, render_template, redirect, url_for
from codebuddy.model.dataclasses import APIkeys
from codebuddy.services.getrepo import RepoWrangler
from codebuddy.services.order import OrderCreator
from codebuddy.services.promptsplicer import PromptSplicer
from codebuddy.services.promptsender import PromptSender

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    repo = request.args.get('repo')
    token = request.args.get('token')

    return redirect((url_for('results', repo=repo, token=token)))  # or what you want

@app.route('/results', methods=['GET'])
def results():
    repo = request.args.get('repo')
    token = request.args.get('token')

    wrangler = RepoWrangler()

    files, filetypes, structure = wrangler.get_repo(repo, token)
    
    return render_template('search_result.html', repo=repo, files=files, filetypes=filetypes, html_structure=structure)

@app.route('/order', methods=['GET', 'POST'])
def order():

    selected_files = request.form
    oc = OrderCreator()
    order = oc.review_order(selected_files)

    if request.method == 'POST':
        return render_template('order_review.html', order=order)
    else:
        # Handle GET requests or redirect the user to another page
        return render_template('some_other_page.html')

@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():

    configured_files = request.form
    print(configured_files)

    oc = OrderCreator()
    configured_orders = oc.process_order(configured_files)

    psplice = PromptSplicer()
    prompts = psplice.build_prompt(configured_orders)

    system_prompt = '''
    You are a super intelligent 
    code reviewing robot. 
    You offer concise advice 
    and reviews when code is 
    submitted to you as string'''

    psend = PromptSender()
    optimised_outputs = psend.optimise_code_batch(prompts, system_prompt)

    if request.method == 'POST':
        return render_template('order_confirmation.html', optimised_outputs=optimised_outputs, order_id=configured_files.get('order_id'))
    else:
        # Handle GET requests or redirect the user to another page
        return render_template('some_other_page.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/contact')
def contact():

    return render_template('contact.html')