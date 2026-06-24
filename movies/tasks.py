from celery import shared_task

@shared_task
def send_movie_notification(movie_title):

    print("="*50)
    print(f"New movie added: {movie_title}")
    print("Notification sent to subscribers")
    print("=" * 50)

    return f"Notification sent for {movie_title}"