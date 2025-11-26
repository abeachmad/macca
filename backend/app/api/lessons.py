from fastapi import APIRouter
from typing import List
from app.schemas.macca import Lesson

router = APIRouter(tags=["lessons"])

@router.get("/lessons", response_model=List[Lesson])
async def get_lessons():
    return [
        Lesson(
            id="lesson_1",
            title="Job Interview: Introducing Yourself",
            subtitle="Today's goal: talk about your background in 3–4 sentences.",
            steps=[
                "Step 1 – Warm-up",
                "Step 2 – Key phrases",
                "Step 3 – Practice answer",
                "Step 4 – Follow-up questions"
            ],
            current_step=1
        ),
        Lesson(
            id="lesson_2",
            title="Daily Conversations: At a Restaurant",
            subtitle="Learn to order food and make requests confidently.",
            steps=[
                "Step 1 – Greeting",
                "Step 2 – Reading the menu",
                "Step 3 – Placing order",
                "Step 4 – Making requests"
            ],
            current_step=1
        )
    ]

@router.get("/lessons/{lesson_id}", response_model=Lesson)
async def get_lesson(lesson_id: str):
    lessons = await get_lessons()
    for lesson in lessons:
        if lesson.id == lesson_id:
            return lesson
    return lessons[0]