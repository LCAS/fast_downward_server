from flask import Flask, render_template, request, jsonify, Blueprint
import __future__
from subprocess import check_output, CalledProcessError, STDOUT
import sys
from tempfile import mkdtemp, mktemp
from shutil import rmtree
from os import path

app = Flask(__name__, template_folder="resources/templates")
bp = Blueprint('fd_webserver', __name__, static_folder='static')

def call_cmd(cmd, args, cwd, stdin=None, timeout=30):
    if not path.exists(cmd):
        raise IOError(
            "Could not find %s." %
            (cmd))
    sys.stdout.flush()
    if stdin:
        with open(stdin) as stdin_file:
            return check_output([cmd] + args, cwd=cwd, stdin=stdin_file, stderr=STDOUT, timeout=timeout)
    else:
        return check_output([cmd] + args, cwd=cwd, stderr=STDOUT, timeout=timeout)


def call_planner(domain, problem):
    tmpdir = mkdtemp()

    planner_cmd = '/workspace/downward/fast-downward.py'

    domain_file = path.join(tmpdir, 'domain.pddl')
    problem_file = path.join(tmpdir, 'problem.pddl')
    plan_file = path.join(tmpdir, 'plan.out')

    print("operate in %s" % tmpdir)

    with open(domain_file, "w") as text_file:
        text_file.write(domain)
    with open(problem_file, "w") as text_file:
        text_file.write(problem)

    try:
        log = call_cmd(planner_cmd, ["--plan-file", plan_file, problem_file, "--search", "astar(ff)"], tmpdir, timeout=10)
        with open(plan_file, "r") as text_file:
            p = text_file.read()
        return log, p

    except (CalledProcessError) as e:
        return e.output, "no plan due to error. check logs"

    except (RuntimeError, OSError) as e:
        print(e)
        return str(e), "no plan due to error. check logs"

    rmtree(tmpdir, ignore_errors=True)
    return "This contains the logs", "This shall be the plan"

@app.context_processor
def utility_processor():
    def asset_path(asset):
        import json
        with open('static/manifest.json') as file:
            config = json.load(file)
            #return request.url_root + config[asset]
            return '/'+config[asset]
    return dict(asset_path=asset_path)


@bp.route('/', methods=['POST', 'GET'])
def index(name=None):
    if request.method == 'POST':
        print("post")
        domain = request.form['domain']
        problem = request.form['problem']
        sout, plan = call_planner(domain, problem)
        return jsonify(sout=sout.decode("utf-8").replace('\\n', '&#13;&#10;'), plan=str(plan))
    else:
        domain = request.args.get('domain', '')
        problem = request.args.get('problem', '')
        return render_template('index.html', domain=domain, problem=problem)


if __name__ == '__main__':
    app.register_blueprint(bp, url_prefix='/fast-downward')
    app.config.update(dict(PREFERRED_URL_SCHEME='https'))
    app.run(debug=True, threaded=True, host='0.0.0.0')
