from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime as DateTime

from coverletter import db


class User(db.Model):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column()
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user")


class Resume(db.Model):
    __tablename__ = "resumes"
    resume_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    language: Mapped[str] = mapped_column()
    user: Mapped[User] = relationship(back_populates="resumes")
    resume_items: Mapped[list["ResumeItem"]] = relationship(back_populates="resume")
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="resume")


class ResumeItem(db.Model):
    __tablename__ = "resume_items"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.resume_id"), primary_key=True)
    title: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    # education, work, project, skill, language, certification, volunteer, award, publication, course
    category: Mapped[str] = mapped_column()
    begin_date: Mapped[DateTime | None] = mapped_column()
    end_date: Mapped[DateTime | None] = mapped_column()
    grade: Mapped[float | None] = mapped_column()
    location: Mapped[str | None] = mapped_column()
    resume: Mapped[Resume] = relationship(back_populates="resume_items")


class Prompt(db.Model):
    __tablename__ = "prompts"
    prompt_id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.resume_id"))
    posting_id: Mapped[int] = mapped_column(ForeignKey("postings.posting_id"))
    prompt: Mapped[str] = mapped_column()
    resume: Mapped[Resume] = relationship(back_populates="prompts")
    posting: Mapped["JobPosting"] = relationship(back_populates="prompts")
    cover_letters: Mapped[list["CoverLetter"]] = relationship(back_populates="prompt")


class JobPosting(db.Model):
    __tablename__ = "postings"
    posting_id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column(default="")
    date: Mapped[DateTime] = mapped_column(default=DateTime.today())
    language: Mapped[str] = mapped_column(default="eng")
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="posting")


class CoverLetter(db.Model):
    __tablename__ = "cover_letters"
    cover_letter_id: Mapped[int] = mapped_column(primary_key=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.prompt_id"))
    config_id: Mapped[int] = mapped_column(ForeignKey("model_configs.config_id"))
    response: Mapped[str] = mapped_column()
    prompt: Mapped[Prompt] = relationship(back_populates="cover_letters")
    config: Mapped["Config"] = relationship(back_populates="cover_letters")


class Config(db.Model):
    """Configuration of the TextGenerationModel by Google Cloud."""

    __tablename__ = "model_configs"
    config_id: Mapped[int] = mapped_column(primary_key=True)
    # common name or family fo the model
    name: Mapped[str] = mapped_column()
    # identifier of the google model e.g. "text-bison@002"
    model_id: Mapped[str] = mapped_column()
    # controls the randomness of predictions
    temperature: Mapped[float] = mapped_column()
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
