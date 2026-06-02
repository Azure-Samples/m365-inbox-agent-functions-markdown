"""Local test client for the M365 Inbox Agent function app."""
import json
import os
import urllib.error
import urllib.request

BASE_URL = os.environ.get("AGENT_URL", "http://localhost:7071").rstrip("/")
FUNCTION_KEY = os.environ.get("FUNCTION_KEY", "")

AGENTS = {
    "1": ("inbox-triage", "Trigger inbox-triage now"),
    "2": ("daily-briefing", "Trigger daily-briefing now"),
    "3": ("weekly-rule-suggestions", "Trigger weekly-rule-suggestions now"),
}


def admin_url(agent_name: str) -> str:
    url = f"{BASE_URL}/admin/functions/{agent_name}"
    if FUNCTION_KEY:
        url += f"?code={FUNCTION_KEY}"
    return url


def trigger_agent(agent_name: str) -> None:
    payload = {
        "input": json.dumps(
            {
                "source": "chat.py",
                "mode": "manual-trigger",
            }
        )
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        admin_url(agent_name),
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8").strip()
            print(f"\nTriggered {agent_name} ({response.status}).")
            if body:
                print(body)
            print()
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace").strip()
        print(f"\nError triggering {agent_name}: HTTP {exc.code}")
        if details:
            print(details)
        print("Is the Functions host running with `func start`? Are MCP connections authorized?\n")
    except Exception as exc:  # pragma: no cover - friendly CLI boundary
        print(f"\nError triggering {agent_name}: {exc}")
        print("Start the local host with `func start`, then try again.\n")


def show_log_guidance() -> None:
    print("\nTail Functions host logs")
    print("------------------------")
    print("Keep the terminal running `func start` visible; agent summaries and MCP errors are written there.")
    print("For deployed apps, use Application Insights or `azd monitor` to inspect host logs.\n")


def print_menu() -> None:
    print("M365 Inbox Agent — Local Test Client")
    print("====================================")
    for key in ("1", "2", "3"):
        print(f"{key}) {AGENTS[key][1]}")
    print("4) Tail Functions host logs (`func start` terminal)")
    print("q) Quit")


def main() -> None:
    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        if choice in AGENTS:
            trigger_agent(AGENTS[choice][0])
        elif choice == "4":
            show_log_guidance()
        else:
            print("\nChoose 1, 2, 3, 4, or q.\n")


if __name__ == "__main__":
    main()
