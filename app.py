from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import numpy as np
from io import StringIO
import json
import os

app = Flask(__name__)

def identify_at_risk_students(df):
    """
    Identify at-risk students based on:
    1. Declining performance trend (negative slope)
    2. Low attendance percentage
    """
    at_risk_students = []
    
    for index, row in df.iterrows():
        student_id = row['student_id']
        
        # Extract weekly scores
        weekly_scores = [
            int(row['week_1']),
            int(row['week_2']),
            int(row['week_3']),
            int(row['week_4'])
        ]
        
        # Calculate trend (slope)
        weeks = np.array([1, 2, 3, 4])
        scores = np.array(weekly_scores)
        
        # Linear regression to find slope
        slope = np.polyfit(weeks, scores, 1)[0]
        
        # Attendance percentage
        attendance = row['attendance_pct']
        
        # Convert to Python native types
        slope = float(slope)  # Ensures it's a Python float
        attendance = float(attendance)  # Ensures it's a Python float
        
        # Criteria for at-risk students:
        # 1. Negative performance trend (slope < 0)
        # 2. Low attendance (< 75%)
        if slope < 0 and attendance < 75:
            at_risk_students.append({
                'student_id': str(student_id),  # Ensure string
                'performance_trend': slope,     # Now Python float
                'attendance_pct': attendance,   # Now Python float
                'weekly_scores': weekly_scores  # List of Python ints
            })
    
    return at_risk_students

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Read CSV data
        csv_data = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        
        # Validate required columns
        required_columns = ['student_id', 'week_1', 'week_2', 'week_3', 'week_4', 'attendance_pct']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': f'Missing required columns. Required: {required_columns}'}), 400
        
        # Identify at-risk students
        at_risk_students = identify_at_risk_students(df)
        
        # Prepare response
        response = {
            'total_students': len(df),
            'at_risk_count': len(at_risk_students),
            'at_risk_students': at_risk_students
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_report', methods=['POST'])
def download_report():
    try:
        data = request.get_json()
        at_risk_list = data.get('at_risk_students', [])
        
        if not at_risk_list:
            return jsonify({'error': 'No at-risk students to export'}), 400

        # Create a DataFrame
        df = pd.DataFrame(at_risk_list)
        # Reorder columns for clarity
        df = df[['student_id', 'attendance_pct', 'performance_trend', 'weekly_scores']]

        # Convert weekly_scores list to a string like "70,65,60,55"
        df['weekly_scores'] = df['weekly_scores'].apply(lambda x: ','.join(map(str, x)))

        # Save to in-memory CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='at_risk_students_report.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
