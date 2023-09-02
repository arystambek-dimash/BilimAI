# Django Application

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/WleFVe?referralCode=UBd_g_)

This is a Django template that includes:

- SQLite as a database
- Dockerfile files for easy deployment
- Configuration of the CORS middleware

## 📚 Features

1. User registration.
2. User authentication and token creation.
3. User verification and token validation.
4. Encrypted password management.

## 🚀 Quick Start

You'll need Docker and Docker Compose to run this application.

1. Build the project

```bash
docker-compose build
```

2. Start the project

```bash
docker-compose up -d
```

3. Watch logs

```bash
docker-compose logs -f app
```

This command will start the Django server on port 8000.
You can navigate to `http://localhost:8000/api` in your browser to access the automatically generated API documentation.

## 📚 Project Structure


__Authentication:__

- `POST /api/auth/login/`: User can log in to the application.
- `POST /api/sign-up/`: User can register a new account.
- `GET UPDATE DELETE /api/accounts/profile/`: User Profile 

__Chat:__

- `GET /api/chat/`: User can access the chat interface powered by GPT.

__Test:__

- `POST /api/test/`: Create a new test.
- `DELETE /api/test/my-tests/<int:pk>/detail/:` Delete a specific test.
- `GET /api/test/my-tests/`: View All My Test List.

__Favorites:__

- `GET /api/favorites/`: View a list of favorited items.
- `DELETE /api/favorites/<int:pk>/delete/`: Remove an item from favorites.

__History:__

- `GET /api/history/`: View a list of chat history entries.
- `DELETE /api/history/<int:pk>/delete/`: Delete a specific chat history entry.

__Course:__

- `GET /api/courses/`: View a list of available courses.
- `POST /api/courses/upload/`: Add a new course.
- `DELETE /api/courses/<int:pk>/detail/`: Delete or update a specific course.
- `GET /api/courses/<int:pk>/videos/`: View all videos for a specific course.
- `POST /api/courses/<int:pk>/videos/post-video/`: Post a new video for a course.
- `GET /api/courses/<int:pk>/videos/<int:pk>/`: View details of a specific video for a course.
- `POST /api/courses/<int:pk>/video/<int:pk>/update/`: Update details of a specific video for a course.
- `DELETE /api/courses/<int:pk>/post/video/<int:pk>/delete/`: Delete a specific video for a course.
- `GET /api/courses/<int:pk>/post/video/<int:pk>/materials/`: View all materials related to a specific video.
- `POST /api/courses/<int:pk>/post/video/<int:pk>/materials/<int:pk>/update/`: Update details of video materials.
- `DELETE /api/courses/<int:pk>/post/video/<int:pk>/materials/<int:pk>/delete/`: Delete video materials.
- `POST /add-courses/`: Add courses to MyCourse.
- `GET /api/my-courses/`: View a list of MyCourses.
- `POST /api/courses/<int:pk>/materials/images/post/`: Upload image to Course.
- `GET /api/courses/<int:pk>/materials/images/`: View List of Images.
- `DELETE PUT /api/courses/<int:pk>/materials/images/<int:image_pk>/`: Delete Update Image.

]
## ⚙️ Local Development

```
poetry install
poetry shell
sh ./entrypoint.sh
```