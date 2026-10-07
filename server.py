import http.server
import socketserver

PORT = 8000

# 캐싱할 그림 파일 확장자 목록
IMAGE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.gif', '.webp', 
    '.svg', '.ico', '.bmp', '.tiff', '.avif'
)

class CustomHeaderHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # URL 경로를 소문자로 변환하여 그림 파일 확장자 여부 확인
        path_lower = self.path.lower()
        
        if path_lower.endswith(IMAGE_EXTENSIONS):
            # 모든 그림 파일: 7일간(604800초) 캐시 저장 허용
            self.send_header("Cache-Control", "public, max-age=604800")
        else:
            # 기타 파일(HTML, JS, CSS 등): 캐시 저장 금지 및 항상 재검증
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")

        super().end_headers()

with socketserver.TCPServer(("", PORT), CustomHeaderHandler) as httpd:
    print(f"서버가 실행되었습니다: http://localhost:{PORT}")
    httpd.serve_forever()