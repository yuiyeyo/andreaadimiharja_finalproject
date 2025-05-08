
# NewsHub - Personalized News Portal

NewsHub is a Django-based news web application that provides personalized article recommendations, notifications, and user interaction features. The platform allows users to customize their news experience by selecting interests, subscribing to specific topics, favoriting editors, and managing alerts.

---

## 🚀 Features

### User Personalization

- **Set Interests:** Users can select general interests in their profile (e.g., "Music", "Film").
- **Automatic Interest Tracking:** Articles read with specific keywords 3+ times will automatically add those keywords as hidden interests.
- **Disliked Topics:** Users can hide content related to specific topics.
- **Subscriptions:** Users can subscribe to specific, granular topics (e.g., "Rock and Roll", "Gray’s Anatomy").

### Article Interaction

- **Favorite Editors:** Users can favorite editors via a heart icon on article pages.
- **Notifications:** Configurable options to get notified when:
  - Articles matching interests are posted.
  - Articles under subscribed topics are published.
  - Articles by favorite editors are released.
- **Feed:** View all articles with options to:
  - Sort by latest or most reacted.
  - Load dynamically with pagination (10 articles at a time).
- **Recommendations:** Related articles are suggested based on shared tags.
- **Reactions:** Like or react to articles.
- **Comments:** Users can comment on articles.
- **Edit Profile:** Name, email, interests, subscriptions.

---

## 🛠️ Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/newshub.git
   cd newshub
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python -m venv env
   source env/bin/activate    # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure `.env` (if required):**
   Create a `.env` file and add database or secret key settings if applicable.

---

## ⚙️ Running Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

---

## ▶️ Run the Project

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 🔍 Testing Features

- **Login/Register** and navigate to your profile to edit interests, disliked topics, subscriptions.
- **Read Articles** to trigger automatic interest detection.
- **Go to Feed:** Sort and scroll to dynamically load more articles.
- **Submit Article:** Choose tags with checkboxes.
- **Favorite Editor:** Use the heart icon under an article.
- **Receive Notifications:** Based on preferences; view at `/notifications/`.
- **Comment and React** to posts.

---

## 🔌 APIs

### PokéAPI and OpenWeather API
- Used to enrich article content with Pokémon and city weather info.
- Automatically fetched and displayed in article detail pages.

**Note:** No additional API key required for PokéAPI. For OpenWeather, configure your API key in your settings or `.env`.

---

## 📁 Folder Structure (key files)
- `news_app/models.py`: Models (Article, Tag, Profile, Notification, etc.)
- `news_app/forms.py`: ArticleForm with checkbox for tags.
- `news_app/views.py`: Views including submit, toggle favorite, and feed logic.
- `templates/`: HTML templates for feed, submit form, detail pages.
- `static/`: CSS and JavaScript.

---

## 📩 Notes

- Notifications use a simple database table (`Notification`) checked on page refresh.
- Favorite creators are handled through a many-to-many relationship in the Profile model.
- Recommendations are powered by shared tags.

---

## 🧪 Optional Enhancements (not required but possible)
- Real-time notifications using Django Channels and WebSockets.
- Tag weight scoring for smarter recommendations.
- AI-powered summarization for articles.

---

Enjoy your personalized news experience with **NewsHub**! 🎉
