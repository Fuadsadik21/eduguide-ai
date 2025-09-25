# EduGuardian AI - Student Success Sentinel

An AI-powered early-warning system for identifying at-risk students in community high schools.

## Features

- Identifies students with declining performance trends
- Monitors attendance patterns correlated with academic performance
- Provides early alerts for timely intervention
- Simple CSV upload interface for data analysis

## Requirements

- Python 3.7+
- Flask
- Pandas
- NumPy

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd eduguide-ai
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Prepare your student data in CSV format with the following columns:
   - `student_id`: Unique identifier for each student
   - `week_1`, `week_2`, `week_3`, `week_4`: Weekly performance scores
   - `attendance_pct`: Attendance percentage

2. Upload the CSV file using the web interface
3. Click "Analyze Student Data" to process the information
4. Review the results to identify at-risk students

## How It Works

The system identifies at-risk students based on two criteria:
1. **Declining Performance Trend**: Calculated using linear regression on weekly scores
2. **Low Attendance**: Students with attendance below 75%

Students meeting both criteria are flagged as at-risk for early intervention.

## Sample Data

A sample dataset is provided in `sample_data.csv` for testing purposes.

## Authors

- Fuad Sadik - Statistics Department, Jimma University
- Abdurahim Fanta - Physics Department, Jimma University

## License

This project is licensed under the MIT License.