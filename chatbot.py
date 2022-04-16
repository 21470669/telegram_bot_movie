import os
#import configparser
import logging
import sys

#import redis
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, MessageHandler,
                          PicklePersistence, Updater)
from pymongo import MongoClient

## Get environment variables
#config = configparser.ConfigParser()
#config.read('config.ini')
#TMDB_KEY = config['TMDB']['TMDB_KEY']
TMDB_KEY = (os.environ['TMDB_KEY'])
#BOT_TOKEN = config['TELEGRAM']['ACCESS_TOKEN']
BOT_TOKEN = (os.environ['ACCESS_TOKEN'])


## Database  for /movie(searched count)
#global redis1
#redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']))
#redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))
global collection
#client = MongoClient(config["MONGODB"]["client_link"])
client = MongoClient(os.environ["client_link"])
collection = client["movies"]["search_count"]

#Constant number value for /trend , /toprated and /movie(recommendation button)
trend_no = 5
toprated_no = 10
recommendation_no = 3

#TMDB link
TMDB_API_LINK = "https://api.themoviedb.org/3{}?api_key={}{}"
TMDB_IMG_LINK = "https://www.themoviedb.org/t/p/original"


### GENERAL FUNCTIONS

# Get movie data from TMDB
def get_movie(movie_title: str):
    LINK = TMDB_API_LINK.format("/search/movie", TMDB_KEY, f"&query={movie_title}")
    with requests.get(LINK) as r:
        assert r.status_code == 200
        json_data = r.json()
        return json_data["results"][0]

# Get movie data from TMDB for IMDB
def get_movie_details(movie_id):
    LINK = TMDB_API_LINK.format(f"/movie/{movie_id}", TMDB_KEY, "")
    with requests.get(LINK) as r:
        assert r.status_code == 200
        json_data = r.json()
        return json_data

# Get movie data from TMDB for YouTube
def get_movie_trailer(movie_id):
    LINK = TMDB_API_LINK.format(f"/movie/{movie_id}/videos", TMDB_KEY, "")
    with requests.get(LINK) as r:
        assert r.status_code == 200
        json_data = r.json()
        assert json_data["results"]
        for i in json_data["results"]:
            if i["type"] == "Trailer":
                return f"https://youtube.com/watch?v={i['key']}"
        raise Exception

# Get movie data from TMDB for TMDB recommendation
def get_movie_recommendation(movie_id):
    LINK = TMDB_API_LINK.format(f"/movie/{movie_id}/recommendations", TMDB_KEY, "")
    with requests.get(LINK) as r:
        assert r.status_code == 200
        json_data = r.json() 
        return json_data
        
# Prettify the display movie heading
def prettify_movie_data(movie):
    pretty_movie = f"{movie['title']} ({movie['original_title']}) ~ {movie['release_date'].split('-')[0]}\n"

    # Extra function to count the searched movie - prettify the movie name for storing in DB
    searched_movie = f"{movie['title']} ({movie['original_title']}) ~ {movie['release_date'].split('-')[0]}"

    stars = int(movie["vote_average"] / 2)
    pretty_movie += f"{'⭐'*stars} ~ {str(movie['vote_average'])}\n\n"
    
    return (pretty_movie, searched_movie)
    #return pretty_movie


### HANDLERS

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome!\n\n🎥 Use the following commands to get movie details:\n"
        "/movie [movie name] to get details about a movie\n"
        f"/trend to get the top {trend_no} trending movies\n" 
        f"/toprated to get the top {toprated_no} rated movies\n"
        "/help to check for commands details\n"
        "/discuss to discuss with others"
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        (
            "💡 You can use the /movie command followed by the name"
            " of a movie like what shown below to get more details:\n"
            "/movie [movie name]\n\n"
            f"💡 Use /trend command to get the top {trend_no} trending movies\n\n"
            f"💡 Use /toprated command to get the top {toprated_no} rated movies\n\n"
        )
    )


def not_valid(update: Update, context: CallbackContext):
    update.message.reply_text("❌ The command you entered is not valid")


