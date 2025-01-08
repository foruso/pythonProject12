import pandas as pd

# 학번 리스트 생성
data = []
for grade in range(1, 4):  # 1~3학년
    for class_no in range(1, 5):  # 1~4반
        if class_no == 1:  # 1반은 40번까지
            max_number = 40
        else:  # 나머지 반은 20번까지
            max_number = 20
        for number in range(1, max_number + 1):
            student_id = f"{grade}{class_no}{number:02}"  # 학번 형식
            data.append(student_id)

# 엑셀 파일로 저장
df = pd.DataFrame(data, columns=["학번"])
df.to_excel("student_ids.xlsx", index=False)

print("학번 리스트 엑셀 파일이 생성되었습니다.")
