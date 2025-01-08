import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 학번 데이터 로드
student_ids = pd.read_excel("student_ids.xlsx")["학번"].tolist()

# 사용자 데이터 (학번과 비밀번호 설정)
users = {str(student_id): generate_password_hash(str(student_id)) for student_id in student_ids}  # 비밀번호는 학번과 동일

# 설문조사 데이터 저장 (임시)
surveys = []

@app.route('/')
def home():
    """
    홈 화면: 설문조사 목록 표시
    """
    if 'user_id' in session:
        user = session['user_id']
    else:
        user = None
    return render_template('home.html', surveys=surveys, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    로그인 기능
    """
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']

        # 학번과 비밀번호 확인
        if user_id in users and check_password_hash(users[user_id], password):
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            return "로그인 실패: 학번 또는 비밀번호가 잘못되었습니다."

    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    로그아웃 기능
    """
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    """
    마이페이지: 설문조사 등록 및 관리
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        # 설문조사 등록
        title = request.form['title']
        link = request.form['link']
        description = request.form['description']
        field = request.form['field']
        target = request.form['target']
        survey = {
            "uploader": user_id,
            "title": title,
            "link": link,
            "description": description,
            "field": field,
            "target": target,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        surveys.append(survey)
        return redirect(url_for('mypage'))

    # 해당 사용자가 등록한 설문조사만 필터링
    user_surveys = [survey for survey in surveys if survey["uploader"] == user_id]
    return render_template('mypage.html', user_id=user_id, surveys=user_surveys)


@app.route('/delete_survey', methods=['POST'])
def delete_survey():
    """
    설문조사 삭제
    """
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "로그인이 필요합니다."})

    user_id = session['user_id']
    survey_index = int(request.form['index'])

    if surveys[survey_index]["uploader"] == user_id:
        del surveys[survey_index]
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "권한이 없습니다."})


if __name__ == '__main__':
    app.run(debug=True)
