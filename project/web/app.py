import hashlib
import hmac
import random
import time
import logging
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, abort
from config import Config
from db_queries import (
    User, State, Epoch, EpochDetail, Monster,
    UserClass, UserSubclass, BattleLog
)

app = Flask(__name__)
app.config.from_object(Config)

# Настройка логирования
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

# ------------------- Декораторы -------------------
def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def character_required(f):
    @wraps(f)
    @user_required
    def decorated(*args, **kwargs):
        user = User.get_user(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        return f(user, *args, **kwargs)
    return decorated

def class_required(f):
    @wraps(f)
    @character_required
    def decorated(user, *args, **kwargs):
        if not user[15]:  # class_id
            return redirect(url_for('choose_class'))
        return f(user, *args, **kwargs)
    return decorated

# ------------------- Маршруты -------------------
@app.route('/')
@user_required
def index():
    user = User.get_user(session['user_id'])
    return render_template('index.html', user=user, has_class=user[15] > 0)

@app.route('/login')
def login():
    """Страница входа через Telegram"""
    return render_template('login.html', bot_username=Config.BOT_USERNAME)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/telegram-callback')
def telegram_callback():
    """Обработка данных от Telegram Login"""
    args = request.args.to_dict()
    hash_received = args.pop('hash', None)
    if not hash_received:
        return "Missing hash", 400

    # Проверка подписи
    sorted_keys = sorted(args.keys())
    data_string = "\n".join([f"{k}={args[k]}" for k in sorted_keys])
    secret_key = hashlib.sha256(Config.BOT_TOKEN.encode()).digest()
    computed_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()
    if computed_hash != hash_received:
        return "Invalid auth data", 403

    # Данные валидны
    telegram_id = int(args['id'])
    first_name = args.get('first_name', '')
    last_name = args.get('last_name', '')
    username = args.get('username', '')

    user = User.get_user(telegram_id)
    if not user:
        name = username if username else f"{first_name} {last_name}".strip()
        if not name:
            name = "Странник"
        User.insert_user(telegram_id=telegram_id, name=name)
        # После создания нового пользователя нужно установить государство и класс
        # Перенаправим на выбор государства
        session['user_id'] = telegram_id
        return redirect(url_for('choose_state'))

    session['user_id'] = telegram_id
    # Если у пользователя уже есть класс — сразу на главную, иначе на выбор класса
    if user[15]:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('choose_class'))

@app.route('/choose_state')
@user_required
def choose_state():
    states = State.get_all_states()
    return render_template('choose_state.html', states=states)

@app.route('/select_state/<int:state_id>')
@user_required
def select_state(state_id):
    try:
        User.set_field(session['user_id'], 'state_id', state_id)
    except Exception as e:
        app.logger.error(f"Failed to set state: {e}")
        return "Ошибка при выборе государства", 500
    return redirect(url_for('choose_class'))

@app.route('/state/<int:state_id>')
@user_required
def show_state(state_id):
    state = State.get_state(state_id)
    if not state:
        abort(404)
    epochs = Epoch.get_epochs_by_state(state_id)
    return render_template('state.html', state=state, epochs=epochs)

@app.route('/epoch/<int:epoch_id>')
@user_required
def show_epoch(epoch_id):
    epoch = Epoch.get_epoch(epoch_id)
    if not epoch:
        abort(404)
    details = EpochDetail.get_details_by_epoch(epoch_id)
    return render_template('epoch.html', epoch=epoch, details=details)

@app.route('/epoch_detail/<int:epoch_id>')
@user_required
def epoch_detail(epoch_id):
    category = request.args.get('category')
    if not category:
        abort(400)
    detail = EpochDetail.get_detail_by_category(epoch_id, category)
    if not detail:
        abort(404)
    return render_template('epoch_detail.html', detail=detail, epoch_id=epoch_id)

@app.route('/choose_class')
@user_required
def choose_class():
    user = User.get_user(session['user_id'])
    if user[15]:
        return redirect(url_for('index'))
    return render_template('choose_class.html')

@app.route('/select_class/<int:class_id>')
@user_required
def select_class(class_id):
    user = User.get_user(session['user_id'])
    if user[15]:
        return redirect(url_for('index'))
    if class_id not in (1,2,3,4):
        abort(400)
    User.set_field(session['user_id'], 'class_id', class_id)
    return redirect(url_for('index'))

@app.route('/profile')
@character_required
def profile(user):
    user_text = User.get_user_text(session['user_id'])
    return render_template('profile.html', user=user, user_text=user_text)

