import json
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
POLICY_DIR = ROOT / "datasets" / "policies_corpus" / "policies_parsed"
FIG_DIR = Path(__file__).resolve().parents[1] / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_policies():
    policies = []
    for path in sorted(POLICY_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        policies.append((path.stem, data))
    return policies


def _get_nested(data, *keys, default=None):
    node = data
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def get_policy_stats(policies):
    rows = []
    totals = defaultdict(int)
    for key, data in policies:
        policy_node = data.get("policy", {}) if isinstance(data, dict) else {}
        metadata_node = data.get("metadata", {}) if isinstance(data, dict) else {}

        institution = (
            data.get("institution")
            or metadata_node.get("institution")
            or _get_nested(policy_node, "metadata", "institution")
            or key
        )

        allowed = data.get("allowed_uses") or policy_node.get("allowed_uses") or []
        prohibited = data.get("prohibited_uses") or policy_node.get("prohibited_uses") or []
        faqs = data.get("frequently_asked_questions") or policy_node.get("frequently_asked_questions") or []

        rows.append({
            "policy": key,
            "institution": institution,
            "allowed_uses": len(allowed),
            "prohibited_uses": len(prohibited),
            "faqs": len(faqs),
        })
        totals["allowed_uses"] += len(allowed)
        totals["prohibited_uses"] += len(prohibited)
        totals["faqs"] += len(faqs)

    totals["policies"] = len(rows)
    return rows, totals


def write_summary(rows, totals):
    output = {
        "policies": totals["policies"],
        "total_allowed_uses": totals["allowed_uses"],
        "total_prohibited_uses": totals["prohibited_uses"],
        "total_faqs": totals["faqs"],
        "avg_allowed_uses": round(totals["allowed_uses"] / max(1, totals["policies"]), 2),
        "avg_prohibited_uses": round(totals["prohibited_uses"] / max(1, totals["policies"]), 2),
        "avg_faqs": round(totals["faqs"] / max(1, totals["policies"]), 2),
    }
    summary_path = FIG_DIR / "policy_stats_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump({"summary": output, "rows": rows}, f, indent=2)
    return summary_path


def plot_allowed_vs_prohibited(rows):
    labels = [r["institution"] for r in rows]
    allowed = [r["allowed_uses"] for r in rows]
    prohibited = [r["prohibited_uses"] for r in rows]

    x = range(len(labels))
    width = 0.4

    plt.figure(figsize=(10, 4))
    plt.bar([i - width / 2 for i in x], allowed, width=width, label="Allowed use-cases")
    plt.bar([i + width / 2 for i in x], prohibited, width=width, label="Prohibited use-cases")
    plt.xticks(list(x), labels, rotation=25, ha="right")
    plt.ylabel("Count")
    plt.title("Policy corpus: allowed vs prohibited use-cases")
    plt.legend(frameon=False)
    plt.tight_layout()

    fig_path = FIG_DIR / "policy_actions_distribution.pdf"
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def main():
    policies = load_policies()
    if not policies:
        raise SystemExit("No policy JSON files found.")

    rows, totals = get_policy_stats(policies)
    summary_path = write_summary(rows, totals)
    fig_path = plot_allowed_vs_prohibited(rows)
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote figure: {fig_path}")


if __name__ == "__main__":
    main()
