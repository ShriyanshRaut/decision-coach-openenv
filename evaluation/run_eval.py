from tasks.task_list import ALL_TASKS
from inference import run_inference

results = []

for task in ALL_TASKS:
    print(f"\nRunning task: {task['name']} ({task['difficulty']})")

    result = run_inference(task["input"])
    scores = result["scores"]

    results.append({
        "task": task["name"],
        "difficulty": task["difficulty"],
        "score": scores["final_score"]
    })

    print(f"Score: {scores['final_score']}")


avg_score = sum(r["score"] for r in results) / len(results)

print("\n======================")
print("Average Score:", round(avg_score, 2))
print("======================")