@app.route('/delete_profile')
@character_required
def delete_profile(user):
    User.delete_user(session['user_id'])
    session.clear()
    return redirect(url_for('login'))

@app.route('/battle')
@class_required
def battle(user):
    location_id = user[18] if user else 1
    monster = Monster.get_random_monster_by_location(location_id, user[3])
    if not monster:
        return render_template('battle_no_monsters.html'), 404
    session['battle'] = {
        'monster': list(monster),
        'player_hp': user[6],
        'monster_current_hp': monster[3]
    }
    return render_template('battle.html', monster=monster, player_hp=user[6])

@app.route('/battle_action', methods=['POST'])
@class_required
def battle_action(user):
    battle = session.get('battle')
    if not battle:
        return redirect(url_for('index'))
    action = request.form.get('action')
    if action not in ('attack', 'defend', 'flee'):
        return redirect(url_for('battle'))

    monster = battle['monster']
    (monster_id, name, lvl, hp, damage, defence, exp_reward, coin_reward, _, _) = monster
    player_hp = battle['player_hp']
    monster_hp = battle['monster_current_hp']
    p_dmg = user[10]
    p_def = user[11]
    p_max_hp = user[7]

    action_desc = ""
    if action == "attack":
        dmg = max(1, p_dmg - defence + random.randint(-3, 5))
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

    monster_desc = ""
    if monster_hp > 0:
        dmg_mod = 0.5 if action == "defend" else 1.0
        m_dmg = max(1, int((damage - p_def + random.randint(-2, 3)) * dmg_mod))
        player_hp -= m_dmg
        monster_desc = f"наносит {m_dmg} урона!"
    else:
        monster_desc = "повержен!"

    if player_hp <= 0:
        new_hp = p_max_hp // 2
        User.set_field(session['user_id'], 'hp', new_hp)
        User.set_field(session['user_id'], 'current_hp', new_hp)
        session.pop('battle', None)
        return render_template('battle_result.html', victory=False,
                               message=f"Ты погиб... Воскрес с половиной HP.\nНовое HP: {new_hp}")

    if monster_hp <= 0:
        exp_gain = exp_reward
        coin_gain = coin_reward
        exp_now = user[4]
        lvl = user[3]
        coins = user[13]
        new_exp = exp_now + exp_gain
        new_lvl = lvl
        if new_exp >= 100:
            new_lvl += 1
            new_exp -= 100
            User.set_field(session['user_id'], 'lvl', new_lvl)
            User.set_field(session['user_id'], 'experience_now', new_exp)
            User.set_field(session['user_id'], 'max_hp', user[7] + 10)
            User.set_field(session['user_id'], 'hp', user[7] + 10)
            User.set_field(session['user_id'], 'damage', user[10] + 2)
            User.set_field(session['user_id'], 'defence', user[11] + 1)
            User.set_field(session['user_id'], 'star_coin', coins + coin_gain)
        else:
            User.set_field(session['user_id'], 'experience_now', new_exp)
            User.set_field(session['user_id'], 'star_coin', coins + coin_gain)
        BattleLog.save_battle(session['user_id'], monster_id, "win", exp_gain, coin_gain)
        session.pop('battle', None)
        return render_template('battle_result.html', victory=True, exp=exp_gain, coins=coin_gain)

    battle['player_hp'] = player_hp
    battle['monster_current_hp'] = monster_hp
    session['battle'] = battle
    User.set_field(session['user_id'], 'hp', player_hp)
    User.set_field(session['user_id'], 'current_hp', player_hp)

    monster_dict = {
        'id': monster_id,
        'name': name,
        'level': lvl,
        'hp': hp,
        'damage': damage,
        'defence': defence,
        'exp_reward': exp_reward,
        'coin_reward': coin_reward,
        'location_id': monster[8],
        'type': monster[9],
        'health': monster_hp
    }
    return render_template('battle.html', monster=monster_dict, player_hp=player_hp,
                           action_desc=action_desc, monster_desc=monster_desc)

@app.route('/change_name', methods=['GET', 'POST'])
@character_required
def change_name(user):
    cost = 100
    error = None
    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        if not new_name or len(new_name) > 50:
            error = "Имя должно быть от 1 до 50 символов."
        elif user[13] < cost:
            error = f"Недостаточно золота. Нужно {cost}, у вас {user[13]}."
        else:
            User.set_field(session['user_id'], 'name', new_name)
            User.set_field(session['user_id'], 'star_coin', user[13] - cost)
            return redirect(url_for('profile'))
    return render_template('change_name.html', cost=cost, error=error)

# Обработчики ошибок
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Internal error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)