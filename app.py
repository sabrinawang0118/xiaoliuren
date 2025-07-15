from flask import Flask, render_template, request
from lunarcalendar import Converter, Solar, Lunar
from datetime import datetime

app = Flask(__name__)

# Define the positions on the fingers
positions = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]

def get_position(start_position, steps):
    return positions[(positions.index(start_position) + steps - 1) % len(positions)]

def solar_to_lunar(year, month, day):
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar.year, lunar.month, lunar.day

def parse_time(time_str):
    hour, minute = map(int, time_str.split(':'))
    return hour, minute

def get_lunar_hour(hour, minute):
    if minute >= 30:
        hour += 1
    return (hour // 2) + 1

@app.route('/')
def index():
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year, current_date=current_date)

@app.route('/predict', methods=['POST'])
def predict():
    solar_year = int(request.form['year'])
    date_str = request.form['date']
    time_str = request.form['time']
    
    # Parse the date and time
    solar_month, solar_day = map(int, date_str.split('-')[1:])
    hour, minute = parse_time(time_str)

    lunar_year, lunar_month, lunar_day = solar_to_lunar(solar_year, solar_month, solar_day)

    month_position = get_position("大安", lunar_month)
    day_position = get_position(month_position, lunar_day)
    lunar_hour = get_lunar_hour(hour, minute)
    hour_position = get_position(day_position, lunar_hour)

    return render_template('result.html',
                           solar_year=solar_year, solar_month=solar_month, solar_day=solar_day, time_str=time_str,
                           lunar_year=lunar_year, lunar_month=lunar_month, lunar_day=lunar_day,
                           month_position=month_position, day_position=day_position, hour_position=hour_position)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
