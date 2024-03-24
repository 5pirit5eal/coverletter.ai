from datetime import datetime as DateTime, timezone

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from beartype import beartype
from beartype.vale import Is
from typing import Annotated
from hashlib import md5

from coverletter import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user")
    about_me: Mapped[str | None] = mapped_column(String(140))
    last_seen: Mapped[DateTime | None] = mapped_column(default=lambda: DateTime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.name}>"

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int) -> str:
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def previous_coverletters(self):
        # ORM query
        return (
            CoverLetter.query.join(Prompt)
            .join(Resume)
            .join(User)
            .filter(User.id == self.id)
            .order_by(CoverLetter.timestamp.desc())
        )
        """SQLAlchemy Core query
        return (
            select(CoverLetter)
            .join(Prompt)
            .join(Resume)
            .join(User)
            .where(User.id == self.id)
            .order_by(CoverLetter.timestamp.desc())
        )

        """


class Resume(db.Model):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    language: Mapped[str] = mapped_column(String(3))
    created: Mapped[DateTime] = mapped_column(default=lambda: DateTime.now(timezone.utc))
    user: Mapped[User] = relationship(back_populates="resumes")
    resume_items: Mapped[list["ResumeItem"]] = relationship(back_populates="resume")
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="resume")

    def __repr__(self):
        return f"<Resume {self.id}, Amount of items: {len(self.resume_items)}>"

    def get_items_per_category(self) -> dict[str, list["ResumeItem"]]:
        """Helper function that provides a mapping of resume categories to
        items contained in said category sorted by begin date.
        """
        categories = {item.category for item in self.resume_items}
        resume_categories = {}

        for category in categories:
            resume_items = sorted(
                [item for item in self.resume_items if item.category == category],
                key=lambda x: x.begin_date,
                reverse=True,
            )
            resume_items_preview = [
                {
                    "title": resume_item.title,
                    "description": resume_item.description,
                    "begin_date": (
                        resume_item.begin_date.strftime("%m/%y") if resume_item.begin_date else None
                    ),
                    "end_date": (
                        "- " + resume_item.end_date.strftime("%m/%y")
                        if resume_item.end_date
                        else None
                    ),
                    "grade": resume_item.grade,
                    "location": resume_item.location,
                }
                for resume_item in resume_items
            ]
            resume_categories[category] = resume_items_preview
        return resume_categories


class ResumeItem(db.Model):
    __tablename__ = "resume_items"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String(128), primary_key=True)
    description: Mapped[str] = mapped_column()
    # education, work, project, skill, language, certification, volunteer, award, publication, course
    category: Mapped[str] = mapped_column(String(32), index=True)
    begin_date: Mapped[DateTime | None] = mapped_column()
    end_date: Mapped[DateTime | None] = mapped_column()
    grade: Mapped[float | None] = mapped_column()
    location: Mapped[str | None] = mapped_column()
    resume: Mapped[Resume] = relationship(back_populates="resume_items")

    def __repr__(self):
        return f"<ResumeItem {self.title}: {self.description[:50]}...>"


class Prompt(db.Model):
    __tablename__ = "prompts"
    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    posting_id: Mapped[int] = mapped_column(ForeignKey("postings.id"))
    prompt: Mapped[str] = mapped_column()
    resume: Mapped[Resume] = relationship(back_populates="prompts")
    posting: Mapped["JobPosting"] = relationship(back_populates="prompts")
    cover_letters: Mapped[list["CoverLetter"]] = relationship(back_populates="prompt")

    def __repr__(self):
        return f"<Prompt {self.id} {self.prompt[:25]}>"


class JobPosting(db.Model):
    __tablename__ = "postings"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str | None] = mapped_column()
    text: Mapped[str] = mapped_column(default="")
    date: Mapped[DateTime] = mapped_column(default=lambda: DateTime.today())
    language: Mapped[str | None] = mapped_column(String(3), default="eng")
    company: Mapped[str | None] = mapped_column()
    location: Mapped[str | None] = mapped_column()
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="posting")

    def __repr__(self):
        return f"<JobPosting {self.url}>"


class CoverLetter(db.Model):
    __tablename__ = "cover_letters"
    id: Mapped[int] = mapped_column(primary_key=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"))
    config_id: Mapped[int] = mapped_column(ForeignKey("model_configs.id"))
    response: Mapped[str] = mapped_column()
    timestamp: Mapped[DateTime] = mapped_column(
        default=lambda: DateTime.now(timezone.utc), index=True
    )
    prompt: Mapped[Prompt] = relationship(back_populates="cover_letters")
    config: Mapped["ModelConfig"] = relationship(back_populates="cover_letters")

    def __repr__(self):
        return f"<CoverLetter {self.id}>"


class ModelConfig(db.Model):
    """Configuration of the TextGenerationModel by Google Cloud."""

    __tablename__ = "model_configs"
    id: Mapped[int] = mapped_column(primary_key=True)
    # common name or family fo the model
    name: Mapped[str] = mapped_column()
    # identifier of the google model e.g. "text-bison@002"
    model_id: Mapped[str] = mapped_column()
    # controls the randomness of predictions
    temperature: Mapped[float | None] = mapped_column()
    # max length of the output in tokens
    max_output_tokens: Mapped[int | None] = mapped_column()
    # the number of highest probability vocabulary tokens to keep for top-k-filtering
    top_k: Mapped[int | None] = mapped_column()
    # the cumulative probability of parameter for nucleus sampling
    top_p: Mapped[float | None] = mapped_column()
    # stop generation when this sequence is generated
    stop_sequence: Mapped[str | None] = mapped_column()
    candidate_count: Mapped[int | None] = mapped_column()  # number of candidates to generate
    grounding_source: Mapped[str | None] = mapped_column()  # Optional grounding feature with source
    # Returns the top logprobs for each token
    logprobs: Mapped[float | None] = mapped_column()
    # Positive values penalize tokens in general
    presence_penalty: Mapped[float | None] = mapped_column()
    # Positive values penalize repetition of tokens
    frequency_penalty: Mapped[float | None] = mapped_column()

    cover_letters: Mapped[list["CoverLetter"]] = relationship(back_populates="config")

    def __repr__(self):
        return f"<ModelConfig {self.name} {self.model_id} {self.id}>"


IntString = Annotated[str, Is[lambda s: s.isdigit()]]


@beartype
@login.user_loader
def load_user(user_id: IntString) -> User:
    return User.query.get(int(user_id))


if __name__ == "__main__":
    print(User(name="test", email="", password_hash=""))