def trend(update: Update, context: CallbackContext):
    LINK = TMDB_API_LINK.format(f"/trending/movie/week", TMDB_KEY, "")
    with requests.get(LINK) as r:
        assert r.status_code == 200
        json_data = r.json()         
    
    #Get the first trend_no records
    i = 0    
    while i < trend_no:
    #for i in [0,1,2,3,4]:
        trend_data = json_data["results"][i]
        j = i + 1
        #stars = int(trend_data["vote_average"] / 2)
        if i == 0:
            #update.message.reply_photo(f"{TMDB_IMG_LINK}{trend_data['backdrop_path']}")
            update.message.reply_text(f"https://www.themoviedb.org/movie/{trend_data['id']}")
            display_str = f"The top {trend_no} trending movies for this week:\n"
        
        pretty_movie = f"{j}) {trend_data['title']} {'⭐'}{str(trend_data['vote_average'])}\n"
        display_str += pretty_movie
        i += 1

    update.message.reply_text(f"{display_str}")
        
def toprated(update: Update, context: CallbackContext):
    LINK = TMDB_API_LINK.format(f"/movie/top_rated", TMDB_KEY, "")
    with requests.get(LINK) as r:
        assert r.status_code == 200
        json_data = r.json()         
    
    #Get the first toprated_no records
    i = 0
    while i < toprated_no:
        toprated_data = json_data["results"][i]
        j = i + 1        
        if i == 0:            
            update.message.reply_text(f"https://www.themoviedb.org/movie/{toprated_data['id']}")
            display_str = f"The top {toprated_no} rated movies:\n"
        
        pretty_movie = f"{j}) {toprated_data['title']} {'⭐'}{str(toprated_data['vote_average'])}\n"
        display_str += pretty_movie
        i += 1

    update.message.reply_text(f"{display_str}")

def discuss(update: Update, context: CallbackContext):
     discuss_keyboard = InlineKeyboardMarkup(
                            [[
                    InlineKeyboardButton(
                        "🎞 Movie Discussion",
                        url="https://www.themoviedb.org/discuss/movies"),
                    InlineKeyboardButton(
                        "👥 Celebrity Discussion",
                        url="https://www.themoviedb.org/discuss/people")
                ]]
        )
     update.message.reply_text(
         "Please choose the discussion board that you want to go.\n", reply_markup=discuss_keyboard
        )


def movie_no_args(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Please input in the format /movie [movie name]")


def movie(update: Update, context: CallbackContext):
    if not context.args:
        return movie_no_args(update, context)

    # getting the movie name from user input
    movie = " ".join(context.args)

    try:
        movie_data = get_movie(movie)
        msg_head, msg_count = prettify_movie_data(movie_data)
        
        ### Extra function to count the searched movie
        logging.info(msg_count)
        msg = msg_count   
        #redis1.incr(msg)
        #update.message.reply_text(msg +  ' has been searched for ' + redis1.get(msg).decode('UTF-8') + ' times.')
        collection.update_one({"title": msg}, {"$inc": {"count": 1}}, upsert=True)
        res = collection.find_one({"title": msg})        
        update.message.reply_text(res["title"] +  ' has been searched for ' + str(res["count"]) + ' times.')
        ###
      
        movie_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 Synopsis",
                        callback_data={"cb": "synopsis", "movie": movie_data},
                    ),
                    InlineKeyboardButton(
                        "🎟️ IMDB", 
                        callback_data={"cb": "imdb", "movie": movie_data}
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🎬 Trailer",
                        callback_data={"cb": "trailer", "movie": movie_data},
                    ),
                    InlineKeyboardButton(
                        "✔️ Recommendation",
                        callback_data={"cb": "recommendation", "movie": movie_data},
                    )
                ],
            ]
        )

        #Display movie image, movie heading, and movie overview
        update.message.reply_photo(f"{TMDB_IMG_LINK}{movie_data['backdrop_path']}")
        update.message.reply_text(
            f"{msg_head}{movie_data['overview']}", reply_markup=movie_keyboard
        )

    except Exception as e:
        print(e)
        update.message.reply_text(
            (
                "Something went wrong looking for your movie, "
                "the movie you input may not exist in the database, "
                "or you can try again later."
            )
        )


