from DB.centre import User


# Функция повышения уровня
def user_lvl(user_id, exp):
    user = User.get_user(user_id=user_id)
    user_exp_now = user["experience_now"]
    user_exp_future = user["experience_future"]
    new_exp = user_exp_now + exp

    if new_exp >= user_exp_future:
        new_lvl = user["lvl"] + 1
        new_skill_point = user["skill_point"] + 1
        new_exp_now = user_exp_now - user_exp_future
        new_exp_future = int(user_exp_future * 1.35)
        User.set_user_lvl(user_id=user_id, lvl=new_lvl)
        User.set_user_skill_point(user_id=user_id, skill_point=new_skill_point)
        User.set_user_experience_now(user_id=user_id, exp_now=new_exp_now)
        User.set_user_experience_future(user_id=user_id, exp_future=new_exp_future)
        user_lvl(user_id=user_id, exp=exp-user_exp_future)

    elif new_exp < user_exp_future:
        User.set_user_experience_now(user_id=user_id, experience_now=new_exp)
