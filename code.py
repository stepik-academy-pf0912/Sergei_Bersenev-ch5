from flask import Flask


videos = [
    {"id": 1, "title": "Squadron 42. Trailer 2018", "link": "R9GQ3R0lJXQ"},
    {"id": 2, "title": "Squadron 42. Trailer 2015", "link": "8EC4WHPxnrk"},
    {"id": 3, "title": "Star Citizen. Anvil - Carrack", "link": "Vm4t1jUBT1U"},
    {"id": 4, "title": "Star Citizen. Drake Interplanetary - Kraken", "link": "to1kDbR4L4I"},
    {"id": 5, "title": "Star Citizen. Последний Контракт", "link": "b56DX5SF5sM"},
    {"id": 6, "title": "Star Citizen. Лорвиль (Бегущий По Лезвию)", "link": "pA6P2WserfU"}
]

playlists = [
    {"id": 1, "title": "Trailers", "videos": [1, 2]},
    {"id": 2, "title": "Ships", "videos": [3, 4]},
    {"id": 3, "title": "Fan work", "videos": [5, 6]}
]

app = Flask(__name__)


def return_video(id, number=''):
    return (f"{number}{videos[id - 1]['title']}<br>"
          f"Link: http://youtu.be/{videos[id - 1]['link']}<br>")


@app.route('/')
def main():
    playlist_print_str = "Плейлисты: "
    welcome_text_main_menu = """<H1>======== StarCitizen ========</H1>
    Перейдите на /videos/<номер> чтобы посмотреть конкретное видео.<br>
    Перейдите на /playlists/<номер> чтобы посмотреть конкретный плейлист.<br>
    Перейдите на /about чтобы посмотреть информацию.<br><br>"""
    for playlist in playlists:
        playlist_print_str += f"{playlist['title']} ({len(playlist['videos'])} видео), "
    playlist_print_str = playlist_print_str[:-2]                                   # Отрезаю лишнюю запятую с пробелом
    return welcome_text_main_menu + playlist_print_str


@app.route('/about')
def about():
    return '<h2>Приложение в разработке</h2>'


@app.route('/videos/<id>')
def video(id):
    video_print_str = "Название: "
    try:
        id = int(id)
    except ValueError:
        video_print_str = "В адресе должен быть номер видео, а не текст"
        return video_print_str
    if id in range(1, len(videos) + 1):
        playlist_print_str = "Плейлисты: "
        for playlist in playlists:
            if id in playlist['videos']:
                playlist_print_str += playlist['title'] + ', '
        playlist_print_str = playlist_print_str[:-2]
        for video in videos:
            if video['id'] == id:
                video_print_str += f"{return_video(video['id'])}<br>" + f"{playlist_print_str}<br>"
    else:
        video_print_str = "Такого видео не найдено"
    return video_print_str


@app.route('/playlists/<id>')
def playlist(id):
    try:
        id = int(id)
    except ValueError:
        playlist_print_str = "В адресе должен быть номер плейлиста, а не текст"
        return playlist_print_str
    if id in range(1, len(playlists) + 1):
        playlist_print_str = f"Плейлист: {playlists[id - 1]['title']}:<br><br>"
        for playlist in playlists:
            if id == playlist['id']:
                count = 1
                for video in playlist['videos']:
                    playlist_print_str += return_video(video, str(count) + '. ') + "<br>"
                    count += 1
    else:
        playlist_print_str = "Такого плейлиста нет"
    return playlist_print_str


@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'


app.run('0.0.0.0',8000)