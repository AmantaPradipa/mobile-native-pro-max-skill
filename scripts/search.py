#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile-Native Pro Max Search - BM25 search engine for mobile development rules.

Usage:
  python scripts/search.py "<query>" --architecture [-p "Project Name"]
  python scripts/search.py "<query>" --domain ui-components
  python scripts/search.py "<query>" --stack kotlin
"""

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from datetime import datetime
from math import log
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "src" / "mobile-native-pro-max" / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "ui-components": {
        "file": "ui_components.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "navigation-patterns": {
        "file": "navigation_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "architecture": {
        "file": "architecture_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "state-management": {
        "file": "state_management.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "performance": {
        "file": "performance_optimization.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "testing": {
        "file": "testing_strategies.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "platform-apis": {
        "file": "platform_apis.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "build-deployment": {
        "file": "build_deployment.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "anti-patterns": {
        "file": "anti_patterns.csv",
        "search_cols": ["severity", "name", "bad_example", "why_bad", "good_example", "keywords"],
        "output_cols": ["severity", "name", "bad_example", "why_bad", "good_example", "references"],
    },
}

STACK_CONFIG = {
    "kotlin": "stacks.csv",
    "swift": "stacks.csv",
    "java": "stacks.csv",
    "objective-c": "stacks.csv",
    "dart": "stacks.csv",
    "compose": "stacks.csv",
    "swiftui": "stacks.csv",
    "uikit": "stacks.csv",
    "flutter": "stacks.csv",
    "kmm": "stacks.csv",
    "room": "stacks.csv",
    "coredata": "stacks.csv",
    "sqldelight": "stacks.csv",
    "retrofit": "stacks.csv",
    "ktor": "stacks.csv",
    "hilt": "stacks.csv",
    "koin": "stacks.csv",
    "firebase": "stacks.csv",
    "fastlane": "stacks.csv",
    "gradle": "stacks.csv",
    "xcode": "stacks.csv",
    "coil": "stacks.csv",
    "alamofire": "stacks.csv",
    "compose-multiplatform": "stacks.csv",
}


class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.n = 0

    def tokenize(self, text):
        text = re.sub(r"[^\w\s]", " ", str(text).lower())
        return [word for word in text.split() if len(word) > 2]

    def fit(self, documents):
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.n = len(self.corpus)
        if self.n == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.n
        for doc in self.corpus:
            for word in set(doc):
                self.doc_freqs[word] += 1
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.n - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        query_tokens = self.tokenize(query)
        ranked = []
        for index, doc in enumerate(self.corpus):
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1
            score = 0
            for token in query_tokens:
                if token not in self.idf:
                    continue
                tf = term_freqs[token]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * self.doc_lengths[index] / self.avgdl)
                score += self.idf[token] * numerator / denominator
            ranked.append((index, score))
        return sorted(ranked, key=lambda item: item[1], reverse=True)


def load_csv(filepath):
    with open(filepath, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def search_csv(filepath, search_cols, output_cols, query, max_results, row_filter=None):
    if not filepath.exists():
        return []
    rows = load_csv(filepath)
    if row_filter:
        rows = [row for row in rows if row_filter(row)]
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in rows]
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)
    results = []
    for index, score in ranked[:max_results]:
        if score > 0:
            row = rows[index]
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    if not results and rows:
        for row in rows[:max_results]:
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    return results


def detect_domain(query):
    query_lower = query.lower()
    keywords = {
        "ui-components": ["button", "card", "list", "form", "modal", "sheet", "snackbar", "fab", "chip", "skeleton", "toolbar", "search bar"],
        "navigation-patterns": ["navigation", "navigate", "route", "deep link", "stack", "tab", "drawer", "back"],
        "architecture": ["mvvm", "mvi", "clean architecture", "repository", "module", "coordinator", "offline first"],
        "state-management": ["state", "stateflow", "combine", "viewmodel", "paging", "loading", "undo"],
        "performance": ["startup", "memory", "fps", "frame", "battery", "image loading", "proguard", "compose performance"],
        "testing": ["test", "unit test", "screenshot", "snapshot", "benchmark", "accessibility test", "espresso"],
        "platform-apis": ["camera", "location", "notification", "biometric", "bluetooth", "widget", "permission", "purchase"],
        "build-deployment": ["play store", "app store", "fastlane", "signing", "version", "flavor", "testflight", "crash"],
        "anti-patterns": ["anti", "bad", "avoid", "review", "risk", "leak", "god activity"],
    }
    scores = {
        domain: sum(1 for word in words if re.search(r"\b" + re.escape(word) + r"\b", query_lower))
        for domain, words in keywords.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "architecture"


def search(query, domain=None, max_results=MAX_RESULTS):
    domain = domain or detect_domain(query)
    config = CSV_CONFIG.get(domain)
    if not config:
        return {"error": f"Unknown domain: {domain}"}
    results = search_csv(
        DATA_DIR / config["file"],
        config["search_cols"],
        config["output_cols"],
        query,
        max_results,
    )
    return {"domain": domain, "query": query, "file": config["file"], "count": len(results), "results": results}


def search_stack(query, stack, max_results=MAX_RESULTS):
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(STACK_CONFIG)}"}
    output_cols = ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"]
    search_cols = ["category", "name", "description", "when_to_use", "trade_offs", "keywords"]

    def stack_filter(row):
        row_name = row.get("name", "").lower()
        row_keywords = row.get("keywords", "").lower()
        stack_lower = stack.lower()
        stack_space = stack_lower.replace("-", " ")
        combined = row_name + " " + row_keywords
        return stack_lower in combined or stack_space in combined

    results = search_csv(
        DATA_DIR / STACK_CONFIG[stack],
        search_cols,
        output_cols,
        query,
        max_results,
        row_filter=stack_filter,
    )
    # Add stack field to results for compatibility
    for r in results:
        r["stack"] = stack
    return {"domain": "stack", "stack": stack, "query": query, "file": STACK_CONFIG[stack], "count": len(results), "results": results}


def format_results(result):
    if "error" in result:
        return f"Error: {result['error']}"
    title = "Mobile-Native Pro Max Stack Guidelines" if result.get("stack") else "Mobile-Native Pro Max Search Results"
    lines = [
        f"## {title}",
        f"**Domain:** {result.get('domain')} | **Query:** {result.get('query')}",
        f"**Source:** {result.get('file')} | **Found:** {result.get('count')} results",
        "",
    ]
    for index, row in enumerate(result.get("results", []), 1):
        lines.append(f"### Result {index}")
        for key, value in row.items():
            value = str(value)
            if len(value) > 360:
                value = value[:360] + "..."
            lines.append(f"- **{key}:** {value}")
        lines.append("")
    return "\n".join(lines)


def first_result(query, domain):
    result = search(query, domain, 1)
    return result.get("results", [{}])[0] if result.get("results") else {}


def domain_query(query, domain):
    query_lower = query.lower()
    explicit_terms = {
        "ui-components": ["button", "card", "list", "form", "modal", "toolbar"],
        "navigation-patterns": ["navigation", "route", "deep link", "stack", "tab"],
        "architecture": ["mvvm", "mvi", "clean", "repository", "module"],
        "state-management": ["state", "stateflow", "combine", "viewmodel"],
        "performance": ["startup", "memory", "fps", "battery", "image"],
        "testing": ["test", "unit", "screenshot", "benchmark"],
        "platform-apis": ["camera", "location", "notification", "bluetooth"],
        "build-deployment": ["play store", "app store", "fastlane", "signing"],
    }
    defaults = {
        "ui-components": "bottom navigation list card form",
        "navigation-patterns": "stack navigation deep link tab drawer",
        "architecture": "mvvm clean architecture repository di",
        "state-management": "stateflow viewmodel loading state",
        "performance": "startup memory rendering optimization",
        "testing": "unit test ui screenshot benchmark",
        "platform-apis": "camera location permissions notification",
        "build-deployment": "play store app store fastlane signing",
    }
    if any(term in query_lower for term in explicit_terms.get(domain, [])):
        return query
    return f"{query} {defaults.get(domain, '')}"


def detect_stack_in_query(query):
    query_lower = query.lower()
    for stack in STACK_CONFIG:
        if re.search(r"\b" + re.escape(stack) + r"\b", query_lower):
            return stack
    return None


def box_line(label, value, width=72):
    label_text = f"{label}:" if label else ""
    content_width = width - 19
    value = str(value or "")[:content_width]
    return f"| {label_text:<14} {value:<{content_width}} |"


def generate_architecture(query, project_name=None):
    architecture = first_result(domain_query(query, "architecture"), "architecture")
    navigation = first_result(domain_query(query, "navigation-patterns"), "navigation-patterns")
    state = first_result(domain_query(query, "state-management"), "state-management")
    ui = first_result(domain_query(query, "ui-components"), "ui-components")
    performance = first_result(domain_query(query, "performance"), "performance")
    testing = first_result(domain_query(query, "testing"), "testing")
    platform = first_result(domain_query(query, "platform-apis"), "platform-apis")
    deploy = first_result(domain_query(query, "build-deployment"), "build-deployment")
    anti = search(query, "anti-patterns", 3).get("results", [])

    target = project_name or query
    arch_pattern = architecture.get("name", "MVVM + Clean Architecture")
    stack = detect_stack_in_query(query) or "kotlin + compose"
    key_rules = "; ".join(
        filter(
            None,
            [
                navigation.get("name"),
                state.get("name"),
                performance.get("name"),
            ],
        )
    ) or "stack navigation; stateflow; startup optimization"
    effects = f"{deploy.get('name', 'Play Store')} + {testing.get('name', 'Unit Testing')}"
    avoid = "; ".join(item.get("name", "") for item in anti if item.get("name")) or "main-thread network; god activity; missing accessibility"

    width = 72
    lines = [
        "+" + "-" * (width - 2) + "+",
        box_line("TARGET", target, width),
        "+" + "-" * (width - 2) + "+",
        box_line("PLATFORM", "Android / iOS / KMM", width),
        box_line("ARCH", arch_pattern, width),
        box_line("STACK", stack, width),
        box_line("NAVIGATION", navigation.get("name", "Stack + Tab"), width),
        box_line("STATE", state.get("name", "StateFlow / Combine"), width),
        box_line("UI", ui.get("name", "Bottom Navigation"), width),
        box_line("KEY RULES", key_rules, width),
        box_line("DEPLOY", effects, width),
        box_line("AVOID", avoid, width),
        box_line("CHECKLIST", "[ ] architecture pattern selected", width),
        box_line("", "[ ] navigation graph defined", width),
        box_line("", "[ ] state management wired", width),
        box_line("", "[ ] anti-patterns reviewed", width),
        box_line("", "[ ] performance baseline set", width),
        "+" + "-" * (width - 2) + "+",
        "",
        "## Rationale",
        f"- **Architecture:** {architecture.get('description', '')}",
        f"- **Navigation:** {navigation.get('description', '')}",
        f"- **State:** {state.get('description', '')}",
        f"- **UI:** {ui.get('description', '')}",
        f"- **Performance:** {performance.get('description', '')}",
        f"- **Testing:** {testing.get('description', '')}",
        f"- **Platform APIs:** {platform.get('description', '')}",
        f"- **Deployment:** {deploy.get('description', '')}",
    ]
    return "\n".join(lines)


def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower())
    return value.strip("-") or "mobile-app"


def persist_architecture(query, project_name=None, output_dir=None):
    architecture_block = generate_architecture(query, project_name)
    root = Path(output_dir) if output_dir else Path.cwd()
    project_slug = slugify(project_name or query)
    arch_dir = root / "architecture" / project_slug
    arch_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = [
        f"# Mobile Architecture: {project_name or query}",
        "",
        f"> Generated: {timestamp}",
        f"> Query: {query}",
        "",
        "```text",
        architecture_block,
        "```",
        "",
        "## Usage Notes",
        "",
        "- Treat this file as the mobile app architecture source of truth.",
        "- Validate anti-patterns and performance before release.",
        "- Re-run search before delivery.",
        "",
    ]
    master_path = arch_dir / "MASTER.md"
    master_path.write_text("\n".join(header), encoding="utf-8")
    return "\n".join([architecture_block, "", "## Persisted Files", f"- {master_path}"])


def main():
    parser = argparse.ArgumentParser(description="Mobile-Native Pro Max Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain")
    parser.add_argument("--stack", "-s", choices=list(STACK_CONFIG.keys()), help="Stack-specific search")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results")
    parser.add_argument("--architecture", "-a", action="store_true", help="Generate full mobile architecture recommendation")
    parser.add_argument("--project-name", "-p", default=None, help="Project name")
    parser.add_argument("--persist", action="store_true", help="Save architecture to architecture/<project>/MASTER.md")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory for persisted architecture files")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.architecture:
        if args.persist:
            print(persist_architecture(args.query, args.project_name, args.output_dir))
        else:
            print(generate_architecture(args.query, args.project_name))
        return
    if args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
    else:
        result = search(args.query, args.domain, args.max_results)
    if args.json:
        import json

        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_results(result))


if __name__ == "__main__":
    main()
