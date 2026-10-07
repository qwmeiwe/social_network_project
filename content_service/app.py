from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

# Временное хранилище (БД появится в ПР3)
posts_db = []

# Единый обработчик ошибок валидации
def bad_request(details):
    return jsonify({"error": "Validation Failed", "details": details}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Content Service (Flask)"}), 200

# 1. СОЗДАНИЕ (POST)
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json() or {}
    details = []
    
    # Валидация
    if not data.get('author_id'):
        details.append("author_id is required")
    if not data.get('clan_emoji') or len(data.get('clan_emoji', '')) > 2:
        details.append("clan_emoji is required and should be a valid emoji")
    content = data.get('content', '')
    if not (1 <= len(content) <= 280):
        details.append("content must be between 1 and 280 characters")
        
    if details:
        return bad_request(details)

    new_post = {
        "id": str(uuid.uuid4()),
        "author_id": data['author_id'],
        "clan_emoji": data['clan_emoji'],
        "content": content,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    posts_db.append(new_post)
    return jsonify(new_post), 201

# 2. ПОЛУЧЕНИЕ СПИСКА + ПАГИНАЦИЯ И ФИЛЬТРАЦИЯ (GET)
@app.route('/posts', methods=['GET'])
def get_posts():
    # Параметры пагинации
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    clan_filter = request.args.get('clan_emoji')

    # Фильтрация
    filtered_posts = posts_db
    if clan_filter:
        filtered_posts = [p for p in filtered_posts if p['clan_emoji'] == clan_filter]

    # Пагинация
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_posts = filtered_posts[start_idx:end_idx]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(filtered_posts),
        "data": paginated_posts
    }), 200

# 3. ПОЛУЧЕНИЕ ОДНОЙ ЗАПИСИ (GET)
@app.route('/posts/', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(post), 200

# 4. ОБНОВЛЕНИЕ (PUT)
@app.route('/posts/', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Not Found"}), 404

    data = request.get_json() or {}
    content = data.get('content', '')
    
    # Валидация
    if not (1 <= len(content) <= 280):
        return bad_request(["content must be between 1 and 280 characters"])

    post['content'] = content
    return jsonify(post), 200

# 5. УДАЛЕНИЕ (DELETE)
@app.route('/posts/', methods=['DELETE'])
def delete_post(post_id):
    global posts_db
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Not Found"}), 404
    
    posts_db = [p for p in posts_db if p['id'] != post_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)