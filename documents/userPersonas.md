# User Personas and Features

## Aravind (The Consumer)
An everyday user focused on consuming content, basic interactions, and sharing light thoughts. Represents the majority of the platform's user base.

### Core Features
- **Authentication**: Sign-up, email verification, login, and logout functionality.
- **Profile Management**: Ability to view and edit their own profile (name, bio, and profile photo).
- **Social Interactions**: Follow and unfollow other users.
- **Content Engagement**: Like and comment on posts.
- **Discovery**: Access a basic feed and user search functionality.
- **Content Creation**: Create and publish posts (microblogs) with minimal features.


## Elon Musk (The Power User)
An influential figure who uses the platform primarily for mass broadcasting, driving public narratives, creating high-volume content, and leveraging platform control.

### Core Features
- **High-Security Authentication**: Advanced authentication and authorization mechanisms.
- **Controlled Following**: Users are not notified when followed by the power user (or vice versa).
- **Enhanced Content Creation**: Support for rich media and extended character limits in posts.
- **Post Editing**: Ability to edit published posts.
- **Increased Visibility**: Enhanced reach and visibility of posts across the platform.
- **Verified Badge**: Distinguished verification status.


## Django Admin (The Superuser)
A backend administrator responsible for managing platform data, moderating users, and maintaining system integrity. Operates through Django's admin interface and has unrestricted access to all models and actions.

### Core Features
- **Full Access to Django Admin Panel**: View, create, update, and delete any model instance.
- **User Management**: Activate/deactivate accounts, reset passwords, assign roles.
- **Content Moderation**: Remove inappropriate posts, comments, or media.
- **System Oversight**: Monitor signup logs, email verification status, and user activity.
- **Model Control**: Add/edit/delete models like Xuser, Post, Comment, etc.
- **Permission Assignment**: Grant staff or power user privileges.
- **Site Configuration**: Manage site-wide settings, email backend, and static files.

