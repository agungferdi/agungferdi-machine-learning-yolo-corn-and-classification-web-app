from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import shutil
import cv2
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/ferdiansyahmuhammadagung/Project Mine/Machine learning/check'
RESULTS_FOLDER = '/Users/ferdiansyahmuhammadagung/Project Mine/Machine learning/results'
STATIC_FOLDER = '/Users/ferdiansyahmuhammadagung/Project Mine/Machine learning/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


cumulative_count = 0


model = YOLO('/Users/ferdiansyahmuhammadagung/Project Mine/Machine learning/model/best.pt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global cumulative_count  
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return process_image(filepath)

@app.route('/camera', methods=['POST'])
def camera():
    global cumulative_count  
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        filename = 'camera_capture.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv2.imwrite(filepath, frame)
        return process_image(filepath)
    return jsonify({'error': 'Failed to capture image'}), 500

@app.route('/results/<filename>')
def serve_result(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.route('/reset', methods=['POST'])
def reset_cumulative_count():
    global cumulative_count
    cumulative_count = 0
    return jsonify({'message': 'Cumulative count reset'})

def process_image(filepath):
    global cumulative_count

    results = model.predict(source=filepath)

    counts = {'hitam': 0, 'jagung': 0, 'putih': 0, 'serpihan': 0}
    for result in results[0].boxes.data:
        cls = int(result[5])
        label = model.names[cls]
        if label in counts:
            counts[label] += 1

    total_kernels = sum(counts.values())
    cumulative_count += total_kernels

    result_img_filename = f"result_{os.path.basename(filepath)}"
    result_img_path = os.path.join(app.config['RESULTS_FOLDER'], result_img_filename)

    
    if hasattr(results[0], "plot"):  
        modified_boxes = results[0].boxes.data.clone()
        for box in modified_boxes:
            box[4] = 0  
        results[0].boxes.data = modified_boxes  

       
        results[0].plot(save=True, filename=result_img_path, labels=False)

    static_img_path = os.path.join(app.config['STATIC_FOLDER'], result_img_filename)
    shutil.move(result_img_path, static_img_path)

    return jsonify({
        'image': result_img_filename,
        'counts': counts,
        'total': total_kernels,
        'cumulative': cumulative_count
    })



if __name__ == '__main__':
    app.run(debug=True)