def synopsis(query, movie_data, movie_keyboard):
    msg_head = query.message.text.split("\n\n")[0]
    query.edit_message_text(
        f"{msg_head}\n\n{movie_data['overview']}", reply_markup=movie_keyboard
    )

def recommendation(query, movie_data, movie_keyboard):
    msg_head = query.message.text.split("\n\n")[0]
    try:
        details = get_movie_recommendation(movie_data["id"])        
        
        #Get the first recommendation_no records
        i = 0
        while i < recommendation_no:
            recommendation_data = details["results"][i]
            j = i + 1        
            if i == 0:            
                query.message.reply_text(f"https://www.themoviedb.org/movie/{recommendation_data['id']}")
                display_str = f"Based on your input movie, we recommend these {recommendation_no} movies to you:\n"
        
            pretty_movie = f"{j}) {recommendation_data['title']} {'⭐'}{str(recommendation_data['vote_average'])}\n"
            display_str += pretty_movie
            i += 1

        query.message.reply_text(f"{display_str}")                    

    except:
        query.edit_message_text(
            f"{msg_head}\n\nError getting the imbd link.",
            reply_markup=movie_keyboard,
        )

def imdb(query, movie_data, movie_keyboard):
    msg_head = query.message.text.split("\n\n")[0]
    try:
        details = get_movie_details(movie_data["id"])
        query.edit_message_text(
            f"{msg_head}\n\nhttps://www.imdb.com/title/{details['imdb_id']}",
            reply_markup=movie_keyboard,
        )
    except:
        query.edit_message_text(
            f"{msg_head}\n\nError getting the imbd link.",
            reply_markup=movie_keyboard,
        )


def trailer(query, movie_data, movie_keyboard):
    msg_head = query.message.text.split("\n\n")[0]
    try:
        trailer = get_movie_trailer(movie_data["id"])
        query.edit_message_text(
            f"{msg_head}\n\n{trailer}",
            reply_markup=movie_keyboard,
        )
    except:
        query.edit_message_text(
            f"{msg_head}\n\nError getting the trailer link, it may not be available.",
            reply_markup=movie_keyboard,
        )


def get_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    try:
        query_type = query.data["cb"]
        movie_data = query.data["movie"]

        movie_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 Synopsis",
                        callback_data={"cb": "synopsis", "movie": movie_data},
                    ),
                    InlineKeyboardButton(
                        "🎟️ IMDB", 
                        callback_data={"cb": "imdb", "movie": movie_data}
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🎬 Trailer",
                        callback_data={"cb": "trailer", "movie": movie_data},
                    ),
                    InlineKeyboardButton(
                        "✔️ Recommendation",
                        callback_data={"cb": "recommendation", "movie": movie_data},
                    )
                ],
            ]
        )

        if query_type == "synopsis":
            synopsis(query, movie_data, movie_keyboard)
        elif query_type == "recommendation":
            recommendation(query, movie_data, movie_keyboard)
        elif query_type == "imdb":
            imdb(query, movie_data, movie_keyboard)
        elif query_type == "trailer":
            trailer(query, movie_data, movie_keyboard)
    except:
        pass


def main():
    #config = configparser.ConfigParser()
    #config.read('config.ini')    
    persistence = PicklePersistence(
        filename="callback_storage.pickle", store_callback_data=True
    )
    updater = Updater(token=BOT_TOKEN, persistence=persistence, arbitrary_callback_data=True)
    dispatcher = updater.dispatcher

    ### HANDLERS

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    not_valid_handler = MessageHandler(Filters.all, not_valid)
    query_handler = CallbackQueryHandler(get_query)

    movie_handler = CommandHandler("movie", movie)    
    trend_handler = CommandHandler("trend", trend) 
    toprated_handler = CommandHandler("toprated", toprated) 
    discuss_handler = CommandHandler('discuss', discuss)

    ###

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(movie_handler)
    dispatcher.add_handler(query_handler)
    dispatcher.add_handler(trend_handler)
    dispatcher.add_handler(toprated_handler)
    dispatcher.add_handler(discuss_handler)   
    dispatcher.add_handler(not_valid_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
