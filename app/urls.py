from django.urls import path

from . import views

urlpatterns = [
    path("favicon.ico", views.favicon, name="favicon"),
    path("header-pfp", views.header_pfp, name="header_pfp"),
    path('get-pfp', views.get_pfp, name='get_pfp'),
    path("header-profile-name", views.header_profile_name, name="header_profile_name"),
    path("", views.join_game, name="index"),
    path("login", views.login_, name="login"),
    path("logout", views.logout_, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profil"),
    path("change-pfp", views.change_pfp, name="change_pfp"),
    path("change-user-info", views.change_user_info, name="change_user_info"),
    path("change-pwd", views.change_pwd, name="change_pwd"),
    path("search-notfriend-user", views.search_notfriend_user, name="search_notfriend_user"),
    path("friend-list", views.friend_list, name="friend_list"),
    path("termsofuse", views.termsofuse, name="termsofuse"),
    path("privacypolicy", views.privacypolicy, name="privacypolicy"),
    path("legalmention", views.legalmention, name="legalmention"),
    path("history", views.history, name="history"),
    path("team", views.team, name="team"),
    path("help", views.help, name="help"),
    path("forgotten-password", views.forgotten_password, name="forgotten-password"),
    path("password_reset_confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("add-friend", views.add_friend, name="add_friend"),
    path("delete-friend", views.delete_friend, name="delete_friend"),
    path("delete-account", views.delete_account, name="delete_account"),

    #Tournois
    path("tournament", views.tournament, name="tournament"),
    path("tournament-code", views.tournament_code, name="tournament_code"),
    path("tournament/<id>/", views.tournament_manager, name="tournament_manager"),
    path("tournament-player-list", views.tournament_player_list, name="tournament_player_list"),
    path("create-tournament", views.create_tournament, name="create_tournament"),
    path("edit-tournament/<id_tournament>/", views.edit_tournament, name="edit_tournament"),
    path("search-tournament", views.search_tournament, name="search_tournament"),
    path("tournament-join/<id_tournament>/", views.tournament_join, name="tournament_join"),
    path("search-current-tournament", views.search_current_tournament, name="search_current_tournament"),
    path("delete-tournament/<id_tournament>/", views.delete_tournament, name="delete_tournament"),
    
    #Parties
    path("create-game", views.create_game, name="create_game"),
    path("join-game", views.join_game, name="join_game"),
    path("search-game", views.search_game, name="search_game"),
    path("search-current-game", views.search_current_game, name="search_current_game"),
    path("game", views.game, name="game"),
    path("game-code", views.game_code, name="game_code"),
    path("game-view-player", views.game_view_player, name="game_view_player"),

    # Regarder une partie
    path("watch-game", views.watch_game, name="watch_game"),

    #Carrière
    path("search-games-historic/<int:id_user>/", views.search_games_historic, name="search_games_historic"),
    path("career", views.career, name="career"),
    path("stats", views.stats, name="stats"),
    path("import-game", views.import_game, name="import_game"),
    path("export-game/<int:id_game>/", views.export_game, name="export_game"),
    path("career/<int:id_user>/", views.career, name="public_career"),
    
    #Public Carrière
    path("public-career/<int:id_user>/", views.public_career, name="public_career"),

    #Classement
    path("classement-global", views.global_ranking, name="classement_global"),
    path("classement-tournament/<id_tournament>/", views.tournament_ranking, name="classement_tournament"),
    
]
