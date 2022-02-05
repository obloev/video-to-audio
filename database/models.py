from database import db
from loader import ADMIN


class User(db.Model):
    __tablename__: str = 'video-to-audio'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger(), unique=True)
    referrals = db.Column(db.Integer(), default=0)
    conversions = db.Column(db.Integer(), default=0)
    lang = db.Column(db.String(), default=None)

    def __str__(self):
        return f'<User {self.id}>'

    @staticmethod
    async def get_lang(user_id):
        user = await User.select('lang').where(User.user_id == user_id).gino.first()
        return user.lang

    @staticmethod
    async def set_lang(user_id, lang):
        user = await User.get_user(user_id)
        await user.update(lang=lang).apply()

    @staticmethod
    async def create_user(user_id):
        new_user = User(user_id=user_id)
        await new_user.create()

    @staticmethod
    async def get_user(user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def get_users(admin=False):
        users = await User.query.where(User.user_id != ADMIN if not admin else True).gino.all()
        return users

    @staticmethod
    async def user_exist(user_id) -> bool:
        user = await User.get_user(user_id)
        return bool(user)

    @staticmethod
    async def users_count() -> int:
        count = await db.func.count(User.user_id).gino.scalar()
        return count

    @staticmethod
    async def delete_user(user_id):
        await User.delete.where(User.user_id == user_id).gino.status()

    @staticmethod
    async def add_conversion(user_id):
        user = await User.get_user(user_id)
        conversions = user.conversions + 1
        return await user.update(conversions=conversions).apply()

    @staticmethod
    async def add_referrals(user_id):
        user = await User.get_user(user_id)
        referrals = user.referrals + 1
        return await user.update(referrals=referrals).apply()

    @staticmethod
    async def get_conversions() -> int:
        conversions = 0
        users_conversions = await User.select('conversions').gino.all()
        for user in users_conversions:
            conversions += user[0]
        return conversions

    @staticmethod
    async def get_referrals(user_id: int) -> int:
        user = await User.get_user(user_id)
        return user.referrals

    @staticmethod
    async def get_top_users(limit: int):
        users = await User.query.order_by(User.conversions.desc()).limit(limit + 1).gino.all()
        return users
