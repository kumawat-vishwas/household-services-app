from flask import current_app as app
from flask import send_from_directory

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('static/pdf', filename, as_attachment=True)