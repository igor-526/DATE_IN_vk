from vkwave.bots.fsm import FiniteStateMachine, State

fsm = FiniteStateMachine()


class Reg:
    profile = State('profile')
    name_auto = State('name')
    name_manual = State('name_manual')
    bdate_manual = State('bdate_manual')
    bdate_auto = State('bdate_auto')
    bdate_year = State('bdate_year')
    sex_manual = State('sex_manunal')
    geo = State('geo')
    photo = State('photo')
    description = State('description')
    purposes = State('purposes')
    f_sex = State('f_sex')
    f_age_min = State('f_min_age')
    f_age_max = State('f_max_age')
    tg_id = State('tg_id')
    tg_confirm = State('tg_confirm')
    tg_code = State('tg_code')


class Menu:
    menu = State('menu')
    geo = State('geo')
    report = State('report')
    report_confirm = State('report_confirm')


class Profile:
    show = State('show')
    name = State('name')
    bdate = State('bdate')
    sex = State('sex')
    purposes = State('purposes')
    geo = State('geo')
    description = State('description')
    del_photos = State('del_photos')
    add_photos = State('add_photos')
    age_min = State('age_min')
    age_max = State('age_max')
    sex_f = State('sex_f')
    km_f = State('km_f')
    delete = State('delete')
    desc_more = State('desc_more')
    d_m_height = State('d_m_height')
    d_m_habits = State('d_m_habits')
    d_m_hobby = State('d_m_hobby')
    d_m_children = State('d_m_children')
    d_m_animals = State('d_m_animals')
    d_m_busy = State('d_m_busy')
    filters = State('filters')


class Search:
    searching = State('searching')


class Matches:
    new_matches = State('new_matches')
    old_matches = State('old_matches')


class Complaints:
    category = State('category')
    description = State('description')
    confirm = State('confirm')
