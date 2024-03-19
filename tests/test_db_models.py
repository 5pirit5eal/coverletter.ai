from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from datetime import datetime, timezone, timedelta
from coverletter import app, db
from coverletter.db_models import User, Resume, Prompt, CoverLetter, JobPosting, ModelConfig


class UserModelCase(TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(name="susan")
        u.set_password("cat")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("cat"))

    def test_avatar(self):
        u = User(name="john", email="john@example.com")
        self.assertEqual(
            u.avatar(128),
            "https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128",
        )

    def test_cover_letters(self):
        u = User(name="john", email="john@example.com")
        r = Resume(language="en", user=u)
        posting = JobPosting(
            text="lorem ipsum dolor sit amet",
            language="en",
        )
        p = Prompt(prompt="prompt", resume=r, posting=posting)

        config = ModelConfig(
            name="config",
            model_id="model_id",
        )
        cl = CoverLetter(response="cover letter", prompt=p, config=config)
        db.session.add(u)
        db.session.add(r)
        db.session.add(p)
        db.session.add(cl)
        db.session.commit()
        self.assertEqual(u.previous_coverletters().all(), [cl])
