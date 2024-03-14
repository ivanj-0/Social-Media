# Social Media Platform

## Project Overview

This project is a social media platform built using Django, providing features such as user authentication, profile management, post uploading, commenting, liking, following, and flagging inappropriate content. It allows users to create profiles, share posts, follow other users, like and comment on posts, and manage their preferences.

## Features

- **User Authentication:** Users can sign up, sign in, and log out securely.
- **Profiles:** Users can create and manage their profiles, including uploading profile pictures, adding a bio, and specifying their location.
- **Post Management:** Users can upload images with captions, and they can edit or delete their own posts.
- **Interactivity:** Users can like and comment on posts.
- **Following:** Users can follow/unfollow other users to customize their feed.
- **Notifications:** Users receive email notifications when someone they follow uploads a new post.
- **Preferences:** Users can set their preferences to receive/not receive email notifications.
- **Admin Panel:** Admins can view flagged posts and comments for moderation.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/your_username/social_media_platform.git
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```
    python manage.py migrate
    ```

4. Create a superuser:
    ```
    python manage.py createsuperuser
    ```

5. Run the server:
    ```
    python manage.py runserver
    ```

6. Access the application in your browser at `http://localhost:8000`.

## Usage

- Sign up for a new account or sign in with existing credentials.
- Customize your profile by uploading a profile picture, adding a bio, and specifying your location.
- Explore the platform by viewing posts from users you follow.
- Upload your own posts with captions.
- Like and comment on posts to engage with other users.
- Follow/unfollow users to tailor your feed.
- Set your preferences to receive/not receive email notifications.
- Admins can moderate flagged posts and comments from the admin panel.
