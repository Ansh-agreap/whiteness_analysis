import time
from stage_manage import get_rice_quality, whiteness_analysis
from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
import os

stage_app = Flask(__name__)

# Set upload folder to absolute path in container
upload_start_time = time.time()

UPLOAD_FOLDER = '/app/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
stage_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

upload_end_time = time.time()
print(f'upload extraction runtime = {upload_end_time - upload_start_time}')

@stage_app.route('/get_rice_quality', methods=['POST'])
def count_rice():
    if 'file' not in request.files:
        return jsonify({'error': 'File not uploaded'}), 400
    
    request_start_time = time.time()

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(stage_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    var = request.form.get('VAR')
    request_end_time = time.time()
    print(f'request extraction runtime = {request_end_time - request_start_time}')

    open_start_time = time.time()


    with open(file_path, 'rb') as f:
        image_data = f.read()
    open_end_time = time.time()
    print(f'open extraction runtime = {open_end_time - open_start_time}')    

    try:
        if var == '1':
            model_id = request.form.get('model_id')
            if not model_id:
                return jsonify({'error': 'model_id is required'}), 400
            whiteness_analysis_start_time = time.time()
            WI_value = whiteness_analysis(image_data, id=model_id)
            if not isinstance(WI_value, dict):
                return jsonify({'error': 'Unexpected response from whiteness_analysis'}), 500
            whiteness_analysis_end_time = time.time()
            print(f'whiteness_analysis runtime = {whiteness_analysis_end_time - whiteness_analysis_start_time}')
            return jsonify(WI_value), 200
            # model_id = request.form.get('model_id')
            # quality_type = request.form.get('quality_type')
            # if not model_id:
            #     return jsonify({'error': 'model_id is required'}), 400
            # if not quality_type:
            #     return jsonify({'error': 'quality_type is required'}), 400
            # whiteness_analysis_start_time = time.time()
            # model_id = int(model_id)
            # quality_type = int(quality_type)
            # if quality_type == 1 or quality_type == 2:
            #     print(f"Received model_id: {model_id}")
            #     WI_value = whiteness_analysis(image_data, id=model_id,sample = quality_type)
            #     if not isinstance(WI_value, dict):
            #         return jsonify({'error': 'Unexpected response from whiteness_analysis'}), 500
            #     whiteness_analysis_end_time = time.time()
            #     print(f'whiteness_analysis runtime = {whiteness_analysis_end_time - whiteness_analysis_start_time}')
            #     return jsonify(WI_value), 200
            # else:
            #     return jsonify({'error': 'Invalid quality_type value'}), 400
            
        elif var == '0':
            minl_start_time = time.time()
            minl = request.form.get('minl')
            cp = request.form.get("cp")
            flag_temp = request.form.get('flag_temp', 0)
            minl_end_time = time.time()
            print(f'form features extraction runtime = {minl_end_time - minl_start_time}')


            if flag_temp not in ['0', '1']:
                return jsonify({'error': 'Invalid flag value'}), 400
            try:
                minl = float(minl) if minl else None
                cp = int(cp) if cp else None
                rice_start_time = time.time()
                finalarr = get_rice_quality(
                    image_data,
                    width=10.08,
                    minlen=minl,
                    flag=int(flag_temp),
                    chalky=cp)
                rice_end_time = time.time()
                print("Hello")
                print(f'Rice quality processing runtime = {rice_end_time - rice_start_time}')
            except ValueError as e:
                return jsonify({'error': f'Invalid input: {e}'}), 400

            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing file: {e}")
            check_start_time = time.time()
            if not finalarr:
                return jsonify({'error': 'No result from get_rice_quality'}), 500

            if isinstance(finalarr, dict) and 'error' in finalarr:
                return jsonify(finalarr), 400 
            if isinstance(finalarr, set):
                finalarr = list(finalarr)  
            elif isinstance(finalarr, (list, tuple)):
                finalarr = [list(item) if isinstance(item, set) else item for item in finalarr]
            check_end_time = time.time()
            print(f'check runtime = {check_end_time - check_start_time}')
            return jsonify(finalarr), 200
            
        else:
            return jsonify({'error': 'Invalid VAR value'}), 400

    except Exception as e:
        # Clean up the file in case of error
        try:
            os.remove(file_path)
        except:
            pass
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    stage_app.run(host='0.0.0.0', port=6000, threaded=True)
