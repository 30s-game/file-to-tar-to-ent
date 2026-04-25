/**
 * 엔트리 .ent 파일 생성기 - 팝업 로직 (popup.js)
 * Pyodide를 사용하여 브라우저 환경에서 파이썬 코드를 실행하고,
 * 입력받은 JSON을 엔트리 프로젝트 파일 구조로 압축하여 다운로드합니다.
 */

const jsonInput = document.getElementById('jsonInput');
const convertBtn = document.getElementById('convertBtn');
const statusMsg = document.getElementById('status');
const logArea = document.getElementById('log');
let pyodide;

// 1. Pyodide 및 파이썬 환경 초기화
async function init() {
    try {
        // popup.html에서 로드된 pyodide.js를 기반으로 실행 환경 로드
        pyodide = await loadPyodide();
        statusMsg.innerText = "준비 완료";
        convertBtn.disabled = false;
    } catch (err) {
        statusMsg.innerText = "초기화 실패";
        console.error("Pyodide 로딩 에러:", err);
    }
}

// 초기화 실행
init();

// 2. 변환 및 다운로드 버튼 클릭 이벤트
convertBtn.addEventListener('click', async () => {
    const jsonData = jsonInput.value.trim();
    if (!jsonData) {
        alert("JSON 데이터를 입력해주세요.");
        return;
    }

    logArea.style.display = 'block';
    logArea.innerText = "파일 변환 중...\n";
    convertBtn.disabled = true;

    try {
        /**
         * Python 로직:
         * - 메모리 내 가상 파일 시스템에 entry/temp/project.json 생성
         * - tarfile 라이브러리를 사용해 'entry' 폴더를 압축
         * - 결과를 base64로 인코딩하여 JS로 전달
         */
        const pythonCode = `
import tarfile
import os
import base64
from io import BytesIO

def run_conversion(json_str):
    # 폴더 구조 시뮬레이션
    os.makedirs("entry/temp", exist_ok=True)
    with open("entry/temp/project.json", "w", encoding="utf-8") as f:
        f.write(json_str)
    
    # 메모리 내에서 tar 생성
    out = BytesIO()
    with tarfile.open(fileobj=out, mode="w") as tar:
        # entry 폴더 자체를 루트로 압축
        tar.add("entry", arcname="")
    
    # 바이너리 데이터를 base64로 변환하여 반환
    return base64.b64encode(out.getvalue()).decode()

run_conversion('''${jsonData}''')
        `;

        // 파이썬 코드 실행 및 결과(base64) 수신
        const base64Data = await pyodide.runPythonAsync(pythonCode);
        
        // 3. base64를 바이너리 Blob으로 변환 및 다운로드 실행
        const binary = atob(base64Data);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        
        const blob = new Blob([bytes], { type: "application/octet-stream" });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = "project.ent"; // 엔트리 작품 확장자 설정
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        logArea.innerText += "성공! .ent 파일이 다운로드되었습니다.";
    } catch (err) {
        logArea.innerText += "\n에러 발생: " + err.message;
        console.error(err);
    } finally {
        convertBtn.disabled = false;
    }
});
