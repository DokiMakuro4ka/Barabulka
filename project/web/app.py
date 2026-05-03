from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from db_queries import (
    User, State, Epoch, EpochDetail, Monster,
    UserClass, UserSubclass, BattleLog
)
import random
import time

app = Flask(__name__)
app.config.from_object(Config)

# ------------------- Вспомогательные функции -------------------
def get_user():
    if 'user_id' not in session:
        return None
    return User.get_user(session['user_id'])

def has_class(user):
    return user and user[15]  # class_id

# ------------------- Маршруты -------------------
@app.route('/')
def index():
    user = get_user()
    if not user:
        return redirect(url_for('start'))
    return render_template('index.html', user=user, has_class=has_class(user))

@app.route('/start')
def start():
    if 'user_id' not in session:
        # Генерируем уникальный целочисленный ID
        # Используем миллисекунды + случайное число для уникальности
        base = int(time.time() * 1000) % (2**48)
        unique_id = base + random.randint(1, 1000)
        # Минимальная защита от коллизий (маловероятно, но проверим)
        while User.get_user(unique_id):
            unique_id = base + random.randint(1, 1000)
        session['user_id'] = unique_id
    user = User.get_user(session['user_id'])
    if not user:
        User.insert_user(telegram_id=session['user_id'], name="Странник")
    return redirect(url_for('choose_state'))

@app.route('/choose_state')
def choose_state():
    states = State.get_all_states()
    return render_template('choose_state.html', states=states)

@app.route('/select_state/<int:state_id>')
def select_state(state_id):
    user = get_user()
    if not user:
        return redirect(url_for('start'))
    User.set_field(session['user_id'], 'state_id', state_id)
    return redirect(url_for('choose_class'))

@app.route('/state/<int:state_id>')
def show_state(state_id):
    state = State.get_state(state_id)
    epochs = Epoch.get_epochs_by_state(state_id)
    return render_template('state.html', state=state, epochs=epochs)

@app.route('/epoch/<int:epoch_id>')
def show_epoch(epoch_id):
    epoch = Epoch.get_epoch(epoch_id)
    details = EpochDetail.get_details_by_epoch(epoch_id)
    return render_template('epoch.html', epoch=epoch, details=details)

@app.route('/epoch_detail/<int:epoch_id>')
def epoch_detail(epoch_id):
    category = request.args.get('category')
    detail = EpochDetail.get_detail_by_category(epoch_id, category)
    return render_template('epoch_detail.html', detail=detail, epoch_id=epoch_id)

@app.route('/choose_class')
def choose_class():
    user = get_user()
    if not user:
        return redirect(url_for('start'))
    if user[15]:
        return redirect(url_for('index'))
    return render_template('choose_class.html')

@app.route('/select_class/<int:class_id>')
def select_class(class_id):
    user = get_user()
    if not user or user[15]:
        return redirect(url_for('index'))
    User.set_field(session['user_id'], 'class_id', class_id)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    user = get_user()
    if not user:
        return redirect(url_for('start'))
    return render_template('profile.html', user=user, user_text=User.get_user_text(session['user_id']))

@app.route('/delete_profile')
def delete_profile():
    user = get_user()
    if user:
        User.delete_user(session['user_id'])
    session.clear()
    return redirect(url_for('start'))

@app.route('/battle')
def battle():
    user = get_user()
    if not user or not has_class(user):
        return redirect(url_for('index'))
    location_id = user[18] if user else 1
    monster = Monster.get_random_monster_by_location(location_id, user[3])
    if not monster:
        return "Нет монстров", 404
    session['battle'] = {
        'monster': list(monster),
        'player_hp': user[6],
        'monster_current_hp': monster[3]
    }
    return render_template('battle.html', monster=monster, player_hp=user[6])

@app.route('/battle_action', methods=['POST'])
def battle_action():
    user = get_user()
    if not user or 'battle' not in session:
        return redirect(url_for('index'))
    action = request.form['action']
    battle = session['battle']
    monster = battle['monster']
    # monster: (id, name, level, hp, damage, defence, exp_reward, coin_reward, location_id, type)
    monster_id, name, lvl, hp, damage, defence, exp_reward, coin_reward, _, _ = monster
    player_hp = battle['player_hp']
    monster_hp = battle['monster_current_hp']
    p_dmg = user[10]
    p_def = user[11]
    p_max_hp = user[7]

    action_desc = ""
    monster_desc = ""

    if action == "attack":
        dmg = max(1, p_dmg - defence + random.randint(-3,5))
        monster_hp -= dmg
        action_desc = f"наносишь {dmg} урона!"
    elif action == "defend":
        action_desc = "защищаешься"
    elif action == "flee":
        if random.random() < 0.5:
            session.pop('battle', None)
            return redirect(url_for('index'))
        else:
            action_desc = "убежать не удалось"
    else:
        return redirect(url_for('battle'))

    if monster_hp > 0:
        dmg_mod = 0.5 if action == "defend" else 1.0
        m_dmg = max(1, int((damage - p_def + random.randint(-2,3)) * dmg_mod))
        player_hp -= m_dmg
        monster_desc = f"наносит {m_dmg} урона!"
    else:
        monster_desc = "повержен!"

    if player_hp <= 0:
        new_hp = p_max_hp // 2
        User.set_field(session['user_id'], 'hp', new_hp)
        User.set_field(session['user_id'], 'current_hp', new_hp)
        session.pop('battle', None)
        return render_template('battle_result.html', victory=False, message=f"Ты погиб... Воскрес с половиной HP.\nНовое HP: {new_hp}")

    if monster_hp <= 0:
        exp_gain = exp_reward
        coin_gain = coin_reward
        user_obj = get_user()
        exp_now = user_obj[4]
        lvl = user_obj[3]
        coins = user_obj[13]
        new_exp = exp_now + exp_gain
        new_lvl = lvl
        if new_exp >= 100:
            new_lvl += 1
            new_exp -= 100
            User.set_field(session['user_id'], 'lvl', new_lvl)
            User.set_field(session['user_id'], 'experience_now', new_exp)
            User.set_field(session['user_id'], 'max_hp', user_obj[7] + 10)
            User.set_field(session['user_id'], 'hp', user_obj[7] + 10)
            User.set_field(session['user_id'], 'damage', user_obj[10] + 2)
            User.set_field(session['user_id'], 'defence', user_obj[11] + 1)
            User.set_field(session['user_id'], 'star_coin', coins + coin_gain)
        else:
            User.set_field(session['user_id'], 'experience_now', new_exp)
            User.set_field(session['user_id'], 'star_coin', coins + coin_gain)
        BattleLog.save_battle(session['user_id'], monster_id, "win", exp_gain, coin_gain)
        session.pop('battle', None)
        return render_template('battle_result.html', victory=True, exp=exp_gain, coins=coin_gain)

    # Обновляем сессию
    battle['player_hp'] = player_hp
    battle['monster_current_hp'] = monster_hp
    session['battle'] = battle
    User.set_field(session['user_id'], 'hp', player_hp)
    User.set_field(session['user_id'], 'current_hp', player_hp)

    return render_template('battle.html', monster={**dict(zip(['id','name','level','hp','damage','defence','exp_reward','coin_reward','location_id','type'], monster)), 'health': monster_hp},
                           player_hp=player_hp, action_desc=action_desc, monster_desc=monster_desc)

if __name__ == '__main__':
    app.run(debug=True)