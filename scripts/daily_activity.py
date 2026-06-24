"""
Daily activity generator for GitHub profile commits.
Creates 2-6 varying commits per day with different content types.
"""

import os
import random
import subprocess
from datetime import date, datetime

DATE = date.today().isoformat()
ACTIVITY_DIR = "activity"
SNIPPETS_DIR = os.path.join(ACTIVITY_DIR, "snippets")
os.makedirs(SNIPPETS_DIR, exist_ok=True)

TOPICS = [
    "Data Structures", "Algorithms", "Operating Systems",
    "Machine Learning", "Deep Learning", "RAG Systems",
    "Python", "C++", "System Design", "Database Internals",
    "Computer Networks", "Software Engineering", "Cloud Computing",
    "Distributed Systems", "LLMs", "Vector Databases",
]

ACTIVITY_TYPES = [
    "Read about {topic}",
    "Practiced {topic} problems",
    "Wrote code for {topic}",
    "Studied {topic} concepts",
    "Explored {topic} internals",
    "Reviewed {topic} notes",
    "Implemented {topic} example",
    "Learned {topic} fundamentals",
]

FILES = [
    "AGENTS.md", "config.py", "ingest.py", "rag_engine.py",
    "app.py", "README.md", "tools/notes.md",
]


def pick_activities():
    """Pick 2-6 random activities for today."""
    count = random.randint(2, 6)
    activities = []
    used = set()
    for _ in range(count):
        topic = random.choice(TOPICS)
        template = random.choice(ACTIVITY_TYPES)
        activity = template.format(topic=topic)
        if activity not in used:
            used.add(activity)
            activities.append(activity)
    return activities


def create_main_log(activities):
    """Create the main daily activity log."""
    path = os.path.join(ACTIVITY_DIR, f"{DATE}.md")
    now = datetime.now().strftime("%H:%M")
    with open(path, "w") as f:
        f.write(f"# Activity Log - {DATE}\n\n")
        f.write(f"_{now}_\n\n")
        f.write("## Today\n\n")
        for a in activities:
            f.write(f"- {a}\n")
        f.write("\n---\n")
    return path


def create_snippets(activities):
    """Create individual snippet files for extra commits."""
    paths = []
    for i, activity in enumerate(activities):
        path = os.path.join(SNIPPETS_DIR, f"{DATE}-{i+1:03d}.md")
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(f"# {activity}\n\n")
                f.write(f"Date: {DATE}\n")
                f.write(f"Status: In progress\n\n")
                f.write("---\n")
        paths.append(path)
    return paths


def main():
    activities = pick_activities()
    count = len(activities)

    main_file = create_main_log(activities)
    snippets = create_snippets(activities)

    total = 1 + len(snippets)

    for path in [main_file] + snippets:
        subprocess.run(["git", "add", path])
        name = os.path.basename(path)
        msg = f"docs: {name.replace('.md','').replace(DATE,'').strip('-')}"
        if not msg or msg == "docs: ":
            msg = f"docs: daily log {DATE}"
        subprocess.run(["git", "commit", "-m", msg])

    subprocess.run(["git", "push"])
    print(f"✅ Created {total} commits for {DATE}")


if __name__ == "__main__":
    main()
