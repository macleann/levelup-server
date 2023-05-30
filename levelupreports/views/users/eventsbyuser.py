"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            SELECT
                gmr.id AS gamer_id,
                (u.first_name || ' ' || u.last_name) AS full_name,
                e.id AS event_id,
                e.description,
                e.date,
                e.time,
                g.title
            FROM levelupapi_gamer gmr
            LEFT JOIN auth_user u ON gmr.user_id=u.id
            LEFT JOIN levelupapi_event e ON gmr.id=e.organizer_id
            LEFT JOIN levelupapi_game g ON e.game_id=g.id
            """)

            dataset = dict_fetch_all(db_cursor)

            events_by_user = []

            for row in dataset:
                event = {
                    "description": row["description"],
                    "date": row["date"],
                    "time": row["time"],
                    "title": row["title"]
                }

                user_dict = None
                for user_event in events_by_user:
                    if user_event["gamer_id"] == row["gamer_id"]:
                        user_dict = user_event

                if user_dict:
                    user_dict["events"].append(event)
                else:
                    events_by_user.append({
                        "gamer_id": row["gamer_id"],
                        "full_name": row["full_name"],
                        "events": [event]
                    })

        template = 'users/list_with_events.html'

        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
