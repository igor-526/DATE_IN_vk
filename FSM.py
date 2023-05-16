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
    delete = State('delete')


class Search:
    searching = State('searching')
