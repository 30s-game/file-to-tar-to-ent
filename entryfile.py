import tarfile
import os
import json

"""
이 코드는 실행하지 않습니다.
이 python 코드는 html 코드에 포함되어 있으며 삭제하셔도 됩니다.
"""

def create_entry_file(project_json_content, output_filename="my_project.ent"):
    """
    project.json 내용을 바탕으로 엔트리(.ent) 파일을 생성합니다.
    """
    # 1. 임시 작업 경로 설정 (entry/temp)
    temp_dir = "entry/temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    project_path = os.path.join(temp_dir, "project.json")
    
    # 2. project.json 파일 저장
    with open(project_path, "w", encoding="utf-8") as f:
        # dict 형태라면 json.dump, 문자열이라면 직접 쓰기
        if isinstance(project_json_content, dict):
            json.dump(project_json_content, f, ensure_ascii=False, indent=2)
        else:
            f.write(project_json_content)
            
    print(f"파일 저장 완료: {project_path}")

    # 3. tar 압축 후 .ent로 확장자 변경
    # 엔트리 파일 구조는 root에 temp 폴더가 있고 그 안에 project.json이 있어야 함
    with tarfile.open(output_filename, "w") as tar:
        # 'entry' 폴더 자체를 압축에 추가 (내부 구조 유지)
        tar.add("entry", arcname="")

    print(f"압축 및 변환 완료: {output_filename}")

# 실행 예시 (위에서 정의한 MMORPG project.json 데이터를 넣으세요)
mmorpg_data = {
    "objects": [
        {
            "id": "player_main",
            "name": "플레이어(나)",
            "script": "[[{\"id\":\"m1\",\"type\":\"when_run_button_click\",\"params\":[null],\"statements\":[],\"extensions\":[]},{\"id\":\"m2\",\"type\":\"repeat_inf\",\"params\":[null,null],\"statements\":[[{\"id\":\"m3\",\"type\":\"if_then\",\"params\":[{\"id\":\"m4\",\"type\":\"key_pressed\",\"params\":[\"w\"]},null],\"statements\":[[{\"id\":\"m5\",\"type\":\"move_y\",\"params\":[{\"id\":\"m6\",\"type\":\"number\",\"params\":[\"5\"]}],\"statements\":[]}]],\"extensions\":[]},{\"id\":\"m7\",\"type\":\"if_then\",\"params\":[{\"id\":\"m8\",\"type\":\"key_pressed\",\"params\":[\"s\"]},null],\"statements\":[[{\"id\":\"m9\",\"type\":\"move_y\",\"params\":[{\"id\":\"m10\",\"type\":\"number\",\"params\":[\"-5\"]}],\"statements\":[]}]],\"extensions\":[]},{\"id\":\"m11\",\"type\":\"if_then\",\"params\":[{\"id\":\"m12\",\"type\":\"key_pressed\",\"params\":[\"a\"]},null],\"statements\":[[{\"id\":\"m13\",\"type\":\"move_x\",\"params\":[{\"id\":\"m14\",\"type\":\"number\",\"params\":[\"-5\"]}],\"statements\":[]}]],\"extensions\":[]},{\"id\":\"m15\",\"type\":\"if_then\",\"params\":[{\"id\":\"m16\",\"type\":\"key_pressed\",\"params\":[\"d\"]},null],\"statements\":[[{\"id\":\"m17\",\"type\":\"move_x\",\"params\":[{\"id\":\"m18\",\"type\":\"number\",\"params\":[\"5\"]}],\"statements\":[]}]],\"extensions\":[]},{\"id\":\"sync1\",\"type\":\"set_variable\",\"params\":[\"v_my_x\",{\"id\":\"sync2\",\"type\":\"get_x_value\",\"params\":[null]}],\"statements\":[]},{\"id\":\"sync3\",\"type\":\"set_variable\",\"params\":[\"v_my_y\",{\"id\":\"sync4\",\"type\":\"get_y_value\",\"params\":[null]}],\"statements\":[]}]]}]]",
            "objectType": "sprite",
            "x": 0,
            "y": 0,
            "rotation": 0
        }
        # ... 생략
    ],
    "variables": [],
    "messages": [],
    "functions": [],
    "scenes": [{"name": "마을", "id": "scene_1"}]
}

if __name__ == "__main__":
    create_entry_file(mmorpg_data, "MMORPG_Project.ent")
