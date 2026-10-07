from database import db, PostModel

class PostRepository:
    @staticmethod
    def get_all(clan_emoji=None, page=1, limit=10):
        query = PostModel.query
        if clan_emoji:
            query = query.filter_by(clan_emoji=clan_emoji)
        
        # Пагинация
        pagination = query.order_by(PostModel.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        return pagination.items, query.count()

    @staticmethod
    def get_by_id(post_id):
        return PostModel.query.get(post_id)

    @staticmethod
    def create(post_data):
        post = PostModel(**post_data)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def delete(post_id):
        post = PostModel.query.get(post_id)
        if post:
            # Транзакционное удаление (каскадное удаление комментариев/лайков)
            db.session.delete(post)
            db.session.commit()
            return True
        return False