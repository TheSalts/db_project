# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app():
    """Flask 앱 인스턴스 생성 및 초기화 (App Factory)"""
    
    app = Flask(__name__)
    
    # 1. 설정 로드 (config.py의 Config 클래스)
    app.config.from_object(Config)
    
    # 2. CORS 설정 (모든 도메인에서의 요청 허용)
    CORS(app) 
    
    # 3. 블루프린트(API) 등록
    from app.api import auth_api
    app.register_blueprint(auth_api.auth_bp)

    from app.api import club_api
    app.register_blueprint(club_api.club_bp)

    from app.api import mypage_api
    app.register_blueprint(mypage_api.mypage_bp)

    from app.api import apply_api
    app.register_blueprint(apply_api.apply_bp)

    from app.api import post_api
    app.register_blueprint(post_api.post_club_bp)
    app.register_blueprint(post_api.post_manage_bp)

    app.register_blueprint(club_api.club_member_bp) 
    
    

    from app.api import admin_api
    app.register_blueprint(admin_api.admin_bp)

    return app